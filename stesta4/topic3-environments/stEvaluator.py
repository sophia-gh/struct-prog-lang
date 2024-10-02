from stTokenizer import tokenize
from stParser import parse

def evaluate(ast, environment):
    if ast["tag"] == "number":
        assert type(ast["value"]) in [float, int],f"unexpected numerical type {type(ast["value"])}"
        return ast["value"], False
    if ast["tag"] == "identifier":
        identifier = ast["value"]
        assert identifier in environment, f"Unknown identifier: '{identifier}'."
        return environment[identifier], False
    if ast["tag"] == "+":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value + right_value, False
    if ast["tag"] == "-":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value - right_value, False
    if ast["tag"] == "*":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value * right_value, False
    if ast["tag"] == "/":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        assert right_value != 0, "Division by zero"
        return left_value / right_value, False
    if ast["tag"] == "negate":
        value, _ = evaluate(ast["value"], environment)
        return -value, False
    if ast["tag"] == "&&":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value and right_value, False
    if ast["tag"] == "||":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value or right_value, False
    if ast["tag"] == "!":
        value, _ = evaluate(ast["value"], environment)
        return not value, False
    if ast["tag"] == "<":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value < right_value, False
    if ast["tag"] == ">":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value > right_value, False
    if ast["tag"] == "<=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value <= right_value, False
    if ast["tag"] == ">=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value >= right_value, False
    if ast["tag"] == "==":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value == right_value, False
    if ast["tag"] == "!=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value != right_value, False
    if ast["tag"] == "print":
        if ast["value"]:
            value, _ = evaluate(ast["value"], environment)
            print(value)
        else:
            print()
        return None, False
    if ast["tag"] == "=":
        assert 'target' in ast
        target = ast['target']
        assert target['tag'] == 'identifier'
        identifier = target['value']
        value, _ = evaluate(ast["value"], environment)
        environment[identifier] = value
        return None, False
    if ast["tag"] == "list":
        while ast:
            assert "statement" in ast
            value, return_chain = evaluate(ast["statement"], environment)
            ast = ast["list"]
        return value, return_chain
    assert False, "Unknown operator in AST"

#helper function ---------------------------------------------------
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



#tests---------------------------------------------------------------
def test_evaluate_single_value():
    print("\033[38;5;200mtest evaluate single value\033[0m")
    equals("4", {}, 4, {})
    equals("4.2", {}, 4.2, {})
    equals("3", {}, 3, {})
    equals("X", {'X':1}, 1)
    equals("Y", {'X':1, 'Y':2}, 2)

def test_evaluate_addition():
    print("\033[38;5;200mtest evaluate addition\033[0m")
    equals("1+1", {}, 2, {})
    equals("1.2+2.3+3.4", {}, 6.9, {})
    equals("X+Y", {"X": 1, "Y": 2}, 3)


def test_evaluate_subtraction():
    print("\033[38;5;200mtest evaluate subtraction\033[0m")
    equals("1-1", {}, 0, {})
    equals("3-2-1", {}, 0, {})
    equals("3+2*2", {}, 7, {})

def test_evaluate_multiplication():
    print("\033[38;5;200mtest evaluate multiplication\033[0m")
    equals("1*1", {}, 1, {})
    equals("3*2*2", {}, 12, {})
    equals("(3+2)*2", {}, 10, {})

def test_evaluate_division():
    print("\033[38;5;200mtest evaluate division\033[0m")
    equals("1/1", {}, 1, {})
    equals("4/2", {}, 2, {})
    equals("5/2", {}, 2.5, {})

def test_evaluate_negate():
    print("\033[38;5;200mest evaluate negate\033[0m")
    equals("-3", {}, -3, {})
    equals("-8+1", {}, -7, {})

def test_evaluate_print_statement():
    print("\033[38;5;200mtest print statement\033[0m")
    equals("print(77)", {}, None, {})
    equals("print()", {}, None, {})
    equals("print(50+7)", {}, None, {})
    equals("print(50+8)", {}, None, {})

def test_assignment_statement():
    print("\033[38;5;200mtest assignment statement\033[0m")
    equals("X=1", {}, None, {"X": 1})
    equals("x=x+1", {"x": 1}, None, {"x": 2})

def test_statement_list():
    print("\033[38;5;200mtest statement list\033[0m")
    equals("1", {}, 1)
    equals("1;2;print(4);print(5);x=6;print(x)", {}, None)  

if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_negate()
    test_evaluate_print_statement()
    test_assignment_statement()
    test_statement_list()
    print("\033[38;5;76mdone.\033[0m")
