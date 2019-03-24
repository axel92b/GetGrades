import requests
import winsound
import time

#minutes = 0.1

# Fill in your details here to be posted to the login form.

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

def getInfo(p):
    arrNames = fillList(p,"<em>","</em>")
    newStr = (getSubStr("Your grade", "Average", p))[0]
    arrGrades = fillList(newStr,"<td class=\"grade\">","</td>")
    newStr = (getSubStr("Average", "" , p))[0]
    arrAvg = fillList(newStr,"<td class=\"grade\">","</td>")
    return arrNames,arrGrades, arrAvg

# Use 'with' to ensure the session context is closed after use.
def getData(log, passw):
    endOfTable = "Average of all students in this exercise."
    payload = {
        'Login': '1',
        'Course': '234218',
        'Page': 'grades.html',
        'SEM': '201801',
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
        #print("Error(Invalid login/pass or can't get proper response)")
        return ""
    tempStr = str(p.text)
    while True:
        firstIndex = tempStr.find("table bgcolor=\"#112244\"")
        secondIndex = tempStr.find(endOfTable)
        p = tempStr[firstIndex:secondIndex]
        tempStr = tempStr[secondIndex+len(endOfTable):]
        kek = getInfo(p)
        arrNames = arrNames + kek[0]
        arrGrades = arrGrades + kek[1]
        arrAvg = arrAvg + kek[2]
        if curLen == len(arrNames):
            break
        curLen = len(arrNames)
    return arrNames, arrGrades, arrAvg

#debug
# def printData2():
#     p = ""
#     with requests.Session() as s:
#         p = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload)
#         if "Your grade" not in p.text:
#             print("Error(Invalid login/pass or can't get proper response)")
#             return ""
#         firstIndex = str(p.text).find("table bgcolor=\"#112244\"")
#         secondIndex = str(p.text).find("Average of all students in this exercise.</td></tr>")
#         p = p.text[firstIndex:secondIndex]
#     arrNames = []
#     arrGrades = []
#     arrAvg = []
#     arrNames = fillList(p,"<em>","</em>")
#     newStr = (getSubStr("Your grade", "Average", p))[0]
#     arrGrades = fillList(newStr,"<td class=\"grade\">","</td>")
#     newStr = (getSubStr("Average", "" , p))[0]
#     arrAvg = fillList(newStr,"<td class=\"grade\">","</td>")
#     table = tt.Texttable()
#     arrAvg.append("kkek")
#     arrGrades.append("kkek")
#     arrNames.append("kkek")
#     arrOfWidth = [8]*len(arrAvg)
#     table.add_rows([arrNames,arrGrades,arrAvg])
#     table.set_cols_width(arrOfWidth)
#     return table.draw()

# def main():
#     counter = 1
#     firstStr = printData()
#     if firstStr == "":
#         return
#     print(firstStr)
#     print(f"Already checked {counter} time.\r", end="")
#     while True:
#         time.sleep(60*minutes)
#         newCheck = printData()
#         #debug
#         #newCheck = printData2()
#         if newCheck == firstStr:
#             counter += 1
#             print(f"Already checked {counter} times.\r", end="")
#             continue
#         print("\n")
#         counter = 1
#         firstStr = newCheck
#         print(firstStr)
#         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
#         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

# if __name__== "__main__":
#   main()
