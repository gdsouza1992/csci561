import sys
import copy
#
#
# # #
class Facts:
    def __init__(self,fact):
        # Get string befor the '('
        i = fact.find('(')
        self.predicate = fact[:i]
        self.parameters = fact[i+1:-1].split(',')
        self.subGoals = list()

    def __eq__(self, other):
        isEqual = True if self.predicate == other.predicate and self.parameters == other.parameters else False
        return isEqual
class Clauses:
    def __init__(self,clause):

        self.ClauseStr = clause
        pos = clause.find('=>')

        # If Ground Clause
        if (pos == -1):
            self.premise = None
            self.conclusion = Facts(clause)
        # If Implication
        else:
            # Add string from start to => to LHS
            self.premise = [Facts(premiseClause) for premiseClause in clause[:pos].split('&')]
            # Account for 2 characters in '=>' and add to RHS
            self.conclusion = Facts(clause[pos+2:])

class Solution:
    solutions = dict()
    def __init__(self,index,value):
        self.solutions[index] = self.solutions[index] + [value]


class KnowledgeBase:
    kbaseData = dict()
    goalQuery = None

    def __init__(self, goal):
        self.goalQuery = Facts(goal)

    def checkQuery(self):
        solutions = dict()
        # return Inference().FOL_BC_ASK(self.kbaseData,self.goalQuery,0,solutions)

    def insertNewQuery(self,logicStatement):
        # Create A Clause
        newClause = Clauses(logicStatement)
        newPredicate = newClause.conclusion.predicate
        self.kbaseData[newPredicate] = self.kbaseData[newPredicate] + [newClause] if newPredicate in self.kbaseData else [newClause]

class Inference:

    def __init__(self):
        self.varcounter = 0
        self.subGoals = dict()

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


    def replaceQuery(self,parameters,find,replace):
        for index, item in enumerate(parameters):
            if not (item == find):
                parameters[index] = replace
        return parameters

    def intersection(self,a, b):
        return list(set(a) - set(b))[0]

    def checkDupliactes(self,level,solutionDict,count):
        uniqueList = list(set(solutionDict[level]))
        returnList = list()
        for values in uniqueList:
            if solutionDict[level].count(values) == count:
                returnList.append(values)

        return returnList

    def FOL_BC_ASK(self,kb,goalQuery,level,solutions):

        kbGoals = kb[goalQuery.predicate]
        print goalQuery.predicate

        for askQuery in kbGoals:
            goalParams = goalQuery.parameters
            askParams = askQuery.conclusion.parameters

            if 'x' in goalParams and 'x' in askParams:
                print askQuery.ClauseStr
                diffSet = set(goalParams) - set(askParams)
                if(len(diffSet) == 0):
                    for premises in askQuery.premise:
                        solutions[level] = (self.FOL_BC_ASK(kb, premises,level+1,solutions))
                    solutions[level] = self.checkDupliactes(level+1,solutions,len(askQuery.premise))
                    del solutions[level+1][:]

            elif not 'x' in goalParams and 'x' in askParams:
                print askQuery.ClauseStr
                diffSet = list(set(goalParams) - set(askParams))
                if 'x' not in diffSet:
                    for premises in askQuery.premise:
                        premises.parameters = self.replaceQuery(premises.parameters,'x',diffSet[0])
                        solutions[level] = (self.FOL_BC_ASK(kb, premises, level + 1, solutions))
                    solutions[level] = self.checkDupliactes(level + 1, solutions, len(askQuery.premise))
                    del solutions[level+1][:]

            else:
                diffSet = list(set(goalParams) - set(askParams))
                if diffSet == goalParams:
                    continue
                if diffSet[0] == 'x':
                    solutionString = self.intersection(askParams,goalParams)
                    solutions.setdefault(level,[]).append(solutionString)
                    solutions["key"] = goalQuery.predicate

        return solutions[level]
                    # return self.intersection(askParams,goalParams)

            # Cmbine the common Query Truth values
            # goalQuery.subGoals = list(set(goalQuery.subGoals) | set(tempGoals))
            # print tempGoals

        # compoundGoals = list(set(goalQuery.subGoals) | set(tempGoals))

            # print goalQuery.subGoals
            # return tempGoals


            # if 'x' in tempParams and 'x' not in baseParams:


        #
        #
        # if isinstance(goal,Clauses):
        #     goalKey = goal.conclusion.predicate
        # if isinstance(goal,Facts):
        #     goalKey = goal.predicate
        #
        # goalObj = goal
        # goalClauses = kb[goalKey]
        # for queries in goalClauses:
        #     self.Substr(kb, queries, goalObj, dict())
    #
    # def STANDARDIZE(self,premiseLHS,conclusionRHS):
    #
    #
    # def SUBST(self,theta,subStatement):
    #
    #
    #
    # def FOL_BC_AND(self, kb, goals, theta):
    #
    #
    # def UNIFY(self, x, y, theta):
    #
    #
    # def UNIFYVAR(self, var, x, theta):


    # def printQuery(self,query,found,theta):
    #     str = query
    #     str += ": "
    #     if found:
    #         str += "True"
    #         str += ": ["
    #
    #         if theta != None:
    #             for values in theta:
    #                 str += "'" + values + "', "
    #
    #             str = str[:-2]
    #
    #             str += "]"
    #     else:
    #         str += "False"
    #
    #
    #     print str




    # def Substr(self,kb,askQuery,goalQuery,theta):
    #
    #     # print "Query :",myQuery.ClauseStr
    #     tempQuery = copy.deepcopy(goalQuery)
    #     # Check to see if the predicates are the same
    #     if tempQuery.predicate == askQuery.conclusion.predicate:
    #         # Check to see if the argument lists are the same size
    #         tempParams = tempQuery.parameters
    #         baseParams = askQuery.conclusion.parameters
    #         if len(tempParams) == len(baseParams):
    #
    #             # Case 1: substitue constant for x
    #             if 'x' in tempParams and 'x' not in baseParams:
    #                 variable = list(set(tempParams) - set(baseParams))[0]
    #                 constant = list(set(baseParams) - set(tempParams))[0]
    #                 if(len(variable) == 1 and variable[0] == 'x'):
    #                     # print variable,constant
    #                     theta.append(constant)
    #
    #             # Case 2: x in goal and conclusion -> need to look up premise
    #             if 'x' in tempParams and 'x' in baseParams:
    #                 if tempParams == baseParams:
    #                     for compoundPremise in askQuery.premise:
    #                         self.FOL_BC_ASK(kb,compoundPremise)
    #
    #
    #
    #     return theta







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
    print sol



