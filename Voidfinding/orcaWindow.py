from tkinter import *
from tkinter import filedialog



class Application(Frame):

    def say_hi(self):
        print( "hi there, everyone!")

    def openFile(self):
        root.filename = filedialog.askopenfilename(initialdir="./Data", title="Select file",
                                                   filetypes=(("data files", "*.dat"), ("all files", "*.*")))
        #print(root.filename)
        self.filelabel["text"] = root.filename

    def autoFill(self):
        #calculate here k, epsilon and gen
        self.kEntry.insert(10,"7")
        self.epsilonEntry.insert(10,"100")
        self.genEntry.insert(10,"3")

    def run(self):
        import orca as o
        o.run(
            epsilon=float(self.epsilonEntry.get()),
            k=int(self.kEntry.get()),
            file=self.filelabel["text"],
            gen=int(self.genEntry.get()),
            save=False,
            printProgress=True
        )

    def createWidgets(self):

        self.chooseFileButton = Button(self)
        self.chooseFileButton["text"] = "Choose file"
        self.chooseFileButton["command"] = self.openFile
        self.chooseFileButton.grid(row=1)

        self.filelabel = Label(self)
        self.filelabel["text"] = "Choose file"
        self.filelabel.grid(row=1, column=1)


        self.kLabel = Label(self)
        self.kLabel["text"] = "k"
        self.kLabel.grid(row=2,column=0,sticky=E)

        self.kEntry = Entry(self)
        self.kEntry.grid(row=2,column=1,sticky=W)


        self.epsilonLabel = Label(self)
        self.epsilonLabel["text"] = "Epsilon"
        self.epsilonLabel.grid(row=3, column=0,sticky=E)

        self.epsilonEntry = Entry(self)
        self.epsilonEntry.grid(row=3, column=1, sticky=W)


        self.genLabel = Label(self)
        self.genLabel["text"] = "Gen"
        self.genLabel.grid(row=4, column=0,sticky=E)

        self.genEntry = Entry(self)
        self.genEntry.grid(row=4, column=1, sticky=W)

        self.runButton = Button(self,
                                text="RUN ORCA",
                                command = self.run,
                                state=DISABLED)
        self.runButton.grid(row=8,column=0)

        self.autoFillButton = Button(self,text="autofill", command = self.autoFill)
        self.autoFillButton.grid(row=9)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=10,column=1)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()