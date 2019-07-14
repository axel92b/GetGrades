import requests
import winsound
import time

def getSubStr(src, p1, p2):
    """ Returns string that between first appearance of p1 and first appearance of p2 
        and new string starting after first appearance p2.
        
        Parameters: 
            src(str): Source string
            p1(str):  Starting string.
            p2(str):  Ending string.
        Returns:
            res(str): Cut string.
            rem(str): Remainder string.
    """
    if len(src) == 0:
        return "",""
    firstIndex = src.find(p1)
    if p2 == "":
        return  src[firstIndex:], src[firstIndex+len(p1)]
    newStr = src[firstIndex:]
    secondIndex = newStr.find(p2)
    return newStr[len(p1):secondIndex], newStr[secondIndex+len(p2):]

def fillListWithNames(src, p1, p2):
    """ Returns list that contains strings that exactly between p1 and p2 in src string.
        (used for getting course names and numbers)
        Parameters: 
            src(str): Source string
            p1(str):  Starting string.
            p2(str):  Ending string.
        Returns:
            list(str list): List with all strings that between p1 and p2 in src string(numeric).
            list(str list): List with all strings that between p1 and p2 in src string(non numeric).
    """
    tempNumbers = []
    tempNames = []
    while True:
        subStr, src = getSubStr(src,p1,p2)
        if subStr != "" and subStr.isnumeric():
            tempNumbers.append(subStr)
        if subStr != "" and not subStr.isnumeric():
            tempNames.append(subStr)
        if src == "":
            break
    return tempNumbers,tempNames

def fillList(src, p1, p2):
    """ Returns list that contains strings that exactly between p1 and p2 
        in src string(only numeric strings or "-" string).
        
        Parameters: 
            src(str): Source string
            p1(str):  Starting string.
            p2(str):  Ending string.
        Returns:
            list(str list): List with all strings that between p1 and p2 in src string.
    """
    temp = []
    while True:
        subStr, src = getSubStr(src,p1,p2)
        if subStr != "":
            temp.append(subStr)
        if src == "":
            break
    return temp

def getInfo(src):
    """ Cut source string and extracts all data then returns 3 arrays of strings, 
        first contains names, second grades, third avarages.
        
        Parameters: 
            src(str): Source string
        Returns:
            arrNames(str list):     Array of names.
            arrGrades(str list):    Array of grades.
            arrAvg(str list):       Array of averages.
    """
    arrNames = fillList(src,"<em>","</em>")
    newStr = (getSubStr(src, "Your grade", "Average"))[0]
    arrGrades = fillList(newStr,"<td class=\"grade\">","</td>")
    newStr = (getSubStr(src, "Average", "" ))[0]
    arrAvg = fillList(newStr,"<td class=\"grade\">","</td>")
    return arrNames,arrGrades, arrAvg

def getData(log, passw, sem,course):
    """ Main function, login and parse names of courses, grades, averages.
        Returns 3 arrays with names,grades and averages.
        
        Parameters: 
            log(str): Login string
            passw(str): Password string
            sem(str): Semester number string
            course(str): Course number string
        Returns:
            arrNames(str list):     Array of names.
            arrGrades(str list):    Array of grades.
            arrAvg(str list):       Array of averages.
    """
    beginingOfTable = "table bgcolor=\"#112244\""
    endOfTable = "Average of all students in this exercise."
    # package for post request
    payload = {
        'Login': '1',
        'Course': course,
        'Page': 'grades.html',
        'SEM': sem,
        'FromLock': '1',
        'ID': log,
        'Password': passw,
        'submit': 'proceed'
    }
    arrNames = []
    arrGrades = []
    arrAvg = []
    curLen = 0
    # send and receive html with data
    with requests.Session() as s:
        data = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload)
    if "Your grade" not in data.text:
        return [],[],[]
    tempStr = str(data.text)
    # extract data from html
    while True:
        firstIndex = tempStr.find(beginingOfTable)
        secondIndex = tempStr.find(endOfTable)
        data = tempStr[firstIndex+len(beginingOfTable):secondIndex]
        tempStr = tempStr[secondIndex+len(endOfTable):]
        temp = getInfo(data)
        if arrNames == temp[0]:
            break
        arrNames = arrNames + temp[0]
        arrGrades = arrGrades + temp[1]
        arrAvg = arrAvg + temp[2]
        if curLen == len(arrNames):
            break
        curLen = len(arrNames)
    return arrNames, arrGrades, arrAvg

def getCourses(log, passw, sem):
    """ Extracts list of courses in specified semester. Returns list of course numbers.
        
        Parameters: 
            log(str): Login string
            passw(str): Password string
            sem(str): Semester number string
        Returns:
            arrNames(str list):     Array of names.
    """
    beginingOfTable = "semester."
    endOfTable = "Add the following"
    # some site specific code(not so easy to get to list of courses)
    # package for post request
    payload = {
        'Login': '1',
        'SEM': sem,
        'FromLock': '1',
        'ID': log,
        'Password': passw,
        'submit': 'proceed'
    }
    # dummy package for post request
    payload2 = {
        'Login': '1',
        'Course': '111111',
        'SEM': sem,
        'FromLock': '1',
        'ID': log,
        'Password': passw,
        'submit': 'proceed'
    }
    with requests.Session() as s:
        # first we'll send dummy request
        data = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload2)
        # then we send normal package and get list of courses
        data = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload)
        tempStr = str(data.text)
        if "<span class=\"highlighttab\">Course List</span></td>" not in tempStr:
            data = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload)
        tempStr = str(data.text)
    # extract list from html
    firstIndex = tempStr.find(beginingOfTable)
    secondIndex = tempStr.find(endOfTable)
    data = tempStr[firstIndex:secondIndex]
    arrNumbers,arrNames = fillListWithNames(data,"<span class=\"black-text\">","</span>")
    return arrNumbers, arrNames
