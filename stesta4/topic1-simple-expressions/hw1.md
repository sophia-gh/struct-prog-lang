## Tests for ```test_parse_term()``` and ```test_parse_expression()```
### >```test_parse_term()```
``` py
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
```
### >```test_parse_expression()```

```python
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
```
## Additional Test Cases for the Other Test Functions

### >```test_parse_factor()```
``` python
    ...
    #new test cases for hw 1
    for s in ["-(-4)", "4(4)", "-4(-4)"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
```

### >```test_parse_simple_expression()```
``` python
    ...
    #new test case for hw 1
    tokens = tokenize("(-(4))")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        'tag': 'negate', 
        'value': {'position': 3, 'tag': 'number', 'value': 4}
    }
```



