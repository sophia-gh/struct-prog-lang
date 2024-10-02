import sys

from stTokenizer import tokenize
from stParser import parse
from stEvaluator import evaluate
from pprint import pprint

def main():
    #check for command line arguments
    if len(sys.argv) > 1:
        #open file
        with open(sys.argv[1], 'r') as f:
            source_code = f.read()
        tokens = tokenize(source_code)
        ast = parse(tokens)
        evaluate(ast)
        exit()
    #repl loop
    debug = False
    environment = {} 
    while True:
        try:
            #read input
            source_code = input(">> ")
            if source_code.strip() in ["exit", "quit"]:
                break
            if source_code.strip() in ["debug"]:
                print([debug])
                debug = not debug
            tokens = tokenize(source_code)
            ast = parse(tokens)
            evaluate(ast, environment)
            if debug: 
                print("debugger is on.")
                pprint(environment)
            else: 
                print("debugger is off.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()