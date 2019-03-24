from tkinter import *
from tkinter import messagebox
import GetGradesClass
import time
import threading
import winsound
import datetime

#TODO validate minutes input
#TODO add labels
#TODO clean code
#TODO try to fix errors on exit

class Calculator:

    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)

        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

        self.add_button.grid(row=2, column=0)
        self.subtract_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2, sticky=W+E)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        else: # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

class GetGrades:
    def __init__(self, master , login, passw, sem):
        self.master = master
        self.sem = sem
        self.login = login
        self.passw = passw
        self.count = 0
        self.threadMessage = 1
        self.textCouter = ""
        self.courseLabel = Label(self.master, text= "Course")
        master.title("Get Grades(Alpha) - Hi " + self.login)
        self.a = []
        self.b = []
        self.c = []
        self.chosenCourse = StringVar(self.master)
        #change to parser of course numbers
        courseNum = GetGradesClass.getCourses(self.login,self.passw, self.sem)
        self.chosenCourse.set(courseNum[0])
        self.courseMenu = OptionMenu(self.master, self.chosenCourse, *courseNum)
        self.courseMenu.config(width = 13)
        self.minutes = Entry(self.master, width = 19,justify = RIGHT)
        self.lArr1 = []
        self.lArr2 = []
        self.lArr3 = []

        # BUTTONS
        self.updButt = Button(self.master, text = "Monitor!", command = self.updateFunc)

        # LAYOUT
        self.courseLabel.grid(column = 0, row = 0)
        self.courseMenu.grid(column = 1, row = 0)
        self.minutes.grid(column = 1, row = 1)
        self.updButt.grid(column = 1, row = 2)

    

    def getUpdatedIndexes(self,arr1,arr2):
        temp = []
        for i in range(len(arr2)):
            if arr2[i] not in arr1:
                temp.append(i)
        return temp

    def fillLabels(self, arr, targArr, compArr = None):
        for i in range(len(arr)):
            if compArr != None and i in compArr and self.firstTime == 0:
                targArr.append(Label(self.master, text=arr[i], fg="green"))
                continue
            targArr.append(Label(self.master, text=arr[i]))

    def fillGridOfLabels(self,arr,targArr,r):
        for i in range(2,len(arr)+2):
            targArr[i-2].grid(column = i, row = r)

    def updateFunc(self):
        self.killThread()
        self.threadMessage = 1
        self.t1 = threading.Thread(target=self.monFunc, args=[])
        self.t1.start()

    def killThread(self):
        try:
            if self.t1.isAlive():
                self.threadMessage = 0
                # self.t1.join(10)
                self.t1.join()
        except NameError:
            self.t1 = ""
        except AttributeError:
            self.t1 = ""

    def destroyLabel(self, arr):
        for i in range(len(arr)):
            arr[i].destroy()

    #DEBUG
    def getGradesDebug(self):
        yield ["keke"],['100'],["90"]
        yield ["keke",'jopa'],['100','90'],["90",'80']
        yield ["keke",'xuy','jopa'],['100','30','90'],["90",'20','80']
        yield ["keke",'xuy','jopa','telefon'],['100','30','90','2.3'],["90",'20','80','44']
        yield ["keke",'xuy','jopa','robot','telefon'],['100','30','90','55','2.3'],["90",'20','80','99','44']
        while True:
            yield ["keke",'xuy','jopa','robot','telefon'],['100','30','90','55','2.3'],["90",'20','80','99','44']

    def monFunc(self):
        #messagebox.showinfo("kek", "lol")
        #try catch block or validation block
        kek = self.getGradesDebug()
        self.minutesVal = float(self.minutes.get())
        self.saveCourseNum = self.chosenCourse.get()
        self.firstTime = 1
        while True:
            self.lArr4 = []
            self.lArr5 = []
            self.lArr6 = []
            #DEBUG
            self.d,self.e,self.f = GetGradesClass.getData(self.login,self.passw, self.sem, self.saveCourseNum)
            #self.d,self.e,self.f = next(kek)
            if self.d != self.a or self.e != self.b or self.f != self.c or self.firstTime == 1:
                self.count = 0
                tempCompArr = self.getUpdatedIndexes(self.a, self.d)
                self.fillLabels(self.d,self.lArr4,tempCompArr)
                self.fillLabels(self.e,self.lArr5,tempCompArr)
                self.fillLabels(self.f,self.lArr6,tempCompArr)
                self.destroyLabel(self.lArr1)
                self.destroyLabel(self.lArr2)
                self.destroyLabel(self.lArr3)
                self.fillGridOfLabels(self.d,self.lArr4,0)
                self.fillGridOfLabels(self.e,self.lArr5,1)
                self.fillGridOfLabels(self.f,self.lArr6,2)
                self.master.update()
                self.a = self.d.copy()
                self.b = self.e.copy()
                self.c = self.f.copy()
                self.lArr1 = self.lArr4.copy()
                self.lArr2 = self.lArr5.copy()
                self.lArr3 = self.lArr6.copy()
                if self.firstTime == 0:
                    winsound.PlaySound('SystemQuestion',winsound.SND_ALIAS)
                    winsound.PlaySound('SystemQuestion',winsound.SND_ALIAS)
                self.firstTime = 0
            self.count += 1 
            if self.threadMessage == 0:
                break
            if self.count == 1:
                self.master.title("Get Grades(Alpha) - Hi " + self.login + " - Checked 1 time")
            else:
                self.master.title("Get Grades(Alpha) - Hi " + self.login + " - Checked " + str(self.count) + " times")
            time.sleep(60*self.minutesVal)
            

class LoginWin:
    def __init__(self, master):
        self.master = master
        self.tempDate = datetime.datetime.now()
        master.title("Get Grades(Alpha)")
        self.l1 = Label(master, text="Login")
        self.l2 = Label(master, text="Password")
        self.login = Entry(master, bd = 5)
        self.passw = Entry(master, bd = 5, show = "*")
        self.butt = Button(master, text="Login", command = lambda: self.tryToLogin(""))
        self.yearVal = StringVar(self.master)
        self.yearVal.set(self.tempDate.year)
        self.year = Spinbox(self.master,from_ = self.tempDate.year-2, to = 2055 ,textvariable = self.yearVal, width = 4)
        semNum = ['Winter','Spring', "Summer"]
        self.chosenSem = StringVar(self.master)
        self.chosenSem.set(semNum[0])
        self.semMenu = OptionMenu(self.master, self.chosenSem, *semNum)

        # LAYOUT
        self.l1.grid(column=0, row = 0, sticky=W)
        self.login.grid(column = 1, row = 0, sticky = W, columnspan = 2)
        self.l2.grid(column = 0, row = 1, sticky=W)
        self.passw.grid(column = 1, row = 1, sticky = W, columnspan = 2)
        self.year.grid(column = 2, row = 2, sticky = W)
        self.semMenu.grid(column = 1, row = 2, sticky = W)
        self.butt.grid(column = 1, row = 3)
        self.semMenu.config(width = 7)

    def getDateFormat(self,p1,p2):
        if p2 == "Spring":
            return str(int(p1)-1)+'02'
        elif p2 == "Summer":
            return str(int(p1)-1)+'03'
        else:
            return p1+'01'

    def tryToLogin(self, event):
        self.newGui = Tk()
        newkek = GetGrades(self.newGui,self.login.get(),self.passw.get(),self.getDateFormat(self.yearVal.get(),self.chosenSem.get()))
        self.master.destroy()
        self.newGui.mainloop()



#REMOVE WHEN FINISHED 
try:
    logs = open("logs", "r").read().split('\n')
except FileNotFoundError:
    top = Tk()
    m_gui = LoginWin(top)
    top.bind("<Return>",m_gui.tryToLogin)
    top.mainloop()
    exit()

top = Tk()
other = GetGrades(top,logs[0],logs[1],LoginWin.getDateFormat(None,'2018','Winter'))
top.mainloop()
