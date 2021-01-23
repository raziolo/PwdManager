sys.path.extend(path+"CODE")
from difflib import SequenceMatcher
from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidKey
from datetime import datetime
from CODE.Windows import *
from CODE.FirstLevelLib import *
from CODE.Utils import *
from CODE.Langs import langs
from pydrive.drive import GoogleDrive
from pydrive.settings import InvalidConfigError
from pydrive.auth import GoogleAuth
import PySimpleGUI as sg
from time import sleep
import json,sys,webbrowser
#os.system("color")
sg.theme("Dark Purple 4")
font10 = ("Calibri",10)
font15 = ("Calibri",20)
font20 = ("Calibri",20)
font25 = ("Calibri",25)


# chars = shuffle(chars)
oggi = datetime.today().strftime("%m%d%Y")
ora = datetime.today().strftime("%H_%M")
lang = str
gui = bool
fast_load = bool


class BigFile:
    def __init__(self, name, key, dictionary, passwords,notes, encrypted):
        self.name = name
        self.key = key
        self.dictionary = dictionary
        self.passwords = passwords
        self.notes = notes
        self.encrypted = encrypted


    def renamedb(self,new):
        old_file = open(path_big_files+self.name,"r")
        old_file = old_file.read()
        new_file = open(path_big_files+new,"w")
        new_file.write(old_file)
        new_file.close()
        if self.name == new:
            pass
        else:
            os.remove(path_big_files + self.name)
        self.name = new


    def charge(self):
        global fast_load
        files = [file for file in os.listdir(path_big_files) if file.endswith(".aesdb")]
        try:
            if not files:
                self.new_db(sub=True)
                return
            if fast_load:
                try:
                    self.key = fast_load_key
                    self.name = "fastload.aesdb"
                    self.passwords, self.dictionary,self.notes = Big.Deconstruction(
                        (Big.decrypt(open(path_big_files + self.name, "r").read().encode("utf-8"))))
                    self.encrypted = False
                    print(fg.red + "FASTLOADFASTLOADFASTLOAD" + fg.norm)
                except FileNotFoundError:
                    print(langs("err",7))
                    fast_load=False
                    preferences(("f",False))
                    return
                except InvalidKey:
                    fast_load = False
                    preferences(("f",False))
                    return
                except (InvalidToken, ValueError):
                    fast_load = False
                    preferences(("f",False))
                    return
            if not fast_load:
                if gui:
                    loading_with_gui(Big,files)
                else:
                    for item in enumerate(files,start=1):
                        print(item[0],item[1])
                    user = int(getinputnoerrors("Database (1-n|0=new db) : "))
                    if user == 0:
                        self.new_db(True)
                    else:
                        for file in enumerate(files,start=1):
                            if user == file[0]:
                                self.name = file[1]
                            else:
                                print(langs("err",3))
                                return main()
                            self.key = getinputnoerrors("Key: ").encode("utf-8")
                            self.passwords, self.dictionary,self.notes = Big.Deconstruction(
                                (Big.decrypt(open(path_big_files + self.name, "r").read().encode("utf-8"))))
                            self.encrypted = False
                            print(langs("p", 3))
        except FileNotFoundError:
            print(langs("err",7))
            fast_load = False
            preferences(("f", False))
            return
        except InvalidKey:
            print(langs("err",1))
            fast_load = False
            preferences(("f", False))
            return
        except (InvalidToken, ValueError):
            print(langs("err",2))
            fast_load = False
            preferences(("f", False))

    def new_db(self, sub=False):

        if gui:
            if sub:
                self.name = "DB_" + secure_hash(3, pwd=True) + ".aesdb"
                self.key = Fernet.generate_key()
                self.dictionary = new_dictionary(default=True)
                self.passwords = []
                self.encrypted = False
                self.encrypt()
                if fast_load:
                    preferences(("f", True))
                return winshowkey(self.key)
            if not sub:
                TEMP = BigFile(
                    name="DB_" + secure_hash(3, pwd=True) + ".aesdb",
                    key=Fernet.generate_key(),
                    dictionary=new_dictionary(default=True),
                    passwords=[],
                    notes=[],
                    encrypted=False
                )
                TEMP.encrypt()
                return winshowkey(TEMP.key.decode("utf-8"))

        if not gui:
            if sub:
                print(langs("p", 1))
                self.name = "DB_" + secure_hash(3, pwd=True) + ".aesdb"
                self.key = Fernet.generate_key()
                self.dictionary = new_dictionary(default=True)
                self.passwords = []
                self.notes = []
                self.encrypted = False
                new = open(path_big_files + self.name, "w")
                new.write("")
                new.close()
                print(langs("p", 9))
                print(fg.red + langs("p", 8 )+ fg.yellow + str(self.key.decode("utf-8") + fg.norm))
                self.encrypt()
                print(langs("p", 3))
                preferences(default=True)
            if not sub:
                TEMP = BigFile(
                    name = "DB_" + secure_hash(3, pwd=True) + ".aesdb",
                    key = Fernet.generate_key(),
                    dictionary = new_dictionary(default=True),
                    passwords = [],
                    notes=[],
                    encrypted = False
                )
                print(fg.red + langs("p", 8 )+ fg.yellow + str(TEMP.key.decode("utf-8") + fg.norm))
                TEMP.encrypt()

    ### THIS FUNCTION IS CURRENTLY UNDER DEVELOPMENT ###

    def cloudupload(self):
        gauth = GoogleAuth()
        try:
            gauth.LoadCredentialsFile("cloud.txt")
        except:
            print(langs("err",9))
        if gauth.credentials is None:
            try:
                gauth.LocalWebserverAuth()
                print(langs("p",41))
                if getinputnoerrors("y/n : ") == "y":
                    gauth.SaveCredentialsFile("cloud.txt")
            except InvalidConfigError:
                print(langs("err", 10))
        drive = GoogleDrive(gauth)
        file1 = drive.CreateFile({'title': self.name})
        file1.SetContentString(str(open(path_big_files + self.name, 'r').read()))
        try:
            file1.Upload()
            if gui:
                sg.Popup("Success",auto_close=True,auto_close_duration=2)
            else:
                print(langs("p",38))
        except InvalidConfigError:
            print(langs("err",8))
            print(langs("p",42))
            comando = getinputnoerrors(": ")
            if comando== "console":
                webbrowser.open('https://console.developers.google.com/apis/api/drive/overview')
            elif comando == "readme":
                sleep(8)
            elif comando== "guide":
                webbrowser.open("https://medium.com/@annissouames99/how-to-upload-files-automatically-to-drive-with-python-ee19bb13dda")


        return
    ### END OF WIP FUNCTION ###

    def Construction(self):

        Constructed = [self.passwords,self.dictionary,self.notes]
        Constructed = json.dumps(Constructed)
        return Constructed

    @staticmethod
    def Deconstruction(big_file):  # static method here for grouping purposes
        # OLD DECONSTRUCTION METHOD
        '''import ast
        out = ast.literal_eval(big_file)
        a = out.index("################")
        passwords = out[:a]
        dictionary = eval(str(out[a[0] + 1:][0]))
        notes = a[1]"'''
        # NEW DECONSTRUCTION METHOD
        passwords,dictionary,notes = json.loads(big_file)
        return passwords, dictionary,notes

    def Migration(self, new_dict):
        old_dict = self.dictionary
        new_passwords = []
        for password in Big.passwords:
            self.dictionary = old_dict
            decrypted = self.fromfirstlevel(password["firstlevel"])
            self.dictionary = new_dict
            encrypted = self.tofirstlevel(decrypted)
            password["firstlevel"] = encrypted
            new_passwords.append(password)
        self.dictionary = new_dict
        self.passwords = new_passwords
        self.encrypt()

    def tofirstlevel(self, password):
        password = str(password)
        encrypted = ""
        for letter in password:
            for item, value in self.dictionary.items():
                if letter == item:
                    encrypted += value
        return encrypted

    def fromvalues(self, value):
        for plain_char, single in self.dictionary.items():
            if single == value:
                return plain_char

    def fromfirstlevel(self, single): # ASD1anbgASD1ahbg 
        result = ""
        lungh_pezzo = len(self.dictionary["A"]) # ASD1adsv
        hashed = [single[i:i + lungh_pezzo] for i in range(0, len(single), lungh_pezzo)]
        for pezzo in hashed:
            pezzo = pezzo.rstrip()
            result += self.fromvalues(pezzo)
        return result

    def encrypt(self,message:bool=False):
        f = Fernet(self.key)
        encrypted_big_file = f.encrypt(str(self.Construction()).encode("utf-8"))
        file = open(path_big_files + self.name, "wb")
        file.write(encrypted_big_file)
        if message:
            print(langs("p", 7))
        file.close()
        return fg.green + "Success" +fg.norm

    def decrypt(self, what):
        try:
            f = Fernet(self.key)
            decrypted = f.decrypt(what).decode("utf-8")
            self.encrypted = False
            return decrypted
        except ValueError:
            print(langs("err",1))
            self.encrypted = True
        except (InvalidKey, InvalidToken):
            print(langs("err",2))
            self.encrypted = True

    def delete(self,key):
        results = []
        for item in self.passwords:
            for i,v in item.items():
                if i == "plain_pass":
                    v = self.fromfirstlevel(item["firstlevel"])
                if key == v:
                    results.append(item)
        if len(results) > 1:
            print(langs("p",39))
            if getinputnoerrors("y/n : ") == "y":
                for item in results:
                    self.passwords.remove(item)
                self.encrypt()
            else:
                pass
        elif len(results) == 1:
            self.passwords.remove(results[0])
            self.encrypt()
        elif not results:
            print(langs("p",33))

    def modpwd(self,new, ind):
        self.passwords.pop(ind)
        self.passwords.insert(ind,new)


    def printpwd(self,password_id):
        for item,value in password_id.items():
            if item == "plain_pass":
                value = self.fromfirstlevel(password_id["firstlevel"])
            print(f"{fg.yellow}{item} : {fg.red}{value}{fg.norm}")

    def search(self,key=""):
        if key:
            results = []
            for pwd in self.passwords:
                for item,value in pwd.items():
                    if item == "plain_pass":
                        value = self.fromfirstlevel(pwd["firstlevel"])
                    if SequenceMatcher(value,key).ratio() > 0.66 or value == key:
                        results.append(self.passwords.index(pwd))
                    else:
                        pass
            if not results:
                print(langs("p",33))
            elif len(results) > 1:
                print(langs("p",34))
            return results


    def printall(self, comando):
        def parser_printall(comando):
            if comando.__contains__("-p"):
                p = 1
            else:
                p = 0
            if comando.__contains__("-d"):
                d = 1
            else:
                d = 0
            if comando.__contains__("-h"):
                h = 1
            else:
                h = 0
            return p, d, h
        p,d,h = parser_printall(comando)
        if p == 1:
            # print all passwords
            print(fg.green + 'PWDS' + fg.norm)

            for password in self.passwords:
                if password:
                    password["plain_pass"] = self.fromfirstlevel(password["firstlevel"])
                    for item, value in password.items():
                        row = fg.yellow + item + fg.norm + " : " + fg.red + value + fg.norm
                        if h == 1: # if h parsed then hide the plain_pass
                            if item == "plain_pass":
                                value = "######"
                                row = fg.yellow + item + fg.norm + " : " + fg.red + value + fg.norm
                                print(row)
                            else:
                                print(row)
                        else:
                            print(row)
                    print("\n")
                else:
                    print(langs("err",5))
        if d == 1:
            try:
                # print all dictionary chars and hashes, separated in groups
                print(fg.green + 'AlphaBeta Dictionary' + fg.norm)
                row_ups, row_lows, row_digits, row_simbols = "", "", "", ""
                uppercases_res, lowercases_res, digits_res, simbols_res = [["UPPERCASES",""]], \
                                                                          [["LOWERCASES",""]], \
                                                                          [["DIGITS",""]], \
                                                                          [["NUMBERS",""]]
                for char, value in self.dictionary.items():
                    if char in chars_up:
                        uppercases_res.append([char, value])
                    elif char in chars_down:
                        lowercases_res.append([char, value])
                    elif char in digits:
                        digits_res.append([char, value])
                    elif char in simbols:
                        simbols_res.append([char, value])
                # Crea liste di caratteri e hash
                chars = [uppercases_res,lowercases_res,digits_res,simbols_res]
                for l in chars:
                    print(format(l))
                print(fg.norm)

            except AttributeError:
                print(langs("p",31))
                try:
                    new = new_dictionary(default=True)
                    self.Migration(new)
                except AttributeError:
                    self.dictionary = new_dictionary(default=True)
                    print(langs("p",32))

    def __clean_db__(self):
        self.passwords = []
        print(langs("p",30))
        print(self.encrypt())

    def savekey(self):
        file = open(path_keys + "key_" + self.name[:-6] + ".aeskey", "w")
        file.write(self.key.decode("utf-8"))
        file.close()
        return "key_" + self.name[:-6] + ".aeskey"

    def add_password(self, pwd="",site="",username=""):

        password_id = {
            "plain_pass": "",
            "username": username,
            "site": site,
            "firstlevel": self.tofirstlevel(pwd)
        }
        self.passwords.append(password_id)
        self.encrypt()

    def checkfirstlevel(self,note:list):
        for val in self.dictionary.values():
            for i in note:
                if i.__contains__(val):
                    return True
        return False

    def new_key(self,new):
        self.key= new

    def add_note(self,note):
        self.notes.append(note)
        self.encrypt()

    def delnote(self,ind):
        self.notes.pop(ind)

def __keys__():
    print(langs("p",18))
    print(langs("p",19))
    while True:
        user = getinputnoerrors("comando: ")
        if user == "new":
            new_key = Fernet.generate_key()
            print(langs("p",22) + fg.yellow + str(new_key.decode("utf-8")) + fg.norm)
            print(langs("p",20))
            user = getinputnoerrors(": ")
            if user == "y":
                Big.new_key(new_key)
                Big.encrypt()
                preferences(save=True)
                break

        elif user == "show":
            print(langs("p",37))
        elif user == "save":
            name = Big.savekey()
            print("Saved to: " + name)
        elif user == "help":
            m = langs("keys_help", 0)
            for command in m:
                print(fg.red + str(command[0]) + fg.norm + " : " + fg.yellow + str(command[1]) + fg.norm)
        else:
            break

def __dicts__():
    print(langs("p",3))
    user = getinputnoerrors(": ")
    if user == "new":
        crc = getinputnoerrors(langs("p",45))
        len_hash = int(getinputnoerrors(langs("p",46)))
        if crc.isdigit():
            crc = int(crc)
            new = new_dictionary(len_hash, crc)
        else:
            new = new_dictionary(len_hash, custom_crc=crc)
        print(langs("p",2))
        name = "EncryptDict" + str(oggi) + ".dict"
        print(langs("p",1) + name)
        user = getinputnoerrors("y/n: ")
        if user == "y":
            Big.Migration(new)
        elif user == "n":
            file = open(path_dicts + name, "w")
            file.write(str(new))
            file.close()


def modpwd_cli(res):
    if len(res) > 1:
        for item in enumerate(res, start=1):
            print(f"N: {str(item[0])}")
            Big.printpwd(Big.passwords[item[1]])
        user = int(getinputnoerrors("N: "))
        for item in enumerate(res):
            if user == item[0]:
                res = [item[0]]
                break
    new_entry = {}
    ind = res[0] - 1
    i = Big.passwords[ind]
    for ident, value in i.items():
        if ident == "firstlevel":
            new_entry[ident] = Big.tofirstlevel(new_entry["plain_pass"])
            break
        new = getinputnoerrors(f"New \"{ident}\" (old: {value}):")
        if new == "" or new == value:
            new_entry[ident] = value
        elif ident == "plain_pass" and new == "gen":
            new_entry["plain_pass"] = secure_pass(9)
        else:
            new_entry[ident] = new
        return new_entry, ind

def notes_cli(comando):

    if comando.__contains__("-v"):
        if not Big.notes:
            print(langs("p", 33))
            return
        for i in enumerate(Big.notes):
            print(fg.red + str(i[0]) + fg.norm, fg.yellow + " ".join(i[1][:2]) + fg.red + " ..." + fg.norm)
        user = int(getinputnoerrors("N: "))
        note = []
        for i in enumerate(Big.notes):
            if user == i[0]:
                note = i[1]
        print("\n")
        for i in note:
            print(i)
        print("\n")
        return notes_cli("note -v".split())
    elif comando.__contains__("-d"):
        if not Big.notes:
            print(langs("p", 33))
            return
        for i in enumerate(Big.notes):
            print(fg.red + str(i[0]) + fg.norm, fg.yellow + " ".join(i[1][:2]) + fg.red + " ..." + fg.norm)
        user = int(getinputnoerrors("N: "))
        for i in enumerate(Big.notes):
            if user == i[0]:
                Big.delnote(i[0])
                Big.encrypt()
    else:
        print(langs("p", 47))
        note = getinputnoerrors("", multiline=True)
        Big.add_note(note)


Big = BigFile("", b'', 0, [],[], True)

def main():
    global lang,gui,fast_load,fast_load_key
    while True:
        if Big.dictionary == 0:
            Big.charge()
        else:
            break

    while True:
        if gui:

            layout = [[sg.Text("Current Database: "), sg.Text(Big.name,key="showdb",text_color="yellow",justification="right")],
                      [sg.Text("Current Dictionary: ",justification="left"),sg.Text(toshow(Big.dictionary["A"],5),justification="right",text_color="yellow",key="showdict")],
                      [sg.Text("Current key:     "),sg.Text(toshow(Big.key.decode("utf-8"),5),key="showkey",text_color="yellow",justification="right")],
                      [sg.Text("--- DB OPERATIONS ---")],
                      [sg.Button("New",key="newdb"),sg.Button("Rename",key="rename"),sg.InputText(key="newname",size=(10,1)),sg.Button("Upload",key="upload")],
                      [sg.Text("--- KEY OPERATIONS ---")],
                      [sg.Button("Copy", key="copy_key"), sg.Button("Change", key="change_key"),sg.Button("Save",key="save_key")],
                      [sg.Text("--- DICTIONARY OPERATIONS ---")],
                      [sg.Button("Visualize", key="gui_dicts"),sg.Button("Save",key="save_dict"),sg.Button("Import",key="import_dict"),sg.Button("New",key="new_dict"),sg.Checkbox("Custom Build",key="custom")],
                      [sg.Text("--- FIRSTLEVEL TECHNOLOGY---")],
                      [sg.Button("To Firstlevel",key="tofirstlevel"),sg.Button("From Firstlevel",key="fromfirstlevel")],
                      [sg.Text("--- PASSWORD OPERATIONS ---")],
                      [sg.Button("Passwords",key="PWDS_"),sg.Button("Add",key="newpwd"),sg.Button("Secure Pass",key="securepass")],
                      [sg.Text("--- NOTES OPERATIONS ---")],
                      [sg.Button("Add",key="newnote"),sg.Button("All", key="notes")],
                      [sg.Text("-------------")],
                      [sg.Button("EXIT",key="exit"),sg.Text("Preferences"),sg.Checkbox("Gui: ",default=bool(gui),key="gui",enable_events=True),sg.Checkbox("Fast-Load: ",default=bool(fast_load),key="fast_load",enable_events=True)]
                      ]
            root = sg.Window("PWD Manager 2.1",layout,font=font20,icon=path + "ico.ico")

            ### FUNCTIONS ###
            ### CATEGORY: FUNCTION NAME: EVENT KEY
            ### DB: NEW DB: newdb
            ### DB: RENAME: rename
            ### DB: UPLOAD: upload
            ### KEY: COPY: copy_key
            ### KEY: SAVE: save_key
            ### KEY: NEW: change_key
            ### PWD: ALL: PWDS_
            ### PWD: ADD: newpwd
            ### PWD: SECUREPASS: securepass
            ### FIRST: TOFIRSTLVL: tofirstlevel
            ### FIRST: FROMFIRSTLVL: fromfirstlevel
            ### DICTS: SAVE: savedict
            ### DICTS: ALL: gui_dicts
            ### DICTS: NEW: new_dict
            ### DICTS: IMPORT: import_dict
            ### NOTES: ADD: newnote
            ### NOTES: ALL: allnotes

            while True:
                events, values = root.read()
                if events == sg.WIN_CLOSED or events == "exit":
                    root.close()
                    quit(0)

                ### DB FUNCTIONS ###
                elif events == "newdb":
                    Big.new_db(sub=False)
                elif events == "rename":
                    new = values["newname"] + ".aesdb"
                    Big.renamedb(new)
                    root["showdb"].update(Big.name)
                elif events == "upload":
                    Big.cloudupload()


                ### KEY FUNCTIONS ###
                elif events == "copy_key":
                    clipboard(Big.key.decode("utf-8"))
                elif events == "save_key": # SAVE KEY
                        name = Big.savekey()
                        sg.Popup("Saved To:\n key_" + name , auto_close=True, auto_close_duration=5)
                elif events == "change_key":
                    Big.new_key(Fernet.generate_key())
                    Big.encrypt()
                    if fast_load:
                        preferences(save=True)
                    root["showkey"].update(toshow(Big.key.decode("utf-8"), 5))


                ### DICTIONARY FUNCTIONS ###
                elif events == "save_dict":
                    name = "EncryptDict_" + Big.name.strip(".aesdb") + ".dict"
                    file = open(path_dicts + name, "w")
                    file.write(str(Big.dictionary))
                    file.close()
                elif events == "gui_dicts":
                    wind_dicts(Big)
                elif events == "import_dict":
                    window_import = sg.Window("Import Dictionary",layout=[[sg.In(), sg.FileBrowse(initial_folder=path_dicts,file_types=("Dict Files", "*.dict")),sg.Button("Ok",key="ok")]])
                    events, values = window_import.read()
                    if events == sg.WIN_CLOSED:
                        pass
                    elif events == "ok":
                        if values[0]:
                            imp = eval(open(values[0], "r").read())
                            Big.Migration(imp)
                            sleep(0.2)
                            root["showdict"].update(toshow(Big.dictionary["A"],5))
                            sg.Popup("Success",text_color="green",background_color="black",
                                     font=font25,auto_close_duration=1,auto_close=True)
                        window_import.close()
                elif events=="new_dict":
                    if values["custom"]:
                        wind_custom_dictionary(Big)
                        root["showdict"].update(toshow(Big.dictionary["A"], 5))
                    elif not values["custom"]:
                        new = new_dictionary(default=True)
                        ch = wind_get_choice("Swap dictionary?", "Yes", "No")
                        if ch:
                            Big.Migration(new)
                            sg.Popup("Success", text_color="green", background_color="black", font=font25,
                                     auto_close_duration=4, auto_close=True)
                            root["showdict"].update(toshow(Big.dictionary["A"], 5))
                        elif not ch:
                            name = wind_get_input("Name: Leave blank for a gen name",canbeblank=True)
                            if not name:
                                name = "FirstLevel" + ora
                            file = open(path_dicts + name + ".dict", "w")
                            file.write(str(new))
                            file.close()

                ### FIRSTLEVEL FUNCTIONS ###
                elif events == "fromfirstlevel":
                    first = wind_get_input("Firstlevel hash")
                    if not first:
                        pass
                    else:
                        one_shot_copy(Big.fromfirstlevel(first), "Decripted Firstlevel Hash: ")
                elif events == "tofirstlevel":
                    first = wind_get_input("To Firstlevel: ")
                    if not first:
                        pass
                    else:
                        one_shot_copy(Big.tofirstlevel(first), "Encrypted Firstlevel Hash: ")

                ### PASSWORDS FUNCTIONS ###
                elif events == "PWDS_":
                        wind_pwds(Big)
                elif events == "newpwd":
                        wind_new_pwd(Big)
                elif events == "securepass":
                        one_shot_copy(secure_pass(randint(10, 14)), "Brand New Password")

                ### NOTES FUNCTIONS ###

                elif events == "newnote":
                    wind_new_note(Big)

                elif events == "notes":
                    wind_notes(Big)
                
                ### PREFERENCES ###
                try:
                    if values["gui"]:
                        if gui:
                            pass
                        else:
                            gui = True
                            preferences(save=True)
                    if values["fast_load"]:
                        if fast_load:
                            pass
                        else:
                            fast_load = True
                            preferences(save=True)
                    if not values["gui"]:
                        gui = False
                        preferences(save=True)
                        root.Close()
                        break
                    if not values["fast_load"]:
                        fast_load = False
                        preferences(save=True)
                except KeyError:
                    pass
        ### CLI ###
        try:
            print(langs("p", 5) + fg.red + Big.name + fg.norm)
            print(langs("p",48))
            comando = getinputnoerrors(f"{fg.red}{Big.name}: {fg.norm}")
            if comando == "add":
                print(langs("p", 6))
                print(langs("p",21))
                user = getinputnoerrors(": ")
                if user == "gen" or user == "":
                    user = secure_pass(randint(9, 12))
                site = getinputnoerrors("URL: ")
                username = getinputnoerrors("Username: ")
                Big.add_password(user,site,username)
            elif comando == "exit":
                Big.encrypt(True)
                quit(0)
            elif comando == "dicts":
                __dicts__()
            elif comando == "keys":
                __keys__()
            elif comando.__contains__("printall"):
                Big.printall(comando)
            elif comando == "__clean_db__":
                Big.__clean_db__()
            elif comando.__contains__("print"):
                key = comando.strip().split(" ")[1]
                for item in Big.search(key):
                    Big.printpwd(Big.passwords[item])
                    print("\n")
            elif comando == "help":
                for command in langs("c_prompt", 0):
                    print(fg.blue + command[0] + fg.red + " : " + fg.green + command[1] + fg.norm)
            elif comando == "prefs":
                preferences(mode="man")
            elif comando == "upload":
                Big.cloudupload()
            elif comando.__contains__("del"):
                key = comando.split()[1]
                Big.delete(key = key)
            elif comando.__contains__("mod"):
                key = comando.split()[1]
                res = Big.search(key)
                new_entry,ind = modpwd_cli(res)
                Big.modpwd(new_entry,ind)
            elif comando.__contains__("note"):
                notes_cli(comando)
        except ValueError:
            continue


def preferences(*args,mode = "auto",default=False,save=False):
    # ("argument",value) arguments = "f" or "g" or "l"
    global lang, gui, fast_load
    fast_load_key = ""

    def saveprefs(prefs):
        if fast_load:
            prefs["key"] = Big.key.decode("utf-8")
            Big.renamedb("fastload.aesdb")
        else:
            prefs["key"] = ""
        file = open(path + "preferences.json", "w")
        file.write(json.dumps(prefs))
        print(fg.green + "saved..." + fg.norm)
    if default:
        lang = 'en'
        gui = False
        fast_load = True
        fast_load_key = Big.key.decode("utf-8")
        save = True
    if save:
        prefs = {"lang": lang, "gui": gui, "fast_load": fast_load, "key": fast_load_key}
        return saveprefs(prefs)
    if mode == "auto":
        for arg in args:
            if arg[0] == "l":
                lang = arg[1]
            elif arg[0] == "f":
                if arg[1]:
                    fast_load = arg[1]
                else:
                    fast_load = arg[1]
            elif arg[0] == "g":
                gui = arg[1]


    elif mode == "man":
        prefs = {"lang": lang, "gui": gui, "fast_load": fast_load, "key": fast_load_key}
        for item,value in prefs.items():
            if item == "key":
                continue
            print(f'{item} : {value}')

            if item == "lang":
                print(langs("p",15))
                if getinputnoerrors(": ") == "y":
                    if lang == "it":
                        lang = "en"
                    else:
                        lang = "it"
                else:
                    pass
            elif item == "gui":
                if gui:
                    print(langs("p",17))
                    if getinputnoerrors(": ") == "n":
                        gui = False
                else:
                    print(langs("p",16))
                    if getinputnoerrors(": ") == "y":
                        gui = True
            elif item == "fast_load":
                if fast_load:
                    print(langs("p",25))
                    if getinputnoerrors(": ") == "n":
                        fast_load = False
                        fast_load_key = ""
                else:
                    print(langs("p",24))
                    if getinputnoerrors(": ") == "y":
                        fast_load = True
                        fast_load_key = Big.key.decode("utf-8")

    return saveprefs(prefs = {"lang": lang, "gui": gui, "fast_load": fast_load, "key": fast_load_key})


def closedetect():
    Big.encrypt()
    print(fg.red + "FORCE SAVING DUE TO FORCE CLOSE...")
    sleep(2)


def load():
    global lang, gui, fast_load,fast_load_key
    prefs = open(path + "preferences.json", "r").read()
    try:
        prefs = json.loads(prefs)
    except:
         return preferences(default=True)
    lang = prefs["lang"]
    gui = prefs["gui"]
    fast_load = prefs["fast_load"]
    fast_load_key = prefs["key"].encode("utf-8")


if __name__ == "__main__":
    load()
    main()
