# -*- coding: utf-8 -*-




with open("the_file.txt","w") as f:
    f.write("Toto\n")
    f.write("Toto 1\n")
    f.write("Toto 2\n")
    f.write("Toto 3\n")
    f.write("Toto 4\n")

with open("the_file.txt","r") as f:
    lines = f.readlines()
    print(lines)