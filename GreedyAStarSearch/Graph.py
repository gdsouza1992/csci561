import operator

class Node:
    def __init__(self,node):
        self.id = node
	    #dictionary to store adjacent nodes
        self.adjacent = {}
        self.costOfSum = 999999
        self.costToGoal = 999999
        self.costToHere = 999999
        self.greedyCostToGoal = 999999

        # To keep track during backtracking
        self.cameFrom = None
        self.cameFromGreedy = None

    def add_neighbor(self,neighbor,weight = 1):
        self.adjacent[neighbor] = weight

    def get_id(self):
        return  self.id

    def get_weight(self,neighbor):
        return  self.adjacent[neighbor]

    def get_connections(self):
        connectionList = list()
        for node in self.adjacent:
            connectionList.append(node)
        return connectionList


class Graph:
    def __init__(self):
        self.node_dict = {}
        self.num_nodes = 0

    def __iter__(self):
        return iter(self.node_dict.values())

    def add_node(self,node):
        self.num_nodes += 1
        new_node = Node(node)
        self.node_dict[node] = new_node

    def add_edge(self,fromNode,toNode,costFrom = 1,costTo=0):
        if fromNode not in self.node_dict:
            self.add_node(fromNode)
        if toNode not in self.node_dict:
            self.add_node(toNode)

        self.node_dict[fromNode].add_neighbor(self.node_dict[toNode],costFrom)


def calculateAStarHeurstics(g):
    # Take the minimum cost edge as a heuristic for the given node
    # Will be 0 for node that has no outgoing edges
    for node in g:
        nodeValues = node.adjacent.values()

        # Check if the node has out going edges
        if(nodeValues):
            node.costToGoal = min(nodeValues)

def calculateGreedyHeuristics(g):
    for node in g:
        nodeValues = node.adjacent.values()

        # Check if the node has out going edges
        if (nodeValues):
            node.greedyCostToGoal = max(nodeValues)

# Recursively find the came from and print
def backTrackPath(visited,start,goal,path,isGreedy):
    if(goal.id == start.id):
        path.append(start.id)
        return path
    else:
        # Back track from goal to start by going thru which child came from which parent
        if isGreedy:
            backTrackPath(visited,start,goal.cameFromGreedy,path,isGreedy)
        else:
            backTrackPath(visited, start, goal.cameFrom, path,isGreedy)
        path.append(goal.id)
        return path


def BestFirstSearch(graph,start,goal,isGreedy):

    # Hard code the goal state to have a heuristic of 0 so it is not +Infinity (999999) by default
    goal.costToGoal = 0
    start.costToHere = 0
    start.costOfSum = 0

    frontier = list()
    visited = list()

    frontier.append(start);

    while(len(frontier) != 0):

        # get the node with the least heuristic after sorting it will pe the first element in list
        parentNode = frontier.pop(0)
        visited.append(parentNode)

        #check if we reached the goal
        if (parentNode.id == goal.id):
            break

        #get all possible children that can be explored
        children = parentNode.get_connections()

        if isGreedy:
            for eachChild in children:
                # Add the children to the frontier if we have not visited them and they are not already in the frontier
                if (eachChild not in visited and eachChild not in frontier):
                    # Keep track from where the child came
                    eachChild.cameFromGreedy = parentNode
                    frontier.append(eachChild)

                    # if there are no more children in the frontier and we have not reached the goal we cant find the node
            if (len(frontier) == 0):
                print("Unsuccessful in finding goal")
                break

                # Sort the frontier as per heuristic
            frontier.sort(key=operator.attrgetter("greedyCostToGoal"), reverse=True)
        else:
            for eachChild in children:
                # Add the children to the frontier if we have not visited them and they are not already in the frontier
                if (eachChild not in visited):

                    eachChild.costToHere = parentNode.adjacent[eachChild] + parentNode.costToHere;

                    # Keep track from where the child came
                    if (eachChild in frontier):
                        if (eachChild.costOfSum >= parentNode.costToHere + parentNode.adjacent[
                            eachChild] + eachChild.costToGoal):
                            eachChild.costOfSum = parentNode.costToHere + parentNode.adjacent[
                                eachChild] + eachChild.costToGoal
                            eachChild.cameFrom = parentNode
                    else:
                        eachChild.costOfSum = eachChild.costToHere + eachChild.costToGoal
                        eachChild.cameFrom = parentNode
                        frontier.append(eachChild)

            # if there are no more children in the frontier and we have not reached the goal we cant find the node
            if (len(frontier) == 0):
                print("Unsuccessful in finding goal")
                break

            # Sort the frontier as per heuristic
            frontier.sort(key=operator.attrgetter("costOfSum"), reverse=False)

    #Recursivley backtrack till you reach the start
    if(goal in visited):
        # Print the path as desired
        path = backTrackPath(visited,start,goal,list(),isGreedy)
        print('>'.join(path))


    # print("Successful in finding goal")


if __name__ == '__main__':
    g = Graph()

    fileLines = None
    with open('pa1.in', 'r') as f:
        fileLines = f.read().splitlines()




    nodeList = list()
    startString = '0'
    endString = str(int(fileLines[0])-1)
    for fileLine in fileLines[1:]:
        lineArray = fileLine.split()
        g.add_edge(str(lineArray[0]),str(lineArray[1]),int(lineArray[2]))




    # for vertex in g:
    #     for weight in vertex.get_connections():
    #         vid = vertex.get_id()
    #         wid = weight.get_id()
    #         print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))

    # If you dont hard code the heuristics then calculate as per the function else commit this line
    calculateGreedyHeuristics(g);
    calculateAStarHeurstics(g);

    BestFirstSearch(g,g.node_dict[startString],g.node_dict[endString],True)
    BestFirstSearch(g,g.node_dict[startString],g.node_dict[endString],False)
