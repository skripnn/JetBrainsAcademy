import re
import sys
import os
import ast


class Error:
    blank_lines = 0
    pattern_snake_case = re.compile(r'^[a-z_]+[a-z0-9_]*$')

    def __init__(self, x, line, file):
        self.messages = {
            'S001': 'Too long',
            'S002': 'Indentation is not a multiple of four',
            'S003': 'Unnecessary semicolon after a statement (note, semicolons are admissible in comments)',
            'S004': 'At least two spaces before inline comments required',
            'S005': 'TODO found (only in comments; the case does not matter)',
            'S006': 'More than two blank lines used before this line (must be output for the first non-empty line)',
            'S007': "Too many spaces after construction_name '{}'",
            'S008': "Class name '{}' should use CamelCase",
            'S009': "Function name '{}' should use snake_case",
            'S010': "Argument name '{}' should be snake_case",
            'S011': 'Variable {} should be snake_case',
            'S012': 'Default argument value is mutable'
        }
        self.function = self.get_function(x)
        self.def_or_class = None
        self.line = line
        self.n = x
        self.blank = re.search(r'[\S]', self.line) is None

        for code in self.messages.keys():
            if eval(f'self.{code}()'):
                print(f'{file}: Line {x}: {code} {self.messages[code]}')
        if self.blank:
            Error.blank_lines += 1
        else:
            Error.blank_lines = 0

    @staticmethod
    def get_function(n):
        for f in Function.functions:
            if f.start_line <= n <= f.end_line:
                return f

    def S001(self):
        return len(self.line) > 79

    def S002(self):
        check = re.match(r' +', self.line)
        if check is not None:
            if len(check.group(0)) % 4 != 0:
                return True

    def S003(self):
        new_line = re.split(r' *#', self.line, maxsplit=1)[0]
        check = re.search(r'.*;$', new_line)
        return check is not None

    def S004(self):
        check = re.search(r'[\S] *#', self.line)
        if check is not None:
            if len(check.group(0)) < 4:
                return True

    def S005(self):
        check = re.search(r'#.*([Tt][Oo][Dd][Oo])', self.line)
        return check is not None

    def S006(self):
        if not self.blank:
            return self.blank_lines > 2

    def S007(self):
        pattern = re.compile(r'^[\s]*(def)|(class)')
        if re.match(pattern, self.line):
            self.def_or_class = re.match(pattern, self.line).group(0).strip()
            self.messages['S007'].format(self.def_or_class)
            new_line = re.sub(pattern, '', self.line)
            def_or_class_name = new_line.strip()
            self.messages['S008'].format(def_or_class_name)
            self.messages['S009'].format(def_or_class_name)
            check = re.match(r' +', new_line)
            if check is not None:
                if len(check.group(0)) > 1:
                    return True

    def S008(self):
        if self.def_or_class == 'class':
            check = re.match(r'[\s]*(class) *[A-Z]+[A-Za-z0-9]*(\(|:)', self.line)
            return check is None

    def S009(self):
        if self.def_or_class == 'def':
            check = re.match(r'^[\s]*(def) *[a-z_]+[a-z0-9_]*\(', self.line)
            return check is None

    def S010(self):
        if self.function is not None:
            if self.function.start_line == self.n:
                for arg in self.function.args:
                    check = re.match(self.pattern_snake_case, arg)
                    if check is None:
                        self.messages['S010'].format(arg)
                        self.function.errors.append('S010')
                        return True

    def S011(self):
        if self.function is not None:
            if str(self.n) in self.function.lines and 'S011' not in self.function.errors:
                for var in self.function.lines[str(self.n)]:
                    check = re.match(self.pattern_snake_case, var)
                    if check is None:
                        self.messages['S011'].format(var)
                        self.function.errors.append('S011')
                        return True

    def S012(self):
        if self.function is not None:
            if 'default' in self.function.errors:
                self.function.errors.remove('default')
                self.function.errors.append('S012')
                return True


class Function:
    functions = []

    def __init__(self, start_line, end_line, name, args, lines, errors):
        self.start_line = start_line
        self.end_line = end_line
        self.name = name
        self.errors = errors
        self.args = args
        self.lines = lines
        self.functions.append(self)


class FunctionAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.test = None

    def visit_FunctionDef(self, node):
        lines = LinesAnalyzer()
        lines.visit(node)
        errors = []
        for default in node.args.defaults:
            try:
                default.value
            except AttributeError:
                errors.append('default')

        Function(
            start_line=node.lineno,
            end_line=node.end_lineno,
            name=node.name,
            args=[arg.arg for arg in node.args.args],
            lines=lines.report(),
            errors=errors
        )
        self.generic_visit(node)


class LinesAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {}

    def visit_Name(self, node):
        lineno = self.stats.get(str(node.lineno), [])
        lineno.append(node.id)
        self.stats[str(node.lineno)] = lineno
        self.generic_visit(node)

    def report(self):
        return self.stats


def start():
    file_list = []
    path = sys.argv[1]
    if os.path.isfile(path):
        file_list.append(path)
    elif os.path.isdir(path):
        file_list = [os.path.join(path, file) for file in os.listdir(path)]
        file_list.sort()

    for file in file_list:
        with open(file) as f:
            tree = ast.parse(f.read())
            analyzer = FunctionAnalyzer()
            analyzer.visit(tree)

        with open(file) as f:
            for x, line in enumerate(f, 1):
                Error(x, line, file)
            Function.functions = []


if __name__ == '__main__':
    start()
