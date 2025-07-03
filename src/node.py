from abc import ABC, abstractmethod
from enum import Enum
from src.common import Token

from src.common import Span

class Node(ABC):
    class Kind(Enum):
        SYMBOL = 0
        NUMBER = 1
        STRING = 2
        BINARY = 3
        MUTATE = 4
        CALL = 5
        ASSIGN = 6
         
    def __init__(self, kind: 'Node.Kind', span: Span):
        self.span = span
        self.kind = kind

    @abstractmethod
    def print(self, i):
        pass

class Binary(Node):
    def __init__(self, span: Span, lhs: Node, rhs: Node, op: Token.Kind):
        super().__init__(Node.Kind.BINARY, span)
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def print(self, i):
        spaces = ' ' * i
        print(f'{spaces}BINARY(')
        print(f'{spaces}  LHS:', end='')
        self.lhs.print(i + 2)
        print(f'{spaces}  OP: {self.op.name}')
        print(f'{spaces}  RHS:', end='')
        self.rhs.print(i + 2)
        print(f'{spaces})')

class Mutate(Node):
    def __init__(self, span: Span, symbol: Node, new_val: Node):
        super().__init__(Node.Kind.MUTATE, span)
        self.symbol = symbol
        self.new_val = new_val

    def print(self, i):
        spaces = ' ' * i
        print(f'{spaces}MUTATION(')
        print(f'{spaces}  SYM:', end='')
        self.symbol.print(i + 2)
        print(f'{spaces}  VAL:', end='')
        self.new_val.print(i + 2)
        print(f'{spaces})')
    
class Number(Node):
    def __init__(self, span: Span, value: float):
        super().__init__(Node.Kind.NUMBER, span)
        self.value = value

    def print(self, i):
        spaces = ' ' * i
        print(f'{spaces}NUMBER({self.value})')
    
class Symbol(Node):
    def __init__(self, span: Span, name: str):
        super().__init__(Node.Kind.SYMBOL, span)
        self.name = name

    def print(self, i):
        spaces = ' ' * i
        print(f'{spaces}SYMBOL({self.name})')
    
class String(Node):
    def __init__(self, span: Span, value: str):
        super().__init__(Node.Kind.STRING, span)
        self.value = value

    def print(self, i):
        spaces = ' ' * i
        print(f'{spaces}STRING("{self.value}")')

class Call(Node):
    def __init__(self, span: Span, name: Node, args: list[Node]):
        super().__init__(Node.Kind.CALL, span)
        self.name = name
        self.args = args
        self.arity = len(args)

    def print(self, i):
        spaces = ' ' * i
        print(f'{spaces}CALL[{self.arity}](')
        print(f'{spaces}  NAME:', end='')
        self.name.print(i + 2)
        print(f'{spaces}  ARGS(')
        for a in self.args:
            a.print(i + 4)
        print(f'{spaces}  )\n{spaces})')

class Assign(Node):
    def __init__(self, span: Span, name: Node, initializer: Node | None):
        super().__init__(Node.Kind.ASSIGN, span)
        self.name = name
        self.initializer = initializer

    def print(self, i):
        spaces = ' ' * i
        print(f'{spaces}ASSIGN(')
        print(f'{spaces}  NAME:', end='')
        self.name.print(i + 1)
        
        if self.initializer is not None:
            print(f'{spaces}  INIT:', end='')
            self.initializer.print(i + 1)
        print(f'{spaces})')