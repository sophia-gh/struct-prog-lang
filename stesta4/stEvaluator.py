from stTokenizer import tokenize
from stParser import parse

def evaluate(ast, environment):
    if ast["tag"] == "number":
        assert type(ast["value"]) in [float, int], f"unexpected numerical type {type(ast["value"])}"
        return ast["value"], False  #second value is return chain value (if not in return chain then false )
    if ast['tag'] == "+":
        left_value, _ = evaluate(ast['left'], environment)
        right_value, _ = evaluate(ast['right'], environment)
        return left_value + right_value, False
    if ast['tag'] == "-":
        left_value, _ = evaluate(ast['left'], environment)
        right_value, _ = evaluate(ast['right'], environment)
        return left_value - right_value, False
    if ast['tag'] == "*":
        left_value, _ = evaluate(ast['left'], environment)
        right_value, _ = evaluate(ast['right'], environment)
        return left_value * right_value, False
    if ast['tag'] == "/":
        left_value, _ = evaluate(ast['left'], environment)
        right_value, _ = evaluate(ast['right'], environment)
        return left_value / right_value, False
    if ast['tag'] == "negate":
        value, _ = evaluate(ast['value'], environment)
        return -value, False
    assert False, "Unknown Operator in AST"

#tests---------------------------------------------------------------
def test_evaluate_single_value():
    print("\033[38;5;200m--test evaluate single value--\033[0m")
    equals("4", {}, 4, {})
    equals("4.2", {}, 4.2, {})
    equals("3", {}, 3, {})

def test_evaluate_addition():
    print("\033[38;5;200m--test evaluate addition--\033[0m")
    equals("1+1", {}, 2, {})
    equals("1.2+2.3+3.4", {}, 6.9, {})

def test_evaluate_subtraction():
    print("\033[38;5;200m--test evaluate subtraction--\033[0m")
    equals("1-1", {}, 0, {})
    equals("3-2-1", {}, 0, {})
    equals("3+2*2", {}, 7, {})

def test_evaluate_multiplication():
    print("\033[38;5;200m--test evaluate multiplication--\033[0m")
    equals("1*1", {}, 1, {})
    equals("3*2*2", {}, 12, {})
    equals("(3+2)*2", {}, 10, {})

def test_evaluate_division():
    print("\033[38;5;200m--test evaluate division--\033[0m")
    equals("1/1", {}, 1, {})
    equals("4/2", {}, 2, {})
    equals("5/2", {}, 2.5, {})

def test_evaluate_negate():
    print("\033[38;5;200m--test evaluate negate--\033[0m")
    equals("-3", {}, -3, {})
    equals("-8+1", {}, -7, {})
    

def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (result == expected_result), f"""\033[31m{"ERROR"}\033[0m: when executing 
    {[code]}
    -- expected -- 
    {[expected_result]}
    -- got -- 
    {[result]}."""
    if expected_environment != None:
         assert (environment == expected_environment), f"""\033[31m{"ERROR"}\033[0m: when executing 
        {[code]}
        -- expected environment-- 
        {[expected_environment]}
        -- got -- 
        {[environment]}."""


if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_negate()
    print("\033[38;5;76mdone.\033[0m")
