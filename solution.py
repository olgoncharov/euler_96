from sudoku_solver import Sudoku

solved = 0
result = 0

with open('p096_sudoku.txt', 'r') as f:
    line = f.readline()
    while line.startswith('Grid'):
        print(line.strip())
        matrix = [[int(ch) for ch in f.readline().strip()] for i in range(9)]
        sudoku = Sudoku(matrix)
        sudoku.solve()
        if sudoku.unsolved_cells == 0:
            solved += 1
            result += (sudoku.cells[0][0].value * 100 + sudoku.cells[0][1].value * 10 + sudoku.cells[0][2].value)
        print(sudoku)
        line = f.readline()

print(f'Решено {solved} судоку из 50')
print(f'Ответ: {result}')