import syntax
import execute

for line in syntax.read_lines("> "):
    try:
        if(line == "quit"):
            exit(0)
        t = syntax.parse_term(line)
        print(execute.evaluation(t))
    except syntax.ParseError as e:
        print("error: {}".format(e))
