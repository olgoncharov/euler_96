
class Sudoku:
    """
    Класс головоломки судоку.

    Атрибуты
    --------
    cells: list
        Матрица, состоящая из объектов Cell. Представлена в виде списка из 9 вложенных списков, содержащих
        по 9 объектов Cell.
    """
    def __init__(self, content_matrix):

        self.cells = []

        for row in content_matrix:
            self.cells.append([])
            for value in row:
                self.cells[-1].append(Cell(value))

        self._update_all_choices()

    def __repr__(self):
        result = '---+' * 8 + '---\n'
        for i in range(3):
            for idx_row in range(3 * i, 3 * i + 3):
                row = [str(cell.value) if cell.value != 0 else 'X' for cell in self.cells[idx_row]]
                result += ' {}   {}   {} | {}   {}   {} | {}   {}   {} \n'.format(*row)
                if idx_row != 3 * i + 2:
                    result += '{}+{}+{}\n'.format(' ' * 11, ' ' * 11, ' ' * 11)
            result += '---+' * 8 + '---\n'

        return result

    def _update_all_choices(self):
        """Для каждой ячейки судоку обновляет перечень возможных вариантов для заполнения."""

        full_set = set(range(1, 10))
        rows_choices = []
        for row in self.cells:
            filled = {cell.value for cell in row if cell.value != 0}
            rows_choices.append(full_set - filled)

        column_choices = []
        for i in range(9):
            filled = {cell.value for cell in self.column(i) if cell.value != 0}
            column_choices.append(full_set - filled)

        square_choices = []
        for i in range(9):
            filled = {cell.value for cell in self.square(i) if cell.value != 0}
            square_choices.append(full_set - filled)

        for i in range(3):
            for idx_row in range(3 * i, 3 * i + 3):
                row = self.cells[idx_row]
                for j in range(3):
                    for idx_col in range(3 * j, 3 * j + 3):
                        idx_square = i * 3 + j
                        cell = row[idx_col]
                        if cell.value == 0:
                            cell.choices = rows_choices[idx_row] & \
                                                   column_choices[idx_col] & \
                                                   square_choices[idx_square]

    def column(self, idx):
        """Возвращает итератор, предоставляющий доступ к ячейкам столбца.
        :param idx: integer
            Индекс столбца (0 - 8).
        """
        if idx not in range(9):
            raise ValueError

        for row in self.cells:
            yield row[idx]

    def square(self, idx):
        """
        Возвращает итератор, предоставляющий доступ к ячейкам квадрата.
        :param idx: integer
            Индекс квадрата (0 - 8).
        """
        if idx not in range(9):
            raise ValueError

        if idx < 3:
            start_row = 0
        elif idx < 6:
            start_row = 3
        else:
            start_row = 6

        start_col = 3 * (idx % 3)

        for row in self.cells[start_row : start_row + 3]:
            for cell in row[start_col : start_col + 3]:
                yield cell

    def set_value(self, idx_row, idx_col, value):
        """
        Устанавливает значение ячейки на пересечении заданной строки и колонки.
        :param idx_row: integer
            Индекс строки (0 - 8).
        :param idx_col: integer
            Индекс колонки (0 - 8).
        :param value: integer
            Устанавливаемое значение ячейки (1 - 9)
        """

        self.cells[idx_row][idx_col].value = value
        self.cells[idx_row][idx_col].choices = set()

        Sudoku.exclude_from_choices(self.cells[idx_row], value)
        Sudoku.exclude_from_choices(self.column(idx_col), value)

        idx_square = (idx_row // 3) * 3 + idx_col // 3
        Sudoku.exclude_from_choices(self.square(idx_square), value)


    @staticmethod
    def exclude_from_choices(cells, value):
        for cell in cells:
            if value in cell.choices:
                cell.choices.remove(value)

class Cell:
    """
    Класс ячейки судоку.

    Атрибуты
    --------
    value: integer
        Значение в ячейке. Может равняться 0, если значение еще не разгадано, либо числу от 1 до 9.
    choices: set
        Содержит перечень возможных значений для заполнения в ячейке. Если ячейка разгадана, то содержит пустое
        множество.
    """
    def __init__(self, value=None):

        if value is None:
            self.value = 0
        else:
            if not isinstance(value, int):
                raise TypeError('Значением ячейки может быть только целое число')
            elif value not in range(10):
                raise ValueError('Значение ячейки должно находится в интервале 0-9')
            self.value = int(value)

        if self.value:
            self.choices = set()
        else:
            self.choices = set(range(1, 10))
