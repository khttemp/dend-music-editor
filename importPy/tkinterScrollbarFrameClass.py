import tkinter
from tkinter import ttk

LS = 0
BS = 1
CS = 2
RS = 3


class ScrollbarFrame():
    def __init__(self, parent, content, btnList):
        self.content = content
        self.btnList = btnList

        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill=tkinter.BOTH)

        self.tree = ttk.Treeview(self.frame, selectmode="browse")

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("", 14))
        self.style.configure("Treeview", font=("", 12))

        self.scrollbar_x = ttk.Scrollbar(self.frame, orient=tkinter.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=lambda first, last: self.scrollbar_x.set(first, last))
        self.scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.scrollbar_y = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=lambda first, last: self.scrollbar_y.set(first, last))
        self.scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.tree.pack(expand=True, fill=tkinter.BOTH)
        self.tree.bind("<<TreeviewSelect>>", self.treeSelect)

    def treeSelect(self, event):
        editButton = self.btnList[0]
        swapButton = self.btnList[1]

        selectId = self.tree.selection()[0]
        self.tree.set(selectId)
        editButton['state'] = 'normal'

        if self.content != LS:
            swapButton['state'] = 'normal'
