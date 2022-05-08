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
headerList = []
varList = []
btnList = []

LS = 0
BS = 1
CS = 2
RS = 3

class Scrollbarframe():
    def __init__(self, parent):
        self.canvas = Canvas(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.frame = Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollbar = Scrollbar(parent, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack()

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class bgmHeaderWidget():
    global headerList
    
    def __init__(self, i, frame, headerName, headerWidth):
        self.bgmHeaderLb = Label(frame,
                                 text=headerName,
                                 font=("", 20),
                                 width=headerWidth,
                                 borderwidth=1,
                                 relief="solid")
        self.bgmHeaderLb.grid(row=0, column=i, sticky=N+S)
        headerList.append(self.bgmHeaderLb)
        
        
class bgmWidget():
    global decryptFile
    
    def __init__(self, i, notchCnt, frame, speed):
        pass
        

    def editVar(self, var, value, flag = False):
        result = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        """
        if result:
            try:
                if flag:
                    try:
                        result = int(result)
                        var.set(result)
                    except:
                        errorMsg = "整数で入力してください。"
                        mb.showerror(title="整数エラー", message=errorMsg)
                else:
                    try:
                        result = float(result)
                        var.set(result)
                    except:
                        errorMsg = "数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
        """
        
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
    global varList
    global btnList
    
    width = bgmLf.winfo_width()
    height = bgmLf.winfo_height()
    frame = Scrollbarframe(bgmLf)
    frame.frame.config(bg="red")
    frame2 = Scrollbarframe(bgmLf)

    for i in range(len(decryptFile.headerList)):
        bgmHeaderWidget(i, frame.frame, decryptFile.headerList[i][0], decryptFile.headerList[i][1])
    headerList[0].config(bg="white")

    for i in range(len(decryptFile.headerList)):
        bgmHeaderWidget(i, frame2.frame, decryptFile.headerList[i][0], decryptFile.headerList[i][1])

def editMusic():
    global btnList
    for btn in btnList:
        btn['state'] = 'normal'

    v_edit.set("保存する")
    edit_button["command"] = saveMusic

def saveMusic():
    global v_edit
    global varList
    global btnList
    global decryptFile
    
    v_edit.set("このBGMリストを修正する")
    edit_button["command"] = editMusic
    for btn in btnList:
        btn['state'] = 'disabled'

    #TODO

    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
    if not decryptFile.saveMusic():
        decryptFile.printError()
        mb.showerror(title="保存エラー", message=errorMsg)
    else:
        mb.showinfo(title="成功", message="BGMリストを改造しました")
        reloadFile()

def reloadFile():
    global v
    global decryptFile

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title="エラー", message=errorMsg)
        return
    
    deleteWidget()
    createWidget()

def deleteWidget():
    global bgmLf
    global varList
    global btnList
    children = bgmLf.winfo_children()
    for child in children:
        child.destroy()

    varList = []
    btnList = []
    v_edit.set("このBGMリストを修正する")

def selectGame():
    deleteWidget()
    edit_button['command'] = editMusic
    edit_button['state'] = 'disabled'
    v_edit.set("このBGMリストを修正する")
        
root = Tk()
root.title("電車でD LBCR BGM改造 1.0.0")
root.geometry("1024x768")

menubar = Menu(root)
menubar.add_cascade(label='ファイルを開く', command= lambda: openFile())
root.config(menu=menubar)

v_edit = StringVar()
v_edit.set("このBGMリストを修正する")
edit_button = ttk.Button(root, textvariable=v_edit, command=editMusic, state='disabled')
edit_button.place(relx = 0.75, rely=0.02, relwidth=0.2, height=25)

v_radio = IntVar()

lsRb = Radiobutton(root, text="Lightning Stage", command = selectGame, variable=v_radio, value=LS)
lsRb.place(relx=0.04, rely=0.02)

bsRb = Radiobutton(root, text="Burning Stage", command = selectGame, variable=v_radio, value=BS)
bsRb.place(relx=0.22, rely=0.02)

csRb = Radiobutton(root, text="Climax Stage", command = selectGame, variable=v_radio, value=CS)
csRb.place(relx=0.40, rely=0.02)

rsRb = Radiobutton(root, text="Rising Stage", command = selectGame, variable=v_radio, value=RS)
rsRb.select()
rsRb.place(relx=0.58, rely=0.02)

bgmLf = ttk.LabelFrame(root, text="BGMリスト")
bgmLf.place(relx=0.03, rely=0.07, relwidth=0.94, relheight=0.5)

#perfLf = ttk.LabelFrame(root, text="性能")
#perfLf.place(relx=0.45, rely=0.12, relwidth=0.52, relheight=0.8)

root.mainloop()
