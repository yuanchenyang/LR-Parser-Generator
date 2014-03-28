DEBUG = True
TERMINATOR = "$"

class S:
    """ Shift stack state n """
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return "S({})".format(self.n)

class R:
    """ Reduce by production n """
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return "R({})".format(self.n)

class ACC:
    """ Accept """
    def __repr__(self):
        return "ACC()"

class Symbol:
    """ Symbol with attributes """
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs
    def __getattr__(self, name):
        return self.attrs[name]
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
        return "Symbol({}, {})".format(self.name, self.attrs)

class Stack:
    def __init__(self, l=[]):
        self.l = l
    def push(self, a):
        self.l.append(a)
    def pop(self):
        return self.l.pop()
    def popl(self, n):
        res = self.l[-n:]
        self.l = self.l[:-n]
        return res
    def peek(self):
        return self.l[-1]
    def __repr__(self):
        return "Stack({})".format(self.l)

class Rstack(Stack):
    def __init__(self, l=[]):
        self.l = l[::-1]
    def __repr__(self):
        return "Rstack({})".format(self.l[::-1])

def parse(actions, prods, start_vertex, string):
    stack = Stack([S(start_vertex)])
    buf = Rstack(tokenize(string))
    while True:
        if DEBUG:
            print (stack, buf)
        state = stack.peek()
        tok = buf.peek()
        action = actions[state.n][tok]
        #import pdb; pdb.set_trace()
        if isinstance(action, ACC):
            return RESULT(stack)

        elif isinstance(action, S): # Shift
            buf.pop()
            stack.push(tok)
            stack.push(action)

        elif isinstance(action, R): # Reduce
            num, fn = prods[action.n]
            reduced = stack.popl(2 * num)
            goto_start_state = stack.peek()

            symbol = fn(*[elem for i, elem in enumerate(reduced) if i % 2 == 0])
            goto_state = actions[goto_start_state.n][symbol.name]

            stack.push(symbol)
            stack.push(goto_state)
        else:
            raise ValueError("Invalid action: " + str(action))

def tokenize(s):
    return s.split() + [TERMINATOR]

def RESULT(stack):
    stack.pop()
    #print(stack.pop().n)
