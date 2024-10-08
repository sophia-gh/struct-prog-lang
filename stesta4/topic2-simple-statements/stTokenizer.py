# tokenizer
""" 
break character stream into tokens, provide a token stream
"""
import re #syntax for regular expressions is universal, implementation is defined in this library 

patterns = [
    ["\\(", "("], 
    ["\\)", ")"],
    ["\\+\\+", "++"],
    ["\\+", "+"], #if encounter a 'plus' token, produce a plus
    ["\\-", "-"], #if encounter a 'minus' token, produce a minus
    ["\\*", "*"], 
    ["\\/", "/"],
    ["==", "=="],
    ["!=", "!="],
    [">=", ">="],
    ["<=", "<="],
    ["<", "<"],
    [">", ">"],
    ["=", "="],
    ["or", "or"],
    ["and", "and"],
    ["not", "not"],
    ["print", "print"],
    ["while", "while"],
    ["do", "do"],
    ["if", "if"],
    ["else", "else"],
    ["function", "function"],
    ["return", "return"],
    ["(\\d+\\.\\d*)|(\\d*\\.\\d+)|(\\d+)","number"], #describing floating point number, syntax of regular expressions
    ["[A-Za-z][A-Za-z0-9]*","identifier"],
    ["\\&\\&", "&&"], ["\\|\\|", "||"], ["\\!", "!"],
]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])

#tokenize takes a string checks if it matches a pattern in patterns, adds that coresponding tag
#what does it return-->look at notes 
def tokenize(characters):
    tokens = []
    position = 0
    while position < len(characters):
        for pattern, tag in patterns: 
            match = pattern.match(characters, position) #if reg expression matches characters starting at position, match = true
            if match:
                break
        assert match, f"did not find match for {characters[position:]}"
        token = {
            'tag':tag,
            'value': match.group(0), #tokens can sometimes match multiple times, go with smallest group
            'position': position, #important to see where the error is
        }
        tokens.append(token)
        position = match.end()
    for token in tokens:
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] = float(token["value"])
            else:
                token["value"] = int(token["value"])
    token = {
        "tag" : None, 
        "value": None, 
        "position": None
    }
    tokens.append(token)
    return tokens

#tests-----------------------------------------------------------------------------------------------------------------------------------------
def test_simple_tokens():
    print("testing simple tokens") 
    assert tokenize("+") == [{'tag': '+', 'value': '+', 'position': 0}, {'tag': None, 'value': None, 'position': None}]
    assert tokenize("-") == [{'tag': '-', 'value': '-', 'position': 0}, {'tag': None, 'value': None, 'position': None}]
    i = 0
    for char in "+-*/()":
        tokens = tokenize(char)
        assert tokens[0]['tag'] == char
        assert tokens[0]['value'] == char
        assert tokens[0]['position'] == i
    for char in ["(", ")","+", "++", "-", "*", "/", "==", "!=", "<",">", "<=", ">=","=", "||", "&&", "!", "print"]:
        tokens = tokenize(char)
        assert tokens[0]['tag'] == char
        assert tokens[0]['value'] == char
        assert tokens[0]['position'] == i
    for number in ["123.45", "1.", ".1", "123"]:
        tokens = tokenize(number)
        assert tokens[0]["tag"] == "number"
        assert tokens[0]["value"] == float(number) 

if __name__ == "__main__":
    test_simple_tokens()
    print("done.")

