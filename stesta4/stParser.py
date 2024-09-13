"""
parser.py - implement parser for simple expressions

Accept a string of tokens, return an AST expressed as a stack of dictionaries 
"""

"""
    simple_expression = number | "("expression")" | "-" simple_expression
    factor = simple_expression
    term = factor {"*"|"/" factor}
    expression = term {"+"|"-" term}
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
        node, tokens = parse_simple_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "error: expected ')'"
        return node, tokens
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag": "negate", "value": node}
        return node, tokens


def parse_expression(tokens):
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


def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
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


def parse(tokens):
    return parse_expression(tokens)


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
    print(f"\033[38;5;117m{"done."}\033[0m")


def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print(f"\033[38;5;43m{"testing parse expression"}\033[0m")
    node, tokens = parse_expression(tokenize("7+8"))
    assert node == {
        "tag": "+",
        "left": {"tag": "number", "value": 7, "position": 0},
        "right": {"tag": "number", "value": 8, "position": 2},
    }
    node, tokens = parse_expression(tokenize("8+9-10"))
    assert node == {
        "tag": "-",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": 8, "position": 0},
            "right": {"tag": "number", "value": 9, "position": 2},
        },
        "right": {"tag": "number", "value": 10, "position": 4},
    }
    node, tokens = parse_expression(tokenize("2+3/4*5"))
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
    print(f"\033[38;5;117m{"done."}\033[0m")


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
    print(f"\033[38;5;117m{"done."}\033[0m")


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
    print(f"\033[38;5;117m{"done."}\033[0m")


def test_parse():
    print(f"\033[38;5;43m{"testing parse"}\033[0m")
    tokens = tokenize("2+3+4/6")
    assert parse(tokens) == parse_expression(tokens)
    print(f"\033[38;5;117m{"done."}\033[0m")


if __name__ == "__main__":
    print(f"\033[38;5;221m{"--Parser Test Cases--"}\033[0m")
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse()
    parse(tokenize("4"))


# tokens is never populated by the parse_simple_expression() function
