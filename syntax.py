import sys
import os
import collections
try:
    import readline
except ImportError:
    pass

class ParseError(Exception):
    pass

### Constants

special_toks = ["(", ")"]

reserved_words = ["0", "succ", "pred", "iszero",
                  "true", "false", "if", "then", "else"]

### Lexer

def lexer(s):
    i = j = 0
    tokens = []
    def flush():
        nonlocal i
        if i < j:
            tokens.append("".join(s[i:j]))
            i = j
    while j < len(s):
        if s[j].isspace():
            flush()
            i = j = j+1
        else:
            for tok in special_toks:
                if s[j:j+len(tok)] == tok:
                    flush()
                    tokens.append(tok)
                    i = j = j+len(tok)
                    break
            else:
                j += 1
    flush()
    return tokens

### Parser

def expect(what, w):
    if len(w) == 0 or w[0] != what:
        raise ParseError("expected '{}'".format(what))
    w.popleft()
    
def parse_term(s):
    w = collections.deque(lexer(s))
    t = parse_abs(w)
    #print(t)
    if len(w) != 0:
        raise ParseError("unexpected '{}' after term".format(w[0]))
    return t
    
def parse_abs(w):
    if len(w) == 0:
        raise ParseError("unexpected end of string")
    elif w[0] == "if":
        expect("if", w)
        t1 = parse_abs(w)
        expect("then", w)
        t2 = parse_abs(w)
        expect("else", w)
        t3 = parse_abs(w)
        return ["if", t1, t2, t3]
    else:
        return parse_app(w)

def parse_app(w):
    if w[0] in ["succ", "pred", "iszero"]:
        op = w.popleft()
        t = [op, parse_atom(w)]
    else:
        t = parse_atom(w)
    while len(w) > 0 and w[0] not in [")", "then", "else"]:
        t = ["app", t, parse_atom(w)]
    return t

def parse_atom(w):
    if len(w) == 0:
        raise ParseError("unexpected end of string")
    elif w[0] == "(":
        expect("(", w)
        t = parse_abs(w)
        expect(")", w)
        return t
    elif w[0] == "0":
        expect("0", w)
        return "zero"
    elif w[0] in ["true", "false"]:
        return w.popleft()

def read_lines(prompt=""):
    """Read lines from stdin. If the file is a tty, that is, keyboard input
    from the user, then display a prompt and allow editing and history."""
    if os.isatty(sys.stdin.fileno()):
        while True:
            try:
                line = input(prompt)
            except EOFError:
                print()
                break
            yield line
    else:
        for line in sys.stdin:
            yield line
