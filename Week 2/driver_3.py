# -*- coding: utf-8 -*-

import sys
import time
import math
import heapq

class node():
    def __init__(self,stateStr,path=[],cost=0,depth=0,parentPointer=None):
        self.stateStr = stateStr
        self.path = path
        self.cost = cost
        self.depth = depth
        self.parentPointer = parentPointer

class priorityQueue():     
    def __init__(self):
        self.qList = [] #frontier state in a heap list
        self.qDict = {} #frontier state strings
        self.index = 0 #unique sequence count
    
    def pushObject(self, priority, item):
        #Add new object or update priority of existing object in qDict dictionary
        self.index += 1
        if item.stateStr in self.qDict: #If the item exist in frontier
            itemOld = self.qDict[item.stateStr]
            if item.cost < itemOld.cost:
                self.qDict[item.stateStr] = item
                # Simply add the new node (with a higher priority) without 
                # removing the existing node (with lower priority).     
                heapq.heappush(self.qList,[priority,self.index,item])
        else: #If the item does not exist in frontier
            self.qDict[item.stateStr] = item
            # Simply add the new node (with a higher priority) without 
            # removing the existing node (with lower priority).
            heapq.heappush(self.qList,[priority,self.index,item])
                    
    def popObject(self):
        #Remove and return item wth the highest priority task.
        while True:
            cost0, index0, item0 = heapq.heappop(self.qList)
            if item0.stateStr in self.qDict:
                del self.qDict[item0.stateStr]
                break
            else:
                #Remove duplicate nodes in self.qList with lower priority 
                #(introduced by addObject function) which already have been 
                #explored previously.
                pass      
             
        return item0         
        
class tree():
    def __init__(self,stateStr,method):
        self.node = node(stateStr, path=[], cost=0, depth=0, parentPointer=None) #current state at current node
        self.n = len(stateStr)
        self.n0 = int(math.sqrt(self.n))
        self.goalStateStr = ''.join([str(i) for i in range(self.n)])
        self.maxDepth = 0
        self.exploredState = set()
        if method == 'bfs' or method == 'dfs':
            #for BFS & DFS
            self.qNode = []
            self.qNode.append(self.node)
            self.qState = set()
            self.qState.add(stateStr) 
        if method == 'ast':
            #for ASTAR
            self.manhattanDistance()
            self.qASTAR = priorityQueue()
            self.qASTAR.pushObject(0, self.node)
#        print(stateStr)
#        print('Initialised')    
 
    def createState(self,loc,direction):
        stateList = list(self.node.stateStr)
        if direction == 'Up':
            stateList[loc-self.n0], stateList[loc] = stateList[loc], stateList[loc-self.n0]
        elif direction == 'Down':
            stateList[loc+self.n0], stateList[loc] = stateList[loc], stateList[loc+self.n0]
        elif direction == 'Left':
            stateList[loc-1], stateList[loc] = stateList[loc], stateList[loc-1]
        elif direction == 'Right':
            stateList[loc+1], stateList[loc] = stateList[loc], stateList[loc+1]
        stateStr = ''.join(stateList)
        return stateStr
    
    def addChild(self,loc,direction):
        childStateStr = self.createState(loc,direction)
        childNode = node(childStateStr, path=direction, cost=self.node.cost+1, depth=self.node.depth+1, parentPointer=self.node)
        if self.exploredState.isdisjoint({childStateStr}):
            if self.qState.isdisjoint({childStateStr}):
                self.qNode.append(childNode)
                self.qState.add(childStateStr)
                if self.maxDepth < childNode.depth:
                    self.maxDepth = childNode.depth   
                    
    def addChildASTAR(self,loc,direction):
        childStateStr = self.createState(loc,direction)
        costh = 0
        for i in range(self.n):
            if childStateStr[i] == '0':
                continue
            costh = costh + self.manhattanDist[str(i)+childStateStr[i]]   
        costf = costh + self.node.cost+1                                     
        childNode = node(childStateStr, path=direction, cost=self.node.cost+1, depth=self.node.depth+1, parentPointer=self.node)
        if self.exploredState.isdisjoint({childStateStr}):
            self.qASTAR.pushObject(costf, childNode)
            if self.maxDepth < childNode.depth:  #May not be accurate and depends on how max_depth is defined for ASTAR
                self.maxDepth = childNode.depth 
                    
    def expandNodeBFS(self):
        loc = self.node.stateStr.index('0') #0 indexed
        col = loc%self.n0 #0 indexed
        row = int(loc/self.n0) #0 indexed
        if row != 0:
            self.addChild(loc,'Up')                              
        if row != self.n0-1:
            self.addChild(loc,'Down')                              
        if col != 0:
            self.addChild(loc,'Left')                              
        if col != self.n0-1:
            self.addChild(loc,'Right') 
            
    def expandNodeDFS(self):
        loc = self.node.stateStr.index('0') #0 indexed
        col = loc%self.n0 #0 indexed
        row = int(loc/self.n0) #0 indexed
        if col != self.n0-1:
            self.addChild(loc,'Right') 
        if col != 0:
            self.addChild(loc,'Left')                              
        if row != self.n0-1:
            self.addChild(loc,'Down')                              
        if row != 0:
            self.addChild(loc,'Up')      

    def expandNodeASTAR(self):
        loc = self.node.stateStr.index('0') #0 indexed
        col = loc%self.n0 #0 indexed
        row = int(loc/self.n0) #0 indexed
        if row != 0:
            self.addChildASTAR(loc,'Up')                              
        if row != self.n0-1:
            self.addChildASTAR(loc,'Down')                              
        if col != 0:
            self.addChildASTAR(loc,'Left')                              
        if col != self.n0-1:
            self.addChildASTAR(loc,'Right')       
            
    def manhattanDistance(self):
        self.manhattanDist = {}        
        index1 = -1
        for i in range(self.n0):
            for j in range(self.n0):
                index1 += 1
                index2 = -1
                for k in range(self.n0):
                    for l in range(self.n0):
                        index2 += 1
                        key = str(index1)+str(index2)
                        self.manhattanDist.update({key:abs(i-k)+abs(j-l)})
            
    def traceback(self,node):
        path = []
        while node.path:
            path = [node.path] + path
            node = node.parentPointer
        return path
        
    def searchBFS(self):
        maxFringe = 0
        while self.qNode:
            self.node = self.qNode.pop(0) #dequeue the first element   
            self.qState.remove(self.node.stateStr)
            self.exploredState.add(self.node.stateStr)
            if self.node.stateStr == self.goalStateStr:
#                print(self.node.stateStr)
#                print(self.node.cost)
#                print(self.node.depth)
                path = self.traceback(self.node)
#                print(path)
#                print('finish')
                return (self.node, path, len(self.exploredState)-1, len(self.qState), maxFringe, self.maxDepth) 
            self.expandNodeBFS()
            fringe = len(self.qState)
            if maxFringe < fringe:
                maxFringe = fringe
                    
    def searchDFS(self):
        maxFringe = 0
        while self.qNode:
            self.node = self.qNode.pop(-1) #dequeue the last element   
            self.qState.remove(self.node.stateStr)    
            self.exploredState.add(self.node.stateStr)
            if self.node.stateStr == self.goalStateStr:
#                print(self.node.stateStr)
#                print(self.node.cost)
#                print(self.node.depth)
                path = self.traceback(self.node)
#                print(path)
#                print('finish')
                return (self.node, path, len(self.exploredState)-1, len(self.qState), maxFringe, self.maxDepth) 
            self.expandNodeDFS()
            fringe = len(self.qState)
            if maxFringe < fringe:
                maxFringe = fringe
                    
    def searchASTAR(self):
        maxFringe = 0
        while self.qASTAR.qList:
            self.node = self.qASTAR.popObject() #dequeue the first element   
            self.exploredState.add(self.node.stateStr)
            if self.node.stateStr == self.goalStateStr:
#                print(self.node.stateStr)
#                print(self.node.cost)
#                print(self.node.depth)
                path = self.traceback(self.node)
#                print(path)
#                print('finish')
                return (self.node, path, len(self.exploredState)-1, len(self.qASTAR.qDict), maxFringe, self.maxDepth) 
            self.expandNodeASTAR()
            fringe = len(self.qASTAR.qDict)
            if maxFringe < fringe:
                maxFringe = fringe
        
def resource():                    
    if sys.platform == "win32":
        import psutil
        ram_usage = psutil.Process().memory_info().rss
#        print("psutil", ram_usage)
        return ram_usage
    else:
        # Note: if you execute Python from cygwin,
        # the sys.platform is "cygwin"
        # the grading system's sys.platform is "linux2"
        # import resource #only works in linux systems
        import resource
        ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#        print("resource", ram_usage)                    
        return ram_usage
                    
def main():  
    start_time = time.time()
    method = sys.argv[1]
    state = sys.argv[2]
#    print(method + " = " + state)  #print command line arguments
    stateList = state.split(",")
    #StateList
#    print(stateList)
    #StateList ---> StateStr
    stateStr = ''.join(stateList)
#    print(stateStr)
    #StateStr ---> StateList
#    stateList1 = list(stateStr)
#    print(stateList1)
    #Starting search algorithm
#    print('Starting search algorithm')

    path = []
    nodeFound = node(stateStr)
    expanded = 0
    fringe = 0
    maxFringe = 0
    maxDepth = 0
    
    if method == 'bfs':
        treeBFS = tree(stateStr, method)   
        nodeFound, path, expanded, fringe, maxFringe, maxDepth = treeBFS.searchBFS()
    elif method == 'dfs':
        treeDFS = tree(stateStr, method)   
        nodeFound, path, expanded, fringe, maxFringe, maxDepth = treeDFS.searchDFS()
    elif method == 'ast':
        treeASTAR = tree(stateStr, method) 
        nodeFound, path, expanded, fringe, maxFringe, maxDepth = treeASTAR.searchASTAR() 

    file = open("output.txt","w")
    file.write('path_to_goal: {}\n'.format(path))
    file.write('cost_of_path: {}\n'.format(nodeFound.cost))
    file.write('nodes_expanded: {}\n'.format(expanded))
#    file.write('fringe_size: {}\n'.format(fringe))
#    file.write('max_fringe_size: {}\n'.format(maxFringe))
    file.write('search_depth: {}\n'.format(nodeFound.depth))
    file.write('max_search_depth: {}\n'.format(maxDepth))
    file.write('running_time: {:.8f}\n'.format(time.time() - start_time))
    file.write('max_ram_usage: {}\n'.format(resource()))
    file.close()
    
if __name__ == "__main__":
    main()
