import json
import os
import zipfile

import polib

from modClass import mod


class modZip(mod):
    def __init__(self, path, from_lang='en', to_lang='zh-cn'):
        super().__init__(path)
        self.modZip = zipfile.ZipFile(self.in_path, 'a')
        self.rewrite_dict = {}
        self.from_cfg_list = self.get_cfg_list(from_lang)
        self.to_cfg_list = self.get_cfg_list(to_lang)
        self.init_all()

        self.thisPo = polib.POFile()
        self.thisPo.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'you@example.com',
            'POT-Creation-Date': '2007-10-18 14:00+0100',
            'PO-Revision-Date': '2007-10-18 14:00+0100',
            'Last-Translator': 'you <you@example.com>',
            'Language-Team': 'English <yourteam@example.com>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }
        for section in self.from_cfg_all.sections():
            for item in self.from_cfg_all.items(section):
                entry = polib.POEntry(
                    msgid=item[1],
                    msgstr=self.to_cfg_all.get(section, item[0]),
                    msgctxt=section + "." + item[0],
                )
                self.thisPo.append(entry)
        self.thisPo.save('newfile.po')

    '''
    获取json文件'''

    def get_json(self):
        content = self.modZip.read(os.path.splitext(self.fname)[0] + "/info.json").decode('utf-8')
        return json.loads(content)

    '''
    写入json文件'''

    def set_json(self, content):
        content = json.dumps(content, indent=4)
        self.rewrite_dict[os.path.splitext(self.fname)[0] + "/info.json"] = content.encode('utf-8')

    '''
    获取cfg文件列表'''

    def get_cfg_list(self, lang):
        list = [];
        fileList = self.modZip.namelist()
        dirName = os.path.splitext(self.fname)[0] + "/locale/" + lang
        for file in fileList:
            if file[:len(dirName + ".")].upper() == (dirName + ".").upper() or file[:len(dirName + "/")].upper() == (
                dirName + "/").upper():
                if os.path.splitext(file)[1] == '.cfg':
                    list.append(file)
        return list

    '''
    获取cfg文件'''

    def get_cfg(self, path):
        content = self.modZip.read(path)
        content = content.decode('utf-8')
        return content

    '''
    写入cfg文件'''

    def set_cfg(self, path, content):
        self.rewrite_dict[path] = content.encode('utf-8')
        return

    '''
    获取cfg+json集合数组'''

    def get_all(self):
        return

    '''
    初始化MODcfg对象'''

    def init_all(self):
        for file in self.from_cfg_list:
            content = self.get_cfg(file)
            content = '[' + self.key + ']\n' + content
            self.from_cfg_all.read_string(content)
        for file in self.to_cfg_list:
            content = self.get_cfg(file)
            content = '[' + self.key + ']\n' + content
            self.to_cfg_all.read_string(content)
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
