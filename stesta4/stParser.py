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
        node = {"tag":"negate", "value":node}
        return node, tokens[1:]

def parse_expression(tokens):
    return parse_simple_expression(tokens), tokens[1:]

def parse_factor(tokens):
    return parse_simple_expression(tokens)

def test_parse_simple_expression():
    """
    simple_expression = number | "("expression")" | "-" simple_expression
    """
    print("testing simple expressions")
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
        'tag': 'negate', 'value': {'tag': 'number', 'value': 2, 'position': 1}
    }
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        'tag': 'negate', 'value': {'tag': 'number', 'value': 2, 'position': 2}
    }
    print("done.")
    
def test_parse_factor():
    """
    factor = simple_expression
    """
    print("testing factors")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
    print("done")

if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()