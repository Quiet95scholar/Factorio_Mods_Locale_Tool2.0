import os
import re


class mod(object):
    def __init__(self, path):
        self.in_path = path
        self.fname = self.init_fname()
        self.path = self.init_path()
        self.name = self.init_name()
        self.version = self.init_version()

    '''
    获取MOD版本号'''

    def init_version(self):
        val_zip = re.search(r'(?<=_)\d+.\d+.\d+', self.fname)
        if val_zip:
            return val_zip.group(0)
        else:
            return

    '''外部获取MOD版本号'''

    def get_version(self):
        return self.version

    '''
    获取MOD真实地址'''

    def get_path(self):
        return self.path

    '''
    获取MOD名称'''

    def get_name(self):
        return self.name

    '''
    获取MOD文件地址'''

    def init_path(self):
        return os.path.split(self.in_path)[0]

    '''
    获取MOD文件/目录名称'''

    def init_fname(self):
        return os.path.split(self.in_path)[1]

    '''
    获取MOD名称'''

    def init_name(self):
        val_zip = re.search(r'.*(?=_\d+.\d+.\d+)', self.fname)
        if val_zip:
            return val_zip.group(0)
        else:
            return

    '''
    获取json文件'''

    def get_json(self):
        return

    '''
    写入json文件'''

    def set_json(self):
        return

    '''
    获取cfg文件列表'''

    def get_cfg_list(self):
        return

    '''
    获取cfg文件'''

    def get_cfg(self):
        return

    '''
    写入cfg文件'''

    def set_cfg(self):
        return

    '''
    获取cfg+json集合数组'''

    def get_all(self):
        return

    '''
    检查MOD类型'''

    def chack_mod(self):
        return True

    '''
    覆盖文件'''

    def rewrite(self):
        return
