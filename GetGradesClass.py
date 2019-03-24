import requests
import winsound
import time

def getSubStr(p1, p2, src):
    if len(src) == 0:
        return "",""
    firstIndex = src.find(p1)
    if p2 == "":
        return  src[firstIndex:], src[firstIndex+len(p1)]
    newStr = src[firstIndex:]
    secondIndex = newStr.find(p2)
    return newStr[len(p1):secondIndex], newStr[secondIndex+len(p2):]

def fillList(src, p1, p2):
    tempList = []
    for i in range(len(src)):
        subStr, src = getSubStr(p1,p2,src)
        if src == "":
            continue
        tempList.append(subStr)
    return tempList

def fillCourseList(src, p1, p2):
    tempList = []
    for i in range(len(src)):
        subStr, src = getSubStr(p1,p2,src)
        if src == "":
            continue
        if subStr.isnumeric():
            tempList.append(subStr)
    return tempList

def getInfo(p):
    arrNames = fillList(p,"<em>","</em>")
    newStr = (getSubStr("Your grade", "Average", p))[0]
    arrGrades = fillList(newStr,"<td class=\"grade\">","</td>")
    newStr = (getSubStr("Average", "" , p))[0]
    arrAvg = fillList(newStr,"<td class=\"grade\">","</td>")
    return arrNames,arrGrades, arrAvg

def getData(log, passw, sem,course):
    endOfTable = "Average of all students in this exercise."
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
    p = ""
    arrNames = []
    arrGrades = []
    arrAvg = []
    curLen = 0
    with requests.Session() as s:
        p = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload)
    if "Your grade" not in p.text:
        return ""
    tempStr = str(p.text)
    while True:
        firstIndex = tempStr.find("table bgcolor=\"#112244\"")
        secondIndex = tempStr.find(endOfTable)
        p = tempStr[firstIndex:secondIndex]
        tempStr = tempStr[secondIndex+len(endOfTable):]
        temp = getInfo(p)
        arrNames = arrNames + temp[0]
        arrGrades = arrGrades + temp[1]
        arrAvg = arrAvg + temp[2]
        if curLen == len(arrNames):
            break
        curLen = len(arrNames)
    return arrNames, arrGrades, arrAvg

def getCourses(log, passw, sem):
    beginingOfTable = "semester."
    endOfTable = "Add the following"
    payload = {
        'Login': '1',
        'SEM': sem,
        'FromLock': '1',
        'ID': log,
        'Password': passw,
        'submit': 'proceed'
    }
    p = ""
    arrNames = []
    with requests.Session() as s:
        p = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload)
        tempStr = str(p.text)
        if "<span class=\"highlighttab\">Course List</span></td>" not in tempStr:
            p = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload)
        tempStr = str(p.text)
    firstIndex = tempStr.find(beginingOfTable)
    secondIndex = tempStr.find(endOfTable)
    p = tempStr[firstIndex:secondIndex]
    arrNames = fillCourseList(tempStr,"<span class=\"black-text\">","</span>")
    return arrNames
