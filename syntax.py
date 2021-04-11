import sys
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
                  "true", "false", "if", "then", "else", "and", "or", "not"]

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
        if s[j].isspace():                  #Ignores space
            flush()
            i = j = j+1
        else:
            for tok in special_toks: 
                if s[j:j+len(tok)] == tok:  #If paranthesis found
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
    t = parse_conditional(w)
    #print(t)
    if len(w) != 0:                 #If some token remains in w
        raise ParseError("unexpected '{}' after term".format(w[0]))
    return t
    
def parse_conditional(w):
    if len(w) == 0:
        raise ParseError("unexpected end of string")
    elif w[0] == "if":
        expect("if", w)
        t1 = parse_conditional(w)
        expect("then", w)
        t2 = parse_conditional(w)
        expect("else", w)
        t3 = parse_conditional(w)
        return ["if", t1, t2, t3]
    else:
        return parse_and(w)

def parse_and(w):
    if len(w) == 0:
        raise ParseError("unexpected end of string")
    elif w[0] == "and":
        expect("and", w)
        t1 = parse_conditional(w)
        expect("or", w)
        t2 = parse_conditional(w)
        expect("not", w)
        t3 = parse_conditional(w)
        return ["and", t1, t2, t3]
    else:
        return parse_app(w)

def parse_app(w):
    if w[0] in ["succ", "pred", "iszero"]:
        op = w.popleft()
        t = [op, parse_atom(w)]
    else:
        t = parse_atom(w)
    while len(w) > 0 and w[0] not in [")", "then", "else", "or", "not"]:
        t = [t, parse_atom(w)]
    return t

def parse_atom(w):
    if len(w) == 0:
        raise ParseError("unexpected end of string")
    elif w[0] == "(":
        expect("(", w)
        t = parse_conditional(w)
        expect(")", w)              #Closing paranthesis expected
        return t
    elif w[0] == "0":
        expect("0", w)
        return "0"
    elif w[0] in ["true", "false"]:
        return w.popleft()
    else:
        return [parse_var(w)]

def parse_var(w):
    if len(w) == 0:
        raise ParseError("unexpected end of string")
    elif w[0] in special_toks or w[0] in reserved_words:
        raise ParseError("unexpected '{}'".format(w[0]))
    else:
        return w.popleft()

def read_lines(prompt=""):
    while True:
        try:
            line = input(prompt)
        except EOFError:
            print()
            break
        yield line
