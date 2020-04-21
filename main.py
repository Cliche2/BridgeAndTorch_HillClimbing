from tkinter import *
from time import *

from HillClimbing import *

entriesVelocity = []
labelsVelocity = []
persons = []


class MainRoot(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageOne")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def create_persons(self):
        frame = self.frames["PageTwo"]
        frame.createPersons()


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        labelError = Label(self, fg="red")

        labelQuantity = Label(self, text="Cantidad: ")
        labelQuantity.grid(row=0, column=0)

        entryQuantity = Entry(self)
        entryQuantity.grid(row=0, column=1)

        def getVelocity():
            persons.clear()
            for entry in entriesVelocity:
                persons.append(int(entry.get()))
            print(persons)

        def init(*args):
            errorString = ""
            errorVelocity = ""
            for i in range(len(entriesVelocity)):
                entry = entriesVelocity[i]
                if not entry.get():
                    errorVelocity = errorVelocity + str(i + 1) + ","
                else:
                    print(entry.get())

            if errorVelocity != "":
                print(errorVelocity)
                errorVelocity = errorVelocity[:-1]
                errorString = "Falta la velocidad: " + errorVelocity
            labelError["text"] = errorString

            if errorString == "":
                getVelocity()
                controller.show_frame("PageTwo")
                controller.create_persons()

        buttonPrint = Button(self, text="Init", command=init)

        def clearVelocity():
            for i in range(len(entriesVelocity)):
                entriesVelocity[i].destroy()
                labelsVelocity[i].destroy()
            entriesVelocity.clear()
            labelsVelocity.clear()

        def createVelocity(*args):
            clearVelocity()

            quantity = int(entryQuantity.get())
            entries = [Entry(self) for _ in range(quantity)]
            labels = [Label(self, text="Velocidad %s:" % (i + 1)) for i in range(quantity)]

            for i in range(quantity):
                rowIndex = 3 + i
                labels[i].grid(row=rowIndex, column=0)
                entries[i].grid(row=rowIndex, column=1)
                entriesVelocity.append(entries[i])
                labelsVelocity.append(labels[i])
            labelError.grid(row=(3 + quantity), column=0)

            buttonPrint.grid(row=(4 + quantity), column=1)

        buttonCreate = Button(self, text="Create", command=createVelocity)
        buttonCreate.grid(row=1, column=1)


class PageTwo(Frame):
    personsBox = []
    personsText = []
    canvas = None

    def frameSleep(self, sec):
        Frame.update(self)
        sleep(sec)

    def createPersons(self):
        _canvas = Canvas(self, width=300, height=300)

        for i in range(len(persons)):
            person = str(persons[i])
            x = 10 + ((i % 3) * 30)
            y = 10 + (int((i / 3)) * 30)
            box = _canvas.create_rectangle(x, y, x + 20, y + 20)
            text = _canvas.create_text(x + 10, y + 10, text=str(person))
            self.personsBox.append(box)
            self.personsText.append(text)
            _canvas.pack()
        self.canvas = _canvas

    def movement(self, toMove, direction):
        self.frameSleep(1)
        pos = 100
        add = 10
        if direction == "left":
            pos = 200
            add = -10

        self.paint([max(toMove)], "yellow")

        for j in range(10):
            for i in range(len(toMove)):
                y = 20 + (i * 30)
                x = pos + (add * j)
                index = persons.index(toMove[i])
                box = self.personsBox[index]
                text = self.personsText[index]
                self.canvas.coords(box, x, y, x + 20, y + 20)
                self.canvas.coords(text, x + 10, y + 10)
            self.frameSleep(0.2)

        self.setPosition(toMove, direction)
        self.paint(toMove, "white")

    def setPosition(self, toSet, direction):
        add = 0
        if direction == "right":
            add = 200

        for _ in toSet:
            index = persons.index(_)
            x = add + (10 + ((index % 3) * 30))
            y = 10 + (int((index / 3)) * 30)

            box = self.personsBox[index]
            text = self.personsText[index]
            self.canvas.coords(box, x, y, x + 20, y + 20)
            self.canvas.coords(text, x + 10, y + 10)
            self.frameSleep(0.2)

    def paint(self, toPaint, color):
        for _ in toPaint:
            index = persons.index(_)
            box = self.personsBox[index]
            self.canvas.itemconfig(box, fill=color)
        self.frameSleep(0.3)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def hill():
            hillClimbing(persons, self.movement, self.paint)

        # def movement(*args):
        #     canvas.move(cube, 10, 0)
        #     canvas.move(text, 10, 0)
        #     canvas.move(cube, 10, 0)
        #     canvas.move(text, 10, 0)

        buttonCreate = Button(self, text="Start", command=hill)
        buttonCreate.pack()


if __name__ == "__main__":
    root = MainRoot()
    root.mainloop()

# topFrame = Frame(root)
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side="bottom")
#
# button1 = Button(topFrame, text="Button 1", fg="red")
# button2 = Button(topFrame, text="Button 2", fg="green")
# button3 = Button(bottomFrame, text="Button 3", fg="blue")
#
# button1.pack()
# button2.pack()
# button3.pack()


# one = Label(root, text="One", bg="red", fg="white")
# one.pack()
#
# two = Label(root, text="Two", bg="green", fg="blue")
# two.pack(fill=X)
#
# three = Label(root, text="Three", bg="blue", fg="black")
# three.pack(side=LEFT, fill=Y)

#
# label_1 = Label(root, text="Cantidad de Personas")
# label_2 = Label(root, text="Velocidades")
# entry_1 = Entry(root)
# entry_2 = Entry(root)
#
# label_1.grid(row=0, column=0, sticky=E)
# label_2.grid(row=2, column=0)
#
# entry_1.grid(row=0, column=1)
# # entry_2.grid(row=1, column=1)
#
# # c = Checkbutton(root, text="Keep me logged in")
# # c.grid(columnspan=2)
#
#
# def printName():
#     print("Personas: ", entry_1.get())
#
#
# button_1 = Button(root, text="Print my name", command=printName)
# # button_1 = Button(root, text="Print my name")
# # button_1.bind("<Button-1>", printName)
# button_1.grid(row=1, column=0)

# def leftClick(event):
#     print("Left")
#
#
# def rightClick(event):
#     print("Right")
#
#
# frame = Frame(root, width=300, height=250)
# frame.bind("<Button-1>", leftClick)
# frame.bind("<Button-2>", rightClick)
# frame.pack()


# def doNothing():
#     print("Nothing")
#
#
# # Menu
#
# menu = Menu(root)
# root.config(menu=menu)
#
# subMenu = Menu(menu)
# menu.add_cascade(label="File",  menu=subMenu)
# subMenu.add_command(label="New Project...", command=doNothing)
# subMenu.add_command(label="Now...", command=doNothing)
# subMenu.add_separator()
# subMenu.add_command(label="Exit", command=doNothing)
#
# editMenu = Menu(menu)
# menu.add_cascade(label="Edit",  menu=editMenu)
# editMenu.add_command(label="Redo", command=doNothing)
#
# # Tool Bar
#
# toolBar = Frame(root, bg="Blue")
#
# insertButton = Button(toolBar, text="Insert Image", command=doNothing)
# insertButton.pack(side=LEFT, padx=2, pady=2)
#
# printButton = Button(toolBar, text="Print", command=doNothing)
# printButton.pack(side=LEFT, padx=2, pady=2)
#
# toolBar.pack(side=TOP, fill=X)
#
# # Status Bar
#
# status = Label(root, text="Preparing to do nothing...", bd=1, relief=SUNKEN, anchor=W)
# status.pack(side=BOTTOM, fill=X)


# import tkinter.messagebox
#
# tkinter.messagebox.showinfo("Window Title", "Monkeys can live up to 300 years.")
#
# answer = tkinter.messagebox.askquestion('Question 1', "Do you like?")
#
# if answer == "yes":
#     print(':D')


# canvas = Canvas(root, width=200, height=100)
# canvas.pack()
#
# blackLine = canvas.create_line(0, 0, 200, 50)
# redLine = canvas.create_line(0, 100, 200, 50, fill="red")
# greenBox = canvas.create_rectangle(25, 25, 130, 60, fill="green")
#
# canvas.delete(redLine)
# canvas.delete(ALL)
