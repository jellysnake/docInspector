# Formats entered dates into list
import json


def formatDateRange(dateRange):
    dateRangeList = []
    dateRangeList.append(dateRange[:10])
    dateRangeList.append(dateRange[11:])
    return dateRangeList


# Strips target line of unnecessary characters
def formatDate(line, finder):
    line = line.replace('"', '')
    line = line.replace(':', '', 1)
    line = line.replace(',', '')
    line = line.replace(finder, '')
    line = line.strip()
    line = line[:10]
    return line


# Checks if date already in dateList
def checkDate(dateList, line):
    if len(dateList) > 0:
        for i in range(len(dateList)):
            if line in dateList[i]:
                return False
        return True
    else:
        return True


# Checks whether date within specified range
def withinRange(dateRangeList, line):
    if line >= dateRangeList[0] and line <= dateRangeList[1]:
        return True
    else:
        return False


# checks data file for dates and adds to dateList
def findDate(dateRangeList, Sprintdoc, finder, dateList):
    for line in Sprintdoc:
        if finder in line:
            line = ''.join(line)
            line = formatDate(line, finder)
            if withinRange(dateRangeList, line) == True:
                if checkDate(dateList, line) == True:
                    dateList.append(line)


# Prints dates
def printdateList(dateList):
    print('\nDates of document edit between specified range are:\n')
    for i in range(len(dateList)):
        print(dateList[i])


def getDatesModifiedWithin(dates, data):
    # Opens data file
    # Sprintdoc = open('ProjectPlanData.txt')
    Sprintdoc = json.dumps(data, indent=4, separators=(',', ': ')).split('\n')
    # Global variables
    finder = 'modifiedTime'
    dateList = []

    # dateRange = input("Enter date range in format yyyy-mm-dd/yyyy-mm-dd:\n")
    dateRange = dates
    dateRangeList = formatDateRange(dateRange)
    findDate(dateRangeList, Sprintdoc, finder, dateList)

    printdateList(dateList)
