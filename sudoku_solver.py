
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

        for i in range(9):
            self.cells.append([])
            for j in range(9):
                self.cells[-1].append(Cell(content_matrix[i][j], i, j))

        full_set = set(range(1, 10))
        rows_choices = [full_set - {cell.value for cell in row if cell.value != 0} for row in self.cells]
        column_choices = [full_set - {cell.value for cell in self.column(idx) if cell.value != 0} for idx in range(9)]
        square_choices = [full_set - {cell.value for cell in self.square(idx) if cell.value != 0} for idx in range(9)]

        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    cell.choices = rows_choices[cell.idx_row] & \
                                   column_choices[cell.idx_col] & \
                                   square_choices[cell.idx_square]

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

    def column(self, idx):
        """Возвращает ячейки столбца.
        :param idx: integer
            Индекс столбца (0 - 8).
        """
        if idx not in range(9):
            raise ValueError

        return [row[idx] for row in self.cells]

    def square(self, idx):
        """
        Возвращает ячейки квадрата.
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

        result = []
        for row in self.cells[start_row:start_row + 3]:
            for cell in row[start_col:start_col + 3]:
                result.append(cell)

        return result

    def houses(self):
        """
        Генератор для обхода всех блоков судоку - сначала всех строк, потом всех столбцов, потом все квадратов.
        """
        for row in self.cells:
            yield row

        for idx in range(9):
            yield self.column(idx)

        for idx in range(9):
            yield self.square(idx)

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
        idx_square = (idx_row // 3) * 3 + idx_col // 3

        adjoined_cells = self.cells[idx_row] + [cell for cell in self.column(idx_col)] + \
                         [cell for cell in self.square(idx_square)]

        for cell in adjoined_cells:
            if value in cell.choices:
                cell.choices.remove(value)

    def solve_naked_pairs(self):
        """Находит голые пары и обновляет перечень кандидатов в ячейках."""

        updated_cells = 1

        while updated_cells:
            updated_cells = 0
            for house in self.houses():
                pairs = [cell.choices for cell in house if len(cell.choices) == 2]
                naked_pairs = []

                for i in range(len(pairs)):
                    for j in range(i + 1, len(pairs)):
                        if pairs[i] == pairs[j]:
                            naked_pairs.append(pairs[i])
                            break

                for cell in house:
                    for pair in naked_pairs:
                        if cell.choices != pair and not cell.choices.isdisjoint(pair):
                            updated_cells += 1
                            cell.choices -= pair

    def solve_hidden_singles(self):
        """Находит и заполняет скрытые одиночки."""
        solved_cells = 1

        while solved_cells:
            solved_cells = 0
            for house in self.houses():
                for cell in house:
                    if len(cell.choices) == 1:
                        self.set_value(cell.idx_row, cell.idx_col, cell.choices.pop())
                        solved_cells += 1

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
    idx_row: integer
        Индекс строки судоку, которой принадлежит ячейка.
    idx_col: integer
        Индекс столбца судоку, которому принадлежит ячейка.
    idx_square: integer
        Индекс квадрата судоку, которому принадлежит ячейка.
    """
    def __init__(self, value=None, idx_row=0, idx_col=0):

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

        self.idx_row = idx_row
        self.idx_col = idx_col
        self.idx_square = (idx_row // 3) * 3 + idx_col // 3
