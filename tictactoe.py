import random


class AI:
    wins = [[[0, 0], [0, 1], [0, 2]],
            [[1, 0], [1, 1], [1, 2]],
            [[2, 0], [2, 1], [2, 2]],
            [[0, 0], [1, 0], [2, 0]],
            [[0, 1], [1, 1], [2, 1]],
            [[0, 2], [1, 2], [2, 2]],
            [[0, 0], [1, 1], [2, 2]],
            [[2, 0], [1, 1], [0, 2]],
            ]

    def random_coordinates(self):
        x = random.randint(1, 3)
        y = random.randint(1, 3)
        return str(x) + ' ' + str(y)

    def make_xy_from_step(self, step):
        step = step.replace(' ', '')
        x = int(step[1]) - 1
        y = int(step[0]) - 1
        if x == 2:
            x = 0
        elif x == 0:
            x = 2
        return x, y

    def make_step_from_xy(self, x, y):
        if x == 2:
            x = 0
        elif x == 0:
            x = 2
        _y = x + 1
        _x = y + 1
        return str(y + 1) + ' ' + str(x + 1)

    def easy_step(self, field):
        step = self.random_coordinates()
        x, y = self.make_xy_from_step(step)
        while field[x][y] != ' ':
            step = self.random_coordinates()
            x, y = self.make_xy_from_step(step)
        return step

    def find_side(self, field):
        all_cells = [m for n in field for m in n]
        all_x = [x for x in all_cells if x == 'X']
        all_o = [o for o in all_cells if o == 'O']
        if len(all_x) > len(all_o):
            return 'O'
        elif len(all_x) == len(all_o):
            return 'X'


class Easy(AI):

    def step(self, field):
        print('Making move level "easy"')
        step = self.easy_step(field)
        return step


class Medium(AI):

    def step(self, field):
        print('Making move level "medium"')
        side = self.find_side(field)
        step = self.medium_step(field, side)
        if step is None:
            step = self.easy_step(field)
        return step

    def medium_step(self, field, side):
        step = ''
        for win in self.wins:
            _ = ''
            for coordinate in win:
                x = coordinate[0]
                y = coordinate[1]
                _ += field[x][y]
            __ = _.replace(' ', '')
            if len(__) == 2 and __[0] == __[1]:
                option = _.index(' ')
                x = win[option][0]
                y = win[option][1]
                step = self.make_step_from_xy(x, y)
                if __[0] == side:
                    return step
        if step != '':
            return step
        return None


class Hard(AI):

    def step(self, field):
        print('Making move level "hard"')
        side = self.find_side(field)
        steps = self.find_steps(field)
        for xy, score in steps.items():
            steps[xy] += self.minimax(field, int(xy[0]), int(xy[1]), side, score)
        result = None
        for xy, score in steps.items():
            if result is None or score >= result:
                x, y = int(xy[0]), int(xy[1])
                result = score
        step = self.make_step_from_xy(x, y)
        return step

    def find_steps(self, field):
        steps = {}
        for x in range(3):
            for y in range(3):
                if field[x][y] == ' ':
                    steps[str(x)+str(y)] = 0
        return steps

    def minimax(self, field, x, y, side, score):
        result = self.check_wins(field, x, y, side)
        if result == 10:
            return 10
        side = 'X' if side == 'O' else 'O'
        steps = self.find_steps(field)
        for xy, score in steps.items():
            steps[xy] += self.minimax(field, int(xy[0]), int(xy[1]), side, score + result) * -1
        field[x][y] = ' '
        return sum(steps.values()) - 10

    def check_wins(self, field, x, y, side):
        field[x][y] = side
        for win in self.wins:
            _ = ''
            for coordinate in win:
                _x = coordinate[0]
                _y = coordinate[1]
                _ += field[_x][_y]
            if _[0] == _[1] == _[2] == side:
                field[x][y] = ' '
                return 10
        return -10


class Human:

    def step(self, field):
        coordinates = input('Enter the coordinates: ')
        return coordinates


class TicTacToe:
    wins = [[[0, 0], [0, 1], [0, 2]],
            [[1, 0], [1, 1], [1, 2]],
            [[2, 0], [2, 1], [2, 2]],
            [[0, 0], [1, 0], [2, 0]],
            [[0, 1], [1, 1], [2, 1]],
            [[0, 2], [1, 2], [2, 2]],
            [[0, 0], [1, 1], [2, 2]],
            [[2, 0], [1, 1], [0, 2]],
            ]

    def __init__(self, player_x, player_o):
        self.field = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]

        self.cells = None
        self.winners = []
        self.state = None
        self.count_steps = 0
        self.player = 'X'

        self.player_x = player_x
        self.player_o = player_o

        self.algorithm()

    def first_step(self, steps):
        for x in range(3):
            for y in range(3):
                step = steps[y + x * 3]
                if step == 'X' or step == 'O':
                    self.field[x][y] = step
        self.algorithm()

    def algorithm(self):
        self.add_to_cells()
        self.print_cells()
        self.check_state()
        if self.state == 'Game not finished':
            self.change_player()
            self.count_steps += 1
            self.step()
        else:
            print(self.state)
            print('')

    def step(self):
        step = None
        if self.player == 'X':
            step = self.player_x.step(self.field)
        elif self.player == 'O':
            step = self.player_o.step(self.field)

        if self.count_steps == 0:
            self.first_step(step)
        else:
            if not self.check_step(step):
                self.step()
            else:
                x, y = self.make_coordinates(step)
                self.field[x][y] = self.player
                self.algorithm()

    def change_player(self):
        all_cells = [m for n in self.field for m in n]
        all_x = [x for x in all_cells if x == 'X']
        all_o = [o for o in all_cells if o == 'O']
        if len(all_x) > len(all_o):
            self.player = 'O'
        elif len(all_o) >= len(all_x):
            self.player = 'X'

    def make_coordinates(self, step):
        step = step.replace(' ', '')
        x = int(step[1]) - 1
        y = int(step[0]) - 1
        if x == 2:
            x = 0
        elif x == 0:
            x = 2
        return x, y

    def check_step(self, step):
        step = step.replace(' ', '')
        if not step.isdigit():
            print('You should enter numbers!')
            return False
        elif len(step) != 2:
            print('You should enter two numbers!')
            return False
        for _ in step:
            if int(_) > 3 or int(_) < 1:
                print('Coordinates should be from 1 to 3!')
                return False
        x, y = self.make_coordinates(step)
        if self.field[x][y] != ' ':
            print('This cell is occupied! Choose another one!')
            return False
        return True

    def enter_the_coordinates(self):
        print('Enter the coordinates: ', end='')

    def print_cells(self):
        print(self.cells)

    def add_to_cells(self):
        self.cells = f'''---------
| {self.field[0][0]} {self.field[0][1]} {self.field[0][2]} |
| {self.field[1][0]} {self.field[1][1]} {self.field[1][2]} |
| {self.field[2][0]} {self.field[2][1]} {self.field[2][2]} |
---------'''

    def check_win_rows(self):
        for win in self.wins:
            _ = ''
            for coordinate in win:
                x = coordinate[0]
                y = coordinate[1]
                _ += self.field[x][y]
            if _[0] == _[1] == _[2] == 'X' or _[0] == _[1] == _[2] == 'O':
                self.winners.append(_[0])

    def check_state(self):
        self.check_win_rows()
        all_cells = [m for n in self.field for m in n]
        all_x = [x for x in all_cells if x == 'X']
        all_o = [o for o in all_cells if o == 'O']
        if len(all_x) - len(all_o) > 1:
            self.state = 'Impossible'
        elif len(all_o) - len(all_x) > 1:
            self.state = 'Impossible'
        elif len(self.winners) == 0 and ' ' in all_cells:
            self.state = 'Game not finished'
        elif len(self.winners) == 0 and ' ' not in all_cells:
            self.state = 'Draw'
        else:
            if self.winners[0] == 'X':
                self.state = 'X wins'
            elif self.winners[0] == 'O':
                self.state = 'O wins'


class Menu:

    def __init__(self):
        while True:
            line = input('Input command: ').split()
            command = line.pop(0)
            self.input(command, line)

    def input(self, command, args):
        if command == 'start':
            if len(args) != 2:
                return self.bad_parameters()
            players = []
            for arg in args:
                players.append(self.player_choose(arg))
                if players[-1] is None:
                    return self.bad_parameters()
            return TicTacToe(*players)
        if command == 'exit':
            exit()

    def player_choose(self, player):
        if player == 'user':
            return Human()
        if player == 'easy':
            return Easy()
        if player == 'medium':
            return Medium()
        if player == 'hard':
            return Hard()
        return None

    def bad_parameters(self):
        print('Bad parameters!')
        return None


Menu()