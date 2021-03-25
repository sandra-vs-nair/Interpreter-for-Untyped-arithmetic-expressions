import sys
import syntax
import execute

# REPL that does nothing
for line in syntax.read_lines("> "):
    try:
        if(line == "quit"):
            exit(0)
        t = syntax.parse_term(line)
        print(execute.eval_term(t))
    except syntax.ParseError as e:
        print("error: {}".format(e))
