"""
Write a function that accepts an array of intervals, and returns the sum of all the interval lengths.
Overlapping intervals should only be counted once.

Intervals are represented by a pair of integers in the form of an array.
The first value of the interval will always be less than the second value.
Interval example: [1, 5] is an interval from 1 to 5.
The length of this interval is 4.

Overlapping Intervals
List containing overlapping intervals:

    [
           [1,4],
           [7, 10],
           [3, 5]
    ]

The sum of the lengths of these intervals is 7.
Since [1, 4] and [3, 5] overlap, we can treat the interval as [1, 5], which has a length of 4.
"""

def sum_of_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: x[0])
    _sum = 0
    last_iv = None
    for iv in intervals:
        if not last_iv or last_iv[1] < iv[0]:  # First or non-overlapped iv; Add whole length
            last_iv = tuple(iv)
            _sum += last_iv[1] - last_iv[0]
        elif iv[1] > last_iv[1]:  # overlapped iv, with extension.
            _sum += iv[1] - last_iv[1]
            last_iv = (last_iv[0], iv[1])
        # Otherwise, all iv's are within extension borders, thus ext sum = 0.
    return _sum
