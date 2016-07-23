import sys
import copy
import math


class Table:

    def __init__(self,tableString,tableData):
        self.data = dict()
        self.parentCount = int(math.log(len(tableData),2))
        self.parent = None
        if(self.parentCount > 0):
            parentsNames = tableString.split(" | ")[1]
            self.parent = parentsNames.split(" ")



        self.text = tableString
        for row in tableData:
            i = row.find(" ")
            if(i is not -1):
                self.data[str(row[:i])] = str(row[i:]).strip()
            else:
                self.data[row] = "+"


class EventObject:

    def __init__(self,queryString):
        i = queryString.find('=')
        self.EventName = queryString[:i].strip()
        self.EventOccur = queryString[i+1:].strip()


class QueryObject:
    def __init__(self, LHS, RHS):
        self.happens = LHS
        self.given = RHS
        if(len(RHS) == 0):
            self.probType = "Joint"
        else:
            self.probType = "Conditional"
        self.solution = 0.00

class Bayes:
    bayesData = dict()
    bayesQuery = dict()
    # bayesQuery = dict()
    queries = list()

    def AddQueries(self,fileLines,queryCount):
        for query in range(1, queryCount + 1):  # Python indexes start at zero
            self.queries.append(fileLines[query])

    def MakeTables(self,dataLines,queryCount):
        probabilityData = copy.deepcopy(dataLines[queryCount + 1:])
        # Add '***' for generalized table delimeter and prepend to tables list
        probabilityData.append('***')

        tables = dict()
        text = ''
        key = ''
        data = list()
        for lines in probabilityData:
            if lines == '***':
                key = text.split("|")[0]
                self.bayesData[key] = Table(text,copy.deepcopy(data))
                # Empty data list
                text = ''
                data = []

            elif(lines[0].isupper() or lines[0].islower()):
                text = lines
            else:
                data.append(lines)



    def SolveQuery(self):


        count = 0
        for query in self.queries:
            rhs = list()
            lhs = list()
            query = query[query.find('(')+1:query.find(')')]


            if("|" in query):
                conditionsCount = query.count('|')
                conditionalList = query.split('|')
                lhs.append(EventObject(conditionalList[0]))
                splitData = conditionalList[1].split(',')
                for splitPart in splitData:
                    rhs.append(EventObject(splitPart))
                self.bayesQuery[count] = QueryObject(lhs, rhs)

            else:
                rhs = []
                splitData = query.split(',')
                for splitPart in splitData:
                    lhs.append(EventObject(splitPart))
                self.bayesQuery[count] = QueryObject(lhs,rhs)



            count += 1
        print "Gareth"

    def splitEventProblem(self,eventString):
        returnDict = {eventString.split('=')[0].strip():eventString.split('=')[1].strip()}
        return copy.deepcopy(returnDict)






if __name__ == '__main__':
    fileLines = None
    with open(sys.argv[1], 'r') as f:
        fileLines = f.read().splitlines()


    queryCount = int(fileLines[0])

    _bayes = Bayes()
    _bayes.AddQueries(fileLines,queryCount)
    _bayes.MakeTables(fileLines,queryCount)
    _bayes.SolveQuery()











