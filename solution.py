from sudoku_solver import Sudoku

with open('p096_sudoku.txt', 'r') as f:
    line = f.readline()
    while line.startswith('Grid'):
        print(line)
        matrix = [[int(ch) for ch in f.readline().strip()] for i in range(9)]
        sudoku = Sudoku(matrix)
        print(sudoku)
        line = f.readline()