import os
import sys
x = [str(i) for i in sorted([int(i) for i in os.listdir("uploads")])]
mainFile = open(str(sys.argv[1]),"w")
for i in x:
    pathRelative = os.path.join("uploads",str(i))
    foo = open(pathRelative,"r").read()
    mainFile.write(foo)
    mainFile.write("\n")


