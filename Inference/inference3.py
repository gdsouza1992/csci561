import sys
import copy
#
#
# # #
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

    def __init__(self, goal):
        self.goalQuery = Facts(goal)

    def checkQuery(self):
        solutions = dict()
        return Inference().Search(self.kbaseData,self.goalQuery,self.goalQuery)

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

        print "Query:",goal.text
        d = {goal.predicate:list()}



        self.unifications.append(d)
        targetQueries = self.getClausePredicates(kb,goal,parentGoal)
        for clause in targetQueries:



            checkPredicate = self.MatchConclusionParams(goal.parameters,clause.conclusion.parameters)
            if(checkPredicate):
                if goal.parameters == clause.conclusion.parameters and 'x' not in clause.conclusion.parameters:
                    self.unifications[self.unifyCounter][goal.predicate].append(True)
                    break

                # Ground Fact verification
                if clause.premise is None:
                    theta = self.UnifyGroundFact(goal,clause,parentGoal)
                    if theta is not None:
                        if theta not in self.unifications[self.unifyCounter][goal.predicate]:
                            if(self.merge) or self.levelUp:
                                self.unifications[self.unifyCounter][goal.predicate].append(theta)
                                self.merge = False
                            else:
                                self.unifications[self.unifyCounter][goal.predicate].insert(0,theta)


                #Implication Verification
                if clause.premise is not None:
                    #The AND step of the BC algorithm
                    print "Query:",clause.text

                    self.parentSolution = dict()

                    for eachPremise in clause.premise:
                        self.levelUp = False
                        eachPremise = self.UpdateParentGoal(eachPremise,goal,clause)
                        self.unifyCounter += 1
                        self.Search(kb, eachPremise, goal)


        printed = False
        if len(self.unifications)>0:
            if len(self.unifications[-1].values()[0]) > 0:
                if self.unifications[-1].values()[0][0] == True:
                    printed = True
                    print goal.text,": True"

        if len(self.unifications) > 0 and not printed:
            if len(self.unifications[-1].values()[0]) == 0:
                print goal.text,": False"
            else:
                print goal.text,": True:",self.unifications[-1].values()[0]
        else:
            if not printed:
                print goal.text,": False"


        #Merge with parent based on common values
        if not self.skipUnify:
            parentKey = self.unifications[self.unifyCounter - 1].keys()[0]
            parentList = copy.deepcopy(self.unifications[self.unifyCounter - 1][parentKey])
            childList = copy.deepcopy(self.unifications[self.unifyCounter][goal.predicate])
            self.unifications[self.unifyCounter - 1][parentKey] = self.findIntersection(parentList,childList)
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


    def PrintResults(self,goal,flag,values,level):
        if flag:
            print goal.text, ": True:",values,"Level ",level
        else:
            print goal.text, ": False","Level",level









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

    knowledgeBase = KnowledgeBase(goalQuery)
    for logicStatement in statements:
        knowledgeBase.insertNewQuery(logicStatement)

    sol = knowledgeBase.checkQuery()




