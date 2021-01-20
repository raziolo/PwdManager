import PySimpleGUI as sg
import os
from time import sleep
from tkinter import Tk
from random import randint
from CODE.Utils import *
path = os.getcwd() + "//"
path_dicts = path + "dicts/"
path_big_files = path + "bigfiles/"
path_keys = path + "keys/"
font10 = ("Calibri",10)
font15 = ("Calibri",20)
font20 = ("Calibri",20)
font25 = ("Calibri",25)


def clipboard(s):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(s)
    r.update()
    r.destroy()


def one_shot_copy(s, hint=""):
    out = s
    s = hint + ":" + "\n" + s
    cop = sg.Window("Success", auto_size_text=True,
                    layout=[[sg.Text(s, text_color="yellow")], [sg.Button("Copy", key="copy")]], font=font20)
    events, values = cop.read()
    if events == sg.WIN_CLOSED:
        return
    elif events == "copy":
        clipboard(out)
        cop.close()

def loading_with_gui(Big,files):
        layout = [[sg.Text("DB: ")],
                  [sg.Listbox(files, size=(30, 3))],
                  [sg.Text("Key: ")],
                  [sg.InputText(size=(50, 10)), sg.Button("Go", key="Ok")],
                  ]
        root = sg.Window("Seleziona DB", layout)
        events, values = root.read()
        while True:
            if events == sg.WIN_CLOSED:
                quit("User closed")
            elif events == "Ok":
                Big.key = bytes(values[1].encode("utf-8"))
                Big.name = values[0][0]
                Big.passwords, Big.dictionary, Big.notes = Big.Deconstruction(
                    (Big.decrypt(open(path_big_files + Big.name, "r").read().encode("utf-8"))))
                Big.encrypted = False
                root.close()
                return


def wind_get_input(hint,canbeblank=False):
    window_input = sg.Window(hint,layout=[[sg.InputText("",key="in")],[sg.Button("Ok")]],font=font20)
    events,values = window_input.read()
    if events == sg.WIN_CLOSED:
        window_input.Close()
        return
    if not canbeblank:
        if not values["in"] or checknull(values["in"]):
            window_input.Close()
            sg.Popup("Bad Input",auto_close_duration=1,auto_close=True)
            return False
    window_input.Close()
    return values["in"]

def wind_notes(Big):
    data = Big.notes
    layout = [[sg.Listbox(data, size=(30,7),key="box",enable_events=True),sg.Multiline(size=(30,7),key="mod")],
              [sg.Button("Delete"),sg.Button("Save",),sg.Button("New")]]

    window_note = sg.Window('Notes - All',layout, resizable=True, font=font20)
    while True:
        event, values = window_note.read()


        if event == sg.WIN_CLOSED:
            Big.encrypt()
            break
        if values["box"]:
            note = values["box"][0]
            note = "\n".join(note)
            window_note["mod"].update(note)
        if event == "Save":
            if not values["mod"]:
                window_note["mod"].update("Note can't be null")
                continue
            if checknull(values["mod"]):
                window_note["mod"].update("Note can't be null")
                continue
            index = Big.notes.index(values["box"][0])
            Big.notes[index] = values["mod"].split("\n")
            window_note["box"].update(values=Big.notes)
            window_note["mod"].update("Succesfully Modified")
            window_note.Refresh()
            Big.encrypt()
        try:
            if event == "Delete":
                index = Big.notes.index(values["box"][0])
                Big.notes.pop(index)
                window_note["box"].update(values=Big.notes)
                window_note["mod"].update("Succesfully Deleted")
                window_note.Refresh()
                Big.encrypt()
        except IndexError:
            window_note["mod"].update("Select a Note to delete")
        if event == "New":
            if not values["mod"]:
                window_note["mod"].update("Note can't be null")
                continue
            if checknull(values["mod"]):
                window_note["mod"].update("Note can't be null")
                continue
            note = values["mod"].split("\n")
            Big.notes.append(note)
            window_note["box"].update(values=Big.notes)
            window_note["mod"].update("Succesfully Created")
            window_note.Refresh()
            Big.encrypt()


def wind_pwds(Big):
    def getvals(p=False):
        datas = []
        for pwd in Big.passwords:
            res = []
            for item, value in pwd.items():
                if item == "plain_pass" and p:
                    value = Big.fromfirstlevel(pwd["firstlevel"])
                else:
                    pass
                res.append(value)
                sleep(0.1)
            datas.append(res)
        return datas

    data = getvals(False)

    head = ["plain_pass", "Site", "username", "firstlevel"]
    layout = [[sg.Table(values=data, headings=head,
                        background_color='black',
                        auto_size_columns=True,
                        justification='left',
                        num_rows=len(data) + 4,
                        alternating_row_color='black',
                        key='-TAB-',
                        row_height=35,
                        enable_events=True)],
              [sg.Button('Show/Hide Passwords', key="show"),
               sg.Text("error - no item selected", visible=False, text_color="red", key="error", pad=(100, 0))],
              [sg.Text("Password: "), sg.InputText(key="tbox_pwd",size=(30,1)),sg.Button("Copy",key="copy_pwd")],
              [sg.Text("Site:\t"), sg.InputText(key="tbox_url",size=(30,1)),sg.Button("Copy",key="copy_url")],
              [sg.Text("Username: "), sg.InputText(key="tbox_username",size=(30,1)),sg.Button("Copy",key="copy_username")],
              [sg.Text("Firstlevel: "), sg.InputText(key="tbox_firstlevel",size=(30,1)),sg.Button("Copy",key="copy_first")],
              [sg.Button("Update",key="upd")]]
              #[sg.Button("Copy", key="copy"), sg.Radio("Password", group_id=0), sg.Radio("URL", group_id=0),
               #sg.Radio("Username", group_id=0), sg.Radio("Firstlevel", group_id=0),
               #sg.Radio("All", group_id=0)]]'''
    window_pwd = sg.Window('Password Manager - All', layout,font=font20)

    while True:
        try:
            event, values = window_pwd.read()
        except KeyError:
            sg.Popup("No Passwords",auto_close=True,auto_close_duration=1,font=font20)
            break
        if event == sg.WIN_CLOSED:
            break

        if event == "show":
            if data[0][0]:
                data = getvals(False)
                window_pwd['-TAB-'].update(values=data)
            else:
                data = getvals(True)
                window_pwd['-TAB-'].update(values=data)
        if values["-TAB-"]:
            l = ["tbox_pwd","tbox_url","tbox_username","tbox_firstlevel"]
            ch = values["-TAB-"][0]
            for i in l:
                window_pwd[i].update(data[ch][l.index(i)])
        if event == "upd":
            try:
                old = values["-TAB-"][0]
                new = [values["tbox_pwd"], values["tbox_url"], values["tbox_username"], values["tbox_firstlevel"]]
                if not new[0]:
                    new[0] = Big.fromfirstlevel(Big.passwords["-TAB-"][0]["firstlevel"])
                temp = {
                    "plain_pass": "",
                    "username": new[1],
                    "site": new[2],
                    "firstlevel": Big.tofirstlevel(new[0])
                }
                Big.passwords.pop(old)
                Big.passwords.insert(old, temp)
                Big.encrypt()
                window_pwd['-TAB-'].update(values=getvals(False))
                window_pwd["error"].update(visible=False)
                window_pwd.refresh()
            except IndexError:
                window_pwd["error"].update(visible=True)

        elif event == "copy_pwd" or "copy_url" or "copy_username" or "copy_first":
            try:
                if event == "copy_pwd":
                    clipboard(values["tbox_pwd"])
                elif event == "copy_url":
                    clipboard(values["tbox_url"])
                elif event == "copy_username":
                    clipboard(values["tbox_username"])
                elif event == "copy_first":
                    clipboard(values["tbox_firstlevel"])
            except TypeError:
                window_pwd["error"].update(visible=True)


def wind_dicts(Big):
    def getvals():
        datas = []
        for item, value in Big.dictionary.items():
            res = [item, value]
            datas.append(res)
        return datas

    data = getvals()
    head = ["char", "hash"]
    layout = [[sg.Table(values=data, headings=head, #col_widths=[10 for i in range(len(data))],
                        background_color="black",
                        auto_size_columns=True,
                        justification='left',
                        num_rows=len(data),
                        alternating_row_color='black',
                        key='-TABLE-',
                        row_height=40,
                        )]
              ]
    window_dict = sg.Window('Password Manager - Dictionaries', layout, resizable=True, font=font25)

    while True:
        event, values = window_dict.read()
        if event == sg.WIN_CLOSED:
            break

def wind_new_pwd(Big):
    from FirstLevelLib import secure_pass
    layout = [[sg.Text("Password")], [sg.InputText()], [sg.Text("empty for a secure pass")],
              [sg.Text("URL")], [sg.InputText()],
              [sg.Text("Username")], [sg.InputText()],
              [sg.Button("OK", key="ok",auto_size_button=True), sg.Button("Add Another",auto_size_button=True, key="another",)]]
    window_new = sg.Window('Password Manager - New Password', layout, size=(300,400),resizable=True, font=font15)
    while True:
        events, values = window_new.read()
        if events == sg.WIN_CLOSED:
            break
        elif events == "ok":
            if not values[0]:
                Big.add_password(pwd=secure_pass(randint(9, 13)), site=values[1], username=values[2])
                sleep(0.1)
                window_new.close()
            else:
                Big.add_password(pwd=values[0], site=values[1], username=values[2])
                sleep(0.2)
                window_new.close()
            break
        elif events ==  "another":
            if not values[0]:
                Big.add_password(pwd=secure_pass(randint(9, 13)), site=values[1], username=values[2])
                sleep(0.1)
                window_new[0].update("")
                window_new[1].update("")
                window_new[2].update("")
                continue
            else:
                Big.add_password(pwd=values[0], site=values[1], username=values[2])
                sleep(0.2)
                window_new[0].update("")
                window_new[1].update("")
                window_new[2].update("")
                continue
        return

def wind_custom_dictionary(Big):
    from FirstLevelLib import CRC__,password_base,new_dictionary,secure_hash
    layout_custom = [
        [sg.Slider((2, 6), orientation="h",enable_events=True), sg.Text("Constant part\nlenght")],
        [sg.Slider((3, 7), orientation="h",enable_events=True), sg.Text("Variable part\nlenght")],
        [sg.InputText("",key="custom_const",size=(8,1)),sg.Text("Custom Constant part")],
        [sg.Radio("Save to", group_id=1, key="saveto"), sg.InputText(key="savetotext",size=(25,1))],
        [sg.Radio("Swap with Current Dict", group_id=1, key="swap")],
        [sg.Button("Ok", key="ok"),sg.Button("Preview",key="preview_button"), sg.Text("HashPreview: "), sg.InputText("",key="preview",font=font10)]
    ]
    win_custom_dict = sg.Window("Custom Dictionary Building", layout=layout_custom, font=font15)
    while True:
        events, values = win_custom_dict.read()
        if events == sg.WIN_CLOSED:

            return
        elif events == "preview_button":
            if values[0] and values[1]:
                if values["custom_const"]:
                    win_custom_dict["preview"].update(str(values["custom_const"]) + secure_hash(int(values[1])))


                else:
                    win_custom_dict["preview"].update(CRC__(password_base(int(values[0]))) + secure_hash(int(values[1])))
        if events == "ok":
            if values["custom_const"]:
                new = new_dictionary(len_hash=int(values[0]),custom_crc=values["custom_const"])
            else:
                new = new_dictionary(values[0],(values[1]))

            if values["swap"] == 1:
                Big.Migration(new)
                sleep(1)
                win_custom_dict.close()
                return sg.Popup("Success", auto_close=True, auto_close_duration=1,font=font20,text_color="green")

            elif values["saveto"]:
                to = values["savetotext"] + ".dict"
                file = open(path_dicts + to, "w")
                file.write(str(new))
                file.close()
                sleep(0.2)
                win_custom_dict.close()
                return sg.Popup(values["savetotext"], auto_close=True, auto_close_duration=1,font=font20,text_color="green")

def wind_get_choice(t, b1, b2):
    win_choice = sg.Window("Choice",[[sg.Text(t,justification="center")],[sg.Button(b1),sg.Button(b2)]],font=font15)

    events,values = win_choice.read()

    if events == sg.WIN_CLOSED:
        win_choice.close()
        return
    if events == b1:
        win_choice.close()
        return True
    elif events == b2:
        win_choice.close()
        return False

def wind_new_note(Big):
    layout = [
        [sg.Text("Note Text: ")],
        [sg.Multiline("",size=(30,5), key="notetext")],
        [sg.Button("Add",key="add"),sg.Button("Add Another",key="another")],
    ]
    win = sg.Window("Add note",layout=layout,font=font20)
    while True:
        events, values = win.read()
        note = values["notetext"].split("\n")
        if events == sg.WIN_CLOSED:
            break
        if events == "add":
            Big.add_note(note)
            win.Close()
            break
        if events == "another":
            Big.add_note(note)
            win["notetext"].update("")
            continue

def winshowkey(k):
    window_show_key = sg.Window(title="Brand New Key",
                                layout=[[sg.Text(k.decode("utf-8"), text_color="yellow")],
                                        [sg.Button("Copy", key="copy")]])
    while True:
        events, values = window_show_key.read()
        if events == sg.WIN_CLOSED:
            break
        elif events == "copy":
            clipboard(k.decode("utf-8"))





