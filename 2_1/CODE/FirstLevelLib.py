from random import choice
import string
chars_up = list(string.ascii_uppercase)
chars_down = list(string.ascii_lowercase) + list("àèìòù")
digits = list(string.digits)
simbols = list(string.punctuation)
chars = chars_up + chars_down + digits + simbols

def password_base(lenght):
    types = ["a", "A", "N", "S"]
    last = ""
    base = ""
    # aNASaNSA
    def subst(word, old_index, char):
        return word[:old_index] + char + word[old_index + 1:]

    for i in range(0, lenght):
        ch = choice(types)
        if last == "ch":
            while ch == last:
                ch = choice(types)
        base += ch
        last = ch
    last = ""
    cont = 0
    for char in base:
        if last == char:
            types.remove(char)
            new = choice(types)
            base = subst(base, cont, new)
            types.append(char)
            cont = 0
        last = char
        cont += 1
    return base

def CRC__(base,pwd=False):
    crc = ""
    usr = list("`{|}<>~^[\],.()\'")
    if pwd: # if Generating a password: Annoying to digit characters removed
        for item in usr:
            simbols.remove(item)
    for char in base:
        if char == "a":
            crc += choice(chars_down)
        elif char == "A":
            crc += choice(chars_up)
        elif char == "N":
            crc += choice(digits)
        elif char == "S":
            crc += choice(simbols)
    if pwd:
        for item in usr:
            simbols.append(item)
    return crc

def secure_pass(lenght,p=True):
    spass = CRC__(password_base(lenght),pwd=p)
    return spass

def secure_hash(lenght,pwd =False):
    rstring = ""
    usr = list("`/{|}<>~^[\],.")
    if pwd: # Annoying to digit characters removed, creating db hash
        for item in usr:
            simbols.remove(item)
    for i in range(0, lenght):
        rstring += choice(chars)
    if pwd:
        for item in usr:
            simbols.append(item) # then re-appended
    return rstring

def new_dictionary(len_hash=0,len_crc=0,default = False,custom_crc=""):
    if default:
        len_crc,len_hash=5,4
    # Parte variabile / Variable Part
                # +
    # Parte Costante / Constant Part
                # =
    # Generazione AlphaBeta v1.0 / AlphaBeta v1.0 Generation
    CRC = custom_crc
    if len(CRC) == 0:
        CRC = CRC__(password_base(len_crc))

    alphaBeta = {}
    for i in range(0, len(chars)):
        var = secure_hash(len_hash)
        alphaBeta[chars[i]] = CRC + var
    return alphaBeta
