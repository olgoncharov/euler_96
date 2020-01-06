import collections
import copy

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
        self.unsolved_cells = 0

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
                    self.unsolved_cells += 1
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
        self.unsolved_cells -= 1
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

    def solve_hidden_pairs(self):
        """Находит скрытые пары и обновляет перечень кандидатов в ячейках."""
        updated_cells = 1

        while updated_cells:
            updated_cells = 0
            for cells in self.houses():
                counter_pairs = collections.Counter()
                counter_digits = collections.Counter()
                for cell in cells:
                    ls_choices = list(cell.choices)
                    for i in range(len(ls_choices)):
                        counter_digits[ls_choices[i]] += 1
                        for j in range(i + 1, len(ls_choices)):
                            counter_pairs[(ls_choices[i], ls_choices[j])] += 1

                hidden_pairs = [set(key) for key, value in counter_pairs.items() if value == 2 and
                                counter_digits[key[0]] == 2 and counter_digits[key[1]] == 2]

                for cell in cells:
                    for pair in hidden_pairs:
                        if len(cell.choices) > 2 and pair <= cell.choices:
                            cell.choices = cell.choices & pair
                            updated_cells += 1


    def solve_naked_singles(self):
        """Находит и заполняет голые одиночки."""
        solved_cells = 1

        while solved_cells:
            solved_cells = 0
            for house in self.houses():
                for cell in house:
                    if len(cell.choices) == 1:
                        self.set_value(cell.idx_row, cell.idx_col, cell.choices.pop())
                        solved_cells += 1

    def solve_hidden_singles(self):

        solved_cells = 1

        while solved_cells:
            solved_cells = 0
            for cells in self.houses():
                for i in range(9):
                    reminder_set = cells[i].choices.copy()
                    for j in range(9):
                        if j == i:
                            continue
                        reminder_set -= cells[j].choices

                    if len(reminder_set) == 1:
                        self.set_value(cells[i].idx_row, cells[i].idx_col, reminder_set.pop())
                        solved_cells += 1

    def solve_intersection_removal(self):

        solved = 1

        while solved:
            solved = 0

            # 1. Обходим квадраты
            for idx in range(9):
                cells = self.square(idx)

                rows_choices = [set(), set(), set()]
                cols_choices = [set(), set(), set()]

                min_row = cells[0].idx_row
                min_col = cells[0].idx_col

                for cell in cells:
                    rows_choices[cell.idx_row - min_row] |= cell.choices
                    cols_choices[cell.idx_col - min_col] |= cell.choices

                rows_unique = copy.deepcopy(rows_choices)
                cols_unique = copy.deepcopy(cols_choices)

                for i in range(3):
                    for j in range(3):
                        if i == j:
                            continue
                        rows_unique[i] -= rows_choices[j]
                        cols_unique[i] -= cols_choices[j]

                for i in range(3):
                    while len(rows_unique[i]) > 0:
                        value = rows_unique[i].pop()
                        idx_row = min_row + i
                        for c in self.cells[idx_row]:
                            if c.idx_square != idx and value in c.choices:
                                c.choices.remove(value)
                                solved += 1

                    while len(cols_unique[i]) > 0:
                        value = cols_unique[i].pop()
                        idx_col = min_col + i
                        for c in self.column(idx_col):
                            if c.idx_square != idx and value in c.choices:
                                c.choices.remove(value)
                                solved += 1

            # Обходим строки
            for idx in range(9):
                square_choices = [set(), set(), set()]
                min_square = self.cells[idx][0].idx_square

                for cell in self.cells[idx]:
                    square_choices[cell.idx_square - min_square] |= cell.choices

                square_unique = copy.deepcopy(square_choices)
                for i in range(3):
                    for j in range(3):
                        if i == j:
                            continue
                        square_unique[i] -= square_choices[j]

                for i in range(3):
                    while len(square_unique[i]) > 0:
                        value = square_unique[i].pop()
                        idx_square = min_square + i
                        for c in self.square(idx_square):
                            if c.idx_row != idx and value in c.choices:
                                c.choices.remove(value)
                                solved += 1

            # Обходим столбцы
            for idx in range(9):
                square_choices = [set(), set(), set()]
                cells = self.column(idx)
                min_square = cells[0].idx_square

                for cell in cells:
                    if cell.idx_square == min_square:
                        square_choices[0] |= cell.choices
                    elif (cell.idx_square - min_square) == 3:
                        square_choices[1] |= cell.choices
                    else:
                        square_choices[2] |= cell.choices

                square_unique = copy.deepcopy(square_choices)
                for i in range(3):
                    for j in range(3):
                        if i == j:
                            continue
                        square_unique[i] -= square_choices[j]

                for i in range(3):
                    while len(square_unique[i]) > 0:
                        value = square_unique[i].pop()
                        if i == 0:
                            idx_square = min_square
                        elif i == 1:
                            idx_square = min_square + 3
                        else:
                            idx_square = min_square + 6

                        for c in self.square(idx_square):
                            if c.idx_col != idx and value in c.choices:
                                c.choices.remove(value)
                                solved += 1

    def solve_x_wing(self):
        """Находит связанные пары и обновляет перечень кандидатов в ячейках."""

        solved = 1

        while solved:
            solved = 0
            row_counters = [dict() for i in range(9)]
            col_counters = copy.deepcopy(row_counters)

            for row in self.cells:
                for cell in row:
                    for value in cell.choices:
                        row_counters[cell.idx_row].setdefault(value, [])
                        col_counters[cell.idx_col].setdefault(value, [])
                        row_counters[cell.idx_row][value].append(cell.idx_col)
                        col_counters[cell.idx_col][value].append(cell.idx_row)

            row_pairs = [{k for k,v in row_counters[i].items() if len(v) == 2} for i in range(9)]
            col_pairs = [{k for k,v in col_counters[i].items() if len(v) == 2} for i in range(9)]

            for i in range(9):
                for j in range(i + 1, 9):
                    # связанные пары по строкам
                    common_pairs = row_pairs[i] & row_pairs[j]
                    for value in common_pairs:
                        if row_counters[i][value] == row_counters[j][value]:
                            for idx_col in row_counters[i][value]:
                                for cell in self.column(idx_col):
                                    if cell.idx_row not in [i, j] and value in cell.choices:
                                        cell.choices.remove(value)
                                        solved += 1

                    # связанные пары по столбцам
                    common_pairs = col_pairs[i] & col_pairs[j]
                    for value in common_pairs:
                        if col_counters[i][value] == col_counters[j][value]:
                            for idx_row in col_counters[i][value]:
                                for cell in self.cells[idx_row]:
                                    if cell.idx_col not in [i, j] and value in cell.choices:
                                        cell.choices.remove(value)
                                        solved += 1


    def solve(self):
        """Решает судоку."""
        solved = 1

        while solved:
            unsolved_before = self.unsolved_cells

            self.solve_naked_pairs()
            self.solve_hidden_pairs()
            self.solve_intersection_removal()
            self.solve_x_wing()

            self.solve_naked_singles()
            if self.unsolved_cells == 0:
                break

            self.solve_hidden_singles()
            if self.unsolved_cells == 0:
                break

            solved = unsolved_before - self.unsolved_cells


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
