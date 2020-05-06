class SmartCalculator:

    variables = {}

    def input(self, line):
        if self.check_line(line):
            try:
                self.process(line)
            except ValueError:
                print('Invalid expression')

    def check_line(self, line):
        if line == '':
            return False
        if line.startswith('/'):
            self.command(line)
            return False
        if line.lstrip()[0].isalpha():
            if '=' not in line and len(line.split()) == 1:
                self.print_variable(line)
                return False
            if '=' in line:
                self.add_variable(line)
                return False
        return True

    def print_variable(self, line):
        if line.strip().isalpha():
            try:
                print(self.variables[line.strip()])
            except KeyError:
                print('Unknown variable')
        else:
            print('Invalid identifier')

    def add_variable(self, line):
        key = line[:line.index('=')].strip()
        value = line[line.index('=') + 1:].strip()

        if not key.isalpha():
            print('Invalid identifier')
            return False

        if value.isalpha():
            try:
                self.variables[key] = self.variables[value]
                return True
            except KeyError:
                print('Unknown variable')
                return False

        try:
            self.variables[key] = int(value)
            return True
        except ValueError:
            print('Invalid assignment')
            return False

    def command(self, line):
        if line == '/help':
            self.c_help()
        if line == '/exit':
            self.c_exit()
        else:
            print('Unknown command')

    def c_help(self):
        print('The program calculates the sum of numbers')
        print('If you want addition - input +')
        print('If you want subtraction - input -')

    def c_exit(self):
        print('Bye!')
        exit()

    def replace_variables(self, line):
        numbers = ''
        for n in line.split():
            if n.isalpha():
                try:
                    n = self.variables[n]
                except KeyError:
                    print('Unknown variable')
            numbers += f' {str(n)}'
        return numbers.strip()

    def process(self, numbers):
        numbers = self.replace_variables(numbers)
        while '  ' in numbers:
            numbers = numbers.replace('  ', ' ')
        numbers = numbers.replace('- ', '-')
        numbers = numbers.replace('+ ', '+')
        numbers = numbers.replace('-', ' -')
        numbers = numbers.replace('+', ' +')
        while '+ -' in numbers or '- +' in numbers or '- -' in numbers or '+ +' in numbers:
            numbers = numbers.replace('+ +', '+')
            numbers = numbers.replace('+ -', '-')
            numbers = numbers.replace('- +', '-')
            numbers = numbers.replace('- -', '+')
        result = 0
        for n in numbers.split():
            if numbers.split().index(n) != 0:
                if not (n.startswith('-') or n.startswith('+')):
                    n = ''
            result += int(n)
        print(result)


project = SmartCalculator()
while True:
    project.input(input())
