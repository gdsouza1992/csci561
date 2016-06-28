import sys
import copy
#
#
# # #
masterGoalFlag = False
masterGoalFlagTemp = False
masterGoalSolution = list()
masterGoalSolutionTemp = list()

class Facts:
    def __init__(self,fact):
        # Get string befor the '('
        self.text = fact
        i = fact.find('(')
        self.predicate = fact[:i]
        self.parameters = fact[i+1:-1].split(',')


    # def __eq__(self, other):
    #     isEqual = True if self.predicate == other.predicate and self.parameters == other.parameters else False
    #     return isEqual



class Clauses:
    def __init__(self,clause):

        self.text = clause
        pos = clause.find('=>')

        # If Ground Clause
        if (pos == -1):
            self.premise = None
            self.conclusion = Facts(clause)
            self.type = "Ground"
        # If Implication
        else:
            # Add string from start to => to LHS
            self.premise = [Facts(premiseClause) for premiseClause in clause[:pos].split('&')]
            # Account for 2 characters in '=>' and add to RHS
            self.conclusion = Facts(clause[pos+2:])
            self.type = "Implication"



class KnowledgeBase:
    kbaseData = dict()
    goalQuery = None
    goals = list()

    def __init__(self, goal,fileoutput):
        if "&" in goal:
            fileoutput.write(str("Query:")+" "+ str(goal)+str("\n"))
            print str("Query:")+" "+ str(goal)+str("\n")

            for compoundGoal in goal.split("&"):
                self.goals.append(Facts(compoundGoal))
        else:
            self.goals.append(Facts(goal))


    def checkQuery(self):
        solutions = dict()
        tempFlag = True
        tempSolution = list()
        for query in self.goals:

            Inference().Search(self.kbaseData,query,query)
            global masterGoalFlag
            global masterGoalSolution
            tempFlag = tempFlag and masterGoalFlag
            tempSolution = Inference().findIntersection(tempSolution,masterGoalSolution)
            # tempSolution
            masterGoalFlag = tempFlag

        masterGoalFlagTemp = masterGoalFlag
        masterGoalSolutionTemp = masterGoalSolution
        return masterGoalFlagTemp,masterGoalSolutionTemp

    def insertNewQuery(self,logicStatement):
        # Create A Clause
        newClause = Clauses(logicStatement)
        newPredicate = newClause.conclusion.predicate
        self.kbaseData[newPredicate] = self.kbaseData[newPredicate] + [newClause] if newPredicate in self.kbaseData else [newClause]

class Inference:

    def __init__(self):

        self.varcounter = 0
        self.unifyCounter = 0
        self.rules = None
        self.unifications = list()
        self.merge = False
        self.levelUp = False
        self.skipUnify = False
        self.AndFail = False




    def isVariable(self,variable):
        if(isinstance(variable,str)):
            if(variable[0] == 'x'):
                return True
            else:
                return False

    def isList(self,variable):
        if(isinstance(variable,list)):
            return True
        else:
            return False



    def Search(self,kb,goal,parentGoal):

        # print "Query:",goal.text
        self.PrintResults(1, "Query:", goal.text, None)
        d = {goal.predicate:list()}



        self.unifications.append(d)
        targetQueries = self.getClausePredicates(kb,goal,parentGoal)
        for clause in targetQueries:
            self.AndFail = False


            checkPredicate = self.MatchConclusionParams(goal.parameters,clause.conclusion.parameters)
            if(checkPredicate):
                if goal.parameters == clause.conclusion.parameters and 'x' not in clause.conclusion.parameters:
                    self.unifications[self.unifyCounter][goal.predicate].append(True)
                    break

                # Ground Fact verification
                if clause.premise is None:
                    theta = self.UnifyGroundFact(goal,clause,parentGoal)
                    if theta is not None:
                        if theta not in self.unifications[self.unifyCounter][goal.predicate] or False not in self.unifications[self.unifyCounter][goal.predicate]:
                            if(self.merge) or self.levelUp:
                                if len(self.unifications[-1].values()[0]) > 1 and False in self.unifications[-1].values()[0]:
                                    self.unifications[-1].values()[0].remove(False)
                                self.unifications[self.unifyCounter][goal.predicate].append(theta)
                                self.merge = False
                            else:
                                self.unifications[self.unifyCounter][goal.predicate].insert(0,theta)


                #Implication Verification
                if clause.premise is not None:
                    #The AND step of the BC algorithm
                    self.PrintResults(1,"Query:",clause.text,None)

                    self.parentSolution = dict()

                    for eachPremise in clause.premise:
                        if self.AndFail:
                            self.unifications[self.unifyCounter][goal.predicate].append(False)
                        else:
                            self.levelUp = False
                            self.AndFail = False
                            eachPremise = self.UpdateParentGoal(eachPremise,goal,clause)
                            self.unifyCounter += 1
                            self.Search(kb, eachPremise, goal)



        printed = False
        if len(self.unifications)>0:
            if len(self.unifications[-1].values()[0]) > 0:
                if self.unifications[-1].values()[0][0] == True:
                    printed = True
                    # goal.text,": True"
                    self.PrintResults(5,goal.text,": True",None)
                    self.setMasterGoal(True)

        if len(self.unifications) > 0 and not printed:
            if len(self.unifications[-1].values()[0]) == 0 or False in self.unifications[-1].values()[0]:

                self.PrintResults(4, goal.text, ": False",None)
                self.setMasterGoal(False)
                # print goal.text,": False"
                self.AndFail = True
            else:
                self.PrintResults(3, goal.text, ": True:",self.unifications[-1].values()[0])
                self.setMasterGoal(True)
                # print goal.text,": True:",self.unifications[-1].values()[0]
        else:
            if not printed:
                self.PrintResults(4, goal.text, ": False",None)
                self.setMasterGoal(False)
                # print goal.text,": False"


        #Merge with parent based on common values
        if not self.skipUnify:
            parentKey = self.unifications[self.unifyCounter - 1].keys()[0]
            parentList = copy.deepcopy(self.unifications[self.unifyCounter - 1][parentKey])
            childList = copy.deepcopy(self.unifications[self.unifyCounter][goal.predicate])
            self.unifications[self.unifyCounter - 1][parentKey] = self.findIntersection(parentList,childList)
            global masterGoalSolution
            masterGoalSolution = self.unifications[self.unifyCounter - 1][parentKey]
            self.unifyCounter -= 1
            self.unifications.pop(-1)
            self.levelUp = True

    def UpdateParentGoal(self,eachPremise,goal,clause):
        eachPremise.parameters[eachPremise.parameters.index('x')] = goal.parameters[clause.conclusion.parameters.index('x')]
        return eachPremise


    def UnifyGroundFact(self,goal,clause,parentGoal):


        goalParamsTemp = copy.deepcopy(goal.parameters)
        clauseParamsTemp = copy.deepcopy(clause.conclusion.parameters)


        # varIndex = goalParamsTemp.index("x")

        if 'x' in goalParamsTemp:
            varIndex = goalParamsTemp.index("x")
            variable = goalParamsTemp.pop(varIndex)
            value = clauseParamsTemp.pop(varIndex)
            # Check that all other parameters are matches
            if len(list(set(goalParamsTemp)-set(clauseParamsTemp))) == 0:
                d = value

                return d


        else:
            return None


    def getClausePredicates(self, kb, goal, parentGoal):
        if 'x' in goal.parameters:
            return kb[goal.predicate]
        else:

            checkList = list()
            for eachClause in kb[goal.predicate]:
                if eachClause.type == "Ground":
                    if goal.parameters == eachClause.conclusion.parameters:
                        checkList.append(eachClause)

            if len(checkList) > 0:
                return checkList

            for eachClause in kb[goal.predicate]:
                checkList.append(eachClause)

            return checkList


    def setMasterGoal(self,flag):
        global masterGoalFlag
        masterGoalFlag = flag

    def MatchConclusionParams(self,goalRHS,clauseRHS):
        goalParamLength = len(goalRHS)
        clauseParamLength = len(clauseRHS)
        if goalParamLength != clauseParamLength:
            return False

        flag = False
        for i in range(goalParamLength):
            # If both 'x'
            if goalRHS[i] == clauseRHS[i] and goalRHS[i] == 'x' and clauseRHS[i] == 'x':
                flag = True
                continue

            # If goal is  'x' and other is Constant
            if goalRHS[i] == 'x' and clauseRHS[i] != 'x':
                flag = True
                continue

            # If goal is not 'x' and other is 'x'
            if goalRHS[i] != 'x' and clauseRHS[i] == 'x':
                flag = True
                continue

            # If goal is constant and other is same constant
            if goalRHS[i] == clauseRHS[i] and goalRHS != 'x':
                flag = True
                continue

            if goalRHS[i] != clauseRHS[i] and goalRHS[i] != 'x' and clauseRHS[i] != 'x':
                flag = False
                return flag

        return flag


    def findIntersection(self,parentList,childList):
        if len(parentList) == 0:
            return childList
        else:
            returnList = list(set(parentList).intersection(childList))
            if(len(returnList)>0):
                self.merge = True

            return returnList


    def PrintResults(self,num,part1,part2,part3):
        if num == 1 or num == 2:
            fileoutput.write(str(part1)+" "+ str(part2)+str("\n"))
            print str(part1) + str(part2)
        elif num == 3:
            fileoutput.write(str(part1)+str(part2)+" "+str(part3)+str("\n"))
            print (str(part1)+str(part2)+" "+str(part3))
        elif num == 4:
            fileoutput.write(str(part1) + str(part2) + str("\n"))
            print str(part1)+str(part2)
        elif num == 5:
            fileoutput.write(str(part1) + str(part2) + str("\n"))
            print str(part1) + str(part2)








    def printLine(type,value):
        print type,":",value.values()[0]


if __name__ == '__main__':
    fileLines = None
    with open(sys.argv[1], 'r') as f:
        fileLines = f.read().splitlines()

    # Separate the Query and Number of lines and the Logic Statements
    goalQuery = str(fileLines[0])
    logicCount = int(fileLines[1])
    statements = fileLines[2:]



    fileoutput = open("output.txt", "w")
    knowledgeBase = KnowledgeBase(goalQuery,fileoutput)

    for logicStatement in statements:
        knowledgeBase.insertNewQuery(logicStatement)


    solution = knowledgeBase.checkQuery()
    if "&" in goalQuery:

        if solution[0]:
            fileoutput.write(str(goalQuery) + str(": True:") + " " + str(solution[1]) + str("\n"))
            print str(goalQuery) + str(": True:") + " " + str(solution[1]) + str("\n")
        else:
            fileoutput.write(str(goalQuery) + str(": False")+ str("\n"))
            print str(goalQuery) + str(": False")+ str("\n")
        # self.PrintResults(3, goal.text, ": True:", self.unifications[-1].values()[0])
    # HasTravelled(x, Congo) & Diagnosis(x, Cough):True: ['John']
    fileoutput.close()



