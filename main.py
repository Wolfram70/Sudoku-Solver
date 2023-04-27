from sudoku_connections import SudokuConnections
import random


class SudokuBoard : 
    def __init__(self, size = 9) : 
        if size != 9 and size != 16:
            raise ValueError("Size can only be 9 or 16")

        self.size = size
        self.board = self.getDefaultBoard()
        
        self.sudokuGraph = SudokuConnections(self.size)
        self.mappedGrid = self.__getMappedMatrix() # Maps all the ids to the position in the matrix

    def __getMappedMatrix(self) : 
        matrix = [[0 for cols in range(self.size)]  for rows in range(self.size)]

        count = 1
        for rows in range(self.size) : 
            for cols in range(self.size):
                matrix[rows][cols] = count
                count+=1
        return matrix

    def getDefaultBoard(self) : 

        board = [[0 for cols in range(self.size)]  for rows in range(self.size)]
        return board

    def printBoard(self) : 
        
        if self.size == 16 :
            symbols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"]
            print("    1 2 3 4     5 6 7 8     9 A B C     D E F G")
            for i in range(len(self.board)) : 
                if i%4 == 0  :#and i != 0:
                    print("  - - - - - - - - - - - - - - - - - - - - - - - - ")

                for j in range(len(self.board[i])) : 
                    if j %4 == 0 :#and j != 0 : 
                        print(" |  ", end = "")
                    if j == 15 :
                        print(symbols[self.board[i][j]]," | ", symbols[i+1])
                    else : 
                        print(f"{ symbols[self.board[i][j]] } ", end="")
            print("  - - - - - - - - - - - - - - - - - - - - - - - - ")
        
        elif self.size == 9 :
            print("    1 2 3     4 5 6     7 8 9")
            for i in range(len(self.board)) : 
                if i%3 == 0  :#and i != 0:
                    print("  - - - - - - - - - - - - - - ")

                for j in range(len(self.board[i])) : 
                    if j %3 == 0 :#and j != 0 : 
                        print(" |  ", end = "")
                    if j == 8 :
                        print(self.board[i][j]," | ", i+1)
                    else : 
                        print(f"{ self.board[i][j] } ", end="")
            print("  - - - - - - - - - - - - - - ")

    def is_Blank(self) : 
        
        for row in range(len(self.board)) :
            for col in range(len(self.board[row])) : 
                if self.board[row][col] == 0 : 
                    return (row, col)
        return None

    def graphColoringInitializeColor(self):
        """
        fill the already given colors
        """
        color = [0] * (self.sudokuGraph.graph.totalV+1)
        given = [] # list of all the ids whos value is already given. Thus cannot be changed
        for row in range(len(self.board)) : 
            for col in range(len(self.board[row])) : 
                if self.board[row][col] != 0 : 
                    #first get the idx of the position
                    idx = self.mappedGrid[row][col]
                    #update the color
                    color[idx] = self.board[row][col] # this is the main imp part
                    given.append(idx)
        return color, given

    def solveGraphColoring(self, m =9) : 
        
        color, given = self.graphColoringInitializeColor()
        if self.__graphColorUtility(m =m, color=color, v =1, given=given) is None :
            print(":(")
            return False
        count = 1
        for row in range(self.size) : 
            for col in range(self.size) :
                self.board[row][col] = color[count]
                count += 1
        return color
    
    def __graphColorUtility(self, m, color, v, given) :
        
        if v == self.sudokuGraph.graph.totalV+1  : 
            return True
        safecolors = []
        for c in range(1, m+1):
            if self.__isSafe2Color(v, color, c, given) == True :
                safecolors.append(c)
        
        random.shuffle(safecolors)

        for c in safecolors :
            color[v] = c
            if self.__graphColorUtility(m, color, v+1, given) : 
                return True
            if v not in given : 
                color[v] = 0

    def __isSafe2Color(self, v, color, c, given) : 
        
        if v in given and color[v] == c: 
            return True
        elif v in given : 
            return False

        for i in range(1, self.sudokuGraph.graph.totalV+1) :
            if color[i] == c and self.sudokuGraph.graph.isNeighbour(v, i) :
                return False
        return True
    
    def getSudokuProblem(fraction = 0.2, size = 9):
        """
        generate a sudoku problem with given fraction of values missing
        """
        s = SudokuBoard(size)
        s.solveGraphColoring(size)
        #zero out some of the values (probability = fraction)
        for row in range(len(s.board)) :
            for col in range(len(s.board[row])) : 
                if random.random() < fraction : 
                    s.board[row][col] = 0
        return s.board
    
    def setBoard(self, board):
        self.board = board

    def checkBoard(self) : 
        """
        check if the problem is valid or not
        """
        for row in range(len(self.board)) : 
            for col in range(len(self.board[row])) : 
                if self.board[row][col] == 0 : 
                    continue
                if self.__checkRow(row, col) == False or self.__checkCol(row, col) == False or self.__checkSubGrid(row, col) == False :
                    return False
            return True
    
    def __checkRow(self, row, col) : 
        #utlity function to check if the row is valid or not
        for i in range(len(self.board[row])) : 
            if i == col : 
                continue
            if self.board[row][i] == self.board[row][col] : 
                return False
        return True
    
    def __checkCol(self, row, col) :
        #utility function to check if the col is valid or not
        for i in range(len(self.board)) : 
            if i == row : 
                continue
            if self.board[i][col] == self.board[row][col] : 
                return False
        return True
    
    def __checkSubGrid(self, row, col) :
        #utility function to check if the subgrid is valid or not
        if self.size == 9 : 
            if row < 3 : 
                row = 0
            elif row < 6 : 
                row = 3
            else : 
                row = 6
            if col < 3 : 
                col = 0
            elif col < 6 : 
                col = 3
            else : 
                col = 6
            for i in range(row, row+3) : 
                for j in range(col, col+3) : 
                    if i == row and j == col : 
                        continue
                    if self.board[i][j] == self.board[row][col] : 
                        return False
            return True
        elif self.size == 16 : 
            if row < 4 : 
                row = 0
            elif row < 8 : 
                row = 4
            elif row < 12 : 
                row = 8
            else : 
                row = 12
            if col < 4 : 
                col = 0
            elif col < 8 : 
                col = 4
            elif col < 12 : 
                col = 8
            else : 
                col = 12
            for i in range(row, row+4) : 
                for j in range(col, col+4) : 
                    if i == row and j == col : 
                        continue
                    if self.board[i][j] == self.board[row][col] : 
                        return False
            return True




def main() :
    #ask the user if they want to enter the problem or generate a random problem
    choice = int(input("Enter 1 to enter the problem yourself or 2 to generate a random problem : "))
    if choice != 1 and choice != 2 :
        print("Invalid choice")
        return
    #take input from the user for size of suduko board
    size = int(input("Enter the size of the sudoku board (9 or 16) : "))

    if choice == 1 :
        #take input from the user for the problem
        print("Enter the problem row wise with 0 for empty spaces")
        board = []
        for i in range(size) : 
            row = list(map(int, input().split()))
            board.append(row)
        s = SudokuBoard(size)
        s.setBoard(board)
        while s.checkBoard() == False :
            print("Invalid problem. Please enter again")
            board = []
            for i in range(size) : 
                row = list(map(int, input().split()))
                board.append(row)
            s.setBoard(board)
        print("\nBEFORE SOLVING ...")
        print("\n\n")
        s.printBoard()
        print("\nSolving ...")
        print("\n\n\nAFTER SOLVING ...")
        print("\n\n")
        s.solveGraphColoring(size)
        s.printBoard()

    if choice == 2 :
        #take input from the user for the fraction of the board to be filled
        fraction = float(input("Enter the dfficulty of the randomly generated problem (0.0 - 1.0) : "))
        s = SudokuBoard(size)
        print("\nBEFORE SOLVING ...")
        print("\n\n")
        s.setBoard(SudokuBoard.getSudokuProblem(fraction = fraction, size = size))
        s.printBoard()
        print("\nSolving ...")
        print("\n\n\nAFTER SOLVING ...")
        print("\n\n")
        s.solveGraphColoring(size)
        s.printBoard()

if __name__ == "__main__" : 
    main()
