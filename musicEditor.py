# -*- coding: utf-8 -*-

import os

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
from pygame import mixer

from dendMusicDecrypt import LSMusicDecrypt as dendLs
from dendMusicDecrypt import BSMusicDecrypt as dendBs
from dendMusicDecrypt import CSMusicDecrypt as dendCs
from dendMusicDecrypt import RSMusicDecrypt as dendRs

from importPy.tkinterScrollbarFrameClass import *
from importPy.tkinterEditClass import *

playback = None
decryptFile = None
frame = None
after_id = None
loopFlag = False

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

def openBgmFile():
    global bgmScale
    global after_id

    try:
        file_path = fd.askopenfilename(filetypes=[("bgm", "*.ogg;*.wav")])
        if file_path:
            base, ext = os.path.splitext(os.path.basename(file_path))
            if ext.lower() == ".wav":
                warnMsg = "このファイル形式は途中再生ができません"
                mb.showwarning(title="警告", message=warnMsg)
                
            if after_id != None:
                root.after_cancel(after_id)

            mixer.init()
            mixer.music.load(file_path)
            sound = mixer.Sound(file_path)
            
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            v_readBgm.set(file_name)
            startEt["state"] = "readonly"
            loopStartEt["state"] = "readonly"
            loopEndEt["state"] = "readonly"
            bgmScale["state"] = "disabled"
            bgmPlayBtn["state"] = "disabled"
            bgmPauseBtn["state"] = "disabled"
            root.update()
            
            bgmScale["to"] = round(sound.get_length(), 2)
            
            startEt["state"] = "normal"
            loopStartEt["state"] = "normal"
            loopEndEt["state"] = "normal"
            v_start.set(0.0)
            v_loopStart.set(0.0)
            v_loopEnd.set(-1.0)
            val.set(0.0)
            bgmScale["state"] = "normal"
            bgmPlayBtn["state"] = "normal"
            bgmPauseBtn["state"] = "disabled"
    except Exception as e:
        print(e)
        errorMsg = "サポートしないファイル形式です。"
        mb.showerror(title="ファイルエラー", message=errorMsg)
        return


def adjustPlayback():
    global val
    val.set(round(val.get(), 3))

def playBgm():
    global after_id
    global loopFlag

    try:
        float(v_start.get())
        float(v_loopStart.get())
        float(v_loopEnd.get())
    except:
        errorMsg = "数字で入力してください。"
        mb.showerror(title="エラー", message=errorMsg)
        return

    if v_start.get() < 0:
        errorMsg = "startは、0以上で設定してください。"
        mb.showerror(title="エラー", message=errorMsg)
        return
    if v_start.get() > bgmScale["to"]-0.5:
        errorMsg = "startが曲の長さと近すぎ、あるいは超えています。"
        mb.showerror(title="エラー", message=errorMsg)
        return
    if v_loopStart.get() < 0:
        errorMsg = "loop startは、0以上で設定してください。"
        mb.showerror(title="エラー", message=errorMsg)
        return
    if v_loopEnd.get() > 0 and v_loopStart.get() > v_loopEnd.get():
        errorMsg = "loop startがloop endより大きいです。"
        mb.showerror(title="エラー", message=errorMsg)
        return

    try:
        mixer.music.play(0, v_start.get())
    except:
        errorMsg = "このファイル形式は、途中再生ができません"
        mb.showerror(title="エラー", message=errorMsg)
        return
    val.set(round(v_start.get(), 3))
    loopFlag = False
    
    bgmPlayBtn["state"] = "disabled"
    bgmPauseBtn["state"] = "normal"
    startEt["state"] = "readonly"
    loopStartEt["state"] = "readonly"
    loopEndEt["state"] = "readonly"
    after_id = root.after(1, updateBgm)

def pauseBgm():
    global playback
    global after_id
    global loopFlag
    
    loopFlag = False
    mixer.music.pause()
    bgmPlayBtn["state"] = "normal"
    bgmPauseBtn["state"] = "disabled"
    startEt["state"] = "normal"
    loopStartEt["state"] = "normal"
    loopEndEt["state"] = "normal"
    root.after_cancel(after_id)

def updateBgm():
    global after_id
    global val
    global loopFlag

    fixTime = 0
    if not loopFlag:
        fixTime = v_start.get()
    else:
        fixTime = v_loopStart.get()
        
    val.set(round(fixTime + mixer.music.get_pos()/1000, 3))
    if v_loopStart.get() <= v_loopEnd.get():
        if fixTime + mixer.music.get_pos()/1000 >= v_loopEnd.get():
            loopFlag = True
            fixTime = v_loopStart.get()
            try:
                mixer.music.play(0, v_loopStart.get())
            except:
                errorMsg = "このファイル形式は、途中再生ができません"
                mb.showerror(title="エラー", message=errorMsg)
                return
            val.set(round(fixTime + mixer.music.get_pos()/1000, 3))
    
    if round(fixTime + mixer.music.get_pos()/1000,3) >= bgmScale["to"]-0.01:
        loopFlag = True
        fixTime = v_loopStart.get()
        try:
            mixer.music.play(0, fixTime)
        except:
            errorMsg = "このファイル形式は、途中再生ができません"
            mb.showerror(title="エラー", message=errorMsg)
            return
            
    after_id = root.after(1, updateBgm)

def createWidget():
    global decryptFile
    global bgmLf
    global frame
    
    width = bgmLf.winfo_width()
    height = bgmLf.winfo_height()

    content = v_radio.get()
    btnList = [edit_button, swap_button]
    frame = ScrollbarFrame(bgmLf, content, btnList)

    treeHeaderList = []

    for i in range(len(decryptFile.headerList)):
        treeHeaderList.append(decryptFile.headerList[i][0])

    frame.tree["columns"] = tuple(treeHeaderList)

    frame.tree.column('#0',width=0, stretch='no')
    for i in range(len(decryptFile.headerList)):
        frame.tree.column(decryptFile.headerList[i][0], anchor=CENTER, width=decryptFile.headerList[i][1])

    for i in range(len(decryptFile.headerList)):
        frame.tree.heading(decryptFile.headerList[i][0], text=decryptFile.headerList[i][0], anchor=CENTER)

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
        
root = Tk()
root.title("電車でD LBCR BGM改造 1.1.2")
root.geometry("1024x768")

menubar = Menu(root)
menubar.add_cascade(label='ファイルを開く', command= lambda: openFile())
menubar.add_cascade(label='BGMファイルを開く', command= lambda: openBgmFile())
root.config(menu=menubar)

v_edit = StringVar()
v_edit.set("このBGMを修正する")
edit_button = ttk.Button(root, textvariable=v_edit, command=editMusic, state='disabled')
edit_button.place(relx = 0.48, rely=0.02, relwidth=0.2, height=25)

v_swap = StringVar()
v_swap.set("このBGMを入れ替える")
swap_button = ttk.Button(root, textvariable=v_swap, command=swapMusic, state='disabled')
swap_button.place(relx = 0.75, rely=0.02, relwidth=0.2, height=25)

v_radio = IntVar()

lsRb = Radiobutton(root, text="Lightning Stage", command = deleteWidget, variable=v_radio, value=LS)
lsRb.place(relx=0.04, rely=0.02)

bsRb = Radiobutton(root, text="Burning Stage", command = deleteWidget, variable=v_radio, value=BS)
bsRb.place(relx=0.22, rely=0.02)

csRb = Radiobutton(root, text="Climax Stage", command = deleteWidget, variable=v_radio, value=CS)
csRb.place(relx=0.04, rely=0.07)

rsRb = Radiobutton(root, text="Rising Stage", command = deleteWidget, variable=v_radio, value=RS)
rsRb.select()
rsRb.place(relx=0.22, rely=0.07)

bgmLf = ttk.LabelFrame(root, text="BGMリスト")
bgmLf.place(relx=0.03, rely=0.12, relwidth=0.94, relheight=0.5)

playerLf = ttk.LabelFrame(root, text="プレイヤー")
playerLf.place(relx=0.03, rely=0.63, relwidth=0.94, relheight=0.35)

startLb = ttk.Label(playerLf, text="start", font=("", 20), relief="groove", anchor=CENTER)
startLb.place(relx=0.03, rely=0.1, relwidth=0.1, relheight=0.205)
v_start = DoubleVar()
v_start.set(0.0)
startEt = ttk.Entry(playerLf, textvariable=v_start, font=("", 20), justify=CENTER)
startEt.place(relx=0.13, rely=0.1, relwidth=0.13, relheight=0.2)

loopStartLb = ttk.Label(playerLf, text="loop start", font=("", 20), relief="groove", anchor=CENTER)
loopStartLb.place(relx=0.31, rely=0.1, relwidth=0.18, relheight=0.205)
v_loopStart = DoubleVar()
v_loopStart.set(0.0)
loopStartEt = ttk.Entry(playerLf, textvariable=v_loopStart, font=("", 20), justify=CENTER)
loopStartEt.place(relx=0.49, rely=0.1, relwidth=0.13, relheight=0.2)

loopEndLb = ttk.Label(playerLf, text="loop end", font=("", 20), relief="groove", anchor=CENTER)
loopEndLb.place(relx=0.66, rely=0.1, relwidth=0.18, relheight=0.205)
v_loopEnd = DoubleVar()
v_loopEnd.set(-1.0)
loopEndEt = ttk.Entry(playerLf, textvariable=v_loopEnd, font=("", 20), justify=CENTER)
loopEndEt.place(relx=0.84, rely=0.1, relwidth=0.13, relheight=0.2)

startEt["state"] = "readonly"
loopStartEt["state"] = "readonly"
loopEndEt["state"] = "readonly"

val = DoubleVar()
bgmScale = ttk.Scale(playerLf, variable=val, from_=0, to=100, command=lambda e: adjustPlayback())
bgmScale.place(relx=0.03, rely=0.4, relwidth=0.85)

bgmValueLb = ttk.Label(playerLf, textvariable=val, font=("", 20))
bgmValueLb.place(relx=0.90, rely=0.4)

bgmScale["state"] = "disabled"

v_readBgm = StringVar()
bgmPlayNameLb = ttk.Label(playerLf, textvariable=v_readBgm, font=("", 14), relief="groove", anchor=CENTER)
bgmPlayNameLb.place(relx=0.03, rely=0.6, relwidth=0.28, relheight=0.2)

bgmPlayBtn = ttk.Button(playerLf, text="Play", command=playBgm)
bgmPlayBtn.place(relx=0.40, rely=0.6, relwidth=0.2, relheight=0.2)
bgmPlayBtn["state"] = "disabled"
bgmPauseBtn = ttk.Button(playerLf, text="Pause", command=pauseBgm)
bgmPauseBtn.place(relx=0.68, rely=0.6, relwidth=0.2, relheight=0.2)
bgmPauseBtn["state"] = "disabled"

root.mainloop()
