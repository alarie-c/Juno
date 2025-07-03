from src.tokenizer import tokenize
from src.common import *

def test_tokenizer(capsys):
    src = 'x = 5 - 10\nx -> "hello"'

    tokens, errs = tokenize(src, 'test.juno')

    assert tokens[0].kind == Token.Kind.SYMBOL
    assert tokens[1].kind == Token.Kind.EQUALS
    assert tokens[2].kind == Token.Kind.NUMBER
    assert tokens[3].kind == Token.Kind.MINUS
    assert tokens[4].kind == Token.Kind.NUMBER
    assert tokens[5].kind == Token.Kind.SYMBOL
    assert tokens[6].kind == Token.Kind.ARROW
    assert tokens[7].kind == Token.Kind.STRING
    
    with capsys.disabled():
        for t in tokens:
            print(t)
        for e in errs:
            e.show(src)