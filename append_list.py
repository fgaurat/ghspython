# -*- coding: utf-8 -*-

def show_list(lines):    
    for line in lines:
        print(line.upper())
    return 0

def append_items(list,*items):
    for item in items:
        list.append(item)


a = {"a","b","r",'a'}
la_liste = []
append_items(la_liste,"toto")
print(la_liste)

append_items(la_liste,"toto","titi")
print(la_liste)

append_items(la_liste,"toto","titi","tata")
print(la_liste)

# lines = []
# str = input("Valeur : ")
# while str != 'end':
#     lines.append(str)
#     str = input("Valeur : ")


# if show_list(lines)



