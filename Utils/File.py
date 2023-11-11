def convertFilePath(path):
    x = ""
    for i in path:
        if i == ".":
            x += i
        elif i == "/":
            x += i
        elif i.isalnum():
            x += i
        elif i == " ":
            x += i
        elif i == "-":
            x += i

    while "  " in x:
        x = x.replace("  ", " ")
    return x