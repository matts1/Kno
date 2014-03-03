sudo rm -rf /usr/local/lib/python3.3/dist-packages/codejail-0.1-py3.3.egg/
cp -r codejail codejail_installer
cd codejail_installer
sudo python3 setup.py install
cd ../..
sudo rm -rf install/codejail_installer

sudo addgroup sandbox
sudo adduser --disabled-login sandbox --ingroup sandbox


sudo rm -rf $(pwd)/sandbox
sudo virtualenv-3.3 $(pwd)/sandbox

echo "#include <tunables/global>

$(pwd)/sandbox/bin/python {
    #include <abstractions/base>
    #include <abstractions/python>

    $(pwd)/sandbox/** mr,
    # If you have code that the sandbox must be able to access, add lines
    # pointing to those directories:
#    /the/path/to/your/sandbox-packages/** r,

    /tmp/codejail-*/ rix,
    /tmp/codejail-*/** rix,
}" | sudo tee $(echo "/etc/apparmor.d/$(echo $(pwd) | sed "s/\//./g" | tail -c +2).sandbox.bin.python")

sudo apparmor_parser $(echo "/etc/apparmor.d/$(echo $(pwd) | sed "s/\//./g" | tail -c +2).sandbox.bin.python")

echo "Copy this to your clipboard. When you press enter, nano will come up - paste it and save."
echo "$(whoami) ALL=(sandbox) SETENV:NOPASSWD:$(pwd)/sandbox/bin/python"
echo "$(whoami) ALL=(ALL) NOPASSWD:/usr/bin/pkill"

read a

sudo visudo -f /etc/sudoers.d/01-sandbox

python3 manage.py test noselenium
python3 manage.py syncdb
