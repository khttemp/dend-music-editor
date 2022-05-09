# -*- coding: utf-8 -*-

import struct
import copy
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from dendMusicDecrypt import RSMusicDecrypt as dendRs

decryptFile = None
frame = None

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
        if self.bgmItem != None:
            self.mode = "edit"
            self.infoMsg = "このまま修正してもよろしいですか？"
        else:
            self.mode = "swap"
            self.infoMsg = ""
            self.swapInfoMsg = "このまま入れ替えてもよろしいですか？"
            
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
            self.swapLb = ttk.Label(master, text="変えるbgm番号", font=("", 14))
            self.swapLb.grid(row=0, column=0, sticky=N+S)

            swapBgmList = []
            for bgm in range(len(decryptFile.musicList)):
                if bgm == self.num:
                    continue
                swapBgmList.append("%02d(%s)" % (bgm, decryptFile.musicList[bgm][2]))

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
                        errorMsg = "数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg, parent=self)
                        return
                else:
                    self.itemList[i-2] = self.v_itemList[i-2].get()
                    if len(self.itemList[i-2].encode("shift-jis")) > 0xFF:
                        errorMsg = "文字列の長さが長すぎです。"
                        mb.showerror(title="数字エラー", message=errorMsg, parent=self)
                        return
        else:
            comboName = self.v_swap.get()
            bgmNo = int(comboName[0:2])
            self.infoMsg = "{0}番と{1}番を入れ替えます。\n".format(selectId, bgmNo) + self.swapInfoMsg
                
        result = mb.askokcancel(title="確認", message=self.infoMsg, parent=self)
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

            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            if not decryptFile.saveMusic():
                decryptFile.printError()
                mb.showerror(title="保存エラー", message=errorMsg)
            else:
                mb.showinfo(title="成功", message="BGMを修正しました")
                reloadFile()

def openFile():
    global decryptFile

    if v_radio.get() == LS:
        pass
    elif v_radio.get() == BS:
        pass
    elif v_radio.get() == CS:
        pass
    elif v_radio.get() == RS:
        file_path = fd.askopenfilename(filetypes=[("MUSIC_DATA", "SOUNDTRACK_INFO_4TH.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            decryptFile = dendRs.RSMusicDecrypt(file_path)

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if file_path:        
        if not decryptFile.open():
            decryptFile.printError()
            mb.showerror(title="エラー", message=errorMsg)
            return
        
        deleteWidget()
        createWidget()

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

def selectGame():
    deleteWidget()
    edit_button['state'] = 'disabled'
    swap_button['state'] = 'disabled'
        
root = Tk()
root.title("電車でD LBCR BGM改造 1.0.0")
root.geometry("1024x768")

menubar = Menu(root)
menubar.add_cascade(label='ファイルを開く', command= lambda: openFile())
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

lsRb = Radiobutton(root, text="Lightning Stage", command = selectGame, variable=v_radio, value=LS)
lsRb.place(relx=0.04, rely=0.02)

bsRb = Radiobutton(root, text="Burning Stage", command = selectGame, variable=v_radio, value=BS)
bsRb.place(relx=0.22, rely=0.02)

csRb = Radiobutton(root, text="Climax Stage", command = selectGame, variable=v_radio, value=CS)
csRb.place(relx=0.04, rely=0.07)

rsRb = Radiobutton(root, text="Rising Stage", command = selectGame, variable=v_radio, value=RS)
rsRb.select()
rsRb.place(relx=0.22, rely=0.07)

bgmLf = ttk.LabelFrame(root, text="BGMリスト")
bgmLf.place(relx=0.03, rely=0.12, relwidth=0.94, relheight=0.5)

#perfLf = ttk.LabelFrame(root, text="性能")
#perfLf.place(relx=0.45, rely=0.12, relwidth=0.52, relheight=0.8)

root.mainloop()
