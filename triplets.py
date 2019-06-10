"""
There is a secret string which is unknown to you.
Given a collection of random triplets from the string,
recover the original string.

A triplet here is defined as a sequence of three letters such
that each letter occurs somewhere before the next in the given string.
"whi" is a triplet for the string "whatisup".

As a simplification, you may assume that no letter occurs more than once in the secret string.

You can assume nothing about the triplets given to you other than that they are valid triplets
and that they contain sufficient information to deduce the original string.
In particular, this means that the secret string will never contain letters
that do not occur in one of the triplets given to you.
"""

from time import time

def build_tree(triplets):
    tree = {}
    all_roots = set()
    all_leafs = set()
    for top, mid, bot in triplets:
        for _el in (top, mid, bot):
            if _el not in tree:
                tree[_el] = set()
        tree[mid].add(bot)
        tree[top].add(mid)
        all_roots.add(top)
        all_leafs.add(mid)
        all_leafs.add(bot)
    root = (all_roots - all_leafs).pop()
    return tree, root


def recoverSecret(triplets):
    tree, _root = build_tree(triplets)

    def walk_tree(root, depth):
        result = root
        for sib in tree[root]:
            sub_res = root + walk_tree(sib, depth - 1)
            if len(sub_res) > len(result):
                result = sub_res
                if len(result) == depth:
                    return result
        return result
    return walk_tree(_root, len(tree))
