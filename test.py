from LR_gen import generate
from LR import parse, S, R, ACC, Symbol

def main():
    actions, prods, start_vertex = generate(GRAMMAR1, "E")
    print actions, prods
    parse(actions, prods, start_vertex, "id + id * ( id + id )")

ACTIONS = \
    [
        {"id": S(5), "(": S(4), "E": S(1), "T": S(2), "F": S(3)},
        {"+": S(6), "$": ACC()},
        {"+": R(1), "*": S(7), ")": R(1), "$": R(1)},
        {"+": R(3), "*": R(3), ")": R(3), "$": R(3)},
        {"id": S(5), "(": S(4), "E": S(8), "T": S(2), "F": S(3)},
        {"+": R(5), "*": R(5), ")": R(5), "$": R(5)},
        {"id": S(5), "(": S(4), "T": S(9), "F": S(3)},
        {"id": S(5), "(": S(4), "F": S(10)},
        {"+": S(6), ")": S(11)},
        {"+": R(0), "*": S(7), ")": R(0), "$": R(0)},
        {"+": R(2), "*": R(2), ")": R(2), "$": R(2)},
        {"+": R(4), "*": R(4), ")": R(4), "$": R(4)}
    ]

PRODS = \
    [
        (3, lambda e, _, t: Symbol("E", {"n": e.n + t.n})),
        (1, lambda t      : Symbol("E", {"n": t.n})),
        (3, lambda t, _, f: Symbol("T", {"n": t.n * f.n})),
        (1, lambda f      : Symbol("T", {"n": f.n})),
        (3, lambda _, e,__: Symbol("F", {"n": e.n})),
        (1, lambda _      : Symbol("F", {"n": 1}))
    ]

GRAMMAR = \
"""
letter -> a | b
E -> ( regexp ) | letter
mod_group -> E + | E ? | E * | E
string -> mod_group | mod_group . string | mod_group string
regexp -> string | string 1 regexp
"""

GRAMMAR1 = \
"""
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
"""

GRAMMAR2 = \
"""
S -> L = R | R
L -> * R | id
R -> L
"""

GRAMMAR3 = \
"""
E -> t | a E b
"""

if __name__ == "__main__":
    main()
