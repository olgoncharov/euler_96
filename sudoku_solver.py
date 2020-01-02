
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
            if value not in range(10):
                raise ValueError('Значение ячейки должно находится в интервале 0-9')
            self.value = int(value)

        if self.value:
            self.choices = set()
        else:
            self.choices = set(range(1, 10))
