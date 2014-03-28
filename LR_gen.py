from itertools import groupby
from LR import S, R, ACC, Symbol, TERMINATOR

class Pos:
    def __init__(self, lhs, rhs, pos):
        self.lhs = lhs
        self.rhs = rhs
        self.pos = pos
    def cur_symbol(self):
        if len(self.rhs) <= self.pos:
            return None
        return self.rhs[self.pos]
    def increment(self):
        return Pos(self.lhs, self.rhs, self.pos + 1)
    def can_increment(self):
        return self.pos < len(self.rhs)
    def __hash__(self):
        return hash((self.lhs, self.rhs, self.pos))
    def __eq__(self, other):
        return (self.lhs, self.rhs) == (other.lhs, other.rhs)
    def __str__(self):
        newrhs = list(self.rhs)
        newrhs.insert(self.pos, ".")
        return "{} -> {}".format(self.lhs, " ".join(newrhs))
    def __repr__(self):
        return "Pos({}, {}, {})".format(self.lhs, self.rhs, self.pos)

class GraphNode:
    def __init__(self, pos_list, edges, vertex):
        self.pos_list = pos_list
        self.edges = edges
        self.vertex = vertex
    def get_edges_str(self):
        res = []
        for sym, dest in self.edges.items():
            res.append("{} -> N{}".format(sym, dest))
        return res

def print_dfa(dfa):
    for k, v in dfa.items():
        print(k)
        if v != []:
            print ("  " + "\n  ".join(map(str, v)))

def print_graph(graph):
    for k, v in graph.items():
        print ("N{}: {}".format(k, v.vertex))
        if v.edges != []:
            print ("  " + "\n  ".join(v.get_edges_str()))

def possible_expansions(g, symbol, seen):
    seen.add(symbol)
    result = []
    for prod in g.get(symbol, []):
        result.append(Pos(symbol, prod, 0))
        if prod[0] not in seen:
            result.extend(possible_expansions(g, prod[0], seen))
    return result

def create_node(g, dfa, positions):
    # POSITIONS contain productions all at the same symbol
    pos_id = positions[0]
    symbol = pos_id.cur_symbol()
    expanded = possible_expansions(g, symbol, set())
    dfa[pos_id] = positions[1:] + expanded

    for symbol, group in groupby(positions + expanded, Pos.cur_symbol):
        group = sorted(filter(Pos.can_increment, group), key=Pos.__repr__)
        if group != [] and group[0].increment() not in dfa:
            create_node(g, dfa, list(map(Pos.increment, group)))

def make_graph(g, dfa):
    graph = {}
    vertex_map = {}

    for vertex, pos in enumerate(dfa):
        vertex_map[pos] = vertex

    for vertex, pos_list in dfa.items():
        edges = {}
        for pos in pos_list + [vertex]:
            next_pos = pos.increment()
            if next_pos in vertex_map:
                edges[pos.cur_symbol()] = vertex_map[next_pos]
        graph[vertex_map[vertex]] = GraphNode(pos_list, edges, vertex)
    return graph

def make_table(g, graph, start_point):
    actions = {}
    terminals = get_terminals(g)

    productions = []
    for lhs, prods in g.items():
        for rhs in prods:
            productions.append(Pos(lhs, rhs, 0))
    prod_map = {p.rhs: i for i, p in enumerate(productions)}

    def table_entry(node):
        entry = {}
        if not node.vertex.can_increment():
            if node.vertex.lhs == start_point:
                entry[TERMINATOR] = ACC()
            else:
                # TODO: Need FOLLOW to work properly
                for t in terminals:
                    entry[t] = R(prod_map[node.vertex.rhs])
        for symbol, dest in node.edges.items():
            entry[symbol] = S(dest)
        return entry

    table = [table_entry(graph[i]) for i in range(len(graph))]

    return table, productions

def parse_grammar(g):
    lines = g.strip().split("\n")
    grammar = {}
    for line in lines:
        lhs, rhs = line.split('->')
        options = rhs.split("|")
        grammar[lhs.strip()] = [tuple(o.split()) for o in options]
    return grammar

def get_terminals(g):
    non_terminals = set(g.keys())
    symbols = set(TERMINATOR)
    for prods in g.values():
        for prod in prods:
            symbols.update(set(prod))
    return symbols.difference(non_terminals)

def find_start_vertex(graph, start_point):
    for num, node in graph.items():
        pos = node.vertex
        if pos.lhs == start_point and pos.pos == 0:
            return num

def bind(symb):
    def printn(*args):
        print(", ".join(map(str, args)))
        return Symbol(symb, {})
    return printn

def generate(grammar_str, start):
    start_point = start + "'"
    dfa = {}

    grammar = parse_grammar(grammar_str)
    grammar[start_point] = [(start,)]

    create_node(grammar, dfa, [Pos(start_point, (start,), 0)])
    graph = make_graph(grammar, dfa)
    print_graph(graph)

    actions, productions = make_table(grammar, graph, start_point)
    productions = [(len(p.rhs), bind(p.lhs)) for p in productions]

    return actions, productions, find_start_vertex(graph, start_point)
