from tkinter import *
from tkinter import messagebox
import GetGradesClass
import time
import threading
import winsound
import datetime

class GetGrades:
    def __init__(self, master , login, passw, sem, courseNums, courseNames):
        """ Draw second window with grades and monitors site for changes.
        
        Parameters: 
            master: Tkinter parent window.
            login(str): Login string.
            passw(str): Password string.
            sem(str): Semester string.
            courseNums(str list): List of courses in provided semester.
            courseNames(str list): List of course names.
        Returns:
            Nothing.
        """
        self.master = master
        self.sem = sem
        self.login = login
        self.passw = passw
        self.courseNums = courseNums
        self.courseNames = courseNames
        self.statusBarText = StringVar(self.master)
        self.statusBarCountText = StringVar(self.master)
        self.statusBarText.set("Ready")
        self.mainFrame = Frame(self.master)
        self.courseLabel = Label(self.mainFrame, text= "Course")
        self.durationLabel = Label(self.mainFrame, text= "Duration")
        master.title("Get Grades(Alpha) - Hi " + self.login + ".")
        self.names = []
        self.grades = []
        self.avgs = []
        self.chosenCourse = StringVar(self.mainFrame)
        self.chosenCourse.set(courseNums[0])
        self.courseMenu = OptionMenu(self.mainFrame, self.chosenCourse, *courseNums)
        self.courseMenu.config(width = 13)
        self.minutes = Entry(self.mainFrame, width = 19,justify = RIGHT)
        self.layoutArr1 = []
        self.layoutArr2 = []
        self.layoutArr3 = []
        self.statusBar = Label(self.master, textvariable = self.statusBarText, bd=1, relief=SUNKEN, anchor=W)
        self.statusBarCount = Label(self.master, textvariable = self.statusBarCountText, bd=1, relief=SUNKEN, anchor=W)

        # BUTTONS
        self.updButt = Button(self.mainFrame, text = "Monitor!", command = self.updateFunc)

        # LAYOUT
        self.courseLabel.grid(column = 0, row = 0,sticky = W)
        self.durationLabel.grid(column = 0, row = 1,sticky = W)
        self.courseMenu.grid(column = 1, row = 0)
        self.minutes.grid(column = 1, row = 1)
        self.updButt.grid(column = 1, row = 2)
        self.mainFrame.pack(side=TOP,fill=X)
        self.statusBar.pack(side=LEFT)
        self.statusBarCount.pack(side=LEFT, fill=X, expand=1)

    def getUpdatedIndexes(self,orig,newArr):
        """ Compare 2 arrays to find indexes for new items in newArr.
        
        Parameters: 
            orig(str list): List of original(old) items.
            newArr(str list): List of new items.
        Returns:
            indexes(int list): list of idexes of new items.
        """
        indexes = []
        for i in range(len(newArr)):
            if newArr[i] not in orig:
                indexes.append(i)
        return indexes

    def fillLabels(self, arr, targArr, newIndexes = None):
        """ Fills arrays with new labels, if there new label will print it green.
        
        Parameters: 
            arr(str list): List of strings.
            targArr(Label list): List of labels(usually empty).
            newIndexes(int list): List of new indexes that we need to print green.
        Returns:
            Fills list and doesn't return anything.
        """
        for i in range(len(arr)):
            if newIndexes != None and i in newIndexes and not self.firstTime:
                targArr.append(Label(self.mainFrame, text=arr[i], fg="green"))
                continue
            targArr.append(Label(self.mainFrame, text=arr[i]))

    def fillGridOfLabels(self,targArr,r):
        """ Fills grid layout for grades on specified row.
        
        Parameters: 
            targArr(Label list): List of labels.
            r(int): Row for which we are filling.
        Returns:
            Fills list and doesn't return anything.
        """
        for i in range(2,len(targArr)+2):
            targArr[i-2].grid(column = i, row = r)

    def updateFunc(self, event = ""):
        """ Creates new thread for monitoring.

            Parameters: 
                event: Empty but needed to bind this method to keyboard key.
            Returns:
                Nothing.
        """
        try:
            self.minutesVal = float(self.minutes.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid duration")
            return
        self.killThread()
        self.threadCanRun = 1
        self.t1 = threading.Thread(target=self.monFunc, args=[]).start()

    def killThread(self, destroy=0):
        """ Kills thread(sends message to thread that he isn't permitted to run anymore).

            Parameters: 
                destroy(int): When set to 1 means that we are closing app and need simply 
                              to destroy thread before exit.
            Returns:
                Nothing.
        """
        if destroy == 1:
            self.master.destroy()
        try:
            if self.t1.isAlive():
                self.threadCanRun = 0
                self.t1.join()
        except:
            self.t1 = ""

    def destroyLabel(self, arr):
        """ Destroy old labels before creating new ones.

            Parameters: 
                arr(Labels list): List of labels that we want to destroy.
            Returns:
                Nothing.
        """
        for i in range(len(arr)):
            arr[i].destroy()

    #DEBUG
    def getGradesDebug(self):
        yield ["HW 1"],['100'],["90"]
        yield ["HW 1",'HW 3'],['100','90'],["90",'80']
        yield ["HW 1",'HW 2','HW 3'],['100','30','90'],["90",'20','80']
        yield ["HW 1",'HW 2','HW 3','HW 5'],['100','30','90','2.3'],["90",'20','80','44']
        yield ["HW 1",'HW 2','HW 3','HW 4','HW 5'],['100','30','90','55','2.3'],["90",'20','80','99','44']
        while True:
            yield ["HW 1",'HW 2','HW 3','HW 4','HW 5'],['100','30','90','55','2.3'],["90",'20','80','99','44']

    def monFunc(self):
        """ Monitor function, checks site for new grades and if there new grades, updates UI.

            Parameters: 
                Only "self".
            Returns:
                Nothing.
        """
        # debugGen = self.getGradesDebug()
        self.saveCourseNum = self.chosenCourse.get()
        self.firstTime = 1
        self.statusBarText.set(self.courseNames[self.courseNums.index(self.saveCourseNum)])
        self.count = 0
        while True:
            self.layoutArr4 = []
            self.layoutArr5 = []
            self.layoutArr6 = []
            self.newNames,self.newGrades,self.newAvgs = GetGradesClass.getData(self.login,self.passw, self.sem, self.saveCourseNum)
            #DEBUG
            # self.newNames,self.newGrades,self.newAvgs = next(debugGen)
            # if found new grades, then update.
            if self.newNames != self.names or self.firstTime == 1:
                tempCompArr = self.getUpdatedIndexes(self.names, self.newNames)
                self.fillLabels(self.newNames,self.layoutArr4,tempCompArr)
                self.fillLabels(self.newGrades,self.layoutArr5,tempCompArr)
                self.fillLabels(self.newAvgs,self.layoutArr6,tempCompArr)
                self.destroyLabel(self.layoutArr1)
                self.destroyLabel(self.layoutArr2)
                self.destroyLabel(self.layoutArr3)
                self.fillGridOfLabels(self.layoutArr4,0)
                self.fillGridOfLabels(self.layoutArr5,1)
                self.fillGridOfLabels(self.layoutArr6,2)
                self.master.update()
                self.names = self.newNames.copy()
                self.grades = self.newGrades.copy()
                self.avgs = self.newAvgs.copy()
                self.layoutArr1 = self.layoutArr4.copy()
                self.layoutArr2 = self.layoutArr5.copy()
                self.layoutArr3 = self.layoutArr6.copy()
                if self.firstTime == 0:
                    winsound.PlaySound('SystemQuestion',winsound.SND_ALIAS)
                    winsound.PlaySound('SystemQuestion',winsound.SND_ALIAS)
                self.firstTime = 0
            self.count += 1 
            if self.count == 1:
                self.statusBarCountText.set("Checked 1 time")
            else:
                self.statusBarCountText.set("Checked " + str(self.count) + " times")
            tempTime = 0
            while (tempTime < 60*self.minutesVal):
                if self.threadCanRun == 0:
                    return
                time.sleep(1)
                tempTime += 1

            
class LoginWin:
    def __init__(self, master):
        """ Draw first login window.
        
        Parameters: 
            master: Tkinter parent window.
        Returns:
            Nothing.
        """
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
        """ Convert userprovided date to gr++ format.
        
        Parameters: 
            p1(str): Year.
            p2(str): Month.
        Returns:
            String represents user desired semester in gr++ format.
        """
        if p2 == "Spring":
            return str(int(p1)-1)+'02'
        elif p2 == "Summer":
            return str(int(p1)-1)+'03'
        else:
            return p1+'01'

    def tryToLogin(self, event = ""):
        """ Tries to login with userprovided login and password, incase of success 
            creates second window.

        Parameters: 
            Only "self".
        Returns:
            Noting.
        """
        self.newGui = Tk()
        self.sem = self.getDateFormat(self.yearVal.get(),self.chosenSem.get())
        courseNums,courseNames = GetGradesClass.getCourses(self.login.get(),self.passw.get(), self.sem)
        if len(courseNums) == 0:
            messagebox.showerror("Error", "Invalid login/password or you don't have any courses in semester: "+str(self.chosenSem.get())+" "+str(self.yearVal.get()))
            return
        monGUI = GetGrades(self.newGui,self.login.get(),self.passw.get(),self.sem, courseNums, courseNames)
        self.newGui.bind("<Return>",monGUI.updateFunc)
        self.newGui.protocol("WM_DELETE_WINDOW", lambda: monGUI.killThread(1))
        self.master.destroy()
        self.newGui.mainloop()

def main():
    #REMOVE WHEN FINISHED 
    try:
        logs = open("logs3", "r").read().split('\n')
    except FileNotFoundError:
        top = Tk()
        m_gui = LoginWin(top)
        top.bind("<Return>",m_gui.tryToLogin)
        top.mainloop()
        return

    top = Tk()
    temp1,temp2 = GetGradesClass.getCourses(logs[0],logs[1], '201801')
    other = GetGrades(top,logs[0],logs[1],LoginWin.getDateFormat(None,'2018','Winter'),temp1,temp2)
    top.bind("<Return>",other.updateFunc)
    top.protocol("WM_DELETE_WINDOW", lambda: other.killThread(1))
    top.mainloop()


if __name__== "__main__":
    main()