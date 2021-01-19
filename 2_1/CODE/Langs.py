


def langs(category, code,name="",key=b""):
    from CODE.Utils import toshow, fg

    def getlang():
        import json
        return json.loads(open("preferences.json","r").read())["lang"]

    lang = getlang()
    ERRORS = {
        1: ["La key inserita non è del formato corretto.", "The key isn't of the proper format."],
        2: ["Questa key non è valida per questo BigFile", "This key is invalid for this BigFile"],
        3: ["Il valore inserito non è corretto", "The submitted value is incorrect"],
        4: ["Comando errato! help per una lista comandi", "Wrong command! Help for a commands list"],
        5: ["Nessuna password nel database " + name, "There's no passwords in " + name],
        6: ["Hash incompatibili: Lunghezze diverse.", "Incompatible hashes, different lenghts"],
        7: ["Key non trovata. Fast-Load disattivato.", "Key not found. Fast-Load disabled."],
        8: ["File \"client_secrets.json\" non trovato. \"console\" per essere reindirizzato alla Dev Console di GDrive.\n\"readme\" per essere reindirizzato al readme.md su GitHub\n\"guide\" per aprire la guida","File \"client_secrets.json\" not found.\n\"console\" to be redirected to the GDrive's Dev Console.\n\"readme\" to be redirected to the GitHub readme.md\n\"guide\" to open the guide"],
        9: ["File cloud.txt non trovato", "Can't find the cloud.txt file"],
        10: ["Per creare un file \"client_secrets.json\" e far funzionare l'upload fai riferimento al primo paragrafo di questa guida:\n\
            https://medium.com/@annissouames99/how-to-upload-files-automatically-to-drive-with-python-ee19bb13dda" +"\n"
            "successivamente inserisci il file nella stessa directory di \"passwords.py\"",
             "\"client_secrets.json\" file is missing, to create on refer to the first paraghraph of this guide:\n\
            https://medium.com/@annissouames99/how-to-upload-files-automatically-to-drive-with-python-ee19bb13dda" +"\n"
            "then put the file in the same directory of \"passwords.py\""],
    }
    PHRASES = {
        1: ["Se selezioni \"n\" il dizionario verrà salvato in: ",
            "If you select \"n\" the dictionary will be saved in "],
        2: [
            "Vuoi sostituire l'attuale dizionario con questo? y/n",
            "Would you like to substitute the actual dictionary with this? y/n"],
        3: ["\"new\" per creare un nuovo dizionario",
            "\"new to create a new dictionary\""],
        4: ["Comando: help per una lista comandi", "Command: help for a commands list"],
        5: ["Database e Dizionario attualmente in uso: ", "Current Dictionary and Database: "],
        6: ["Password: gen per generare una nuova password sicura",
            "Password: use gen to generate a new secure password"],
        7: ["Correttamente criptato in AES e salvato in: " + name, "Succesfully encrypted in AES and saved in: " + name],
        8: ["Questa è la tua nuova key: ", "This is your new key: "],
        9: [fg.red + "\nALERT!!ALERT!!ALERT!!\nCONSERVALA CON ESTREMA ATTENZIONE\nLA KEY È STRETTAMENTE LEGATA ALLE PASSWORD\nSE PERDI LA KEY PERDI ANCHE LE PASSWORD\n" + fg.norm,
            fg.red + "\nALERT!!ALERT!!ALERT!!\nCAREFULLY STORE THE KEY\nTHE KEY IS STRICTLY LINKED TO THE DATABASE\nIF YOU LOSE THE KEY YOU'LL LOSE ALL THE DATA.\n" + fg.norm],
        10: ["Creazione nuovo dizionario...", "Creating a new dictionary..."],
        11: ["A quanto pare il database non contiene nulla...",
             "It seems like the database doesn't contains nothing..."],
        12: ["Creazione automatica nuovo DB...", "Auto-create a new DB..."],
        13: ["ERRORE: Nessun database trovato!", "ERROR: No database found"],
        14: ["Lingua corrente:", "Current language: "],
        15: ["y: passa a inglese", "y: switch to italian"],
        16: ["stato GUI: disattivata. \"y\" per attivare", "GUI status: disabled. \"y\" to enable"],
        17: ["stato GUI: attivata. \"n\" per disattivare", "GUI status: enabled. \"n\" to disable."],
        18: [fg.red + "Key attuale: " + fg.yellow + toshow(key.decode("utf-8")) + fg.norm,
             fg.red + "Actual key: " + fg.yellow + toshow(key.decode("utf-8")) + fg.norm],
        19: ["\"help\" per una lista comandi", "\"help\" for a command list"],
        20: ["Vuoi sostituire questa key alla key attuale? N.B. Tutti i dati verranno migrate ma è consigliabile fare un backup del file \".aesdb\" : " + name,
            "Would you like to swap the actual key? N.B. All the data will be migrated but it's higly reccomended to backup the \".aesdb\" file: " + name],
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
        37:[fg.red + "La key attualmente in uso è: " + fg.yellow + key.decode("utf-8") + fg.norm,fg.red + "Key in use: " + fg.yellow + key.decode("utf-8") + fg.norm],
        38:[fg.green+ "Database correttamente caricato su GDrive."+fg.norm, fg.green +"Succesfully uploaded the database on Gdrive"+ fg.norm],
        39:[fg.red + "Password multiple trovate, vuoi eliminarle tutte? y/n" + fg.norm, "Multiple passwords found, do you want to delete them all? y/n" + fg.norm],
        40:["printall -p ? y/n",'printall -p ? y/n'],
        41:["Salvare le credenziali in cloud.txt per l'accesso veloce?", "Do you want to save the credentials into a cloud.txt file for future fast access?"],
        42:["Se hai bisogno di aiuto per la creazione del file \"client_secrets.json\" visualizza la guida ", "If you need help creating your own \"client_secrets.json\" see the linked guide"],
        43:["Vecchio carattere: ", "Old char: "],
        44:["Nuovo hash: ", "New hash: "],
        45:[fg.blue + "Lunghezza CRC (parte costante)\n"+fg.yellow+"oppure"+fg.red+" inserisci una costante custom: " + fg.norm,fg.blue+ "CRC Lenght (constant part)\n"+fg.yellow+"or "+ fg.red +"insert a custom constant: "+ fg.norm],
        46:[fg.red + "Lunghezza parte " + fg.yellow + "variabile: " + fg.norm, fg.yellow + "Variable" +fg.red+ " part lenght: " + fg.norm],
        47:[f"{fg.red}Inserisci testo nota: {fg.norm}", f"{fg.red}Insert note text: {fg.norm}"],
        48:[f"{fg.yellow}help{fg.norm} : lista comandi",f"{fg.yellow}help{fg.norm} : command list"],
    }
    COMMANDS = {
        # HELP ITALIAN
        1: [["add", "Aggiungi password"], ["dicts", "Crea/Modifica Dizionario"], ["keys", "Crea/Modifica Keys"],
            ["mod (pwd/username/URL/)", "Modifica una password"],
            ["del (pwd/username/URL/)", "Elimina una password"],
            ["print (pwd/username/URL)", fg.yellow + "Stampa una password la cui key coincide con quella inserita"],
            ["__clean_db__","Elimina tutte le Password dal Database."],
            ["printall " + fg.purple + "-p : passwords, -d : dizionario Firstlevel" + fg.norm,
             "Stampa IN CHIARO in base agli argomenti dichiarati.\nper nascondere le password in chiaro aggiungi " + fg.purple + "\"-h\"" + fg.norm],
            ["note", fg.green + " Crea una nuova Nota " + fg.purple + "-v" + fg.green + " Visualizza tute le Note " + fg.purple + "-d " + fg.green + "Elimina una Nota" + fg.norm],
            ["help", "Visualizza questo prompt"], ["prefs", "Visualizza e modifica le preferenze correnti"],
            ["upload","Carica il file .aesdb sul Cloud. Solo Google Drive è supportato al momento."],["exit", "Cripta il database e chiudi il programma"]],

        # HELP ENGLISH
        2: [["add", "Add a new password"], ["dicts", "Create/Modify Dictionaries"], ["keys", "Create/Modify Keys"],
            ["printall" + fg.purple + " -p : passwords, -d : Firstlevel dictionary" + fg.norm,
             "Prints IN CLEAR the declared arguments\nto hide the passwords use: " + fg.purple + "\"-h\"" + fg.norm],
            ["mod (pwd/username/site/)", "Modify a password"],
            ["del (pwd/username/site/)", "Delete a password"],
            ["print (pwd/username/site/)", fg.green + "Prints a password that matches the key" ],
            ["note", fg.green + " Creates a New Note, " + fg.purple + "-v" + fg.green + " Visualize All The Notes, " + fg.purple + "-d " + fg.green + "Delete a Note"],
            ["help", "Shows this prompt"], ["prefs", "Visualize and modify current preferences"],
            ["__clean_db__", "Deletes all the passwords in the Database."],
            ["upload","Upload the .aesdb file to the Cloud. Only GDrive is supported for now."],["exit", "Encrypts the database and closes the program"]],

        # KEYS HELP
        5: [["new", "Genera una nuova key sicura"],["show", "Mostra la key collegata al db in uso"], ["save","Salva la key in un file nelle preferenze"]],
        6: [["new", "Create a new key"],["show", "Shows the currently db-linked key"], ["save","Saves the key in a in the preferences file"]]

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
        elif category == "keys_help":
            return COMMANDS[6]
