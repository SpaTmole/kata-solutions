cases = [
    {'values': [60, 100, 120], 'weights': [10, 20, 30], 'W': 50, 'expected': 220},
    {'values': [ 20, 5, 10, 40, 15, 25 ], 'weights': [ 1, 2, 3, 8, 7, 4 ], 'W': 10, 'expected': 60},
]

def knapsack_recursive(values, weights, limit, accum):
    maxValue = 0
    result = accum
    for idx in range(len(values)):
        knapsack_recursive.iterations += 1
        if weights[idx] <= limit and maxValue < values[idx]:
            maxValue = values[idx]
            result = max(
                knapsack_recursive(
                    values[:idx] + values[idx+1:],
                    weights[:idx] + weights[idx+1:],
                    limit - weights[idx],
                    accum + values[idx]
                ),
                result
            )

    return result


for case in cases:
    knapsack_recursive.iterations = 0
    r = knapsack_recursive(case['values'], case['weights'], case['W'], 0)
    print('Recursive result on case ', case, ' = ', r, ' | Expected: ', case['expected'])
    print('Iterations: ', knapsack_recursive.iterations)


print('========')

def knapsack_iterative(values, weights, limit):
    accum = 0
    subtasks = [(values, weights, limit, 0)]
    idx = 0
    result = 0
    while idx < len(subtasks):
        sub_vs, sub_ws, sub_l, accum = subtasks[idx]
        print(f'{idx}: {sub_vs} {sub_ws} || {sub_l} : {accum} | {result}')
        idx += 1
        max_value = 0
        for v_idx in range(len(sub_vs)):
            knapsack_iterative.iterations += 1
            if sub_ws[v_idx] <= sub_l and max_value < sub_vs[v_idx]:
                max_value = sub_vs[v_idx]
                subtasks.append((
                    sub_vs[:v_idx] + sub_vs[v_idx+1:],
                    sub_ws[:v_idx] + sub_ws[v_idx+1:],
                    sub_l - sub_ws[v_idx],
                    accum + max_value,
                ))

        result = max(result, accum + max_value)

    return result


for case in cases:
    knapsack_iterative.iterations = 0
    r = knapsack_iterative(case['values'], case['weights'], case['W'])
    print('Iterative result on case ', case, ' = ', r, ' | Expected: ', case['expected'])
    print('Iterations: ', knapsack_iterative.iterations)


print('========')

def knapsack_memo(values, weights, limit):
    accum = 0
    subtasks = [(values, weights, limit, 0)]
    idx = 0
    result = 0
    memo = {}
    while idx < len(subtasks):
        sub_vs, sub_ws, sub_l, accum = subtasks[idx]
        print(f'{idx}: {sub_vs} {sub_ws} || {sub_l} : {accum} | {result}')
        idx += 1
        max_value = 0
        memo_res = memo.get((tuple(sub_vs), tuple(sub_ws), sub_l))
        if memo_res != None:
            result = max(result, accum + memo_res)
            continue

        for v_idx in range(len(sub_vs)):
            knapsack_memo.iterations += 1
            if sub_ws[v_idx] <= sub_l and max_value < sub_vs[v_idx]:
                max_value = sub_vs[v_idx]
                if sub_l - sub_ws[v_idx] > 0:
                    subtasks.append((
                        sub_vs[:v_idx] + sub_vs[v_idx+1:],
                        sub_ws[:v_idx] + sub_ws[v_idx+1:],
                        sub_l - sub_ws[v_idx],
                        accum + max_value,
                    ))
                    memo[(tuple(sub_vs), tuple(sub_ws), sub_l)] = max_value

        if max_value == 0:
            memo[(tuple(sub_vs), tuple(sub_ws), sub_l)] = 0

        result = max(result, accum + max_value)

    return result


for case in cases:
    knapsack_memo.iterations = 0
    r = knapsack_memo(case['values'], case['weights'], case['W'])
    print('Iterative result on case ', case, ' = ', r, ' | Expected: ', case['expected'])
    print('Iterations: ', knapsack_memo.iterations)
