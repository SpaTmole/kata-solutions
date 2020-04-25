"""
https://leetcode.com/problems/valid-parenthesis-string/

Given a string containing only three types of characters: '(', ')' and '*', write a function to check whether this string is valid. We define the validity of a string by these rules:

Any left parenthesis '(' must have a corresponding right parenthesis ')'.
Any right parenthesis ')' must have a corresponding left parenthesis '('.
Left parenthesis '(' must go before the corresponding right parenthesis ')'.
'*' could be treated as a single right parenthesis ')' or a single left parenthesis '(' or an empty string.
An empty string is also valid.
Example 1:
Input: "()"
Output: True
Example 2:
Input: "(*)"
Output: True
Example 3:
Input: "(*))"
Output: True
Note:
The string size will be in the range [1, 100].
"""

def checkValidString(s: str) -> bool:

    chr_col = {
        '(': 0,
        ')': 0,
        '*': 0,
    }
    following_asteriks_stack = []

    for idx, chr in enumerate(s):
        chr_col[chr] += 1
        if chr == ')':
            if (chr_col['('] + chr_col['*']) < chr_col[')']:
                return False
            chr_col[')'] -= 1
            if chr_col['('] > 0:
                chr_col['('] -= 1
                prev_fw_accum = following_asteriks_stack.pop()
                if following_asteriks_stack:
                    following_asteriks_stack[-1] += prev_fw_accum
            else:
                chr_col['*'] -= 1
                if following_asteriks_stack:
                    following_asteriks_stack[-1] += 1
        elif chr == '(':
            following_asteriks_stack.append(0)
        elif chr == '*':
            if following_asteriks_stack:
                following_asteriks_stack[-1] += 1
        print(chr, ' -------> ', chr_col, '      last: ', following_asteriks_stack)
    print('    ')
    # Poping stack for each '(' subtract at least 1 and move the rest to a previous '('
    # If there was 0 at some point - we out of options to enclose the bracket, means invalid string.
    while following_asteriks_stack:
        volume = following_asteriks_stack.pop()
        if volume == 0:
            return False
        if following_asteriks_stack:
            following_asteriks_stack[-1] += volume-1

    return True


def test():
    assert not checkValidString("(())((())()()(*)(*()(())())())()()((()())((()))(*")
    assert checkValidString("(*)")


test()
