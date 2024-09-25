"""
parser.py - implement parser for simple expressions

Accept a string of tokens, return an AST expressed as a stack of dictionaries 
"""

"""
    simple_expression = number | identifer | "("expression")" | "-" simple_expression
    factor = simple_expression
    term = factor {"*"|"/" factor}
    arithmetic_expression = term { "+"|"-" term }
    comparison_expression = arithmetic_expression [ "==" | "!=" | "<" | ">" | "<=" | ">="  arithmetic expression ]
    boolean_term = comparison_expression { "&&" comparison_expression }
    boolean_expression = boolean_term { "or" boolean_term }
    expression = boolean_expression
    print_statement = "print "("expression")"
    assignment_statement = expression
    statement = print_statement | 
                assignment_expression

"""
from stTokenizer import tokenize
from pprint import pprint


def parse_simple_expression(tokens):
    """
    simple_expression = number | identifier | "("expression")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "identifer":
        pass # copy from topic 3 delozier
    if tokens[0]["tag"] == "(":
        node, tokens = parse_arithmetic_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag": "negate", "value": node}
        return node, tokens


# def parse_arithmetic_expression(tokens):
#     return parse_simple_expression(tokens), tokens[1:]


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
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_comparison_expression(tokens):
    """
    comparison_expression == arithmetic_expression [ "==" | "!=" | "<" | ">" | "<=" | ">="  arithmetic expression ]
    """
    node, tokens = parse_arithmetic_expression(tokens)
    if tokens[0]["tag"] in ["==", "!=", "<=", ">=", "<", ">"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_arithmetic_expression(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_boolean_term(tokens):
    """
    boolean_term == comparison_expression { "&&" comparison_expression }
    """
    node, tokens = parse_comparison_expression(tokens)
    while tokens[0]["tag"] in ["&&"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_comparison_expression(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_boolean_expression(tokens):
    """
    boolean_expression == boolean_term { "||" boolean_term }
    """
    node, tokens = parse_boolean_term(tokens)
    while tokens[0]["tag"] in ["||"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_boolean_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_print_statement(tokens):
    assert tokens[0]["tag"] == "print"
    assert tokens[1]["tag"] == "("
    tokens = tokens[2:]
    if tokens[0]["tag"] != ")":
        expression, tokens = parse_expression(tokens)
    else: 
        expression = None
    assert tokens[0]["tag"] == ")"
    node = {
        "tag":"print",
        "value":expression
    }
    return node, tokens[1:]

def test_parse_print_statement():
    print(f"\033[38;5;43m{"testing parse print statement"}\033[0m")
    tokens = tokenize("print(1)")
    ast, tokens = parse_print_statement(tokens)
    assert ast == {
        'tag': 'print', 
        'value': {'tag': 'number', 'value': 1, 'position': 6}
    }
    tokens = tokenize("print()")
    ast, tokens = parse_print_statement(tokens)
    assert ast == {
        'tag': 'print', 'value': None
        }

def parse_assignment_statement(tokens):
    """
    assignment_statement = expression
    """
    node, tokens = parse_expression(tokens)
    if tokens[0]["tag"] == "=":
        tag = tokens[0]["tag"]
        value, tokens = parse_expression(tokens[1:])
        node = {"tag": tag, "target": node, "value": value}
    return node, tokens

def test_parse_assignment_statement():
    print(f"\033[38;5;43m{"testing parse assignment statement"}\033[0m")
    tokens = tokenize("2")
    ast1, tokens1 = parse_expression(tokens)
    ast2, tokens1 = parse_assignment_statement(tokens)
    assert ast1 == ast2
    tokens = tokenize("3=4")
    node, tokens = parse(tokens)
    print(node)
    assert ast1 == ast2
    
def parse_expression(tokens):
    return parse_boolean_expression(tokens)

def test_parse_expression():
    print(f"\033[38;5;43m{"testing parse expression"}\033[0m")
    ast1, tokens = parse_expression(tokenize("8+9-10"))
    ast2, tokens = parse_boolean_expression(tokenize("8+9-10"))
    assert ast1 == ast2

def parse_statement(tokens):
    """statement = print_statement | 
                   expression
    """
    if tokens[0]["tag"] == "print":
        return parse_print_statement(tokens)
    return parse_expression(tokens)

def parse(tokens):
    ast, tokens = parse_statement(tokens)
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
    print(f"\033[38;5;43m{"testing arithmetic expression"}\033[0m")
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
    """
    comparison_expression == arithmetic_expression [ "==" | "!=" | "<" | ">" | "<=" | ">="  arithmetic expression ]
    """
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
    for op in ["<",">"]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_boolean_term(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        }
    op = "&&"
    node, tokens = parse_boolean_term(tokenize(f"7{op}8"))
    assert node == {
        "tag": op,
        "left": {"tag": "number", "value": 7, "position": 0},
        "right": {"tag": "number", "value": 8, "position": 3},
    } 

def test_parse_boolean_expression():
    print(f"\033[38;5;43m{"testing parse boolean expression"}\033[0m")
    for op in ["<",">"]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_boolean_expression(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        }
    tokens = tokenize(f"2||3")
    ast, tokens = parse_boolean_expression(tokens)
    assert ast == {
        "tag": "||",
        "left": {"tag": "number", "value": 2, "position": 0},
        "right": {"tag": "number", "value": 3, "position": 3},
    }

def test_parse():
    print(f"\033[38;5;43m{"testing parse"}\033[0m")
    tokens = tokenize("2+3+4/6")
    ast, _ = parse_statement(tokens)
    assert parse(tokens) == ast
    tokens = tokenize("1*2<3*4||5>6&&7")
    ast = parse(tokens)
    assert ast == {
        "tag": "||",
        "left": {
            "tag": "<",
            "left": {
                "tag": "*",
                "left": {"tag": "number", "value": 1, "position": 0},
                "right": {"tag": "number", "value": 2, "position": 2},
            },
            "right": {
                "tag": "*",
                "left": {"tag": "number", "value": 3, "position": 4},
                "right": {"tag": "number", "value": 4, "position": 6},
            },
        },
        "right": {
            "tag": "&&",
            "left": {
                "tag": ">",
                "left": {"tag": "number", "value": 5, "position": 9},
                "right": {"tag": "number", "value": 6, "position": 11},
            },
            "right": {"tag": "number", "value": 7, "position": 14},
        },
    }

def test_parse_statment():
    print(f"\033[38;5;43m{"testing parse statement"}\033[0m")
    tokens = tokenize("2+3+4/6")
    assert parse_statement(tokens) == parse_expression(tokens)
    ast, _ = parse_statement(tokens)
    


if __name__ == "__main__":
    print(f"\033[38;5;221m{"--Parser Test Cases--"}\033[0m")
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_arithmetic_expression()
    test_parse_comparison_expression()
    test_parse_boolean_term()
    test_parse_boolean_expression()
    test_parse_assignment_statement()
    test_parse_expression()
    test_parse_statment()
    test_parse_print_statement()
    test_parse()
    print(f"\033[38;5;117m{"done."}\033[0m")


# tokens is never populated by the parse_simple_expression() function
