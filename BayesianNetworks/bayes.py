
import sys
import copy

class BayseianOps:
    def ENUMERATE_ALL(self,variables, evidence, bayesnet):
        if len(variables) == 0:
            return 1.0

        Y = variables[0]

        if Y in evidence:
            solution = self.CalculateP(Y, evidence, bayesnet) * self.ENUMERATE_ALL(variables[1:], evidence, bayesnet)
        else:
            sigmaTerms = []
            evidenceCopy = copy.deepcopy(evidence)
            for y in [True, False]:
                evidenceCopy[Y] = y
                sigmaTerms.append(
                    self.CalculateP(Y, evidenceCopy, bayesnet) * self.ENUMERATE_ALL(variables[1:], evidenceCopy, bayesnet))
            solution = sum(sigmaTerms)

        return solution


    def CalculateP(self,Y, e, bayesnet):

        if len(bayesnet[Y]['parents']) == 0:
            if e[Y] == True:
                return float(bayesnet[Y]['probability+'])
            else:
                return float(bayesnet[Y]['probability-'])
        else:
            parentKey = tuple(e[parent] for parent in bayesnet[Y]['parents'])

            if e[Y] == True:
                return float(bayesnet[Y]['conditionalProbability'][parentKey])
            else:
                return 1 - float(bayesnet[Y]['conditionalProbability'][parentKey])

class Helper:
    def SignToTuple(self,signList):
        BoolKey = list()
        for occurs in signList:
            if (occurs == '+'):
                tempBoolKey = True
            else:
                tempBoolKey = False
            BoolKey.append(tempBoolKey)
        return tuple(BoolKey)


    def splitAssignment(self,assignmentString):
        assignment = assignmentString.strip()
        assignmentList = assignment.split(' = ')
        rhs = assignmentList[1].strip()
        lhs = assignmentList[0].strip()
        if '+' in rhs:
            rhs = True
        else:
            rhs = False
        return (lhs, rhs)

    def getParticipatingNodes(self,e, bayesnet, topoNodes):
        existingNodes = set(e.keys())
        nodeExistsList = [True if x in existingNodes else False for x in topoNodes]
        newSortedNodes = []
        while len(existingNodes) != 0:
            for parent in bayesnet[existingNodes.pop()]['parents']:
                existingNodes.add(parent)
                nodeExistsList[sortedNodes.index(parent)] = True
        for node in topoNodes:
            if nodeExistsList[sortedNodes.index(node)] == True:
                newSortedNodes.append(node)
        return newSortedNodes

    def sortNodes(self,bayesnet):
        # List of node names
        bayesnetNodes = bayesnet.keys()
        # Empty return List
        sortedList = []

        while len(sortedList) < len(bayesnetNodes):
            for keyNode in bayesnetNodes:
                if keyNode not in sortedList and all(parent in sortedList for parent in bayesnet[keyNode]['parents']):
                    sortedList.append(keyNode)

        return sortedList

    def stripEventString(self,query):
        return query[query.index('(') + 1:query.index(')')]

class BayesNode:
    parent = list()
    children = list()
    name = ''
    probability = 0.0
    conditionalProbability = dict()

    def __init__(self,name,parents,children,probability=0.0):
        self.name = name
        self.parent = parents
        self.children = children
        self.probability = probability


    def __setitem__(self, key, value):
        if key == 'probability':
            self.probability = float(value)
        if key == 'conditionalProbability':
            if(isinstance(value,dict)):
                self.conditionalProbability = value

    def __getitem__(self, item):

        if item == 'children':
            return self.children
        if item == 'parents':
            return self.parent

        if item == 'probability+':
            return self.probability
        if item == 'probability-':
            return 1-self.probability

        if item == 'conditionalProbability':
            return self.conditionalProbability

class Query:
    query = ''
    completeJointTerms = dict()
    evidence = dict()
    solution = 1.00
    isConditional = False

    def __init__(self, queryString):
        self.resetLocalVariables()
        self.query = Helper().stripEventString(queryString)
        if '|' in self.query:
            self.isConditional = True
            queryEvent = self.query[:self.query.index(' | ')]
            queryEventsList = queryEvent.strip().split(',')
            for eachEvent in queryEventsList:
                self.makeJointTerms(eachEvent)
            queryEvent = self.query[self.query.index(' | ') + 3:]
        else:
            queryEvent = self.query

        queryEventsList = queryEvent.strip().split(',')
        for assignment in queryEventsList:
            self.makeJointTerms(assignment)
            self.makeEvidence(assignment)


    def makeEvidence(self,assignment):
        variable, value = Helper().splitAssignment(assignment.strip())
        self.completeJointTerms[variable] = value
        self.evidence[variable] = value

    def makeJointTerms(self,assignment):
        variable, value = Helper().splitAssignment(assignment.strip())
        self.completeJointTerms[variable] = value

    def resetLocalVariables(self):
        self.query = ''
        self.completeJointTerms = dict()
        self.evidence = dict()
        self.solution = 1.00
        self.isConditional = False


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        fileLines = f.read().splitlines()

    BayesNet = {}
    sortedNodes = []
    queryStringsList = []
    H = Helper()

    queryCount = int(fileLines[0])
    for lines in fileLines[1:queryCount+1]:
        queryStringsList.append(lines)

    rhs = list()


    conditionalProbability= {}          # key = boolean values and value is probability for give occurances in key
    for lines in fileLines[queryCount+1:]:

        if lines == '***':
            conditionalProbability = {}         # Reset the lists and dictionaries
            rhs = []                            # Reset the lists and dictionaries
            continue                            # continue execution

        if(lines[0].isupper() or lines[0].islower()):
            tableHeader = lines.split(' | ')
            nodeKey = tableHeader[0].strip()
            if len(tableHeader) != 1:
                rhs = tableHeader[1].strip().split(' ')

            BayesNet[nodeKey] = BayesNode(nodeKey,rhs,[])

            for parent in rhs:
                BayesNet[parent]['children'].append(nodeKey)
        else:
            if len(rhs) == 0:
                BayesNet[nodeKey]['probability'] = lines
            else:
                linesSplit = lines.split(' ')           # Find Conditional Probability
                conditionalProbValue= linesSplit[0]     # Split Value and store in conditionalProbValue
                signsList = linesSplit[1:]              # Get list of + and -  signs
                conditionalProbability[H.SignToTuple(signsList)] = conditionalProbValue      # Convert + and - to True False represntation
                BayesNet[nodeKey]['conditionalProbability'] = conditionalProbability



    sortedNodes = H.sortNodes(BayesNet)          #get topological order
    finalSolutionList = list()
    B = BayseianOps()

    for queryString in queryStringsList:
        query = Query(queryString)
        if query.isConditional == False:
            query.solution = B.ENUMERATE_ALL(H.getParticipatingNodes(query.evidence, BayesNet, sortedNodes), query.evidence, BayesNet)
        else:
            N = B.ENUMERATE_ALL(H.getParticipatingNodes(query.completeJointTerms,BayesNet,sortedNodes),query.completeJointTerms,BayesNet)
            D = B.ENUMERATE_ALL(H.getParticipatingNodes(query.evidence,BayesNet,sortedNodes),query.evidence,BayesNet)
            query.solution = N/D
        query.solution = format(query.solution, '.2f')


        # print query.solution
        finalSolutionList.append(query.solution)

    fileoutput = open("output.txt", "w")
    for values in finalSolutionList:
        fileoutput.write(str(values)+'\n')




