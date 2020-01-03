import pytest
from sudoku_solver import Cell, Sudoku

class TestCell:

    def test_init_empty(self, full_choices):
        result = Cell()
        assert result.value == 0
        assert result.choices == full_choices

    def test_init_zero(self, full_choices):
        result = Cell(0)
        assert result.value == 0
        assert result.choices == full_choices

    @pytest.mark.parametrize('value', [1, 5, 9])
    def test_init_valid(self, value):
        result = Cell(value)
        assert result.value == value
        assert result.choices == set()

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