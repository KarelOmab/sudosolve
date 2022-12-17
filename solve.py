class Board:

    rows = []
    cols = []

    def __init__(self, board):
        self.board = board

        for col in range(9):
            vertical_row = [row[col] for row in self.board]
            self.cols.append(vertical_row)
        
        for row in self.board:
            self.rows.append(row)
    
    # evaluate all columns vertically
    def eval_cols(self):
        res = []
        for col in self.cols:
            self.eval_row(col)
        return res 

    # evaluate all rows horizontally
    def eval_rows(self):
        res = []
        for row in self.rows:
            res.append(self.eval_row(row))
        return res  

    # returns -1 on error
    # returns 0 on incomplete
    # return 1 on complete
    def eval_row(self, arr):
        #check for error (more than one of the same number)
        is_incomplete = False
        for a in arr:
            if a != 0 and arr.count(a) > 1:
                return -1
            if a == 0:
                is_incomplete = True
        
        return 0 if is_incomplete else 1   # complete 
    
    def eval_state(self):
        if -1 in self.rows or -1 in self.cols:
            return "invalid board"

        if self.rows.count(1) == 9 and self.cols.count(1) == 9:
            return "solved board"
        else:
            return "unsolved board"
    
    # write a function that takes in a board state and returns a solved board
    # if the board is invalid, return an error
    def solve_board(self):
        while (self.eval_state() != "solved board"):
            self.next_move()

    def next_move(self):
        # pick a cell that contains a number, attempt to solve it
        pass

    def __str__(self):
        s = []
        for row in self.rows:
            buff = []
            for col in row:
                buff.append(str(col))
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










                         
    

# driver code
#r = eval_rows(invalid)
#c = eval_cols(invalid)
#eval_rows_cols(r, c)


#r = eval_rows(solved)
#c = eval_cols(solved)
#eval_rows_cols(r, c)

b = Board(board)

print(b)
#print(b.eval_state())
   




