# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from dendMusicDecrypt import LSMusicDecrypt as dendLs
from dendMusicDecrypt import BSMusicDecrypt as dendBs
from dendMusicDecrypt import CSMusicDecrypt as dendCs
from dendMusicDecrypt import RSMusicDecrypt as dendRs

from importPy.tkinterScrollbarFrameClass import ScrollbarFrame
from importPy.tkinterEditClass import InputDialog

decryptFile = None
frame = None

LS = 0
BS = 1
CS = 2
RS = 3


def openFile():
    global decryptFile

    if v_radio.get() == LS:
        file_path = fd.askopenfilename(filetypes=[("RAIL_DATA", "RAIL*.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendLs.LSMusicDecrypt(file_path)
    elif v_radio.get() == BS:
        file_path = fd.askopenfilename(filetypes=[("MUSIC_DATA", "LS_INFO.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendBs.BSMusicDecrypt(file_path)
    elif v_radio.get() == CS:
        file_path = fd.askopenfilename(filetypes=[("MUSIC_DATA", "SOUNDTRACK_INFO.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendCs.CSMusicDecrypt(file_path)
    elif v_radio.get() == RS:
        file_path = fd.askopenfilename(filetypes=[("MUSIC_DATA", "SOUNDTRACK_INFO_4TH.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendRs.RSMusicDecrypt(file_path)

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if file_path:
        deleteWidget()
        if not decryptFile.open():
            decryptFile.printError()
            mb.showerror(title="エラー", message=errorMsg)
            return

        if v_radio.get() == LS and decryptFile.error != "":
            mb.showerror(title="エラー", message=decryptFile.error)
            return

        createWidget()


def createWidget():
    global decryptFile
    global bgmLf
    global frame

    content = v_radio.get()
    btnList = [edit_button, swap_button]
    frame = ScrollbarFrame(bgmLf, content, btnList)

    treeHeaderList = []

    for i in range(len(decryptFile.headerList)):
        treeHeaderList.append(decryptFile.headerList[i][0])

    frame.tree["columns"] = tuple(treeHeaderList)

    frame.tree.column('#0', width=0, stretch='no')
    for i in range(len(decryptFile.headerList)):
        frame.tree.column(decryptFile.headerList[i][0], anchor=tkinter.CENTER, width=decryptFile.headerList[i][1])

    for i in range(len(decryptFile.headerList)):
        frame.tree.heading(decryptFile.headerList[i][0], text=decryptFile.headerList[i][0], anchor=tkinter.CENTER)

    for i in range(len(decryptFile.musicList)):
        data = tuple([i]) + tuple(decryptFile.musicList[i])
        frame.tree.insert(parent='', index='end', iid=i, values=data)


def editMusic():
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, "BGM修正", decryptFile, int(selectItem["No"]), selectItem)
    if result.reloadFlag:
        reloadFile()


def swapMusic():
    global decryptFile
    global frame

    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    result = InputDialog(root, "BGM入れ替え", decryptFile, int(selectItem["No"]))
    if result.reloadFlag:
        reloadFile()


def reloadFile():
    global decryptFile

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title="エラー", message=errorMsg)
        return

    deleteWidget()
    createWidget()
    edit_button['state'] = 'disabled'
    swap_button['state'] = 'disabled'


def deleteWidget():
    global bgmLf
    children = bgmLf.winfo_children()
    for child in children:
        child.destroy()

    edit_button['state'] = 'disabled'
    swap_button['state'] = 'disabled'


root = tkinter.Tk()
root.title("電車でD LBCR BGM改造 1.1.2(no-player)")
root.geometry("1024x768")

menubar = tkinter.Menu(root)
menubar.add_cascade(label='ファイルを開く', command=lambda: openFile())
root.config(menu=menubar)

v_edit = tkinter.StringVar()
v_edit.set("このBGMを修正する")
edit_button = ttk.Button(root, textvariable=v_edit, command=editMusic, state='disabled')
edit_button.place(relx=0.48, rely=0.02, relwidth=0.2, height=25)

v_swap = tkinter.StringVar()
v_swap.set("このBGMを入れ替える")
swap_button = ttk.Button(root, textvariable=v_swap, command=swapMusic, state='disabled')
swap_button.place(relx=0.75, rely=0.02, relwidth=0.2, height=25)

v_radio = tkinter.IntVar()

lsRb = tkinter.Radiobutton(root, text="Lightning Stage", command=deleteWidget, variable=v_radio, value=LS)
lsRb.place(relx=0.04, rely=0.02)

bsRb = tkinter.Radiobutton(root, text="Burning Stage", command=deleteWidget, variable=v_radio, value=BS)
bsRb.place(relx=0.22, rely=0.02)

csRb = tkinter.Radiobutton(root, text="Climax Stage", command=deleteWidget, variable=v_radio, value=CS)
csRb.place(relx=0.04, rely=0.07)

rsRb = tkinter.Radiobutton(root, text="Rising Stage", command=deleteWidget, variable=v_radio, value=RS)
rsRb.select()
rsRb.place(relx=0.22, rely=0.07)

bgmLf = ttk.LabelFrame(root, text="BGMリスト")
bgmLf.place(relx=0.03, rely=0.12, relwidth=0.94, relheight=0.85)

root.mainloop()
