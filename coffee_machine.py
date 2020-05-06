class CoffeeMachine:
    espresso = {'water': 250,
                'milk': 0,
                'coffee beans': 16,
                'money': -4,
                'disposable cups': 1}

    latte = {'water': 350,
             'milk': 75,
             'coffee beans': 20,
             'money': -7,
             'disposable cups': 1}

    cappuccino = {'water': 200,
                  'milk': 100,
                  'coffee beans': 12,
                  'money': -6,
                  'disposable cups': 1}

    machine = {'water': 400,
               'milk': 540,
               'coffee beans': 120,
               'money': 550,
               'disposable cups': 9}

    fill_states = ['ml of water', 'ml of milk', 'grams of coffee beans', 'disposable cups of coffee']

    machine_state = None
    fill_state = None

    def __init__(self):
        self.start()

    def start(self):
        self.machine_state = 'action'
        print('Write action (buy, fill, take, remaining, exit):')

    def command(self, command):
        self.check_menu(command)

    def check_menu(self, command):
        if self.machine_state == 'action':
            self.action(command)
        elif self.machine_state == 'buy':
            self.buy(command)
        elif self.machine_state == 'fill':
            self.fill(command)

    def check_button(self, button):
        if button == 1:
            return self.espresso
        elif button == 2:
            return self.latte
        elif button == 3:
            return self.cappuccino

    def check_enough(self, coffee):
        for key in self.machine.keys():
            if self.machine[key] < coffee[key]:
                print(f'Sorry, not enough {key}!')
                print('')
                return False
        print('I have enough resources, making you a coffee!')
        print('')
        return True

    def buy(self, button):
        if not button:
            self.machine_state = 'buy'
            print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        else:
            if button == 'back':
                return self.start()
            coffee = self.check_button(int(button))
            if self.check_enough(coffee):
                for key in self.machine.keys():
                    self.machine[key] -= coffee[key]
            self.start()

    def fill(self, command):
        self.machine_state = 'fill'
        if not command:
            self.fill_state = 0
            print(f'Write how many {self.fill_states[self.fill_state]} do you want to add:')
        elif self.fill_state < 3:
            self.filling(command)
            self.fill_state += 1
            print(f'Write how many {self.fill_states[self.fill_state]} do you want to add:')
        else:
            self.filling(command)
            self.fill_state = None
            print('')
            self.start()

    def filling(self, how_much):
        keys = list(self.machine.keys())
        if self.fill_state != 3:
            key = keys[self.fill_state]
        else:
            key = keys[self.fill_state + 1]
        self.machine[key] += int(how_much)

    def take(self):
        self.machine_state = 'take'
        print(f"I gave you ${self.machine['money']}")
        print('')
        self.machine['money'] = 0
        self.start()

    def remaining(self):
        print(f"""The coffee machine has:
    {self.machine['water']} of water
    {self.machine['milk']} of milk
    {self.machine['coffee beans']} of coffee beans
    {self.machine['disposable cups']} of disposable cups
    ${self.machine['money']} of money"""
              )
        print('')
        self.start()

    def action(self, text):
        print('')
        self.machine_state = text
        if text == 'take':
            self.take()
        elif text == 'fill':
            self.fill(False)
        elif text == 'buy':
            self.buy(False)
        elif text == 'remaining':
            self.remaining()
        elif text == 'exit':
            self.machine_state = 'action'
            exit()


temp_machine = CoffeeMachine()
while True:
    temp_machine.command(input())
