from stTokenizer import tokenize
from stParser import parse

def evaluate(ast, environment):
    return 6, False  #second value is return chain value (if not in return chain then false )

#tests---------------------------------------------------------------
def test_evaluate_single_value():
    print("test evaluate single value")
    equals("4", {}, 4, {})
    
start = "\033[1;31m"
end = "\033[0;0m"
def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (result == expected_result), f"""ERROR: when executing 
    {[code]}
    -- expected -- 
    {[expected_result]}
    -- got -- 
    {[result]}."""
    if expected_environment:
         assert (environment == expected_environment), f""" ERROR: when executing 
    {[code]}
    -- expected -- 
    {[expected_environment]}
    -- got -- 
    {[environment]}."""


if __name__ == "__main__":
    test_evaluate_single_value()
    print("done.")
