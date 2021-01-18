import re

def toshow(nottoshow, showing=7):
    showing = nottoshow[:showing - 1]
    for i in range(10, 13):
        showing += "#"
    return showing

def getinputnoerrors(prompt : str,multiline= False):
    try:
        if multiline:
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    return lines
        user = input(prompt)
        return user
    except ValueError:
        print("User Error")

def format(l):
    formatted = ""
    for char in l:
        formatted += f"{fg.red}{char[0]} {fg.blue}: {fg.yellow}{char[1]}"
        if l.index(char) == 0:
            pass
        else:
            formatted += " , "
    return formatted

def checknull(note):
    return bool(re.match('^[\n]+$', note))

class fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    darkgrey = '\033[90m'
    yellow = '\033[93m'
    pink = '\033[95m'
    norm = '\033[0m'