from src.parser import Parser
from src.common import *
from src.node import Node

def test_assign(capsys):
    src = "x -> add (1, 2)"

    parser = Parser(src, 'testpath.juno')
    ast = parser.parse()

    with capsys.disabled():
        for n in ast:
            n.print(0)

        for e in parser.errs:
            e.show(src)

    assert len(parser.errs) == 0
    assert ast[0].kind == Node.Kind.MUTATE
    assert ast[0].span.offset == 0
    assert ast[0].span.length == 15

