import operator
from functools import reduce

noop = lambda x: x

def compose_unary(f, g):
    return lambda item: f(g(item))

def calculate_stack(stack):
    operands = []
    highorder_action = None
    loworder = []
    while len(stack):
        elem = stack.pop()
        if elem in (operator.add, operator.sub):
            loworder.append(elem)
            continue
        elif elem in (operator.mul, operator.truediv):
            highorder_action = elem
            continue
        elif elem in (noop, operator.neg):
            # in case of trailing -+ operators: ---2 == -2

            chain = [elem]
            following = stack.pop()
            while following in (noop, operator.neg):
                chain.append(following)
                following = stack.pop()

            res = reduce(compose_unary, chain, noop)
            operands.append(res(following))
        else:
            operands.append(elem)

        if len(operands) >= 2 and highorder_action:
            second_operand = operands.pop()
            first_operand = operands.pop()
            stack.append(highorder_action(first_operand, second_operand))
            highorder_action = None


    res = operands.pop(0)
    while len(operands) and len(loworder):
        op = loworder.pop(0)
        res = op(res, operands.pop(0))

    return res

def calculate(expression):
    stash = []
    stack = []
    level = 0
    previous = ''
    last_operator = noop
    number_buf = ''
    for ch in expression:
        if ch == ' ':
            continue

        if previous.isnumeric() and not ch.isnumeric() and ch != '.':
            stack.insert(0, float(number_buf))
            number_buf = ''

        if ch == '(':
            # push everything to the stack
            stash.append(stack)
            stack = []
        elif ch == ')':
            # calculate stack
            res = calculate_stack(stack)
            stack = stash.pop()
            stack.insert(0, res)
        elif ch == '-':
            if previous in ('', '-', '+', '/', '*', '('):
                stack.insert(0, operator.neg)
            else:
                stack.insert(0, operator.sub)
        elif ch == '+':
            if previous in ('', '-', '+', '/', '*', '('):
                stack.insert(0, noop)
            else:
                stack.insert(0, operator.add)
        elif ch == '*':
            stack.insert(0, operator.mul)
        elif ch == '/':
            stack.insert(0, operator.truediv)
        elif ch.isnumeric() or ch == '.':
            number_buf += ch

        previous = ch

    if previous.isnumeric() or ch == '.':
        stack.insert(0, float(number_buf))

    return calculate_stack(stack)


cases = (
    ("1 + 1", 2),
    ("8/16", 0.5),
    ("3 -(-1)", 4),
    ("2 + -2", 0),
    ("10- 2- -5", 13),
    ("(((10)))", 10),
    ("3 * 5", 15),
    ("-7 * -(6 / 3)", 14),
    # extra cases
    ('999/3/3', 111),
    ('14/2+7*8/2--5', 40),
    ('---5', -5),
    # decimals
    ('2.5 * 2.5 / 0.5', 12.5),
    ('0.123456789 + 1.0987654321 - 1', 0.2222222211),
    ('0.1 + 0.2', 0.1 + 0.2),
    # hard cases
    ('(7) * (55 - -77 + -(43)) - (-69 * ((((97 / -74)))) * 31)', -2180.824324324324),
    ('(-73) * (-94 - 33 / -(56)) + (-55 / (((-(95 * 77)))) - -24)', 6842.9896616541355)

)

for src, expected in cases:
    res = calculate(src)
    print(src, res, "expected:", expected)
    assert res == expected
