from copy import copy
src =  [ 'this', 'th', 'is', 'famous', 'Word', 'break', 'b', 'r', 'e', 'a', 'k', 'br', 'bre', 'brea', 'ak', 'problem' ];

dist = 'Wordbreakproblem'


src_set = set(src)

output = set([
"Word b r e a k problem",
"Word b r e ak problem",
"Word br e a k problem",
"Word br e ak problem",
"Word bre a k problem",
"Word bre ak problem",
"Word brea k problem",
"Word break problem"
])

def find_word_break_recursive(src, dist, enriched_dist, result):
    find_word_break_recursive.calls += 1
    accum = ""
    for ch in dist:
        accum += ch
        find_word_break_recursive.counter += 1
        if accum in src:
            find_word_break_recursive(src, dist[len(accum):], [] + enriched_dist + [accum], result)
    if dist == "":
        result.append(" ".join(enriched_dist))
        return


result = []
find_word_break_recursive.counter = 0
find_word_break_recursive.calls = 0
find_word_break_recursive(src_set, dist, [], result)
print('Total calls: ', find_word_break_recursive.calls)
print('Total recursive iterations over the string: ', find_word_break_recursive.counter)

assert set(result) == output

#############
print("============")

def find_word_break_iterative(src, dist):
    find_word_break_iterative.counter = 0
    results = []
    intermediate_results = [([], 0)]
    idx = 0
    while idx < len(intermediate_results):
        sentence, substr_idx = intermediate_results[idx]
        idx += 1
        substr = dist[substr_idx:]
        accum = ""
        word_added = False
        for i, ch in enumerate(substr):
            accum += ch
            find_word_break_iterative.counter += 1
            if accum in src:
                new_sentence = [] + sentence + [accum]
                if i + 1 == len(substr):
                    results.append(" ".join(new_sentence))
                else:
                    intermediate_results.append((new_sentence, substr_idx + i+1))

    print("Total iterations: ", idx)
    print("Total iterations over the string: ", find_word_break_iterative.counter)
    return results

iter_res = find_word_break_iterative(src_set, dist)
assert set(iter_res) == output

#############
print("============")

def find_word_break_iterative_with_memo(src, dist):
    find_word_break_iterative_with_memo.counter = 0
    results = []
    intermediate_results = [([], 0)]
    memoized_results = {}
    idx = 0
    while idx < len(intermediate_results):
        sentence, substr_idx = intermediate_results[idx]
        idx += 1
        substr = dist[substr_idx:]
        accum = ""

        if substr == "":
            results.append(sentence)
            continue

        if substr not in memoized_results:
            memoized_results[substr] = []
        else:
            for token, substr_idx in memoized_results[substr]:
                new_sentence = [] + sentence + [token]
                intermediate_results.append((new_sentence, substr_idx))

            continue

        for i, ch in enumerate(substr):
            accum += ch
            find_word_break_iterative_with_memo.counter += 1
            if accum in src:
                new_sentence = [] + sentence + [accum]
                intermediate_results.append((new_sentence, substr_idx + i+1))
                memoized_results[substr].append((accum, substr_idx + i+1))

    print("Total iterations with memo: ", idx)
    print("Total iterations with memo over the string: ", find_word_break_iterative_with_memo.counter)

    return [" ".join(items) for items in results]


mem_res = find_word_break_iterative_with_memo(src_set, dist)
assert set(mem_res) == output
