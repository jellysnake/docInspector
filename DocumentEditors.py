#Opens data file 
Sprintdoc = open('ProjectPlanData.txt')

#Global variables 
finder = 'lastModifyingUserName'
docNames =[]

#Strips target line of unnecessary characters 
def stripName(line, finder):
    line = line.replace('"', '')
    line = line.replace(':', '')
    line = line.replace(',', '')
    line = line.replace(finder, '')
    line = line.strip()
    return line

#Checks if user name already in docNames list
def checkDocNames (docNames, line):
    if len(docNames)>0:
        for i in range(len(docNames)):
            if line in docNames[i]:
                return False
        return True
    else:
        return True
    
#checks data file for user names and adds them to docNames list 
def findDocEditors(docNames):
    for line in Sprintdoc:
        if finder in line:
            line = ''.join(line)
            line = stripName(line, finder)
            if checkDocNames(docNames, line) == True:
                docNames.append(line)

#Prints user names 
def printDocNames(docNames):
    print('Users that have edited this document are:\n')
    for i in range(len(docNames)):
        print(docNames[i])
            



findDocEditors(docNames)

printDocNames(docNames)


            
            
            
            
    
     
