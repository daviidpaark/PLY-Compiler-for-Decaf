# David Park
# dappark
# 109582425


global f


def openFile(file):
    global f
    f = open(file + ".ami", "w")
    return f


def writeFile(code):
    code = "\t" + code + "\n"
    f.write(code)


def closeFile(file):
    file.close()


def newLabel(name):
    label = name + ":\n"
    f.write(label)
