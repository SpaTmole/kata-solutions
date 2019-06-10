"""
You have to create a function that takes a positive integer number and returns the next bigger number formed by the same digits:

>>> 12 ==> 21
>>> 513 ==> 531
>>> 2017 ==> 2071

If no bigger number can be composed using those digits, return -1:

>>> 9 ==> -1
>>> 111 ==> -1
>>> 531 ==> -1

"""

def next_bigger(n):
    src = str(n)
    pivot, prev_pivot = -1, -1
    for pivot_idx in xrange(1, len(src) + 1):
        pivot = int(src[len(src) - pivot_idx])
        if prev_pivot > pivot:
            break
        else:
            prev_pivot = pivot
    if pivot == prev_pivot:
        return -1

    right_part = src[len(src) - pivot_idx + 1:]
    left_part = src[:len(src) - pivot_idx]

    for sub_idx, subst in sorted(enumerate(right_part), key=lambda x: x[1]):
        if int(subst) > pivot:
            right_part = ''.join(sorted(
                right_part[:sub_idx] + str(pivot) + right_part[sub_idx + 1:]
            ))
            return int(left_part + subst + right_part)
    return -1
