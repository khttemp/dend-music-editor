from tkinter import *

LS = 0
BS = 1
CS = 2
RS = 3

class ScrollbarFrame():
    def __init__(self, parent, content, btnList):
        self.content = content
        self.btnList = btnList
        
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
        editButton = self.btnList[0]
        swapButton = self.btnList[1]
        
        selectId = self.tree.selection()[0]
        selectItem = self.tree.set(selectId)
        editButton['state'] = 'normal'

        if self.content != LS:
            swapButton['state'] = 'normal'
