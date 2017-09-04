import json
import os
import re
import zipfile

from modClass import mod


class modZip(mod):
    def __init__(self, path, from_lang='en', to_lang=''):
        super().__init__(path, from_lang, to_lang)
        self.modZip = zipfile.ZipFile(self.in_path, 'a')
        self.init_all()

    '''
    获取json文件'''

    def get_json(self):
        read_name = ""
        fileList = self.modZip.namelist()
        for file_name in fileList:
            if file_name[-len("/info.json"):] == "/info.json":
                if "version" in json.loads(self.modZip.read(file_name).decode('utf-8')).keys():
                    read_name = file_name
        content = self.modZip.read(read_name)
        content = content.decode('utf-8')
        content = json.loads(content)
        return content

    '''
    写入json文件'''

    def set_json(self, content):
        content = json.dumps(content, indent=4)
        self.rewrite_dict[os.path.splitext(self.fname)[0] + "/info.json"] = content.encode('utf-8')

    '''
    获取cfg文件列表'''

    def get_cfg_list(self, lang):
        list = []
        fileList = self.modZip.namelist()
        dirName = os.path.splitext(self.fname)[0] + "/locale/" + lang
        for file in fileList:
            if re.search(r'(.*\/)*\/locale\/' + lang + '\/.*\.[cC][fF][gG]', file):
                if os.path.splitext(file)[1] == '.cfg':
                    list.append(file)
        return list

    '''
    获取cfg文件'''

    def get_cfg(self, path):
        content = self.modZip.read(path)
        try:
            content = content.decode('utf-8')
        except:
            error = 1
            content = ""
        return content

    '''
    写入cfg文件'''

    def set_cfg(self, path, content):
        self.rewrite_dict[path] = content.encode('utf-8')
        return

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
