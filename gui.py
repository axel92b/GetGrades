from tkinter import *
from tkinter import messagebox
import GetGradesClass
import time
import threading
import winsound
import datetime

class GetGrades:
    def __init__(self, master , login, passw, sem, courseNums):
        self.master = master
        self.sem = sem
        self.login = login
        self.passw = passw
        self.courseNums = courseNums
        self.count = 0
        self.threadMessage = 1
        self.courseLabel = Label(self.master, text= "Course")
        self.durationLabel = Label(self.master, text= "Duration")
        master.title("Get Grades(Alpha) - Hi " + self.login)
        self.a = []
        self.b = []
        self.c = []
        self.chosenCourse = StringVar(self.master)
        self.chosenCourse.set(courseNums[0])
        self.courseMenu = OptionMenu(self.master, self.chosenCourse, *courseNums)
        self.courseMenu.config(width = 13)
        self.minutes = Entry(self.master, width = 19,justify = RIGHT)
        self.lArr1 = []
        self.lArr2 = []
        self.lArr3 = []

        # BUTTONS
        self.updButt = Button(self.master, text = "Monitor!", command = self.updateFunc)

        # LAYOUT
        self.courseLabel.grid(column = 0, row = 0,sticky = W)
        self.durationLabel.grid(column = 0, row = 1,sticky = W)
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

    def updateFunc(self, event = ""):
        try:
            self.minutesVal = float(self.minutes.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid duration")
            return
        self.killThread()
        self.threadMessage = 1
        self.t1 = threading.Thread(target=self.monFunc, args=[])
        self.t1.start()

    def killThread(self, destroy=0):
        if destroy == 1:
            self.master.destroy()
        try:
            if self.t1.isAlive():
                self.threadMessage = 0
                self.t1.join()
        except:
            self.t1 = ""

    def destroyLabel(self, arr):
        for i in range(len(arr)):
            arr[i].destroy()

    #DEBUG
    def getGradesDebug(self):
        yield ["course 1"],['100'],["90"]
        yield ["course 1",'course 3'],['100','90'],["90",'80']
        yield ["course 1",'course 2','course 3'],['100','30','90'],["90",'20','80']
        yield ["course 1",'course 2','course 3','course 5'],['100','30','90','2.3'],["90",'20','80','44']
        yield ["course 1",'course 2','course 3','course 4','course 5'],['100','30','90','55','2.3'],["90",'20','80','99','44']
        while True:
            yield ["course 1",'course 2','course 3','course 4','course 5'],['100','30','90','55','2.3'],["90",'20','80','99','44']

    def monFunc(self):
        # debugGen = self.getGradesDebug()
        self.saveCourseNum = self.chosenCourse.get()
        self.firstTime = 1
        while True:
            self.lArr4 = []
            self.lArr5 = []
            self.lArr6 = []
            self.d,self.e,self.f = GetGradesClass.getData(self.login,self.passw, self.sem, self.saveCourseNum)
            #DEBUG
            #self.d,self.e,self.f = next(debugGen)
            if self.d != self.a or self.firstTime == 1:
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
            if self.count == 1:
                self.master.title("Get Grades(Alpha) - Hi " + self.login + " - Checked 1 time")
            else:
                self.master.title("Get Grades(Alpha) - Hi " + self.login + " - Checked " + str(self.count) + " times")
            tempTime = 0
            while (tempTime < 60*self.minutesVal):
                if self.threadMessage == 0:
                    return
                time.sleep(5)
                tempTime += 5

            
class LoginWin:
    def __init__(self, master):
        self.master = master
        self.tempDate = datetime.datetime.now()
        master.title("Get Grades(Alpha)")
        self.l1 = Label(master, text="Login")
        self.l2 = Label(master, text="Password")
        self.login = Entry(master, bd = 5)
        self.passw = Entry(master, bd = 5, show = "*")
        self.butt = Button(master, text="Login", command = self.tryToLogin)
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

    def tryToLogin(self, event = ""):
        self.newGui = Tk()
        self.sem = self.getDateFormat(self.yearVal.get(),self.chosenSem.get())
        courseNums = GetGradesClass.getCourses(self.login.get(),self.passw.get(), self.sem)
        if len(courseNums) == 0:
            messagebox.showerror("Error", "Invalid login/password or you don't have any courses in semester: "+str(self.chosenSem.get())+" "+str(self.yearVal.get()))
            return
        monGUI = GetGrades(self.newGui,self.login.get(),self.passw.get(),self.sem, courseNums)
        self.master.destroy()
        self.newGui.bind("<Return>",monGUI.updateFunc)
        self.newGui.protocol("WM_DELETE_WINDOW", lambda: monGUI.killThread(1))
        self.newGui.mainloop()

def main():
    #REMOVE WHEN FINISHED 
    try:
        logs = open("logs", "r").read().split('\n')
    except FileNotFoundError:
        top = Tk()
        m_gui = LoginWin(top)
        top.bind("<Return>",m_gui.tryToLogin)
        top.mainloop()
        return

    top = Tk()
    other = GetGrades(top,logs[0],logs[1],LoginWin.getDateFormat(None,'2018','Winter'),GetGradesClass.getCourses(logs[0],logs[1], '201801'))
    top.bind("<Return>",other.updateFunc)
    top.protocol("WM_DELETE_WINDOW", lambda: other.killThread(1))
    top.mainloop()


if __name__== "__main__":
    main()