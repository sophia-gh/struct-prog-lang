# in lisp there was a single language instruction called CAR(contents of .. register)
# ex (CAR '(1 2 3)) --> 1 returns first element of a list                "first"
# (CDR '(1 2 3)) --> '(2 3) returns list of elements after first element "tail"

# rules of functional programming: 
# no access to global variables, yes access to reading global state, do not mutate external state, can return values to affect global state
# use functions as first class variables 
# no changing outside world from within the function 
# break problem into smaller sub problems, rather than iteration 
# suggestion: do not use local variables 

def length(t):
    if t == [ ]:
        return 0
    return 1 + length(tail(t))

def first(t):
    if t == [ ]:
        return None
    return t[0]

def tail(t):
    if t == []:
        return []
    return t[1:]

def construct(n, t):
    return [n] + t

def concat(t, v):
    if length(t) == 0:
        return v
    else: 
        return construct(first(t), concat(tail(t), v))

# tests ---------------------------------------------------------------------------------------------
def test_length():
    print("testing length()")
    assert length([]) == 0
    assert length([1]) == 1
    assert length([1, 2, 3]) == 3

def test_first():
    print("testing first()")
    assert first([]) == None
    assert first([1]) == 1
    assert first([1, 2, 3]) == 1

def test_tail():
    print("testing tail()")
    assert tail([]) == []
    assert tail([1]) == []
    assert tail([1, 2, 3]) == [2, 3]

def test_construct():
    print("testing construct()")
    assert construct(1, []) == [1]
    assert construct(1, [2]) == [1, 2]
    assert construct(1, [2, 3]) == [1, 2, 3]

def test_concat():
    print("testing concat()")
    assert concat(1, []) == [1]
    assert concat([1], [2]) == [1, 2]
    assert concat([1,2], [3, 4]) == [1, 2, 3, 4]


if __name__ == "__main__":
    test_first()
    test_tail()
    test_construct()
    test_construct()
    print("done!!")
    