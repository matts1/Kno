# modified version of peter's automarking code from here https://bitbucket.org/flowblok/enscribe/src/3e89de1d94a386c5e20165e20dd3e94b5e0fb6b1/enscribe/worker/environment.py

# provides an environment for running unsafe user code
# NOTE: at the moment, we're not using a chroot,
# just a protected temporary directory and another user

import fcntl
import os.path
from select import select
import shutil
from subprocess import check_call, Popen, PIPE
import tempfile
import time
import traceback
from string import punctuation, whitespace

def try_utf8(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return repr(s)

def kill_process(p):
    p.poll()
    if p.returncode is not None:
        return

    try:
        p.terminate()
    except OSError as e:
        traceback.print_exc(e)

    p.poll()
    if p.returncode is not None:
        return

    try:
        p.kill()
    except OSError as e:
        traceback.print_exc(e)

class Environment(object):
    def __init__(self):
        self.directory = tempfile.mkdtemp()
        os.chmod(self.directory, 0o755)

    def __del__(self):
        self.close()

    def add_file(self, filename, contents, mode=4):
        path = os.path.join(self.directory, filename)

        if isinstance(contents, str):
            contents = contents.encode('utf-8')

        with open(path, 'wb') as f:
            f.write(contents)

        # worker_group = current_app.config['WORKER_GROUP']
        # check_call(['sudo', '/bin/chgrp', worker_group, path])

        # mode = 0o600 | ((mode & 7) << 3)
        # os.chmod(path, mode)

    def run(self, args, **kwargs):
        if isinstance(args, str):
            args = args.split()

        if args[0].startswith('-'):
            raise ValueError('bad command arguments')

        # worker_user = current_app.config['WORKER_USER']
        return Popen(
            args=['sudo', '-u', worker_user] + args,
            cwd=self.directory,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            **kwargs
        )

    def run_simple(
        self, args,
        stdin='',
        max_output_size=1024 * 1024,
        max_wall_time=90,
        approx_bufsize=2048,
        allow_stderr=False,
        required_stdout=True,
    ):
        start = time.time()
        p = self.run(args, bufsize=approx_bufsize)

        stdin_bufsize = approx_bufsize
        stdout_bufsize = approx_bufsize
        stderr_bufsize = approx_bufsize

        failed = False

        fcntl.fcntl(p.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(p.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(p.stderr, fcntl.F_SETFL, os.O_NONBLOCK)

        rfiles = [p.stdout, p.stderr]
        wfiles = [p.stdin]
        xfiles = [p.stdin, p.stdout, p.stderr]

        stdout = []
        stdout_size = 0
        stderr = []
        stderr_size = 0

        msg = ''
        while True:
            rl, wl, xl = select(rfiles, wfiles, xfiles, 1)

            if p.stdout in rl:
                try:
                    data = p.stdout.read(stdout_bufsize)
                except IOError:
                    stdout_bufsize = max(1, int(stdout_bufsize / 2.0))
                else:
                    stdout.append(data)
                    stdout_size += len(data)
                    if stdout_size >= max_output_size:
                        failed = True
                        msg = 'Program produced too much output on stdout.'
                        break

            if p.stderr in rl:
                try:
                    data = p.stderr.read(stderr_bufsize)
                except IOError:
                    stderr_bufsize = max(1, int(stderr_bufsize / 2.0))
                else:
                    stderr.append(data)
                    stderr_size += len(data)
                    if stderr_size >= max_output_size:
                        failed = True
                        msg = 'Program produced too much output on stderr.'
                        break

            if p.stdin in wl:
                if not stdin:
                    p.stdin.close()
                    wfiles.remove(p.stdin)
                    xfiles.remove(p.stdin)
                else:
                    try:
                        p.stdin.write(stdin[:stdin_bufsize])
                    except IOError:
                        stdin_bufsize = max(1, int(stdin_bufsize / 2.0))
                    else:
                        stdin = stdin[stdin_bufsize:]

            p.poll()
            ret = p.returncode
            if ret == 0:
                break
            elif ret is not None:
                if ret == 137:
                    msg = 'Your process used too much CPU time.\n'
                msg += 'Process finished with non-zero exit status %d' % p.returncode
                failed = True
                break

            now = time.time()
            if now - start >= max_wall_time:
                msg = 'Program took too long to run.'
                failed = True
                break

        kill_process(p)

        stdout = ''.join(stdout)
        stderr = ''.join(stderr)
        output = [msg] if msg else []

        if not allow_stderr and stderr:
            failed = True
            output.append('Your code printed to stderr:')
            output.append(try_utf8(stderr))

        if required_stdout and not stdout:
            failed = True
            output.append('Submission produced no output (did you forget to print?)')

        return {
            'stdout': stdout,
            'stderr': stderr,
            'failed': failed,
            'output': '\n'.join(output)
        }

    def close(self):
        if self.directory:
            shutil.rmtree(self.directory)
            self.directory = None

def check_output(
    actual:str, expected:str,
    wrong_score=0,
    caps_score=1,
    punctuation_score=2,
    whitespace_score=3,
    correct_score=10,
) -> (int, str):
    if actual == expected:
        return correct_score, 'That looks good to me!'

    actual = ''.join(c for c in actual if c not in whitespace)
    expected = ''.join(c for c in expected if c not in whitespace)
    if actual == expected:
        return whitespace_score, 'Almost there, but check the whitespace (newlines, spaces, tabs)'

    actual = ''.join(c for c in actual if c not in punctuation)
    expected = ''.join(c for c in expected if c not in punctuation)
    if actual == expected:
        return punctuation_score, 'Getting there, but check that the punctuation is correct.'

    actual = ''.join(c for c in actual.lower() if c.islower())
    expected = ''.join(c for c in expected.lower() if c.islower())
    if actual == expected:
        return caps_score, "Your answer looks right, but some letters aren't capitalised correctly."

    return wrong_score, "Doesn't look right to me..."
