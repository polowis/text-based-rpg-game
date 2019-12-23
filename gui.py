

# Comment out the tkinter line not appropriate for your Python version
from tkinter import *  # Python 3
# from Tkinter import *  # Python 2
import tkinter.messagebox
import time
import tkinter.filedialog


class simpleapp_tk(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
       

    def doNothing(self):
        return True
        
    def callback(self):
        """If the user accidentally close the window """
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you want to quit, your data will not be saved"):
            sys.exit(0)

    def initialize(self):
        self.grid()
        # used for polling for user input only
        # i.e. wait variable
        

        self.inputVariable = StringVar()
        self.protocol("WM_DELETE_WINDOW", self.callback)
        scrollbar = Scrollbar(self)
        scrollbar.grid(row=0, column=2, sticky=N + S)

        self.text = Text(self, wrap=WORD, yscrollcommand=scrollbar.set, cursor="spider", font=("Times New Roman", 14, "bold"), fg="white", bg="black")
        self.text.grid(column=0, row=0, columnspan=2, sticky='NSEW')
        self.text.config(state=DISABLED)

        scrollbar.config(command=self.text.yview)

        self.entryVariable = StringVar()
        self.entry = Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=1, sticky='SEW')
        self.entry.bind("<Return>", self.OnPressEnter)

        button = Button(self, text=u"Enter",
                        command=self.OnButtonClick)
        button.grid(column=1, row=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(True, True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, END)
        
    def OnButtonClick(self):
        self.inputVariable.set(self.entryVariable.get())

    def OnPressEnter(self, event):
        self.inputVariable.set(self.entryVariable.get())

    # The write function simulates the behaviour of the print method
    # but uses the input textfield and text display instead of the usual
    # standard input/output we're used to from our previous programs
    def write(self, msg):
        self.text.config(state=NORMAL)
        self.text.insert(END, msg)
        self.text.insert(END, "\n")
        self.update()
        self.text.config(state=DISABLED)
        self.text.see(END)
        self.entryVariable.set('')
        self.entry.focus_set()

    def showinfo(self, msg):
        """Show information in pop up window"""
        tkinter.messagebox.showinfo('Information', msg)
    
    def createMenu(self):
        return Menu()

    def Menu(self, menu):
        """Create a menu"""
        return Menu(menu, tearoff=0)

    def save_file(self):
        """Save file"""
        #open folder using tkinter.filedialog
        return tkinter.filedialog.asksaveasfile(mode="w",defaultextension=".txt")
    
    def load_file(self):
        """Load file from folder"""
        return tkinter.filedialog.askopenfilename(defaultextension=".txt")
        
    def quit(self):
        sys.exit(0)