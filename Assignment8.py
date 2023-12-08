import copy
import random

#Name: Assignment8.py
#Date: 12/5/2023
#Author:Harrison Reed
#Description: Program for EECS Assignment 8. In which we 
#Implement algorithm to find an euler circut if one exisits,
#Implement Dirac's therom to see if a graph has a hamilton circut or might have one
#Implement Ore's therom to see if a graph has a hamilton circut or might have one
#Implement MinMax algorithm, calculate who will win games of nim
#Resources: GeeksforGeeks
#Collaborators: None


#Name: Circuts
#Description: Class for implemeting circuts functionality
#Author: Harrison Reed
class Circuts:
    
    #Name: init
    #Description: creates new adjacency matrix(2 dimensional array), and edge(2 diemensional) array
    #Author: Harrison Reed
    def __init__(self,size) -> None:
        self.adjMat = []*size
        self.edges = []*size
        for i in range(size):
            temp = [0] * size
            self.adjMat.insert(0,temp)
        pass
    
    #Name:insert
    #Description: Inserts given verticies into the adjacency matrix and into the edge array
    #Input: Vertex1, Vertex2(Note these two verticies should be of type char)
    #Output: None
    #Author: Harrison Reed
    def insert(self,vertex1, vertex2):
        #Convert the verticies from their char to respective int
        let1 = ord(vertex1) - 97
        let2 = ord(vertex2) - 97
        #Insert into adjacency matrix
        self.adjMat[let1][let2] += 1
        self.adjMat[let2][let1] += 1
        self.edges.append([vertex1, vertex2])
        self.edges.append([vertex2,vertex1])
        pass
    
    #Name: removeDup
    #Description: removes duplicate items from the given array(i.e removes [b,a] if [a,b] exists)
    #Input: arr
    #Output: None
    #Author: Harrison Reed
    #Resources: GeeksforGeeks
    def removeDup(self, arr):
        #Starting length of loop is = len(arr)
        currLen = len(arr)
        #Pass through entire array
        for i in range(currLen):
            #If the item in reversed order is contained, then remove it from the list
            if([arr[i][1],arr[i][0]] in arr):
                arr.remove([arr[i][1],arr[i][0]])
                #Update the length
                currLen -= 1
    #Name: eulerCircut
    #Description: Detirmines if there is an euler circut, if so finds that circut, if not prints out the verticies with odd degrees
    #Input: None
    #Output: Prints to the user wether or not there is a euler circut or not
    #Author: Harrison Reed
    def eulerCircut(self):
        #Get starting edge list, this is for the case where starting vertex did not work for some reason
        failSafe = copy.deepcopy(self.edges)
        #For verticies that are not isolated
        notIsolated = []
        #List for the case that stores oddDegree verticies
        oddDegree = []
        #If there are verticies with odd degree
        if(not(self.isEvenDegree(notIsolated, oddDegree))):
            #Then graph doesn't satisfy therom 1
            print("No Circut Exists (Doesn't Satisfy Therom 1)")
            #Print out the verticies with odd degree
            print("The Verticies with odd degree are",oddDegree)
            #Return            
            return
        #Else we can begin to find the circut
        #Get a random starting verticy that is not isolated
        currVert = random.choice(notIsolated)
        #array for the path we take
        visited = []
        #Counter for case where there was a mistake along the path(i.e loop doesn't terminate)
        k = 0
        #While we still have edges to visit
        while(len(self.edges) != 0):
            #Case for when loop doesn't terminate
            if(k >= len(self.adjMat) * 10):
                #Set edges back to starting point 
                self.edges = copy.deepcopy(failSafe)
                #Call eulerCircut again to get a different starting vertex
                self.eulerCircut()
                return
            #Else increment k, and continue finding the path
            k+=1
            #Check all the possible moves we can make from current vertex
            for i in range(len(self.edges)):
                #edge list is setup in the way that [a,b] where a is the current vertex, and b is the vertex we can go to
                #So if edge at(i,0) == the current vertex that means it is a valid move
                if(self.edges[i][0] == currVert):
                        #Get a copy of edges incase we need to back track
                        tempCop = copy.deepcopy(self.edges)
                        #Store the current vertex
                        temp = currVert
                        #Update the current vertex
                        currVert = self.edges[i][1]
                        #Remvoe the edges from array since we just used it
                        self.edges.remove([temp,currVert])
                        self.edges.remove([currVert, temp])
                        #Count the number of occurences of the current vertex to make
                        #Sure we can travel to another vertex(i.e a subcycle)
                        numOfOccurence = sum(x.count(currVert) for x in self.edges)
                        #If there are no more edges that current vertex can traverse,
                        #And the length of the edge list != 0(i.e there are still other edges that need to be visited)
                        if(numOfOccurence == 0 and len(self.edges) != 0 ):
                            #We need to back track since we still have edges to use
                            #Set edges back to what is was before the remove
                            self.edges = copy.deepcopy(tempCop)
                            #Set current vertex back to what it was before the move
                            currVert = temp
                        else:
                            #Else it was a valid move for the circut, so we can append the edge to our visited edges
                            visited.append(tempCop[i])
                            break

        #Print that there is a circut
        print("The graph has an euler circut")
        #Print the path we took
        self.printCircut(visited)
        pass
    
    #Name: printCircut
    #Description: Prints a circut in the form a->b->...->a
    #Input: arr
    #Output: prints the path along the circut
    #Author: Harrison Reed
    def printCircut(self, arr):
        #Loop through arr
        for i in range(len(arr)):
            #If i == 0, i.e starting vertex, print both items in subarray
            if(i == 0):
                print(arr[i][0],"->", arr[i][1],end = "")
            #Else just print the second item
            else:
                print("->", arr[i][1], end = "")

        pass
    #Name: isEvenDegree
    #Description: Checks each of the verticies degree, returns boolean value if there is a degree that is odd
    #Also produces 2 lists, 1 is for the not isolated verticies, and the other stores the verticies that have odd degree
    #Input: arr,arr2
    #Output: result - Boolean
    #Author: Harrison Reed
    def isEvenDegree(self,arr, arr2):
        #Assume that all items have even degree
        result = True
        #Loop through adjacency matrix
        for i in range(len(self.adjMat)):
            #Get all items where they are greater than 0(i.e there is an edge connecting two verticies)
            temp = [x for x in self.adjMat[i] if x > 0 ]
            #If the sum of temp is odd(i.e verticiy i has an odd degree)
            if(sum(temp) % 2 != 0):
                #Add the verticy with odd degree to arr2
                arr2.append(chr(i + 97))
                #Set result to false
                result = False
            #If there are edges
            if(len(temp) != 0):
                #Then vertex is not isolated,add to arr 
                arr.append(chr(i + 97))
            
        #Return the result
        return result

    #Name: diracTherom
    #Description: Implements diracs therom to check if a graph has a hamilton circut, or might have one
    #Input: None
    #Output: returns true or false based on if any of the cases are not met
    #Author: Harrison Reed
    def diracTherom(self):
        #First item that needs to be true(There are 3 or more verticies)
        if(len(self.adjMat) >= 3):
            #Loop through entire adjacency matrix
            for i in range(len(self.adjMat)):
                #Get the edges for vertex i
                temp = [x for x in self.adjMat[i] if x > 0]
                #If the degree of vertex i(sum(temp)) is less that the number of verticies /2.
                #Then Diracs therom is not necessary
                if(sum(temp) < len(self.adjMat) / 2):
                    #Return false
                    return False
        else:
            #Return false for n < 3
            return False
        #Else we can return true, diracs therom is necessary
        return True
    
    #Name: oreTherom
    #Description: Implements ores therom to check if a graph has a hamilton circut, or might have one
    #Input: None
    #Output: returns true or false based on if any of the cases are not met
    #Author: Harrison Reed
    def oreTherom(self):
        #list to store the degrees of the verticies
        degrees = []
        #First condition
        if(len(self.adjMat) >= 3):
            #Get the degrees of the verticies
            for i in range(len(self.adjMat)):
                #Get all values where an edges exists
                temp = [x for x in self.adjMat[i] if x > 0]
                #Add the degree to the list
                degrees.append(sum(temp))
            #Second condition
            #Loop through adjacency matrix
            for i in range(len(self.adjMat)):
                #Loop through each vertex, to check if verticies are adjacenet
                for j in range(len(self.adjMat[i])):
                  #If verticies are not adjacent, and not the same vertex
                  if(self.adjMat[i][j] == 0 and j != i):
                      #Get the two degrees sum
                      result = degrees[i] + degrees[j]
                      #If the sum is less than the number of verticies
                      if(result < len(self.adjMat)):
                          #Then condtion was not met return false
                          return False

        else:
            #Return for n < 3
            return False
        #Else return true ore's therom is necessary
        return True

#Name: Node
#Description: Class for creating node objects for game tree, where the number of children is > 2
#Author: Harrison Reed
class Node:
    def __init__(self, val) -> None:
        self.value = val
        self.children = []
        #Value of a nodes move
        self.moveVal = 0
        pass

#Name: Nim
#Description: Class for implementing the game of nim
#Author: Harrison Reed
class Nim:
    #Name: init
    #Description: initalizer for nim, where we assign our board = root node, and create the game tree and get the move values
    #Input: arr
    #Output: none
    #Author: Harrison Reed
    def __init__(self, arr) -> None:
        self.root = Node(arr)
        self.buildGameTree(self.root)
        self.getNodeVals(self.root, 0)
        pass
    
    #Name: buildGameTree
    #Description: Recursive function to build the game tree based on possible move at the current node
    #Input: board, = the current node 
    #Output: none
    #Author: Harrison Reed
    def buildGameTree(self,board):
        #Empty board, no moves can be made, so return 
        if(len(board.value) == 0):
            return
        #Else loop through each value in the given node
        for i in range(len(board.value)):
            #Create copys for both possible moves
            newBoard1 = copy.deepcopy(board)
            newBoard2 = copy.deepcopy(board)
            #If we can subtract 1 without the value <= 0
            if(board.value[i] - 1 > 0):
                #Then update the value at i    
                currVal1 = board.value[i] - 1
                newBoard1.value[i] = currVal1
            else:
                #Else value does = 0 so remove it from the board
                newBoard1.value.pop(i)
            #Other move we can make i - 2
            #If we can subtract 2 without it being <= 0
            if(board.value[i] - 2 > 0):
                #Then update value at i to value[i] - 2
                currVal2 = board.value[i] - 2
                newBoard2.value[i] = currVal2
            #Else if when we subtract 2 it is == 0
            elif(board.value[i] - 2 == 0):
                #Then remove the value from the board
                newBoard2.value.pop(i)
            #Do nothing for the case when new val  < 0, since that is an illegal move
            
            #If the new values arn't equivalent to the current board
            #Then add these new boards to boards children, as they are valid moves
            if(newBoard1.value != board.value):
                board.children.append(newBoard1.value)
            if(newBoard2.value != board.value):
                board.children.append(newBoard2.value)

        #remove the duplicates of these moves since order doesn't matter
        board.children = self.removeDup(board.children)
        
        #Recursivley build the tree using boards children
        for i in range(len(board.children)):
            self.buildGameTree(board.children[i])
        pass
    

    #Name: removeDup
    #Description: Removes duplicate items from list, ie (1,1,2) == (1,2,1), so remove (1,2,1)
    #Input: returns the updated array
    #Output: arr
    #Author: Harrison Reed
    #Resources: GeeksforGeeks
    def removeDup(self, arr):
        #Sort the items in the sub arrays first, so that they are "Equivalent" (1,2,1) -> (1,1,2) == (1,1,2)
        #Then convert the items into tuples, so that we can call set on them
        #Then we can convert back to a list
        arr = list(set(tuple(sorted(sub))for sub in arr))
        #Now we need to convert each item in the list into nodes
        for i in range(len(arr)):
            arr[i] = Node(list(arr[i]))
        #Return arr
        return arr
    

    #Name: printTree
    #Description: Prints the game tree given a starting node, in level order
    #Input: subTree
    #Output: Prints the game tree to the user
    #Author: Harrison Reed
    #Resources: GeeksforGeeks
    def printTree(self, subTree):
        print()
        #If empty node just return
        if(subTree.value) == None:
            return
        #Else we create a queue
        myQueue = []
        #Add the current node to queue
        myQueue.append(subTree)
        print(len(myQueue))
        #While the queue is not empty we add the children, then update the current node
        while(len(myQueue) != 0):
            #Get the size of queue
            n = len(myQueue)
            while(n > 0):
                #get first item
                temp = myQueue.pop(0)
                #Print item
                if(len(temp.value) != 0):
                    print(temp.value, end=" ")
                #Add all the children of temp
                for i in range(len(temp.children)):
                    myQueue.append(temp.children[i])
                #Update n
                n -= 1
            print()


    #Name: getNodeVals
    #Description: Recursivly finds the values(based on minmax) of each node in the tree
    #Input: subTree, level
    #Output: None
    #Author: Harrison Reed
    def getNodeVals(self, subTree, level):
        #Base case: If the value of the subtree = [1], then it is a win for a player
        if(len(subTree.value) == 1 and subTree.value[0] == 1):
            #If the level is even then it is a win for player 2(i.e they just made a move)
            if(level % 2 == 0):
                subTree.moveVal = -1
            #If the level is odd then it is a win for player 1(i.e they just made a move)
            else:
                subTree.moveVal = 1
            #Return
            return
        #Base case: if there are no other moves
        if(len(subTree.children) == 0):
            return
        #Store the values of the children
        childrenVals = []

        #Loop through each children
        for i in range(len(subTree.children)):
            #Recursivly get the childrens values, with level + 1
            self.getNodeVals(subTree.children[i], level + 1)
        
        #Then add all of the current nodes children vals to the list
        for i in range(len(subTree.children)):
            childrenVals.append(subTree.children[i].moveVal)

        #If level is even
        if(level % 2 == 0):
                #Get the max value of the children, and assign it to current nodes val
                subTree.moveVal = max(childrenVals)
        else:
                #Else assign the min
                subTree.moveVal = min(childrenVals)
        return
    

    #Name: minMax
    #Description: Plays the game nim based on both players using min max stratagey
    #Input: none
    #Output: Prints the current board, and what moves are possible, then when game is over recaps the moves and who won
    #Author: Harrison Reed
    def minMax(self):
        #List to keep track of the moves made
        moves = []
        #Current level
        level = 0
        #Start at the root
        currMove = self.root
        #While the current move is not an empty board
        while(len(currMove.value) != 0):
           #Add the current value to the moves
            moves.append(currMove.value)
            #List for the possible moves
            moveList = []
            #Add all possible moves, and their values to move list
            for i in range(len(currMove.children)):
                moveList.append([currMove.children[i].moveVal,currMove.children[i]])

            #Same as move list, except this is used to print the move board, since move list would just print the object not the array
            possMoves = []
            for i in range(len(moveList)):
                if(moveList[i][1].value != []):
                    possMoves.append([moveList[i][0],moveList[i][1].value])
            
            #If there are no possible moves, then exit the loop
            if(len(possMoves) == 0):
                break
            
            #Print current board and level
            print("Current Board", currMove.value,": Current Level", level)
            #If the level is even, then it is player 1's move
            if(level % 2 == 0):
                print("Since the level is even, it is player 1's move")
                #Print the possible moves
                print("Their options are (Move Val, Result of Move):", possMoves)
                #set max to first possible move
                max = moveList[0]
                #Loop through list and get the maximum move value from the list
                for i in range(len(moveList)):
                    if(moveList[i][0] > max[0]):
                        max = moveList[i]
                #Print the move that will be chosen
                print("They will choose the maximum value, which is[", max[0],",",max[1].value,"]")
                #Update the current board
                currMove =  max[1]
            #Else its players two turn 
            else:
                #Same as for player 1, except we are looking for the minimum value 
                print("Since the level is odd, it is player 2's move")
                print("Their options are (Move Val, Result of Move):", possMoves)
                min = moveList[0]
                for i in range(len(moveList)):
                    if(moveList[i][0] < min[0]):
                        min = moveList[i]
                print("They will choose the minimum value, which is[", min[0],',',min[1].value,"]")
                currMove =  min[1]
            print("\n")
            #Increase the level
            level += 1

        #Recap for the moves made in the game
        for i in range(len(moves)):
                if( i != 0):
                        if(i % 2 != 0):
                            print("Player 1's move was ", moves[i])
                            if(len(moves[i]) == 1 and sum(moves[i]) == 1):
                                return "Player 1"
                        else:
                            print("Player 2's move was ", moves[i])
                            if(len(moves[i]) == 1 and sum(moves[i]) == 1):
                                return "Player 2"
                else:
                    print("Starting Board", moves[i])


    #Name: minMaxRand
    #Description: Plays the game nim based on player 1 using min max stratagey, and player 2 choosing random moves
    #Where the order of the players is detirmined by player
    #Input: player, which player starts the game
    #Output: Prints the current board, and what moves are possible, then when game is over recaps the moves and who won
    #Then returns which player won 
    #Author: Harrison Reed
    def minMaxRand(self,player):
            #List to keep track of the moves made
        moves = []
        #Current level
        level = 0
        #Start at the root
        currMove = self.root
        #While the current move is not an empty board
        while(len(currMove.value) != 0):
           #Add the current value to the moves
            moves.append(currMove.value)
            #List for the possible moves
            moveList = []
            #Add all possible moves, and their values to move list
            for i in range(len(currMove.children)):
                moveList.append([currMove.children[i].moveVal,currMove.children[i]])

            #Same as move list, except this is used to print the move board, since move list would just print the object not the array
            possMoves = []
            for i in range(len(moveList)):
                if(moveList[i][1].value != []):
                    possMoves.append([moveList[i][0],moveList[i][1].value])
            
            #If there are no possible moves, then exit the loop
            if(len(possMoves) == 0):
                break
            
            #Print current board and level
            print("Current Board", currMove.value,": Current Level", level)
            #If starting player is 1, they will use max strategy
            if(player == 1):
                #Player 1's move, same as in minMax
                if(level % 2 == 0 ):
                    print("Since the level is even, it is player 1's move")
                    print("Their options are (Move Val, Result of Move):", possMoves)
                    max = moveList[0]
                    for i in range(len(moveList)):
                        if(moveList[i][0] > max[0]):
                            max = moveList[i]
                    print("They will choose the maximum value, which is[", max[0],",",max[1].value,"]")
                    currMove =  max[1]
                else:
                    #Else it is player 2's move
                    print("Since the level is odd, it is player 2's move")
                    print("Their options are (Move Val, Result of Move):", possMoves)
                    #Same as in minMax, except player 2 will choose a random option from the move list
                    randOption = random.choice(moveList)
                    print("They will choose a random option, which is[", randOption[0],',',randOption[1].value,"]")
                    currMove =  randOption[1]

            else:
                #Else player 2 starts
                #So if level is odd its player 1's move
                if(level % 2 != 0):
                    print("Since the level is odd, it is player 1's move")
                    print("Their options are (Move Val, Result of Move):", possMoves)
                    #Since player 1 is second they will use the minimum of the options
                    min = moveList[0]
                    #Get the minimum
                    for i in range(len(moveList)):
                        if(moveList[i][0] < min[0]):
                            min = moveList[i]
                    print("They will choose the minimum value, which is[", min[0],',',min[1].value,"]")
                    #Update the current move
                    currMove =  min[1]
                else:
                    #Else its player twos move and they will pick a random option
                    print("Since the level is even, it is player 2's move")
                    print("Their options are (Move Val, Result of Move):", possMoves)
                    randOption = random.choice(moveList)
                    print("They will choose a random option, which is[", randOption[0],',',randOption[1].value,"]")
                    currMove =  randOption[1]
            #Update the level  
            print("\n")
            level += 1
        
        #Recap the moves based on which player went first
        for i in range(len(moves)):
            if( i != 0):
                #If it was player 1, then player 1's moves were made on even levels(i.e in the list this would be odd index)
                if(player == 1):
                    if(i % 2 != 0):
                        print("Player 1's move was ", moves[i])
                        if(len(moves[i]) == 1 and sum(moves[i]) == 1):
                            return "Player 1"
                    else:
                        print("Player 2's move was ", moves[i])
                        if(len(moves[i]) == 1 and sum(moves[i]) == 1):
                            return "Player 2"
                else:
                    #Else player 1's moves were made on odd levels
                    if(i % 2 != 0):
                        print("Player 2's move was ", moves[i])
                        if(len(moves[i]) == 1 and sum(moves[i]) == 1):
                            return "Player 2"
                    else:
                        print("Player 1's move was ", moves[i])
                        if(len(moves[i]) == 1 and sum(moves[i]) == 1):
                            return "Player 1"
            else:
                print("Starting Board", moves[i])

        return
    

    
    #Name: playNim
    #Description: Calls the two different functions minMax/minMaxRand, based on rand
    #Input: player, which player starts the game, rand, is one of the players chosing randomly
    #Output: returns which player won
    #Author: Harrison Reed
    def playNim(self, rand,player ):
        
        print("\n---------------------------------------")
        #If rand, then we will be using one player with random strategy
        if(rand):
            return self.minMaxRand(player)
        #else both players will use min max
        return self.minMax()
    
    
#Name: main
#Description: Main function, to test classes, nim and circuts, based on user input
#Input: gets the user input.
#Output: Prints results to the screen
#Author: Harrison Reed
if __name__=='__main__':
    while(True):
        userInp = int(input("\n1. Problem 1\n2. Problem 2\n3. Problem 3\n4. Problem 4(A,B)\n5. Problem 4(C)\n6. Exit\nPlease enter an option: "))
        print()
        #For testing problem 1
        if(userInp == 1):
            #Testing G1
            g1 = Circuts(5)
            g1.insert('a','b')
            g1.insert('b','e')
            g1.insert('a','e')
            g1.insert('d','e')
            g1.insert('d','c')
            g1.insert('c','e')
            g1.eulerCircut()

            print("\n\n")
            #Testing G2
            g2 = Circuts(5)
            g2.insert('a','b')
            g2.insert('a','e')
            g2.insert('a','d')
            g2.insert('b','e')
            g2.insert('b','c')
            g2.insert('d','e')
            g2.insert('d','c')
            g2.insert('c','e')
            print("Graph 2 Edges = ", g2.edges)
            g2.eulerCircut()

            print("\n\n")
            #Testing G3
            g3 = Circuts(5)
            g3.insert('a','b')
            g3.insert('a','c')
            g3.insert('a','d')
            g3.insert('b','d')
            g3.insert('b','e')
            g3.insert('c','d')
            g3.insert('d','e')
            print("Graph 3 Edges = ", g3.edges)
            g3.eulerCircut()
            
            print('\n\n')
            #Testing Bridge of Konigsberg
            bridge = Circuts(4)
            bridge.insert('a','b')
            bridge.insert('b','a')
            bridge.insert('a','c')
            bridge.insert('c','a')
            bridge.insert('a','d')
            bridge.insert('b','d')
            bridge.insert('c','d')
            print("Graph Bridge of Konigsberg Edges = ", bridge.edges)
            bridge.eulerCircut()


            print("\n\n")
            #Testing graphFromAssign
            assignGraph = Circuts(9)
            assignGraph.insert('a','b')
            assignGraph.insert('a','d')
            assignGraph.insert('b','c')
            assignGraph.insert('b','d')
            assignGraph.insert('b','e')
            assignGraph.insert('c','f')
            assignGraph.insert('d','e')
            assignGraph.insert('d','g')
            assignGraph.insert('e','f')
            assignGraph.insert('e','h')
            assignGraph.insert('f','h')
            assignGraph.insert('f','i')
            assignGraph.insert('g','h')
            assignGraph.insert('h','i')
            assignGraph.eulerCircut()
            print()
        
        g1 = Circuts(5)
        g1.insert('a','b')
        g1.insert('a','e')
        g1.insert('a','c')
        g1.insert('b','c')
        g1.insert('b','e')
        g1.insert('c','e')
        g1.insert('c','d')
        g1.insert('e','d')

        g2 = Circuts(4)
        g2.insert('a','b')
        g2.insert('b','c')
        g2.insert('b','d')
        g2.insert('c','d')

        g3 = Circuts(7)
        g3.insert('a','b')
        g3.insert('b','g')
        g3.insert('b','c')
        g3.insert('c','d')
        g3.insert('c','e')
        g3.insert('g','e')
        g3.insert('e','f')

        testGraph = Circuts(6)
        testGraph.insert('a','b')
        testGraph.insert('a','c')
        testGraph.insert('b','c')
        testGraph.insert('c','f')
        testGraph.insert('f','d')
        testGraph.insert('f','e')
        testGraph.insert('d','e')
        #For testing problem 2
        if(userInp == 2):
        #Testing number 2
            if(g1.diracTherom()):
                print("From Dirac's Therom Graph G1 has a Hamilton Circut")
            else:
                print("From Dirac's Therom Graph G1 might have a Hamilton Circut")

            #g2
            
            if(g2.diracTherom()):
                print("From Dirac's Therom Graph G2 has a Hamilton Circut")
            else:
                print("From Dirac's Therom Graph G2 might have a Hamilton Circut")

            #g3
            
            if(g3.diracTherom()):
                print("From Dirac's Therom Graph G3 has a Hamilton Circut")
            else:
                print("From Dirac's Therom Graph G3 might have a Hamilton Circut")
            pass

            
            if(testGraph.diracTherom()):
                print("From Dirac's Therom Graph testGraph has a Hamilton Circut")
            else:
                print("From Dirac's Therom Graph testGraph might have a Hamilton Circut")
        #For testing problem 3
        if(userInp == 3):
                #Testing #3
                if(g1.oreTherom()):
                    print("From Ores's Therom Graph G1 has a Hamilton Circut")
                else:
                    print("From Ores's Therom Graph G1 might have a Hamilton Circut")

                if(g2.oreTherom()):
                    print("From Ores's Therom Graph G2 has a Hamilton Circut")
                else:
                    print("From Ores's Therom Graph G2 might have a Hamilton Circut")

                if(g3.oreTherom()):
                    print("From Ores's Therom Graph G3 has a Hamilton Circut")
                else:
                    print("From Ores's Therom Graph G3 might have a Hamilton Circut")

                if(testGraph.oreTherom()):
                    print("From Ores's Therom Graph testGraph has a Hamilton Circut")
                else:
                    print("From Ores's Therom Graph testGraph might have a Hamilton Circut")
        #For testing problem 4A-B
        if(userInp == 4):
            #Tesitng from slides
            #4A
            myGame1 = Nim([2,2,1])
            result = myGame1.playNim(False,0)
            print("Winner of game was", result)
            #4B
            myGame2 = Nim([1,2,3])
            result = myGame2.playNim(False,0)
            print("Winner of game was", result)
        #For Testing problem 4C
        if(userInp == 5):
            #4C
            #Keep track of the winners
            winner = []
            myGame3 = Nim([2,2,1])
            #Play game 100 times
            for i in range(0,100):
                result = myGame3.playNim(True,i % 2)
                winner.append(result)
                print("Winner of game", i, "was", result)

            p1 = [i for i in winner if i == "Player 1"]
            p2 = [i for i in winner if i == "Player 2"]
            #Print how many times each player wins
            print("Player 1 won", len(p1), "times")
            print("Player 2 won", len(p2), "times")

        #Exit the program
        if(userInp == 6):
            break
            
        pass