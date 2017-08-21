from modZipClass import modZip

a = modZip('F:/python_factorio/mods/5dim_nuclear_0.15.2.zip')
a.set_json()
print(a.rewrite_dict)
