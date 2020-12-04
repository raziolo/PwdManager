import os, string
from random import choice, randint, shuffle
from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidKey
from datetime import datetime
#from pydrive.drive import GoogleDrive
#from pydrive.settings import InvalidConfigError
#from pydrive.auth import GoogleAuth
from difflib import SequenceMatcher
import webbrowser
os.system("color")

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

path = os.getcwd() + "\\"
path_big_files = path + "bigfiles/"
# chars = shuffle(chars)
chars_up = list(string.ascii_uppercase)
chars_down = list(string.ascii_lowercase) + list("àèìòù")
digits = list(string.digits)
simbols = list(string.punctuation)
chars = chars_up + chars_down + digits + simbols
oggi = datetime.today().strftime("%m%d%Y")
lang = "it"
gui = 0
fast_load = 0


def langs(category, code):
    ERRORS = {
        1: ["La key inserita non è del formato corretto.", "The key isn't of the proper format."],
        2: ["Questa key non è valida per questo BigFile", "This key is invalid for this BigFile"],
        3: ["Il valore inserito non è corretto", "The submitted value is incorrect"],
        4: ["Comando errato! help per una lista comandi", "Wrong command! Help for a commands list"],
        5: ["Nessuna password nel database " + Big.name, "There's no passwords in " + Big.name],
        6: ["Hash incompatibili: Lunghezze diverse.", "Incompatible hashes, different lenghts"],
        7: ["File key.key non trovato. Caricamento veloce disabilitato.", "key.key file not found. Fast-load disabled."],
        8: ["File \"client_secrets.json\" non trovato. \"console\" per essere reindirizzato alla Dev Console di GDrive.\n\"readme\" per essere reindirizzato al readme.md su GitHub","File \"client_secrets.json\" not found.\n\"console\" to be redirected to the GDrive's Dev Console. \"readme\" to be redirected to the GitHub readme.md"],
        9: ["File cloud.txt non trovato", "Can't find the cloud.txt file"]
    }
    PHRASES = {
        1: ["Se selezioni \"s\" il dizionario verrà salvato in: ",
            "If you select \"s\" the dictionary will be saved in "],
        2: [
            "Vuoi sostituire l'attuale dizionario con questo?\n N.B. \"y\" per migrare le password y/n",
            "Would you like to substitute the actual dictionary with this? \"y\" to migrate the passwords y/n"],
        3: ["new per creare un nuovo dizionario, mod per modificare il dizionario corrente",
            "new to create a new dictionary, mod to modify the current dictionary"],
        4: ["Comando: help per una lista comandi", "Command: help for a commands list"],
        5: ["Database e Dizionario attualmente in uso: ", "Current Dictionary and Database: "],
        6: ["Password: gen per generare una nuova password sicura",
            "Password: use gen to generate a new secure password"],
        7: ["Correttamente criptato in AES e salvato in: ", "Succesfully encrypted in AES and saved with key: "],
        8: ["Questa è la tua nuova key: ", "This is your new key: "],
        9: [fg.red + "\nALERT!!ALERT!!ALERT!!\nCONSERVALA CON ESTREMA ATTENZIONE\nLA KEY È STRETTAMENTE LEGATA ALLE PASSWORD\nSE PERDI LA KEY PERDI ANCHE LE PASSWORD\n" + fg.norm,
            fg.red + "\nALERT!!ALERT!!ALERT!!\nCAREFULLY STORE THE KEY\nTHE KEY IS STRICTLY LINKED TO THE DATABASE\nIF YOU LOSE THE KEY YOU'LL LOSE ALL THEDATA.\n" + fg.norm],
        10: ["Creazione nuovo dizionario...", "Creating a new dictionary..."],
        11: ["A quanto pare il database non contiene nulla...",
             "It seems like the database doesn't contains nothing..."],
        12: ["Creazione automatica nuovo DB...", "Auto-create a new DB..."],
        13: ["ERRORE: Nessun database trovato!", "ERROR: No database found"],
        14: ["Lingua corrente:", "Current language: "],
        15: ["y: passa a inglese", "y: switch to italian"],
        16: ["stato GUI: disattivata. \"y\" per attivare", "GUI status: disabled. \"y\" to enable"],
        17: ["stato GUI: attivata. \"n\" per disattivare", "GUI status: enabled. \"n\" to disable."],
        18: [fg.red + "Key attuale: " + fg.yellow + toshow(Big.key.decode("utf-8")) + fg.norm,
             fg.red + "Actual key: " + fg.yellow + toshow(Big.key.decode("utf-8")) + fg.norm],
        19: ["\"new\" per generare una nuova chiave", "\"new\" to generate a new key"],
        20: [
            "Vuoi sostituire questa key alla key attuale? N.B. Tutti i dati verranno migrate ma è consigliabile fare un backup del file \".aesdb\" : " + Big.name,
            "Would you like to swap the actual key? N.B. All the data will be migrated but it's higly reccomended to backup the \".aesdb\" file: " + Big.name],
        21: ["Tutti i caratteri sono supportati.",
             "All the characters are supported"],
        22: [fg.red + "La chiave generata è: " + fg.norm, fg.red + "The brand-new key is: " + fg.norm],
        23:["Quale carattere vuoi modificare?", "What character would you like to modify?"],
        24:["Caricamento veloce disabilitato \"y\" per abilitare", "Fast Load disabled \"y\" to enable"],
        25:["Caricamento veloce abilitato \"n\" per disattivare","Fast Load enabled \"n\" to disable"],
        26:["Database scelto: ", "Fast-charged database: "],
        27:[["del -key key ","elimina una Password con key corrispondente. Previo check dell'utente. Se non vuoi controllare allora inserisci --auto nella query"],
            ["del -key key","deletes a Password with matching key. With user permisson before. If u want to skip the permissons asking add --auto to the query"]],
        28:["Sei sicuro? y/n ","Are you sure? y/n "],
        29:["Inserisci il valore di una key identificativa: ", "Insert a key value: "],
        30:["Tutti gli elementi sono stati eliminati con successo.", "All the elements have been deleted succesfully."],
        31:[fg.red + "Ci sono dei problemi con il dizionario.\n creo un nuovo dizionario e provo a ripristinare e migrare le vecchie password\n" + fg.norm, "The dictionary is corrupted. Creating a new dictionary and trying to restore passwords."],
        32:["Nuovo dizionario creato tuttavia non è stato possibile migrare le password.", "Succesfully created a new dictionary but it was impossible to restore the Passwords"],
        33:["Nessun risultato.", "No match."],
        34:["Ho trovato dei risultati simili", "I've found similar results "],
        35:["Successo.","Success"],
        36:["Key salvata con successo", "Succesfully saved the key."],
        37:[fg.red + "La key attualmente in uso è: " + fg.yellow + toshow(Big.key.decode("utf-8"), showing=len(Big.key)) + fg.norm,fg.red + "Key in use: " + fg.yellow + toshow(Big.key.decode("utf-8"), showing=len(Big.key)) + fg.norm],
        38:[fg.green+ "Database correttamente caricato su GDrive."+fg.norm, fg.green +"Succesfully uploaded the database on Gdrive"+ fg.norm],
        39:[fg.red + "Password multiple trovate, vuoi eliminarle tutte? y/n" + fg.norm, "Multiple passwords found, do you want to delete them all? y/n" + fg.norm],
        40:["printall -p ? y/n",'printall -p ? y/n'],
        41:["Salvare le credenziali in cloud.txt per l'accesso veloce?", "Do you want to save the credentials into a cloud.txt file for future fast access?"],
        42:["Se hai bisogno di aiuto per la creazione del file \"client_secrets.json\" visualizza il readme.md su GitHub.", "If you need help creating your own \"client_secrets.json\" see the readme.md on GitHub"],
        43:["Vecchio carattere: ", "Old char: "],
        44:["Nuovo hash: ", "New hash: "]
    }
    COMMANDS = {
        1: [["add", "Aggiungi password"], ["dicts", "Crea/Modifica Dizionario"], ["keys", "Crea/Modifica Keys"],
            ["printall " + fg.purple + "-p : passwords, -d : dicts" + fg.norm,
             "Stampa IN CHIARO in base agli argomenti dichiarati.\n\t\t\t\t\t\t\t\t\t  per nascondere le password in chiaro aggiungi \"-h\"" + fg.norm],
            ["help", "Visualizza questo prompt"], ["prefs", "Visualizza e modifica le preferenze correnti"],["mod \"key_identificativa\"","Modifica una password"],["del \"key_identificativa\"","Elimina una password"],["__clean_db__", "Elimina tutte le Password dal Database. Nota bene: potrebbe essere necessario eseguire il comando più di una volta."],
            ["upload","Carica il file .aesdb sul Cloud. Solo Google Drive è supportato al momento."],["exit", "Cripta il database e chiudi il programma"]],
        2: [["add", "Add a new password"], ["dicts", "Create/Modify Dictionaries"], ["keys", "Create/Modify Keys"],
            ["printall" + fg.purple + " -p : passwords, -d : dicts" + fg.norm,
             "Prints IN CLEAR the declared arguments\n\t\t\t\t\t\t\t\t\t  to hide the passwords use: \"-h\"" + fg.norm],
            ["help", "Shows this prompt"], ["prefs", "Visualize and modify current preferences"],["mod \"key\"","Modify a password"],["del \"key\"","Delete a password"],["__clean_db__", "Deletes all the passwords in the Database. Note: It may be necessary to execute the command a couple times."],
            ["upload","Upload the .aesdb file to the Cloud. Only GDrive is supported for now."],["exit", "Encrypts the database and closes the program"]],
        3:  [["mod", "Modifica una Password, digita mod help per una spiegazione dettagliata."],["del","ELimina una Password, del help per istruzioni dettagliate. "],["__clean_db__", "Elimina tutte le Password dal Database. Nota bene: potrebbe essere necessario eseguire il comando più di una volta."],["exit", "Ritorna al menù principale"]],
        4:  [["mod", "Change a Password, type mod help for detailed instructions"],["del", "Delete a password, del help for detailed instructions. "],["__clean_db__", "Deletes all the passwords in the Database. Note: It may be necessary to execute the command a couple times."], ["exit", "Go back to the menù."]],
        5: [["new", "Genera una nuova key sicura"],["show", "Mostra la key collegata al db in uso"], ["save","Salva la key in un file key.key"]],
        6: [["new", "Create a new key"],["show", "Shows the currently db-linked key"], ["save","Saves the key in a key.key file"]]

    }
    if lang == "it":
        if category == "err":
            if code:
                return ERRORS[code][0]
        elif category == "p":
            if code:
                return PHRASES[code][0]
        elif category == "c_prompt":
            return COMMANDS[1]
        elif category == "vault_help":
            return COMMANDS[3]
        elif category == "keys_help":
            return COMMANDS[5]

    elif lang == "en":
        if category == "err":
            if code:
                return ERRORS[code][1]
        elif category == "p":
            if code:
                return PHRASES[code][1]
        elif category == "c_prompt":
            return COMMANDS[2]
        elif category == "vault_help":
            return COMMANDS[4]
        elif category == "keys_help":
            return COMMANDS[6]

def toshow(nottoshow, showing = 7):
        lenght = len(str(nottoshow)) - showing
        chiperkey = nottoshow[:showing-1]
        for i in range(lenght - randint(8,18)):
            chiperkey += "#"
        return chiperkey

class BigFile:
    def __init__(self, name, key, dictionary, passwords, encrypted):
        self.name = name
        self.key = key
        self.dictionary = dictionary
        self.passwords = passwords
        self.encrypted = encrypted

    def charge(self):
        global fast_load
        big_file_read = b''
        files = os.listdir(path_big_files)
        if not files:
            self.new_db()
            main()
        if fast_load == 1:
            try:
                self.key = open(path + "key.key", "rb").read()
                self.name = files[0]
                self.passwords, self.dictionary = Big.Deconstruction(
                    (Big.decrypt(open(path_big_files + self.name, "r").read().encode("utf-8"))))
                self.encrypted = False
                print(fg.red + "FASTLOADFASTLOADFASTLOAD" + fg.norm)
            except FileNotFoundError:
                print(langs("err", 7))
                preferences("auto", f=0)
                self.charge()
            except InvalidKey:
                print(langs("err", 1))
                preferences("auto", f=0)
                self.charge()
            except InvalidToken:
                print(langs("err", 2))
                preferences("auto", f=0)
                self.charge()
        if fast_load == 0:
            cont = 1
            databases = []
            for file in files:
                file = [file, cont]
                databases.append(file)
                print(file[0],file[1])
            user = int(getinputnoerrors("Database (1-n|0=new db) : "))
            if user == 0:
                self.new_db()
            else:
                for file in databases:
                    if user == file[1]:
                        self.name = file[0]
                    else:
                        print(langs("err", 3))
                        main()
                    self.key = getinputnoerrors("Key: ").encode("utf-8")
                    self.passwords, self.dictionary = Big.Deconstruction(
                        (Big.decrypt(open(path_big_files + self.name, "r").read().encode("utf-8"))))
                    self.encrypted = False
                    print(langs("p", 35))


    def new_db(self):
        print(langs("p",12))
        self.name = "DB_" + secure_hash(3) + "_" + oggi + ".aesdb"
        self.key = Fernet.generate_key()
        self.dictionary = new_dictionary()
        self.passwords = []
        self.encrypted = False
        new = open(path_big_files + self.name, "w")
        new.write("")
        new.close()
        print(langs("p", 9))
        print(fg.red + langs("p",8) + fg.yellow + str(self.key.decode("utf-8")+  fg.norm))
        Big.encrypt()
        print(langs("p",35))

    ### THIS FUNCTION IS CURRENTLY UNDER DEVELOPMENT ###
    def cloudupload(self):
        print("WIP - Coming soon")
        return
        gauth = GoogleAuth()
        def getauth():
            gauth.LocalWebserverAuth()
            return gauth
        try:
            gauth.LoadCredentialsFile("cloud.txt")
        except:
            print(langs("err",9))
        if gauth.credentials is None:
            gauth = getauth()
            print(langs("p",41))
            if getinputnoerrors("y/n : ") == "y":
                gauth.SaveCredentials("cloud.txt")
        drive = GoogleDrive(gauth)
        file1 = drive.CreateFile({'title': self.name})
        file1.SetContentString(str(open(path_big_files + self.name, 'r').read()))
        try:
            file1.Upload()
            print(langs("p",38))
        except InvalidConfigError:
            print(langs("err",8))
            print(langs("p",42))
            comando = getinputnoerrors(": ")
            if comando== "console":
                webbrowser.open('https://console.developers.google.com/apis/api/drive/overview')
            elif comando == "readme":
                webbrowser.open("GITHUB")
    ### END OF WIP FUNCTION ###

    def Construction(self):
        Constructed = []
        for item in self.passwords:
            Constructed.append(item)
        Constructed.append("################")
        Constructed.append(str(self.dictionary))
        return Constructed

    @staticmethod
    def Deconstruction(big_file):  # static method here for grouping purposes
        import ast
        out = ast.literal_eval(big_file)
        a = out.index("################")
        passwords = out[:a]
        dictionary = eval(str(out[a + 1:][0]))
        return passwords, dictionary

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

    def fromfirstlevel(self, single):
        result = ""
        lungh_pezzo = len(self.dictionary["A"])
        hashed = [single[i:i + lungh_pezzo] for i in range(0, len(single), lungh_pezzo)]
        for pezzo in hashed:
            pezzo = pezzo.rstrip()
            result += self.fromvalues(pezzo)
        return result

    def encrypt(self):
        f = Fernet(self.key)
        encrypted_big_file = f.encrypt(str(self.Construction()).encode("utf-8"))
        file = open(path_big_files + self.name, "wb")
        file.write(encrypted_big_file)
        self.encrypted = True
        mess = langs("p", 7)
        return mess + toshow(self.key.decode("utf-8")) + "\nsaved in " + path_big_files + self.name

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
            print(langs("err", 2))
            self.encrypted = True

    def delete(self,key):
        last = ""
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

    def parser_printall(self, comando):
        print_args = ["-p", "-d", "-h"]
        toprint = ""
        parser = comando.split(" ")
        for arg in print_args:
            for i in parser:
                if i.__contains__(arg):
                    toprint += arg
        p, d, h = 0, 0, 0
        if toprint.__contains__("-p"):
            p = 1
        if toprint.__contains__("-d"):
            d = 1
        if toprint.__contains__("-h"):
            h = 1
        self.printall(p, d, h)


    def modpwd(self,key):
        if key.__contains__("printall"):
            self.parser_printall(comando)
        else:
            results = []
            for pwd in self.passwords:
                for item, value in pwd.items():
                    if SequenceMatcher(a=key, b=value).ratio() >= 0.66:
                        results.append(pwd)
            new_entry = {}
            if len(results) == 1:
                for ident, value in results[0].items():
                    if ident == "firstlevel":
                        new_entry[ident] = self.tofirstlevel(new_entry["plain_pass"])
                        break
                    new = getinputnoerrors("New \"" + ident + "\": ").strip()
                    if new == "" or new == value:
                        new_entry[ident] = value
                    else:
                        new_entry[ident] = new
                self.passwords.remove(results[0])
                self.passwords.append(new_entry)
            elif len(results) > 1:
                print(langs("p", 34))
                new_results = []
                for item in results:
                    new = (item, results.index(item) + 1)
                    print(fg.red + "Risultato " + fg.norm + str(new[1]))
                    for i, v in new[0].items():
                        if i == "plain_pass":
                            pass
                        else:
                            print(fg.yellow + i + fg.blue + " : " + fg.red + v + fg.norm)
                    new_results.append(new)
                    print("\n")
                u = int(getinputnoerrors("(1-n): "))
                ch = None
                for item in new_results:
                    if u == item[1]:
                        ch = item[0]
                        break
                old = ch
                for ident, value in ch.items():
                    if ident == "firstlevel":
                        ch[ident] = self.tofirstlevel(ch["plain_pass"])
                        break
                    new = getinputnoerrors("New \"" + ident + "\": ").strip()
                    if new == "" or new == value:
                        ch[ident] = value
                    else:
                        ch[ident] = new
                self.passwords.remove(old)
                self.passwords.append(ch)
            elif not results:
                print(langs("p", 33))
            self.encrypt()


    def printall(self, p=0, d=0, h=0):
        if p != 0:
            # print all passwords
            print(fg.green + 'PWDS' + fg.norm)

            for password in self.passwords:
                if password:
                    password["plain_pass"] = self.fromfirstlevel(password["firstlevel"])
                    for item, value in password.items():
                        row = fg.yellow + item + fg.norm + " : " + fg.red + value + fg.norm
                        if h != 0:
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
                    print(langs("err", 5))
        if d != 0:
            try:
                # print all dictionary chars and hashes, separated in groups
                print(fg.green + 'DICTS' + fg.norm)
                row_ups, row_lows, row_digits, row_simbols = "", "", "", ""
                uppercases, lowercases, digits_res, simbols_res = [], [], [], []
                for char, value in self.dictionary.items():
                    if char in chars_up:
                        uppercases.append([char, value])
                    elif char in chars_down:
                        lowercases.append([char, value])
                    elif char in digits:
                        digits_res.append([char, value])
                    elif char in simbols:
                        simbols_res.append([char, value])
                # Crea liste di tuple di caratteri e hash
                for doggo in uppercases:
                    row_ups += fg.red + doggo[0] + fg.norm + " : " + fg.blue + doggo[1] + ", "
                for doggo in lowercases:
                    row_lows += fg.red + doggo[0] + fg.norm + " : " + fg.blue + doggo[1] + ", "
                for doggo in digits_res:
                    row_digits += fg.red + doggo[0] + fg.norm + " : " + fg.blue + doggo[1] + ", "
                for doggo in simbols_res:
                    row_simbols += fg.red + doggo[0] + fg.norm + " : " + fg.blue + doggo[1] + ", "
                print(fg.yellow + "UPPERCASES: " + row_ups + "\n" + fg.yellow + "LOWERCASES: " + row_lows + "\n" + fg.yellow + "DIGITS: " + fg.yellow + row_digits + "\n" + fg.yellow + "SIMBOLS: " + row_simbols + fg.norm)
            except AttributeError:
                print(langs("p",31))
                try:
                    new = new_dictionary()
                    self.Migration(new)
                except AttributeError:
                    self.dictionary = new_dictionary()
                    print(langs("p",32))

    def __clean_db__(self):
        self.passwords = []
        print(langs("p",30))
        print(Big.encrypt())

    def __keys__(self):
        print(langs("p", 18))
        print(langs("p", 19))
        while True:
            user = getinputnoerrors("comando: ")
            if user == "new":
                new_key = Fernet.generate_key()
                print(langs("p", 22) + fg.yellow + str(new_key.decode("utf-8")) + fg.norm)
                print(langs("p", 20))
                user = getinputnoerrors(": ")
                if user == "y":
                    self.key = new_key
                    self.encrypt()
                    break
            elif user == "show":
                print(langs("p",37))
            elif user == "save":
                print(Big.savekey())
            elif user == "help":
                m = langs("keys_help",0)
                for command in m:
                    print(fg.red + str(command[0]) + fg.norm + " : " + fg.yellow + str(command[1]) + fg.norm)
            else:
                break

    def __dicts__(self):
        print(langs("p", 3))
        user = getinputnoerrors(": ")
        if user == "new":
            new = new_dictionary()
            print(langs("p", 2))
            name = "EncryptDict" + str(oggi) + ".dict"
            print(langs("p", 1) + name)
            user = getinputnoerrors("y/n: ")
            if user == "y":
                self.Migration(new)
            elif user == "n":
                self.passwords = []
                self.dictionary = new
                self.encrypt()
            elif user == "s":
                file = open(path + name, "w")
                file.write(str(new))
                file.close()
    def printpwd(self,key, h = 0):
        for password in Big.passwords:
            for item,value in password.items():
                if value == key:
                    for item,value in password.items():
                        if item == "plain_pass":
                            if h == 0:
                                print(fg.red + str(item) + fg.blue + " : " + fg.yellow + str(Big.fromfirstlevel(password["firstlevel"])) + fg.norm)
                            elif h == 1:
                                pass
                        else:
                            print(fg.red + str(item) + fg.blue + " : " + fg.yellow + str(value) + fg.norm)


    def savekey(self):
        file = open(path + "key.key", "w")
        file.write(str(self.key.decode("utf-8")))
        file.close()
        return langs("p",36)

    def add_password(self):
        print(langs("p", 6))
        print(langs("p", 21))
        user = getinputnoerrors(": ")
        if user == "gen":
            user = secure_pass(randint(9, 12))
            firstlevel = self.tofirstlevel(user)
        else:
            firstlevel = self.tofirstlevel(user)
        site = getinputnoerrors("URL: ")
        username = getinputnoerrors("Username: ")
        password_id = {
            "plain_pass": "",
            "username": username,
            "site": site,
            "firstlevel": firstlevel,
        }

        self.passwords.append(password_id)
        print(fg.green + "Ok" + fg.norm)
        self.encrypt()

Big = BigFile("", b'', 0, [], True)


def getinputnoerrors(prompt):
    try:
        user = input(prompt)
        return user
    except ValueError:
        print(langs("err", 3))


def password_base(lenght):
    types = ["a", "A", "N", "S"]
    last = ""
    base = ""

    def subst(word, old_index, char):
        word = word[:old_index] + char + word[old_index + 1:]
        return word

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



def CRC__(base):
    crc = ""
    for char in base:
        if char == "a":
            crc += choice(chars_down)
        elif char == "A":
            crc += choice(chars_up)
        elif char == "N":
            crc += choice(digits)
        elif char == "S":
            crc += choice(simbols)
    return crc


def secure_pass(lenght):
    spass = CRC__(password_base(lenght))
    return spass


def secure_hash(lenght):
    rstring = ""
    for i in range(0, lenght):
        rstring += choice(chars)
    return rstring


def new_dictionary():
    len_hashed = randint(5, 7) # Parte variabile / Variable Part
    complexity_crc = 4 # Parte Costante / Constant Part
    # Generazione CRC 1.0
    CRC = CRC__(password_base(complexity_crc))
    # Generaxione AlphaBeta 1.0
    alphaBeta = {}
    for i in range(0, len(chars)):
        alphaBeta[chars[i]] = CRC + secure_hash(len_hashed)
    return alphaBeta

def main():
    while True:
        if Big.dictionary == 0:
            try:
                Big.charge()
            except:
                quit(0)
        else:
            break

    while True:
        try:
            print(langs("p", 5) + fg.red + Big.name + fg.norm)
            comando = getinputnoerrors(fg.red + Big.name + ": " + fg.norm)
            if comando == "add":
                Big.add_password()
            elif comando == "exit":
                print(Big.encrypt())
                quit(0)
            elif comando == "dicts":
                Big.__dicts__()
            elif comando == "keys":
                Big.__keys__()
            elif comando.__contains__("printall"):
                Big.parser_printall(comando)
            elif comando == "__clean_db__":
                Big.__clean_db__()
            elif comando.__contains__("print"):
                key = comando.strip().split(" ")[1]
                Big.printpwd(key)
            elif comando == "help":
                for command in langs("c_prompt", 0):
                    print(fg.blue + command[0] + fg.red + " : " + fg.green + command[1] + fg.norm)
            elif comando == "prefs":
                preferences("manual")
            elif comando == "upload":
                Big.cloudupload()
            elif comando.__contains__("del"):
                key = comando.split()[1]
                print(key)
                Big.delete(key = key)
            elif comando.__contains__("mod"):
                key = comando.split()[1]
                Big.modpwd(key = key)


        except ValueError:
            continue


def preferences(mode,l="",g=0,f=0):
    global lang, gui, fast_load
    prefs = {
        "lang": lang,
        "gui": gui,
        "fast_load" : fast_load
    }
    languages = ["it", "en"]
    if mode == "manual":
        print(langs("p", 14) + lang)
        print(langs("p", 15))
        if getinputnoerrors(": ") == "y":
            if lang == languages[0]:
                lang = languages[1]
                prefs["lang"] = lang
            else:
                lang = languages[0]
                prefs["lang"] = lang
        if gui == 0:
            print(langs("p", 16))
            if getinputnoerrors(": ") == "y":
                gui = 1
                prefs["gui"] = gui
        else:
            print(langs("p", 17))
            if getinputnoerrors(": ") == "n":
                gui = 0
                prefs["gui"] = gui
        if fast_load == 0:
            print(langs("p",24))
            user = getinputnoerrors(": ")
            if user == "y":
                fast_load = 1
                prefs["fast_load"] = fast_load
        else:
            print(langs("p",25))
            user = getinputnoerrors(": ")
            if user == "n":
                fast_load = 0
                prefs["fast_load"] = fast_load
    elif mode == "auto":
        if l == "en":
            lang = "en"
            prefs["lang"] = "en"
        elif l == "it":
            lang = 'it'
            prefs["lang"] = "it"
        if g == 1:
            gui = 1
            prefs["gui"] = 1
        elif g == 0:
            gui = 0
            prefs["gui"] = 0
        if f == 1:
            fast_load = 1
            prefs["fast_load"] = 1
            Big.savekey()
        elif f == 0:
            fast_load = 0
            prefs["fast_load"] = 0

    towrite = ""
    for pref, value in prefs.items():
        towrite += pref + " = " + str(value) + "\n"
    file = open(path + "preferences.txt", "w")
    file.write(towrite)
    file.close()


def closedetect():
    import time
    Big.encrypt()
    print(fg.red + "FORCE SAVING DUE TO FORCE CLOSE...")
    time.sleep(2)


def load():
    global lang, gui, fast_load
    pref = open(path + "preferences.txt", "r").readlines()
    pref = [item.strip().split(" = ") for item in pref]
    lang = pref[0][1]
    gui = int(pref[1][1])
    fast_load = int(pref[2][1])


if __name__ == "__main__":
    load()
    main()
