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



class KnowledgeBase:
    kbaseData = dict()
    goalQuery = None

    def __init__(self, goal):
        self.goalQuery = Facts(goal)

    def checkQuery(self):
        solutions = dict()
        return Inference().FOL_BC_ASK(self.kbaseData,self.goalQuery)

    def insertNewQuery(self,logicStatement):
        # Create A Clause
        newClause = Clauses(logicStatement)
        newPredicate = newClause.conclusion.predicate
        self.kbaseData[newPredicate] = self.kbaseData[newPredicate] + [newClause] if newPredicate in self.kbaseData else [newClause]

class Inference:

    def __init__(self):
        self.varcounter = 0
        self.subGoals = []

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

    def FIRST(self,list):
        return list[0]

    def REST(self,list):
        return list[1:]

    def FOL_BC_ASK(self, kb, query):
        count = 0
        for substitutions in  self.FOL_BC_OR(kb, query, dict()):
            count += 1

        print count

    def FOL_BC_OR(self,kb,goal,theta):
        subGoals = list()
        print "Query :", goal.predicate, goal.parameters
        if (goal.predicate not in kb):
            return
        goals = kb[goal.predicate]

        for rules in goals:
            self.PrintQuery(rules)
            lhs,rhs = self.STANDARDIZE(rules.premise,rules.conclusion)
            for theta2 in self.FOL_BC_AND(kb,lhs,self.UNIFY(rhs.parameters,goal.parameters,theta)):
                # print theta2.keys(),theta2.values()
                subGoals.append(theta2)

                yield theta2


        print subGoals

    def FOL_BC_AND(self,kb,goal,theta):

        if theta is None:
            return
        elif goal == None:
            yield theta
        elif len(goal) == 0:
            yield theta
        else:
            first = self.FIRST(goal)
            rest =self.REST(goal)
            for theta2 in self.FOL_BC_OR(kb,self.SUBST(theta,first),theta):
                for theta3 in self.FOL_BC_AND(kb,self.SUBST(theta2,rest),theta2):
                    yield theta3

    def STANDARDIZE(self,lhs,rhs):
        lhs = copy.deepcopy(lhs)
        rhs = copy.deepcopy(rhs)
        if lhs != None:
            for lhs_premise in lhs:
                for i in range(len(lhs_premise.parameters)):
                    if self.isVariable(lhs_premise.parameters[i]):
                        lhs_premise.parameters[i] = lhs_premise.parameters[i] + str(self.varcounter)

        for i in range(len(rhs.parameters)):
            if self.isVariable(rhs.parameters[i]):
                rhs.parameters[i] = rhs.parameters[i] + str(self.varcounter)

        self.varcounter += 1
        return (lhs, rhs)


    def SUBST(self,theta,sentence):
        if isinstance(sentence,list):
            if len(sentence) == 0:
                return sentence
            for count in range(len(sentence)):
                for target, substitution in theta.iteritems():
                    for i in range(len(sentence[count].parameters)):
                        if sentence[count].parameters[i] == target:
                            sentence[count].parameters[i] = substitution
                return sentence


        sentence = copy.deepcopy(sentence)
        for target, substitution in theta.iteritems():
            for i in range(len(sentence.parameters)):
                if sentence.parameters[i] == target:
                    sentence.parameters[i] = substitution
        return sentence

    def UNIFY(self, x, y, theta):
        if theta is None:
            return None
        elif x == y:
            return theta
        elif isinstance(x, str) and self.isVariable(x):
            return self.UNIFYVAR(x, y, theta)
        elif isinstance(y, str) and self.isVariable(y):
            return self.UNIFYVAR(y, x, theta)
        elif self.isList(x) and self.isList(y) and len(x) == len(y):
            return self.UNIFY(self.REST(x), self.REST(y), self.UNIFY(self.FIRST(x), self.FIRST(y), theta))
        return None

    def UNIFYVAR(self, var, x, theta):
        if var in theta:
            val = theta[var]
            return self.UNIFY(val, x, theta)
        elif x in theta:
            val = theta[x]
            return self.UNIFY(var, val, theta)
        thetaOccurCheck = theta.copy()
        thetaOccurCheck[var] = x
        return thetaOccurCheck

    def PrintQuery(self,rules):
        if isinstance(rules,Clauses):
            print rules.ClauseStr



            # def STANDARDISE(self,lhs,rhs):
    #     lhs,rhs = copy.deepcopy(lhs),copy.deepcopy(rhs)
    #     if lhs is None:
    #         return (lhs,rhs)
    #
    #     for lhsPredicate in lhs:
    #         for count in range(len(lhsPredicate.parameters)):
    #             if self.isVariable(lhsPredicate.parameters[count]):
    #                 lhsPredicate.parameters[count] = lhsPredicate.parameters[count] + str(self.myCount)
    #
    #     for count in range(len(rhs.parameters)):
    #         if self.isVariable(rhs.parameters[count]):
    #             rhs.parameters[count] = rhs.parameters[count] + str(self.myCount)
    #
    #     self.myCount += 1
    #     return (lhs, rhs)
    #
    # def FOL_BC_ASK(self,kb,query):
    #
    #
    #
    #     print (self.FOL_BC_OR(kb, query, dict()))
    #
    #
    # def FOL_BC_AND(self,kb,goal,theta):
    #     if theta is None:
    #         return
    #     elif isinstance(goal,list):
    #         if len(goal) == 0:
    #             yield theta
    #     elif goal is None:
    #         yield theta
    #
    #     else:
    #         first,rest = goal[0],goal[1:]
    #         for subTheta in self.FOL_BC_OR(kb,self.SUBST(theta,first),dict()):
    #             # for subst1 in self.bcOR(kb, self.subst(theta, first), dict()):
    #             for subTheta2 in self.FOL_BC_AND(kb, rest, subTheta):
    #                 yield subTheta2
    #
    # def FOL_BC_OR(self,kb,goal,theta):
    #     if (goal.predicate not in kb):
    #         return
    #
    #     for rule in kb[goal.predicate]:
    #
    #         (lhs,rhs) = self.STANDARDISE(rule.premise,rule.conclusion)
    #         unifyres = self.UNIFY(rhs.parameters, goal.parameters, theta)
    #         for subtheta in self.FOL_BC_AND(kb,lhs,unifyres):
    #             self.subGoals.pop()
    #             print subtheta
    #             yield subtheta
    #
    #
    #
    # def SUBST(self,theta,subSentence):
    #     subSentence = copy.deepcopy(subSentence)
    #     for lookup,substitution in theta.iteritems():
    #         for count in range(len(subSentence.parameters)):
    #             if subSentence.parameters[count] == lookup:
    #                 subSentence.parameters[count] = substitution
    #     return subSentence
    #










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



