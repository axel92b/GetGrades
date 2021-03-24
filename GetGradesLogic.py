import requests
from lxml import html


def getData(log, passw, sem, course):
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
    arrNames = [""]
    arrGrades = ["Your grade"]
    arrAvg = ["Average"]

    # send and receive html with data
    with requests.Session() as s:
        data = s.post('https://grades.cs.technion.ac.il/grades.cgi', data=payload)
    if "Your grade" not in data.text:
        return [], [], []
    tempStr = str(data.text)
    tree = html.fromstring(tempStr)

    try:
        arrNames.extend(tree.xpath('//div[@class="text-content"]//th/em/text()'))

        for table in tree.xpath('//div[@class="text-content"]/table'):
            grades = table.xpath('.//tr/td[@class="grade"]/text()')
            mid = int(len(grades)/2)
            arrGrades.extend(grades[0:mid])
            arrAvg.extend(grades[mid:])
    except:
        return [], [], []

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
    arrNumbers = []
    arrNames = []

    try:
        tree = html.fromstring(tempStr)
        results: list = tree.xpath('//span[@class="black-text"]/text()')
        results.pop(len(results) - 1)

        for index, value in enumerate(results):
            if index % 2 == 0:
                arrNumbers.append(value)
            else:
                arrNames.append(value)
    except:
        return [], []

    return arrNumbers, arrNames
