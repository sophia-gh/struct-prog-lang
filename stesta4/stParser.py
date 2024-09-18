"""
parser.py - implement parser for simple expressions

Accept a string of tokens, return an AST expressed as a stack of dictionaries 
"""

"""
    simple_expression = number | "("expression")" | "-" simple_expression
    factor = simple_expression
    term = factor {"*"|"/" factor}
    arithmetic_expression = term {"+"|"-" term}
    comparison_expression = arithmetic_expresion ["==" | "!=" | "<" | ">" | "<=" | ">="] arithmetic_expression
    boolean_expression = 
    ### expression = arithmetic_expression 

"""
from stTokenizer import tokenize
from pprint import pprint


def parse_simple_expression(tokens):
    """
    simple_expression = number | "("expression")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_arithmetic_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag": "negate", "value": node}
        return node, tokens


def parse_arithmetic_expression(tokens):
    return parse_simple_expression(tokens), tokens[1:]


def parse_factor(tokens):
    return parse_simple_expression(tokens)


def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in [
        "*",
        "/",
    ]:  # does not attempt to run when tokens is empty
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def parse_arithmetic_expression(tokens):
    """
    arithmetic_expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in [
        "+",
        "-",
    ]:  # does not attempt to run when tokens is empty
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_comparison_expression(tokens):
    """
    arithmetic_expression = term { "+"|"-" term }
    """
    node, tokens = parse_arithmetic_expression(tokens)
    while tokens[0]["tag"] in [
        "==",
        "!=",
        "<=",
        ">=", 
        "<",
        ">"
    ]:  # does not attempt to run when tokens is empty
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_boolean_term(tokens):
    node, tokens = parse_arithmetic_expression(tokens)
    while tokens[0]["tag"] in ["and"]:  # does not attempt to run when tokens is empty
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_boolean_expression(tokens):
    node, tokens = parse_boolean_term(tokens)
    while tokens[0]["tag"] in ["or"]:  # does not attempt to run when tokens is empty
        tag = tokens[0]["tag"]
        right_node, tokens = parse_boolean_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def parse(tokens):
    ast, tokens = parse_comparison_expression(tokens)
    return ast

# test functions ---------------------------------------------------------------------------------------------------
def test_parse_simple_expression():
    """
    simple_expression = number | "("expression")" | "-" simple_expression
    """
    print(f"\033[38;5;43m{"testing simple expressions"}\033[0m")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    tokens = tokenize("(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"tag": "number", "value": 2, "position": 1},
    }
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"tag": "number", "value": 2, "position": 2},
    }

    #new test case for hw 1
    tokens = tokenize("(-(4))")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        'tag': 'negate', 
        'value': {'position': 3, 'tag': 'number', 'value': 4}
    }


def test_parse_arithmetic_expression():
    """
    arithmetic_expression = term { "+"|"-" term }
    """
    print(f"\033[38;5;43m{"testing parse expression"}\033[0m")
    node, tokens = parse_arithmetic_expression(tokenize("7+8"))
    assert node == {
        "tag": "+",
        "left": {"tag": "number", "value": 7, "position": 0},
        "right": {"tag": "number", "value": 8, "position": 2},
    }
    node, tokens = parse_arithmetic_expression(tokenize("8+9-10"))
    assert node == {
        "tag": "-",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": 8, "position": 0},
            "right": {"tag": "number", "value": 9, "position": 2},
        },
        "right": {"tag": "number", "value": 10, "position": 4},
    }
    node, tokens = parse_arithmetic_expression(tokenize("2+3/4*5"))
    assert node == {
        "left": {"position": 0, "tag": "number", "value": 2},
        "right": {
            "left": {
                "left": {"position": 2, "tag": "number", "value": 3},
                "right": {"position": 4, "tag": "number", "value": 4},
                "tag": "/",
            },
            "right": {"position": 6, "tag": "number", "value": 5},
            "tag": "*",
        },
        "tag": "+",
    }


def test_parse_factor():
    """
    factor = simple_expression
    """
    print(f"\033[38;5;43m{"testing parse factors"}\033[0m")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
    
    #new test cases for hw 1
    for s in ["-(-4)", "4(4)", "-4(-4)"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))


def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print(f"\033[38;5;43m{"testing parse term"}\033[0m")
    node, tokens = parse_term(tokenize("7*2"))
    assert node == {
        "tag": "*",
        "left": {"tag": "number", "value": 7, "position": 0},
        "right": {"tag": "number", "value": 2, "position": 2},
    }
    node, tokens = parse_term(tokenize("8*3/7"))
    assert node == {
        "tag": "/",
        "left": {
            "tag": "*",
            "left": {"tag": "number", "value": 8, "position": 0},
            "right": {"tag": "number", "value": 3, "position": 2},
        },
        "right": {"tag": "number", "value": 7, "position": 4},
    }

def test_parse_comparison_expression():
    print(f"\033[38;5;43m{"testing parse comparison expression"}\033[0m")
    for op in ["<", ">"]:
        node, tokens = parse_comparison_expression(tokenize(f"7{op}8"))
        assert node == {
            "tag": op,
            "left": {"tag": "number", "value": 7, "position": 0},
            "right": {"tag": "number", "value": 8, "position": 2},
        } 
    for op in ["<=", "==", "!=", ">="]:
        node, tokens = parse_comparison_expression(tokenize(f"7{op}8"))
        assert node == {
            "tag": op,
            "left": {"tag": "number", "value": 7, "position": 0},
            "right": {"tag": "number", "value": 8, "position": 3},
        }

def test_parse_boolean_term():
    print(f"\033[38;5;43m{"testing parse boolean term"}\033[0m")
    for op in ["and"]:
        node, tokens = parse_boolean_term(tokenize(f"7{op}8"))
        assert node == {
            "tag": op,
            "left": {"tag": "number", "value": 7, "position": 0},
            "right": {"tag": "number", "value": 8, "position": 4},
        } 

def test_parse_boolean_expression():
    print(f"\033[38;5;43m{"testing parse boolean expression"}\033[0m")
    for op in ["or"]:
        node, tokens = parse_boolean_expression(tokenize(f"7{op}8"))
        assert node == {
            "tag": op,
            "left": {"tag": "number", "value": 7, "position": 0},
            "right": {"tag": "number", "value": 8, "position": 3},
        } 
        node, tokens = parse_boolean_expression(tokenize(f"7{op}9{op}8"))
        assert node == {
            'left': {'left': {'position': 0, 'tag': 'number', 'value': 7},
                'right': {'position': 3, 'tag': 'number', 'value': 9},
                'tag': 'or'},
            'right': {'position': 6, 'tag': 'number', 'value': 8},
            'tag': 'or'
        }
def test_parse():
    print(f"\033[38;5;43m{"testing parse"}\033[0m")
    tokens = tokenize("2+3+4/6")
    ast, _ = parse_boolean_expression(tokens)
    assert parse(tokens) == ast
    tokens = tokenize("1*2<3*4or5>6and7")
    ast = parse(tokens)
    pprint(ast)


if __name__ == "__main__":
    print(f"\033[38;5;221m{"--Parser Test Cases--"}\033[0m")
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_arithmetic_expression()
    test_parse_comparison_expression()
    test_parse_boolean_term()
    test_parse_boolean_expression()
    test_parse()
    parse(tokenize("4"))
    print(f"\033[38;5;117m{"done."}\033[0m")


# tokens is never populated by the parse_simple_expression() function
