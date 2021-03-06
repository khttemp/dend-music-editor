# -*- coding: utf-8 -*-

import struct
import copy
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import os
from pygame import mixer
from dendMusicDecrypt import LSMusicDecrypt as dendLs
from dendMusicDecrypt import BSMusicDecrypt as dendBs
from dendMusicDecrypt import CSMusicDecrypt as dendCs
from dendMusicDecrypt import RSMusicDecrypt as dendRs

playback = None
decryptFile = None
frame = None
after_id = None
loopFlag = False

LS = 0
BS = 1
CS = 2
RS = 3

class ScrollbarframeWithHeader():
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill=BOTH)

        self.tree = ttk.Treeview(self.frame, selectmode="browse")

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("", 14))
        self.style.configure("Treeview", font=("", 12))

        self.scrollbar_x = ttk.Scrollbar(self.frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=lambda f, l: self.scrollbar_x.set(f, l))
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.scrollbar_y = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=lambda f, l: self.scrollbar_y.set(f, l))
        self.scrollbar_y.pack(side=RIGHT, fill=Y)

        self.tree.pack(expand=True, fill=BOTH)
        self.tree.bind("<<TreeviewSelect>>", self.treeSelect)
    

    def treeSelect(self, event):
        selectId = self.tree.selection()[0]
        selectItem = self.tree.set(selectId)
        edit_button['state'] = 'normal'

        if v_radio.get() != LS:
            swap_button['state'] = 'normal'

class inputDialog(sd.Dialog):
    global decryptFile
    
    def __init__(self, master, num, bgmItem=None):
        self.bgmList = []
        self.num = num
        self.bgmItem = bgmItem
        self.itemList = []
        self.v_itemList = []
        self.entryList = []
        self.errorFlag = False
        if self.bgmItem != None:
            self.mode = "edit"
            self.infoMsg = "???????????????????????????????????????????????????"
        else:
            self.mode = "swap"
            self.infoMsg = ""
            self.swapInfoMsg = "??????????????????????????????????????????????????????"

        super().__init__(master)
    def body(self, master):
        self.resizable(False, False)
        maxLen = 0

        if self.bgmItem != None:
            for i in range(2, len(decryptFile.headerList)):
                self.editBgmLb = ttk.Label(master, text=decryptFile.headerList[i][0], font=("", 14))
                self.editBgmLb.grid(row=i, column=0, sticky=N+S)

                idxName = decryptFile.headerList[i][0]
                item = self.bgmItem[idxName]
                self.itemList.append(item)
                if maxLen < len(item):
                    maxLen = len(item)
                v_item = StringVar()
                self.v_itemList.append(v_item)
                self.editBgmEt = ttk.Entry(master, textvariable=v_item)
                self.editBgmEt.grid(row=i, column=1, sticky=N+S)
                self.entryList.append(self.editBgmEt)

            for i in range(2, len(decryptFile.headerList)):
                self.v_itemList[i-2].set(self.itemList[i-2])
                self.entryList[i-2].config(width=maxLen+5)
        else:
            self.swapLb = ttk.Label(master, text="?????????bgm??????", font=("", 14))
            self.swapLb.grid(row=0, column=0, sticky=N+S)

            swapBgmList = []
            for bgm in range(len(decryptFile.musicList)):
                if bgm == self.num:
                    continue
                swapBgmList.append("%02d(%s)" % (bgm, decryptFile.musicList[bgm][2]))

            if len(swapBgmList) == 0:
                errorMsg = "???????????????BGM???????????????????????????"
                mb.showwarning(title="??????", message=errorMsg, parent=self)
                self.errorFlag = True
            else:
                self.v_swap = StringVar()
                self.v_swap.set(swapBgmList[0])
                self.swapCb = ttk.Combobox(master, textvariable=self.v_swap, width=30, state="readonly", value=swapBgmList)
                self.swapCb.grid(row=0, column=1, sticky=N+S, pady=10)
                self.swapCb.set(swapBgmList[0])

    def buttonbox(self):
        box = Frame(self, padx=5, pady=5)
        self.okBtn = Button(box, text="OK", width=10, command=self.okPress)
        self.okBtn.grid(row=0, column=0, padx=5)
        self.cancelBtn = Button(box, text="Cancel", width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=1, padx=5)
        box.pack()

    def okPress(self):
        selectId = int(frame.tree.selection()[0])
        if self.bgmItem != None:
            for i in range(2, len(decryptFile.headerList)):
                if decryptFile.headerList[i][0] in ["start", "loop start", "loop end"]:
                    try:
                        self.itemList[i-2] = float(self.v_itemList[i-2].get())
                    except:
                        errorMsg = "????????????????????????????????????"
                        mb.showerror(title="???????????????", message=errorMsg, parent=self)
                        return
                else:
                    self.itemList[i-2] = self.v_itemList[i-2].get()
                    if len(self.itemList[i-2].encode("shift-jis")) > 0xFF:
                        errorMsg = "???????????????????????????????????????"
                        mb.showerror(title="???????????????", message=errorMsg, parent=self)
                        return
        else:
            comboName = self.v_swap.get()
            bgmNo = int(comboName[0:2])
            self.infoMsg = "{0}??????{1}???????????????????????????\n".format(selectId, bgmNo) + self.swapInfoMsg
                
        result = mb.askokcancel(title="??????", message=self.infoMsg, parent=self)
        if result:
            self.ok()
            musicList = decryptFile.musicList[selectId]
            if self.bgmItem != None:
                for i in range(2, len(decryptFile.headerList)):
                    musicList[i-1] = self.itemList[i-2]
                decryptFile.musicList[selectId] = musicList
            else:
                decryptFile.musicList[selectId] = decryptFile.musicList[bgmNo]
                decryptFile.musicList[bgmNo] = musicList

            errorMsg = "??????????????????????????????\n??????????????????????????????????????????????????????????????????\n????????????????????????????????????????????????"
            if not decryptFile.saveMusic():
                decryptFile.printError()
                mb.showerror(title="???????????????", message=errorMsg)
            else:
                mb.showinfo(title="??????", message="BGM?????????????????????")
                reloadFile()

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

    errorMsg = "???????????????????????????????????????\n?????????D??????????????????????????????????????????????????????????????????????????????????????????"
    if file_path:
        deleteWidget()
        if not decryptFile.open():
            decryptFile.printError()
            mb.showerror(title="?????????", message=errorMsg)
            return

        if v_radio.get() == LS and decryptFile.error != "":
            mb.showerror(title="?????????", message=decryptFile.error)
            return
        
        createWidget()

def openBgmFile():
    global bgmScale
    global after_id

    try:
        file_path = fd.askopenfilename(filetypes=[("bgm", "*.ogg;*.wav")])
        if file_path:
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
    except:
        errorMsg = "????????????????????????????????????????????????"
        mb.showerror(title="?????????????????????", message=errorMsg)
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
        errorMsg = "????????????????????????????????????"
        mb.showerror(title="?????????", message=errorMsg)
        return

    if v_start.get() < 0:
        errorMsg = "start??????0????????????????????????????????????"
        mb.showerror(title="?????????", message=errorMsg)
        return
    if v_start.get() > bgmScale["to"]-0.5:
        errorMsg = "start???????????????????????????????????????????????????????????????"
        mb.showerror(title="?????????", message=errorMsg)
        return
    if v_loopStart.get() < 0:
        errorMsg = "loop start??????0????????????????????????????????????"
        mb.showerror(title="?????????", message=errorMsg)
        return
    if v_loopEnd.get() > 0 and v_loopStart.get() > v_loopEnd.get():
        errorMsg = "loop start???loop end????????????????????????"
        mb.showerror(title="?????????", message=errorMsg)
        return

    mixer.music.play(0, v_start.get())
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
            mixer.music.play(0, v_loopStart.get())
            val.set(round(fixTime + mixer.music.get_pos()/1000, 3))
    
    if round(fixTime + mixer.music.get_pos()/1000,3) >= bgmScale["to"]-0.01:
        loopFlag = True
        fixTime = v_loopStart.get()
        mixer.music.play(0, fixTime)
            
    after_id = root.after(1, updateBgm)

def createWidget():
    global decryptFile
    global bgmLf
    global frame
    
    width = bgmLf.winfo_width()
    height = bgmLf.winfo_height()
    frame = ScrollbarframeWithHeader(bgmLf)

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
    global frame
    
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    inputDialog(root, int(selectItem["No"]), selectItem)

def swapMusic():
    global frame
    
    selectId = frame.tree.selection()[0]
    selectItem = frame.tree.set(selectId)
    inputDialog(root, int(selectItem["No"]))

def reloadFile():
    global decryptFile

    errorMsg = "???????????????????????????????????????\n?????????D??????????????????????????????????????????????????????????????????????????????????????????"
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title="?????????", message=errorMsg)
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
root.title("?????????D LBCR BGM?????? 1.1.1")
root.geometry("1024x768")

menubar = Menu(root)
menubar.add_cascade(label='?????????????????????', command= lambda: openFile())
menubar.add_cascade(label='BGM?????????????????????', command= lambda: openBgmFile())
root.config(menu=menubar)

v_edit = StringVar()
v_edit.set("??????BGM???????????????")
edit_button = ttk.Button(root, textvariable=v_edit, command=editMusic, state='disabled')
edit_button.place(relx = 0.48, rely=0.02, relwidth=0.2, height=25)

v_swap = StringVar()
v_swap.set("??????BGM??????????????????")
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

bgmLf = ttk.LabelFrame(root, text="BGM?????????")
bgmLf.place(relx=0.03, rely=0.12, relwidth=0.94, relheight=0.5)

playerLf = ttk.LabelFrame(root, text="???????????????")
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
