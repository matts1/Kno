from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from common.functions import makepath
from tasks.models import Task
import os

class CodeTask(Task):
    class Meta:
        app_label = 'tasks'

    @classmethod
    def create(cls, *args, **kwargs):
        val = super().create(*args, **kwargs)
        os.mkdir(val.get_path())
        return val

    def get_path(self, name=''):
        return makepath('codeio/{}/{}'.format(self.id, name))

    def get_io_files(self):
        files = os.listdir(self.get_path())
        return sorted(set(['.'.join(f.split('.')[:-1]) for f in files]))

    def has_io_files(self, name):
        return os.path.isfile(self.get_path(name + '.in'))

    def add_io_files(self, name, infile, outfile):
        path = self.get_path(name)
        default_storage.save(path + '.in', ContentFile(infile.read()))
        default_storage.save(path + '.out', ContentFile(outfile.read()))

    def delete_io_files(self, name):
        path = self.get_path(name)
        default_storage.delete(path + '.in')
        default_storage.delete(path + '.out')
