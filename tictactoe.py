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

    field = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]

    cells = None

    winners = []

    state = None

    count_steps = 0

    player = 'X'

    def __init__(self):
        print('Enter cells: ', end='')

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
        self.change_player()
        self.count_steps += 1
        if self.count_steps < 2:
            self.enter_the_coordinates()
        else:
            print(self.state)

    def step(self, step):
        if self.count_steps == 0:
            self.first_step(step)
        else:
            if not self.check_step(step):
                self.enter_the_coordinates()
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
        if len(self.winners) > 1:
            self.state = 'Impossible'
        elif len(all_x) - len(all_o) > 1:
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



game = TicTacToe()
while game.count_steps < 2:
# while True:
    game.step(input())
