from typing import Set, Any

import pytest
from sudoku_solver import Cell, Sudoku

class TestCell:

    def test_init_empty(self, full_choices):
        result = Cell()
        assert result.value == 0
        assert result.choices == full_choices
        assert result.idx_row == 0
        assert result.idx_col == 0
        assert result.idx_square == 0

    def test_init_zero(self, full_choices):
        result = Cell(0)
        assert result.value == 0
        assert result.choices == full_choices

    @pytest.mark.parametrize('value, idx_row, idx_col, idx_square', [(1, 0, 1, 0), (5, 4, 4, 4), (9, 6, 1, 6)])
    def test_init_valid(self, value, idx_row, idx_col, idx_square):
        result = Cell(value, idx_row, idx_col)
        assert result.value == value
        assert result.choices == set()
        assert result.idx_row == idx_row
        assert result.idx_col == idx_col
        assert result.idx_square == idx_square

    @pytest.mark.parametrize('value', [-1, 10, 20])
    def test_init_invalid_int(self, value):
        with pytest.raises(ValueError):
            result = Cell(value)

    def test_init_not_int(self):
        with pytest.raises(TypeError):
            result = Cell('fooo')

class TestSudoku:

    init_sudoku_columns = [
        (0, [0, 9, 0, 0, 7, 0, 0, 8, 0]),
        (1, [0, 0, 0, 0, 0, 0, 0, 0, 0]),
        (2, [3, 0, 1, 8, 0, 6, 2, 0, 5]),
        (3, [0, 3, 8, 1, 0, 7, 6, 2, 0]),
        (4, [2, 0, 0, 0, 0, 0, 0, 0, 1]),
        (5, [0, 5, 6, 2, 0, 8, 9, 3, 0]),
        (6, [6, 0, 4, 9, 0, 2, 5, 0, 3]),
        (7, [0, 0, 0, 0, 0, 0, 0, 0, 0]),
        (8, [0, 1, 0, 0, 8, 0, 0, 9, 0])
    ]

    init_sudoku_squares = [
        (0, [0, 0, 3, 9, 0, 0, 0, 0, 1]),
        (1, [0, 2, 0, 3, 0, 5, 8, 0, 6]),
        (2, [6, 0, 0, 0, 0, 1, 4, 0, 0]),
        (3, [0, 0, 8, 7, 0, 0, 0, 0, 6]),
        (4, [1, 0, 2, 0, 0, 0, 7, 0, 8]),
        (5, [9, 0, 0, 0, 0, 8, 2, 0, 0]),
        (6, [0, 0, 2, 8, 0, 0, 0, 0, 5]),
        (7, [6, 0, 9, 2, 0, 3, 0, 1, 0]),
        (8, [5, 0, 0, 0, 0, 9, 3, 0, 0])
    ]

    def test_init(self, init_sudoku, init_sudoku_choices):
        sudoku = Sudoku(init_sudoku)
        assert sudoku.unsolved_cells == 49
        for i in range(9):
            for j in range(9):
                assert isinstance(sudoku.cells[i][j], Cell)
                assert sudoku.cells[i][j].value == init_sudoku[i][j]
                assert sudoku.cells[i][j].choices == init_sudoku_choices[i][j], str(f'{i}, {j}')

    @pytest.mark.parametrize('idx, expected', init_sudoku_columns)
    def test_column(self, init_sudoku, idx, expected):
        sudoku = Sudoku(init_sudoku)
        assert [cell.value for cell in sudoku.column(idx)] == expected

    @pytest.mark.parametrize('idx, expected', init_sudoku_squares)
    def test_square(self, init_sudoku, idx, expected):
        sudoku = Sudoku(init_sudoku)
        assert [cell.value for cell in sudoku.square(idx)] == expected

    def test_set_value(self, init_sudoku):
        sudoku = Sudoku(init_sudoku)
        sudoku.set_value(0, 0, 4)
        assert sudoku.unsolved_cells == 48
        assert sudoku.cells[0][0].value == 4
        assert sudoku.cells[0][0].choices == set()
        assert sudoku.cells[0][1].choices == {5, 7, 8}
        assert sudoku.cells[0][3].choices == {9}
        assert sudoku.cells[3][0].choices == {3, 5}
        assert sudoku.cells[8][0].choices == {6}
        assert sudoku.cells[1][1].choices == {2, 6, 7, 8}
        assert sudoku.cells[1][2].choices == {7}

    def test_solve_naked_pairs(self):

        sudoku = Sudoku([
            [4, 0, 0, 0, 0, 0, 9, 3, 8],
            [0, 3, 2, 0, 9, 4, 1, 0, 0],
            [0, 9, 5, 3, 0, 0, 2, 4, 0],
            [3, 7, 0, 6, 0, 9, 0, 0, 4],
            [5, 2, 9, 0, 0, 1, 6, 7, 3],
            [6, 0, 4, 7, 0, 3, 0, 9, 0],
            [9, 5, 7, 0, 0, 8, 3, 0, 0],
            [0, 0, 3, 9, 0, 0, 4, 0, 0],
            [2, 4, 0, 0, 3, 0, 7, 0, 9]
        ])

        assert sudoku.cells[0][1].choices == {1, 6}
        assert sudoku.cells[0][2].choices == {1, 6}
        assert sudoku.cells[0][3].choices == {1, 2, 5}
        assert sudoku.cells[0][4].choices == {1, 2, 5, 6, 7}
        assert sudoku.cells[0][5].choices == {2, 5, 6, 7}
        assert sudoku.cells[1][0].choices == {7, 8}
        assert sudoku.cells[2][0].choices == {1, 7, 8}
        assert sudoku.cells[2][4].choices == {1, 6, 7, 8}
        assert sudoku.cells[2][5].choices == {6, 7}
        assert sudoku.cells[2][8].choices == {6, 7}
        assert sudoku.cells[3][2].choices == {1, 8}
        assert sudoku.cells[3][4].choices == {2, 5, 8}
        assert sudoku.cells[5][4].choices == {2, 5, 8}
        assert sudoku.cells[3][6].choices == {5, 8}
        assert sudoku.cells[3][7].choices == {1, 2, 5, 8}

        sudoku.solve_naked_pairs()

        assert sudoku.cells[0][1].choices == {1, 6}
        assert sudoku.cells[0][2].choices == {1, 6}
        assert sudoku.cells[0][3].choices == {2, 5}
        assert sudoku.cells[0][4].choices == {7}
        assert sudoku.cells[0][5].choices == {2, 5, 7}
        assert sudoku.cells[1][0].choices == {7}
        assert sudoku.cells[2][0].choices == {8}
        assert sudoku.cells[2][4].choices == {1, 8}
        assert sudoku.cells[2][5].choices == {6, 7}
        assert sudoku.cells[2][8].choices == {6, 7}
        assert sudoku.cells[3][2].choices == {1, 8}
        assert sudoku.cells[3][4].choices == {2, 5}
        assert sudoku.cells[5][4].choices == {2, 5}
        assert sudoku.cells[3][6].choices == {5, 8}
        assert sudoku.cells[3][7].choices == {1, 2}

    def test_solve_lone_singles(self, init_sudoku, init_sudoku_solution):
        sudoku = Sudoku(init_sudoku)
        sudoku.solve_lone_singles()

        empty_set = set()
        for i in range(9):
            for j in range(9):
                assert sudoku.cells[i][j].value == init_sudoku_solution[i][j], f'({i}, {j})'
                assert sudoku.cells[i][j].choices == empty_set

    def test_solve_hidden_singles(self):

        sudoku = Sudoku([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0]
        ])

        sudoku.solve_hidden_singles()
        assert sudoku.cells[4][4].value == 2

    def test_solve_hidden_pairs(self):

        sudoku = Sudoku([
            [0, 6, 0, 3, 9, 0, 1, 0, 0],
            [0, 0, 3, 1, 5, 0, 0, 9, 0],
            [1, 9, 0, 4, 2, 6, 3, 0, 0],
            [8, 3, 0, 5, 7, 9, 4, 1, 0],
            [9, 0, 0, 0, 6, 1, 0, 0, 0],
            [0, 5, 1, 0, 4, 3, 0, 0, 9],
            [4, 1, 9, 6, 3, 5, 8, 2, 7],
            [0, 2, 0, 9, 8, 4, 5, 0, 1],
            [0, 8, 0, 7, 1, 2, 9, 4, 0]
        ])

        sudoku.solve_hidden_pairs()

        assert sudoku.cells[4][7].choices == {3, 5}
        assert sudoku.cells[4][8].choices == {3, 5}