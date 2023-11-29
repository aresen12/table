from sympy.logic.boolalg import to_dnf
from sympy.abc import a, b, c


def translate(expr):
    e = list(expr)
    res = [' ' for _ in range(len(e))]
    for start in range(len(e)):
        if expr[start: start + 3] == 'not':
            res[start] = '~'
            res[start + 1] = ''
            res[start + 2] = ''
        elif expr[start: start + 3] == 'and':
            res[start] = '&'
            res[start + 1] = ''
            res[start + 2] = ''
        else:
            if res[start] == ' ':
                res[start] = e[start]

    expr = ''.join(res)
    e = list(expr)
    res = [' ' for _ in range(len(e))]
    for start in range(len(e)):
        if expr[start: start + 2] == 'or':
            res[start] = '|'
            res[start + 1] = ''
        else:
            if res[start] == ' ':
                res[start] = e[start]

    res = [elt for elt in res if elt != ' ' or elt != '']
    return ''.join(res)


exp1 = '(not ((b or not c) and (not a or not c))) or (not (c or not (b and c))) or (a and not c) and (not a or (a and b and c) or (a and ((b and not c) or (not b))))'
exp2 = '(not (a and not b) or (not c and b)) and (not b) or (not a and b and not c) or (a and not b)'

print('exp1:', '\n', eval(translate(exp1)), '\n', to_dnf(eval(translate(exp1)), simplify=True))
print('exp2:', '\n', eval(translate(exp2)), '\n', to_dnf(eval(translate(exp2)), simplify=True))
