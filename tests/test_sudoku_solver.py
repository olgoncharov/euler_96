import pytest
from sudoku_solver import Cell

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
