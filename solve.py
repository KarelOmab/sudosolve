class Block:
    def __init__(self, cells):
        self.cells = cells
    
    # get numeric values inside block that are missing (blanks)
    # TODO : make it prettier & more efficient
    def get_missing_values(self):
        missing = [x for x in range(1, 10)]
        for c in self.cells:
            if c.value != 0:
                missing.remove(c.value)
        return missing

    
    def __str__(self):
        s = []
        # create blocks from board
        for j in range(0, 9, 3):
            r = self.cells[j:j+3]
            s.append(" ".join(map(str, r)))
        return "\n".join(s)       

class Cell:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.flag = True
    
    def __str__(self):
        return "row:{}, col:{}, val:{}".format(self.row, self.col, self.value)

class Board:

    rows = []   # not set because indexing is important
    cols = []   # not set because indexing is important
    blocks = [] # (9 element cell array of 3x3 blocks)
    

    def __init__(self, board):
        self.board = board
        
        # create blocks from board
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                cells = []
                for k in range(3):
                    for l in range(3):
                        cells.append(self.board[i+k][j+l])
                self.blocks.append(Block(cells))

    # returns 0 on completed board
    # TODO: returns -1 on invalid state
    # TODO: returns 1 on empty cell
    def eval_board_state(self, verbose=True):
        # check if the board is completed
        is_blocks_completed = True
        #check all blocks
        for block in self.blocks:
            buff = set()
            for cell in block.cells:
                if cell.value != 0:
                    buff.add(cell.value)
            
            if len(buff) != 9:
                is_blocks_completed = False

        if verbose:
            print("is_blocks_completed", is_blocks_completed)

        is_rows_completed = True
        #check all rows
        for i in range(9):
            block = self.board[i]

            buff = set()
            for cell in block:
                if cell.value != 0:
                    buff.add(cell.value)
            
            if len(buff) != 9:
                is_rows_completed = False
        
        if verbose:
            print("is_rows_completed", is_rows_completed)

        is_cols_completed = True
        #check all cols
        for i in range(9):
            
            block = [self.board[0][i] for i in range(9)]

            buff = set()
            for cell in block:
                if cell.value != 0:
                    buff.add(cell.value)
            
            if len(buff) != 9:
                is_cols_completed = False
        
        if verbose:
            print("is_cols_completed", is_cols_completed)

        if all([is_blocks_completed, is_rows_completed, is_cols_completed]):
            return 0

    
    def eval_cell_value(self, cell, value):
        #check if (horizontal) row contains value
        cell.flag = False   #reset flag
        for c in self.board[cell.row]:
            if c.value == value:
                cell.flag = True
                break

        #check if (vertical) column contains value
        if not cell.flag:
            for i in range(len(self.board)):
                if self.board[i][cell.col].value == value:
                    cell.flag = True
                    break
    
    # write a function that takes in a board state and returns a solved board
    # if the board is invalid, return an error
    def solve_board(self):
        state = self.eval_board_state()

        while state != 0:
            self.next_move()
            state = self.eval_board_state() # this can be done more efficiently

        self.show()
        
        if state == 0:
            print("Solved!")
        elif state == -1:
            print("Invalid board state!")


    # this is the money maker
    def next_move(self):
        #print("new move")
        # pick a cell that contains a number, attempt to solve it

        # create a dictionary that stores block indexes and the amount of blanks in them
        d = dict()
        for i in range(len(self.blocks)):
            for c in self.blocks[i].cells:
                if c.value == 0:
                    if i in d:
                        d[i] += 1
                    else:
                        d[i] = 1

        #print(d)
        # iterate through (sorted) blocks based on most filled first (0 frequency lowest)
        for key, value in sorted(d.items(), key=lambda item: item[1]):

            block = self.blocks[key]
            
            #print(block)

            # get missing values
            #print("---- checking block " + str(key) + " --------")
            #print(block.get_missing_values())

            for v in block.get_missing_values():
                buff = []
                for c in block.cells:
                    if c.value == 0:
                        self.eval_cell_value(c, v)

                        if not c.flag:
                            buff.append(c)

                #print(len(buff), buff)

                if len(buff) == 1:
                    # guaranteed move
                    #print("guaranteed move!", buff[0], "->", v)
                    self.board[buff[0].row][buff[0].col].value = v
                    #self.show()
                    #input()
                    
                    return

                else:
                    # not guaranteed - make a guess?
                    pass

            #input()

        #input()

        
            

        print("No move possible?")
        self.show()
        self.eval_board_state()
        input()

        # is the board solved?

        #self.show()
        #input()
        #pass

    def show(self):
        print(self)

    def __str__(self):
        s = []
        for i in range(len(self.board)):
            buff = []
            for j in range(len(self.board[0])):
                buff.append(str(self.board[i][j].value))
            s.append("\t".join(buff))
        return "\n\n".join(s)

    

# given a state of a sudoku board
# 1. determine if the board is valid
# 2. if the board is valid, find solution
# 3. if the board is not valid, return error

invalid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 8, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [5, 0, 0, 0, 8, 0, 0, 7, 9]
]

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solved = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

cell_board = []

for i in range(len(board)):
    buff = []
    for j in range(len(board[i])):
        buff.append(Cell(i, j, board[i][j]))
    cell_board.append(buff)




b = Board(cell_board)

#b.show()
b.solve_board()
#print(b.eval_state())
   




