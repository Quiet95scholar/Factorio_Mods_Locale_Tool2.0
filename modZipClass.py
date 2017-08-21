import os
import zipfile
import json
from modClass import mod
import json
import os
import zipfile

from modClass import mod


class modZip(mod):
    def __init__(self, path):
        super().__init__(path)
        self.modZip = zipfile.ZipFile(self.in_path, 'a')
        self.rewrite_dict = {}

    '''
    获取json文件'''

    def get_json(self):
        content = self.modZip.read(os.path.splitext(self.fname)[0] + "/info.json").decode('utf-8')
        return json.loads(content)

    '''
    写入json文件'''

    def set_json(self):
        content = json.dumps(self.get_json(), indent=4)
        self.rewrite_dict[os.path.splitext(self.fname)[0] + "/info.json"] = content.encode('utf-8')

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
        if len(self.rewrite_dict) > 0:
            new_file_name = self.in_path + ".copy"
            new_file = zipfile.ZipFile(new_file_name, 'w')
            fileList = self.modZip.namelist()
            for file in fileList:
                if self.rewrite_dict.get(file, 0) == 0:
                    new_file.writestr(file, self.modZip.read(file))
            for file in self.rewrite_dict:
                new_file.writestr(file, self.rewrite_dict.get(file))
            new_file.close()
            self.modZip.close()
            os.remove(self.in_path)
            os.rename(new_file_name, self.in_path)
        return

    def __del__(self):
        self.rewrite()
        self.modZip.close()
