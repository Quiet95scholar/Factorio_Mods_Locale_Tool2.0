import os
import re
import sys

import polib
from modZipClass import modZip

'''全局变量'''

# 文本库
Factorio_Mods_Locale = 'Factorio_Mods_Locale'
# 默认MOD库
ModsPath = 'mods'
ModsPath = os.path.join(os.getcwd(), ModsPath)
# 操作模式 真 or 假 //TODO 录入
absorb = True
# 汉化者名称//TODO absorb=1的时候录入
name = "安静书生"
# 汉化者邮箱//TODO absorb=0的时候录入
email = "linshuboy@qq.com"
# 汉化团队邮箱
team_email = "linshuboy@qq.com"
# 翻译方向//TODO 最好是录入
from_lang = "en"
to_lang = "zh-CN"


def make_mod_path(file_name):
    return os.path.join(ModsPath, file_name)


try:
    os.mkdir(Factorio_Mods_Locale)
except:
    x = 1
try:
    os.mkdir(ModsPath)
except:
    x = 1

modList = list(map(make_mod_path, os.listdir(ModsPath)))

if len(sys.argv) > 1:
    modList = sys.argv[1:]

for mod_path in modList:
    a = re.search(r'.*_\d+.\d+.\d+(\.[zZ][iI][Pp])+', os.path.split(mod_path)[1])
    if a:
        print(a.group(0))
        mod = modZip(mod_path, from_lang=from_lang, to_lang=to_lang)
        Factorio_Mods_Locale_path = os.path.join(Factorio_Mods_Locale, mod.name + ".po")
        if not os.path.exists(Factorio_Mods_Locale_path):
            mod.po.save(Factorio_Mods_Locale_path)
        pol = polib.pofile(Factorio_Mods_Locale_path)
        if absorb:
            mod.add_matadate(email)
            pol.absorb(mod.po)
            pol.save(Factorio_Mods_Locale_path)
        else:
            mod.translate(pol)
