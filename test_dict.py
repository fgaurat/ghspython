 # -*- coding: utf-8 -*-
import pprint
tel = {'jack': 4098, 'sape': ['toto','titi']}
tel.update({'toto':123})
print(tel)
pprint.pprint(tel)


for key in tel.keys():
    print(key,tel[key])