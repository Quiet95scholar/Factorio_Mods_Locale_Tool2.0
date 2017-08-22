from modZipClass import modZip

a = modZip('/mnt/e/Git/Factorio_Mods_Locale_Tool2.0/mods/helmod_0.5.7.zip')
a.get_cfg_list('en')
print(a.from_cfg_list)
print(a.to_cfg_list)
