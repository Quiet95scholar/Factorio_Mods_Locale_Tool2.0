import configparser
import hashlib
import os
import re
import time

import polib


class mod(object):
    # type localization absorb
    def __init__(self, path, from_lang='en', to_lang='zh_cn'):
        self.in_path = path
        self.from_lang = from_lang
        self.to_lang = to_lang

    def add_matadate(self, email="you@example.com"):
        self.po.metadata = {
            'Project-Id-Version': self.version,
            'Report-Msgid-Bugs-To': email,
            'POT-Creation-Date': time.strftime('%Y-%m-%d %H:%M+%S', time.localtime(time.time())),
            'PO-Revision-Date': time.strftime('%Y-%m-%d %H:%M+%S', time.localtime(time.time())),
            'Last-Translator': email,
            'Language-Team': self.from_lang + ' <' + email + '>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
            'Language': self.to_lang,
        }

    def md5hex(self, word):
        """ MD5加密算法，返回32位小写16进制符号
        """
        m = hashlib.md5()
        m.update(word.encode("utf-8"))
        return m.hexdigest()

    def init_all(self):
        self.key = "factorio"
        self.fname = self.init_fname()
        self.path = self.init_path()
        self.name = self.init_name()
        self.key = self.name + self.md5hex(self.key + self.name)
        self.version = self.init_version()
        self.from_cfg_all = configparser.RawConfigParser()
        self.to_cfg_all = configparser.RawConfigParser()
        self.rewrite_dict = {}
        self.from_cfg_list = self.get_cfg_list(self.from_lang)
        self.to_cfg_list = self.get_cfg_list(self.to_lang)
        self.init_cfg_obj()
        self.po = polib.POFile()
        self.init_po()

    '''
    初始化MODcfg对象'''

    def init_cfg_obj(self):
        for file in self.from_cfg_list:
            content = self.get_cfg(file)
            content = '[' + self.key + ']\n' + content
            self.from_cfg_all.read_string(content)
        for file in self.to_cfg_list:
            content = self.get_cfg(file)
            content = '[' + self.key + ']\n' + content
            self.to_cfg_all.read_string(content)
        json = self.get_json()
        self.to_cfg_all.read_string('[' + self.key + ']\n')
        if json.__contains__('description_original'):
            self.from_cfg_all.set(self.key, "description", json['description_original'])
            self.to_cfg_all.set(self.key, "description", json['description'])
        else:
            self.from_cfg_all.set(self.key, "description", json['description'])
        if json.__contains__('title_original'):
            self.from_cfg_all.set(self.key, "title", json['title_original'])
            self.to_cfg_all.set(self.key, "title", json['title'])
        else:
            self.from_cfg_all.set(self.key, "title", json['title'])

    '''初始化当前对象的po对象'''

    def init_po(self):
        for section in self.from_cfg_all.sections():
            for item in self.from_cfg_all.items(section):
                try:
                    msgstr = self.to_cfg_all.get(section, item[0])
                except:
                    msgstr = ""
                if item[1] == msgstr:
                    msgstr = ""
                entry = polib.POEntry(
                    msgctxt=section + "." + item[0],
                    msgid=item[1],
                    msgstr=msgstr
                )
                self.po.append(entry)

    '''
    获取MOD版本号'''

    def init_version(self):
        return self.get_json()['version']

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

    def get_cfg_list(self, lang):
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

    '''汉化文件'''

    def translate(self, po):
        self.pol = po
        # self.translate_json()
        self.translate_cfg()

    def translate_json(self):
        json = self.get_json()
        title = self.pol.get_entry_by_msgctxt(self.key + ".title")
        description = self.pol.get_entry_by_msgctxt(self.key + ".description")
        if title.msgstr != '' and title.msgstr != title.msgid:
            json['title'] = title.msgstr
            json['title_original'] = title.msgid
        else:
            json['title'] = title.msgid
        if description.msgstr != '' and description.msgstr != description.msgid:
            json['description'] = description.msgstr
            json['description_original'] = description.msgid
        else:
            json['description'] = description.msgid
        self.get_json(json)

    def translate_cfg(self):
        for file_name in self.from_cfg_list:
            content = '[' + self.key + ']\n' + self.get_cfg(file_name)
            for entry in self.pol:
                sele = entry.msgctxt.split('.')[0]
                item = entry.msgctxt.split('.')[1]
                if entry.msgstr != '':
                    zz = r"\[" + re.escape(sele) + "\].*?(?=" + re.escape(item + "=" + entry.msgid) + ")"
                    val_zip = re.search(zz, content, re.DOTALL)
                    if val_zip:
                        content = re.sub(r"(?<=" + re.escape(val_zip.group(0)) + ").*",
                                         item + "=" + repr(entry.msgstr)[1:-1], content)
            self.set_cfg(re.sub(r"(?<=[\\\/])" + self.from_lang + "(?=[\\\/])", self.to_lang, file_name),
                         re.sub(r'\[' + self.key + '\]\n', '', content))
