import os
from netranger.util import Shell
from netranger.util import log
import shutil
import errno

log('')


class FS(object):
    def ls(self, dirname):
        assert os.path.isdir(dirname)
        return os.listdir(dirname)

    def parent_dir(self, cwd):
        return os.path.abspath(os.path.join(cwd, os.pardir))

    def ftype(self, fname):
        if os.path.isdir(fname):
            catlog = 'dir'
        elif os.path.islink(fname):
            catlog = 'link'
        elif os.access(fname, os.X_OK):
            catlog = 'exe'
        else:
            catlog = 'file'
        return catlog

    def mv(self, src, dst):
        shutil.move(src, dst)

    def cp(self, src, dst):
        if os.path.isdir(src) and src[-1]!='/':
            src = src+'/'
        if os.path.isdir(dst) and dst[-1]!='/':
            dst = dst+'/'
        log('cp -r "{}" "{}"'.format(src, dst))
        Shell.run('cp -r "{}" "{}"'.format(src, dst))


class RcloneFile(object):
    def __init__(self, lpath, path):
        self.lpath = lpath
        self.path = path
        self.downloaded = False
        with open(lpath, "w") as f:
            f.write("")

    def download(self):
        if self.downloaded:
            return
        else:
            Shell.run('rclone copyto "{}" "{}"'.format(self.path, self.lpath))
            self.downloaded = True


class RcloneDir(object):
    def __init__(self, lpath, path):
        Shell.mkdir(lpath)
        self.lpath = lpath

        self.child = {}
        self.cached = False
        self.path = path

        if path is None:
            remotes = Shell.run('rclone listremotes').split(':\n')
            for remote in remotes:
                if len(remote)==0:
                    continue
                self.child[remote] = RcloneDir(os.path.join(lpath, remote), remote+':/')
            self.cached = True

    @property
    def contentcache(self):
        return self.child.keys()

    def lsd(self):
        info = Shell.run('rclone lsd {} --max-depth 1'.format(self.path))

        for line in info.split('\n'):
            line = line.strip()
            if len(line)>0:
                name = line.split()[-1]
                self.child[name] = RcloneDir(os.path.join(self.lpath, name), os.path.join(self.path, name))

    def lsl(self):
        info = Shell.run('rclone lsl {} --max-depth 1'.format(self.path))

        for line in info.split('\n'):
            line = line.strip()
            if len(line)>0:
                name = line.split()[-1]
                self.child[name] = RcloneFile(os.path.join(self.lpath, name), os.path.join(self.path, name))

    def ls(self):
        if not self.cached:
            self.cached = True
            # files = Shell.run('rclone lsl --max-depth 1')
            self.lsd()
            self.lsl()
            self.cached = True
        return self.contentcache


class RClone(object):
    def __init__(self, cache_dir):
        if cache_dir[-1] == '/':
            cache_dir = cache_dir[:-1]

        self.rplen = len(cache_dir)+1
        self.root_dir = RcloneDir(cache_dir, None)

    @property
    def has_remote(self):
        return len(self.root_dir.child)>0

    def ftype(self, fname):
        if os.path.isdir(fname):
            catlog = 'dir'
        elif os.path.islink(fname):
            catlog = 'link'
        elif os.access(fname, os.X_OK):
            catlog = 'exe'
        else:
            catlog = 'file'
        return catlog

    def getNode(self, path):
        curNode = self.root_dir

        for name in path[self.rplen:].split('/'):
            if len(name) == 0:
                continue
            curNode = curNode.child[name]
        return curNode

    def ls(self, dirname):
        return self.getNode(dirname).ls()

    def download(self, fname):
        self.getNode(fname).download()

    def parent_dir(self, cwd):
        log('fuck')
        log(cwd, len(cwd), self.rplen-1)
        if len(cwd) == self.rplen-1:
            return cwd
        return os.path.abspath(os.path.join(cwd, os.pardir))

    @classmethod
    def valid_or_install(cls, vim):
        import platform
        import zipfile

        def getUserInput(vim, hint, default=''):
            vim.command('let g:NETRInputReg=input("{}: ", "{}")'.format(hint, default))
            return vim.vars['NETRInputReg']

        if Shell.isinPATH('rclone'):
            return True
        else:
            rclone_dir = getUserInput(vim, 'Rclone not in PATH. Install it at (modify/enter)', os.path.expanduser('~/rclone'))
            Shell.mkdir(rclone_dir)

            system = platform.system().lower()
            processor = 'amd64'
            if '386' in platform.processor():
                processor = '386'
            else:
                # Should support arm??
                pass

            url = 'https://downloads.rclone.org/rclone-current-{}-{}.zip'.format(system, processor)
            zip_fname = os.path.join(rclone_dir, 'rclone.zip')
            Shell.urldownload(url, zip_fname)
            zip_ref = zipfile.ZipFile(zip_fname, 'r')
            zip_ref.extractall(rclone_dir)
            for entry in zip_ref.NameToInfo:
                if entry.endswith('rclone'):
                    Shell.cp(os.path.join(rclone_dir, entry), rclone_dir)
                    Shell.chmod(os.path.join(rclone_dir,'rclone'), 755)

            zip_ref.close()
            os.remove(zip_fname)

            shellrc = getUserInput(vim, 'Update PATH in (leave blank to set manually later)', Shell.shellrc())
            with open(shellrc, 'a') as f:
                f.write('PATH={}:$PATH\n'.format(rclone_dir))
            os.environ['PATH'] += ':' + rclone_dir