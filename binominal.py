"""
Write a function expand that takes in an expresion with a single, one character variable, and expands it.
The expresion is in the form (ax+b)^n where a and b are integers which may be positive or negative,
x is any one character long variable, and n is a natural number.
If a = 1, no coeficient will be placed in front of the variable.
If a = -1, a "-" will be placed in front of the variable.


UPD. This solution is more advanced, as it may expand 2 variables (as (x+y)^2)
"""

def binominal(n, k):
    """
    General formula for this function is: C(n|k) = n! / ((n-k)! * k!)

    Let's simplify it by multiplying only non-anihilated numbers.

    """
    if 0 <= k <= n:
        n_part = k_part = 1
        for unique in range(1, min(k, n - k) + 1):
            n_part *= n - (unique - 1)
            k_part *= unique

        return n_part // k_part
    else:
        return 0


def build_series_member(tokens, n, k):
    cnk = binominal(n, k)
    first_coeff = tokens[0][0] ** (n - k)
    second_coeff = tokens[1][0] ** k
    first_var = ''
    if tokens[0][1] and n - k != 0:
        first_var = f'{tokens[0][1]}^{n - k}' if n - k > 1 else tokens[0][1]

    second_var = ''
    if tokens[1][1] and k != 0:
        second_var = f'{tokens[1][1]}^{k}' if k > 1 else tokens[1][1]

    total_coeff = cnk * first_coeff * second_coeff
    sign = '+' if total_coeff > 0 else '-'
    total_coeff = str(
        abs(total_coeff)
    ) if abs(total_coeff) > 1 or not (first_var or second_var) else ''
    return f'{sign}{total_coeff}{first_var}{second_var}'


def expand(expr):
    expr, n = expr.split('^')
    if n == '0':
        return '1'

    expr = expr[1:-1] # Cut off parentheses
    if n == '1':
        return expr

    n = int(n)
    k = 0

    expr_tokens = None
    if '+' in expr:
        expr_tokens = expr.split('+')
    else:
        expr_tokens = expr.split('-')
        if expr.startswith('-'):
            expr_tokens = ['-' + expr_tokens[1], expr_tokens[2]]
        expr_tokens[1] = '-' + expr_tokens[1]

    # Parse unknown part
    for _idx, token in enumerate(expr_tokens):
        coeff = ''
        var = ''
        for char in token:
            if char.isalpha():
                var += char
            else:
                # '-' or digit
                coeff += char

        if coeff == '-':
            coeff = '-1'
        elif not coeff and var:
            coeff = '1'
        elif not coeff:
            # Shouldn't be such case, but just for case
            coeff = '0'

        token = (int(coeff), var)
        if not token[0]:
            token = None
        expr_tokens[_idx] = token

    # Check for nil-coefficients:
    if not all(expr_tokens):
        for token in expr_token:
            if token is not None:
                coeff = token[0] ** n
                var = f'{token[1]}^{n}' if token[1] else ''
                return f'{coeff}{var}'

    # Let's expand.
    result = [build_series_member(expr_tokens, n, k) for k in range(n + 1)]
    # Fix the accidental '+' for the first member.
    if result[0].startswith('+'):
        result[0] = result[0][1:]

    return ''.join(result)


class Test:
    @classmethod
    def assert_equals(cls, expr1, expr2):
        print(expr1)
        assert expr1 == expr2


Test.assert_equals(expand("(x+1)^0"), "1")
Test.assert_equals(expand("(x+1)^1"), "x+1")
Test.assert_equals(expand("(x+1)^2"), "x^2+2x+1")

Test.assert_equals(expand("(x-1)^0"), "1")
Test.assert_equals(expand("(x-1)^1"), "x-1")
Test.assert_equals(expand("(x-1)^2"), "x^2-2x+1")

Test.assert_equals(expand("(5m+3)^4"), "625m^4+1500m^3+1350m^2+540m+81")
Test.assert_equals(expand("(2x-3)^3"), "8x^3-36x^2+54x-27")
Test.assert_equals(expand("(7x-7)^0"), "1")

Test.assert_equals(expand("(-5m+3)^4"), "625m^4-1500m^3+1350m^2-540m+81")
Test.assert_equals(expand("(-2k-3)^3"), "-8k^3-36k^2-54k-27")
Test.assert_equals(expand("(-7x-7)^0"), "1")
Test.assert_equals(expand("(x+y)^2"), "x^2+2xy+y^2")
Test.assert_equals(expand("(x-y)^2"), "x^2-2xy+y^2")
Test.assert_equals(expand("(-x-y)^2"), "x^2+2xy+y^2")
