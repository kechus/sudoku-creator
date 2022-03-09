import random


class Cell():
    def __init__(self) -> None:
        self.available_values = list(range(1, 10))
        self.number = 0


class Bounds():
    def __init__(self, row_range, col_lower, col_upper):
        self.row_range = row_range
        self.col_lower = col_lower
        self.col_upper = col_upper


class Board():
    def __init__(self) -> None:
        self._cells = [Cell() for _ in range(0, 81)]
        self._board = []
        self._generate_board()
        self._index = 0
        self._current_cell = self._cells[self._index]
        self._create_cols()

    def _generate_board(self):
        self._board = []
        i = 0
        prev_i = 0
        while i != 81:
            prev_i = i
            i = i + 9
            self._board.append(self._cells[prev_i:i])

    def fill_board(self):
        while self._index < 81:
            self._current_cell = self._cells[self._index]
            self._generate_board()
            self._make_pretty_board()

            if self._no_remaining_numbers_in_cell():
                self._cells[self._index].available_values = list(range(1, 10))
                self._cells[self._index].number = 0
                self._index = self._index - 1
                continue

            (number_to_place, random_index) = self._pick_number_from_cell()
            if self._check_conflict(number_to_place):
                del(self._cells[self._index].available_values[random_index])
                continue

            self._cells[self._index].number = number_to_place
            self._index = self._index + 1

    def _no_remaining_numbers_in_cell(self):
        remaining = len(self._cells[self._index].available_values)
        return remaining == 0

    def _pick_number_from_cell(self):
        random_index = random.randint(
            0, len(self._cells[self._index].available_values)-1)
        number_to_place = self._cells[self._index].available_values[random_index]
        return (number_to_place, random_index)

    def _check_conflict(self, number_to_place):
        is_in_row = self._number_in_row(number_to_place)
        is_in_column = self._number_in_column(number_to_place)
        is_in_square = self._number_in_square(number_to_place)
        return is_in_row or is_in_column or is_in_square

    def _number_in_row(self, number_to_place):
        row = self._current_row()
        return True if number_to_place in list(cell.number for cell in row) else False

    def _current_row(self):
        row_number = 0
        for row in self._board:
            if self._cells[self._index] in row:
                return self._board[row_number]
            row_number = row_number + 1
        return None

    def _current_row_number(self):
        row_number = 0
        for row in self._board:
            if self._cells[self._index] in row:
                return row_number
            row_number = row_number + 1
        return None

    def _number_in_column(self, number_to_place):
        column_number = self._current_column_number()
        for row in self._board:
            if row[column_number].number == number_to_place:
                return True
        return False

    def _create_cols(self):
        self._cols = []
        for i in range(0, 9):
            self._cols.append(self.steps(i))

    def _current_column_number(self):
        for i in range(0, len(self._cols)):
            if self._index in self._cols[i]:
                return i
        return None

    def steps(self, x):
        st = []
        for _ in range(0, 9):
            st.append(x)
            x = x + 9
        return st

    def _number_in_square(self, number_to_place):
        square = self._generate_square()
        for square_row in square:
            if number_to_place in list(cell.number for cell in square_row):
                return True
        return False

    def _generate_square(self):
        square = []
        mask = [
            [0, 0, 0, 3, 3, 3, 6, 6, 6],
            [0, 0, 0, 3, 3, 3, 6, 6, 6],
            [0, 0, 0, 3, 3, 3, 6, 6, 6],
            [1, 1, 1, 4, 4, 4, 7, 7, 7],
            [1, 1, 1, 4, 4, 4, 7, 7, 7],
            [1, 1, 1, 4, 4, 4, 7, 7, 7],
            [2, 2, 2, 5, 5, 5, 8, 8, 8],
            [2, 2, 2, 5, 5, 5, 8, 8, 8],
            [2, 2, 2, 5, 5, 5, 8, 8, 8]]
        index = mask[self._current_row_number()][self._current_column_number()]
        dict = [
            Bounds(range(0, 3), 0, 3),
            Bounds(range(3, 6), 0, 3),
            Bounds(range(6, 9), 0, 3),
            Bounds(range(0, 3), 3, 6),
            Bounds(range(3, 6), 3, 6),
            Bounds(range(6, 9), 3, 6),
            Bounds(range(0, 3), 6, 9),
            Bounds(range(3, 6), 6, 9),
            Bounds(range(6, 9), 6, 9),
        ]
        curr_dict = dict[index]
        for i in curr_dict.row_range:
            square.append(
                self._board[i][curr_dict.col_lower:curr_dict.col_upper])
        return square

    def _make_pretty_board(self):
        self.pretty_board = []
        for row in self._board:
            self.pretty_board.append(list(cell.number for cell in row))

    def show_board(self):
        for row in self._board:
            print(list(cell.number for cell in row))


def main():
    board = Board()
    board.fill_board()
    board.show_board()


if __name__ == '__main__':
    main()
