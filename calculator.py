from collections import deque


class SmartCalculator:
    variables = {}
    operators = ['+', '-', '*', '/', '^']
    operators_priority = {'+': 1,
                          '-': 1,
                          '*': 2,
                          '/': 2,
                          '^': 3}

    def input(self, line):                      # Read a line from input
        if self.check_line(line):               # If the line exists and it's not a command
            self.calculating(line)              # Start calculating

    def check_line(self, line):                 # Checking line for special symbols:
        if line == '':
            return False
        if line.startswith('/'):
            self.command(line)
            return False
        if '=' in line:
            self.add_variable(line)
            return False
        return True

    def add_variable(self, line):               # Adding variable to Dict 'variables'
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
            float(value)
        except ValueError:
            print('Invalid assignment')
            return False
        else:
            self.variables[key] = value
            return True

    def command(self, line):                    # List of commands
        if line == '/help':
            self.c_help()
        if line == '/exit':
            self.c_exit()
        else:
            print('Unknown command')

    def c_help(self):                           # Print help
        print('The program calculates the sum of numbers')
        print('If you want addition - input +')
        print('If you want subtraction - input -')

    def c_exit(self):                           # Exit
        print('Bye!')
        exit()

    def replace_variables(self, line):          # Replace variable to value of variable
        numbers = ''
        for n in line.split():
            if n.isalpha():
                try:
                    n = self.variables[n]
                except KeyError:
                    print('Unknown variable')
            numbers += f' {str(n)}'
        return numbers.strip()

    def beauty_line(self, line):                # Making understandable line
        if self.check_doubles(line) or self.check_parentheses(line):            # Error checking
            print('Invalid expression')
            return None
        line = ''.join(line.split())
        while '+-' in line or '-+' in line or '--' in line or '++' in line:     # Replace meanings
            line = line.replace('++', '+')
            line = line.replace('+-', '-')
            line = line.replace('-+', '-')
            line = line.replace('--', '+')
        line = line.replace('-(', '-1*(')
        line = self.make_list(line)
        return line

    def make_list(self, line):              # Making list with digits, variables, operators
        x = []                              # and parentheses from string
        for n in line:                      # Also checking for existing each variable

            if n == ' ':
                continue

            if len(x) == 0:
                x.append(n)
                continue

            if n.isdigit():
                if x[-1] not in self.operators and x[-1] != '(' and x[-1] != ')':
                    x[-1] += n
                elif x[-1] == '-':
                    if len(x) == 1:
                        x[-1] += n
                    elif x[-2] == '*' or x[-2] == '/' or x[-2] == '^':
                        x[-1] += n
                    else:
                        x.append(n)
                else:
                    x.append(n)
                continue

            if n.isalpha and n not in self.operators and n != '(' and n != ')':
                if x[-1] in self.operators or x[-1] != '(' or x[-1] != ')':
                    x.append(n)
                else:
                    x[-1] += n
                continue

            if n == '+' and (x[-1] == '*' or x[-1] == '/' or x[-1] == '^'):
                continue

            x.append(n)

        if self.check_variables(x):
            return x
        return None

    def check_variables(self, line):            # Checking for existing variables
        for n in line:
            if n not in self.operators and n != '(' and n != ')':
                if n in self.variables:
                    continue
                try:
                    float(n)
                except ValueError:
                    print('Unknown variable')
                    return False
        return True

    def check_doubles(self, line):              # Checking for existing doubles of operators
        line = ''.join(line.split())
        doubles = []
        for n in self.operators:
            if n != '+' and n != '-':
                doubles.append(n + n)
        for n in doubles:
            if n in line:
                return True

    def check_parentheses(self, line):          # Checking of parentheses for pairs
        if line.count('(') != line.count(')'):
            return True

    def postfix_notation(self, line):           # Rewrite prefix to postfix (Reverse Polish Notification)
        line = self.beauty_line(line)           # starts from making understandable line
        if not line:
            return None
        stack = deque()
        result = deque()

        for n in line:
            if n not in self.operators and n != '(' and n != ')':
                result.append(n)
            elif n in self.operators:
                while True:
                    if len(stack) == 0 or stack[-1] == '(':
                        stack.append(n)
                        break
                    if self.operators_priority[n] > self.operators_priority[stack[-1]]:
                        stack.append(n)
                        break
                    if self.operators_priority[n] <= self.operators_priority[stack[-1]]:
                        result.append(stack.pop())
            elif n == '(':
                stack.append(n)
            elif n == ')':
                while stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()

        while len(stack) > 0:
            result.append(stack.pop())

        return result

    def calculating(self, line):                # Calculating result
        line = self.postfix_notation(line)      # starts from rewrite to postfix
        if not line:
            return None

        stack = deque()

        for n in line:
            if n in self.variables:
                n = self.variables[n]
            if n not in self.operators and n != '(' and n != ')':
                stack.append(n)
            elif n in self.operators:
                x = stack.pop()
                y = stack.pop()
                stack.append(str(eval(y + n + x)))

        x = float(stack.pop())
        if x == int(x):
            print(int(x))
        else:
            print(x)


project = SmartCalculator()
while True:
    project.input(input())
