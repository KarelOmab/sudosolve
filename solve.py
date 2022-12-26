class Block:
    def __init__(self, cells):
        self.cells = cells

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

    def __init__(self, board):
        self.board = board

    # get numeric values inside block that are missing (blanks)
    # TODO : make it prettier & more efficient
    def get_missing_cell_values(self, cells):
        missing = [x for x in range(1, 10)]
        for c in cells:
            if c.value != 0:
                missing.remove(c.value)
        return missing

    # create blocks from board
    def get_blocks(self):
        blocks = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                cells = []
                for k in range(3):
                    for l in range(3):
                        cells.append(self.board[i+k][j+l])
                blocks.append(Block(cells))
        return blocks
    
    # get rows from board
    # returns a list of type Cell
    def get_rows(self):
        rows = []
        
        for i in range(9):
            row = []
            for j in range(9):
                row.append(self.board[i][j])    
            rows.append(row)
        return rows
    
    # get cols from board
    # returns a list of type Cell
    def get_cols(self):
        cols = []
        
        for i in range(9):
            col = []
            for j in range(9):
                col.append(self.board[j][i])    
            cols.append(col)
        return cols


    # returns 0 on completed board
    # TODO: returns -1 on invalid state
    # TODO: returns 1 on empty cell
    def eval_board_state(self, verbose=True):
        # check if the board is completed
        is_blocks_completed = True
        #check all blocks
        for block in self.get_blocks():
            buff = []
            for cell in block.cells:
                if cell.value != 0:
                    buff.append(cell.value)
                if buff.count(cell.value) > 1:
                    if verbose:
                        print("Value conflict -> invalid board state!")
                    return -1
            
            if len(set(buff)) != 9:
                is_blocks_completed = False

        if verbose:
            print("is_blocks_completed", is_blocks_completed)

        is_rows_completed = True
        #check all rows
        for i in range(9):
            block = self.board[i]

            buff = []
            for cell in block:
                if cell.value != 0:
                    buff.append(cell.value)
                if buff.count(cell.value) > 1:
                    if verbose:
                        print("Value conflict -> invalid board state!")
                    return -1
            
            if len(set(buff)) != 9:
                is_rows_completed = False
        
        if verbose:
            print("is_rows_completed", is_rows_completed)

        is_cols_completed = True
        #check all cols
        for i in range(9):
            
            block = [self.board[0][i] for i in range(9)]

            buff = []
            for cell in block:
                if cell.value != 0:
                    buff.append(cell.value)
                if buff.count(cell.value) > 1:
                    if verbose:
                        print("Value conflict -> invalid board state!")
                    return -1
            
            if len(set(buff)) != 9:
                is_cols_completed = False
        
        if verbose:
            print("is_cols_completed", is_cols_completed)

        if all([is_blocks_completed, is_rows_completed, is_cols_completed]):
            return 0    # board is finished
        else: return 1  # still empty cells

    
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

        while state == 1:
            self.next_move()
            state = self.eval_board_state() # this can be done more efficiently

        self.show()
        
        if state == 0:
            print("Solved!")
        elif state == -1:
            print("Invalid board state!")
        
        return state

     # create a dictionary that stores block indexes and the amount of blanks in them
    def count_blanks_in_blocks(self):
        d = dict()
        for i in range(len(self.get_blocks())):
            for c in self.get_blocks()[i].cells:
                if c.value == 0:
                    if i in d:
                        d[i] += 1
                    else:
                        d[i] = 1
        return d
    
    # create a dictionary that stores row indexes and the amount of blanks in them
    def count_blanks_in_rows(self):
        d = dict()
        
        for i in range(9):
            for j in range(9):
                c = self.board[i][j]
                #print(type(self.board[i][j]), self.board[i][j])
                if c.value == 0:
                    if i in d:
                        d[i] += 1
                    else:
                        d[i] = 1
        return self.get_dict_min_count(d)

    # create a dictionary that stores col indexes and the amount of blanks in them
    def count_blanks_in_cols(self):
        d = dict()
        
        for i in range(9):
            for j in range(9):
                c = self.board[j][i]
                #print(type(self.board[i][j]), self.board[i][j])
                if c.value == 0:
                    if i in d:
                        d[i] += 1
                    else:
                        d[i] = 1
        return self.get_dict_min_count(d)

    def get_dict_min_count(self, dict):
        mi = (10, 10)   #value and index
        for k, v in dict.items():
            if v < mi[0]:
                mi = (v, k)
        
        return mi
    
    def guess(self):
        # logic to create a copy of valid board state and brute force solutions
        import copy
        valid_board_state = copy.deepcopy(self)

        # find block / row / column that has most solved cells
        # make a guess and try to solve, if fails try backtracking...

        min_blanks_block = self.get_dict_min_count(self.count_blanks_in_blocks()) + ("block",)
        min_blanks_row = self.count_blanks_in_rows() + ("row",)
        min_blanks_col = self.count_blanks_in_cols() + ("col",)

        arr = [min_blanks_block, min_blanks_row, min_blanks_col]
        mi = min(arr)     

        if mi[2] == "block":
            #guess within a block
            block = self.get_blocks()[mi[1]]    #Block obj
            cells = [c for c in block.cells]
            missing = self.get_missing_cell_values(cells)

            for c in cells:
                if c.value == 0:
                    for m in missing:
                        c.value = m
                        res = self.solve_board()

                        if res == 0:
                            return

        elif mi[2] == "row":
            row = self.get_rows()[mi[1]]    #row of cells
            missing = self.get_missing_cell_values(row)

            for c in row:
                if c.value == 0:
                    for m in missing:
                        c.value = m
                        res = self.solve_board()

                        if res == 0:
                            return

        elif mi[2] == "col":
            col = self.get_cols()[mi[1]]    #row of cells
            missing = self.get_missing_cell_values(col)

            for c in col:
                if c.value == 0:
                    for m in missing:
                        c.value = m
                        res = self.solve_board()

                        if res == 0:
                            return
                
                        


    # this is the money maker
    def next_move(self):
        #print("new move")
        # pick a cell that contains a number, attempt to solve it

        
        d = self.count_blanks_in_blocks()

        # iterate through (sorted) blocks based on most filled first (0 frequency lowest)
        for key, value in sorted(d.items(), key=lambda item: item[1]):

            block = self.get_blocks()[key]
            
            for v in self.get_missing_cell_values(block.cells):
                buff = []
                for c in block.cells:
                    if c.value == 0:
                        self.eval_cell_value(c, v)

                        if not c.flag:
                            buff.append(c)

                if len(buff) == 1:
                    # guaranteed move
                    self.board[buff[0].row][buff[0].col].value = v
                    return

        self.guess()

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

# read board from text file
board = []
f = open("/Users/karelomab/Documents/GitHub/sudosolve/board.txt", "r")
for line in f:
  arr = line.strip().split(' ')
  board.append(list(map(int,arr)))

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
   




