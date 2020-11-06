import sys
sys.setrecursionlimit(10000)


def match(re, text):
    if re[0] == '':
        return True
    if text[0] == '':
        return False
    if re[0] == '.':
        return True
    if re[0] == text[0]:
        return True
    return False


def skip_operator_and_rematch(re, text):
    return recursion_match(re[2:], text)


def skip_operator(re, text):
    return recursion_match(re[2:], text[1:])


def recursion_match(re, text):
    if len(re) == 0:
        return True

    if re[0] == '$':
        if text == '':
            return True
        return False

    if len(text) == 0:
        return False

    if re[0] == '\\':
        if not match(re[1:], text):
            return False
        return skip_operator(re, text)

    if len(re) > 1 and re[0] != '\\':
        if re[1] == '?':
            if not match(re, text):
                return skip_operator_and_rematch(re, text)
            return skip_operator(re, text)
        if re[1] == '*':
            if not match(re, text):
                return skip_operator_and_rematch(re, text)
            if len(text) - 1 == len(re.replace('$', '')) - 2:
                return skip_operator(re, text)
            return recursion_match(re, text[1:])
        if re[1] == '+':
            if not match(re, text):
                return False
            return recursion_match(re[0] + '*' + re[2:], text)

    if not match(re, text):
        return False
    return recursion_match(re[1:], text[1:])


def search(re, text):
    if not recursion_match(re, text):
        if text == '':
            return False
        return search(re, text[1:])
    return True


def start_end_operators(re, text):
    if re.startswith('^'):
        return recursion_match(re[1:], text)
    if re.endswith('$'):
        if recursion_match(re, text):
            return True
    return search(re, text)


re, text = input().split('|')
if start_end_operators(re, text):
    print('True')
else:
    print('False')
