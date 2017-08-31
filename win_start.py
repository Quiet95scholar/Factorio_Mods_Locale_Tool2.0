import os
import sys

import polib
from modZipClass import modZip

'''全局变量'''

# 文本库
Factorio_Mods_Locale = 'Factorio_Mods_Locale'
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
to_lang = "zh-cn"

if len(sys.argv) > 1:
    modList = sys.argv[1:]
else:
    modList = ['E:\Git\Factorio_Mods_Locale_Tool2.0\mods\Hexi_Maze_Mod_1.2.0.zip']

try:
    os.mkdir(Factorio_Mods_Locale)
except:
    x = 1

for mod_path in modList:
    mod = modZip(mod_path, from_lang=from_lang, to_lang=to_lang)
    Factorio_Mods_Locale_path = os.path.join(Factorio_Mods_Locale, mod.name + ".po")
    mod.add_matadate(email)
    if not os.path.exists(Factorio_Mods_Locale_path):
        mod.po.save(Factorio_Mods_Locale_path)
    pol = polib.pofile(Factorio_Mods_Locale_path)
    if absorb:
        pol.absorb(mod.po)
        pol.save(Factorio_Mods_Locale_path)
