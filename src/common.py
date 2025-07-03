from enum import Enum

class Span:
    """
    Holds the source offset and length of any piece of source code. Can be
    converted into other forms like start/end bounds, or printed.

    Attributes:
        offset (int): what index this span starts on.
        length (int): how long is the span.
    """
    
    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def __str__(self):
        return f'({self.offset}+{self.length})'
    
    def bounds(self) -> tuple[int, int]:
        return (self.offset, self.offset + self.length)
    
    def __add__(self, o: 'Span') -> 'Span':
        diff = abs(o.offset - self.offset) - 1
        return Span(self.offset, (self.length + o.length) + diff)
        
    
class Pos:
    """
    A user-friendly format for source code span tracking, uses line and column
    instead of offset and length. This is recorded by the lexer.

    Attributes:
        line (int): the line number (1 based).
        col (int): the column numbr (1 based).
    """
    
    def __init__(self, line: int, col: int):
        self.line = line
        self.col = col

    def __str__(self):
        return f'{self.line}:{self.col}'
    
class Token:
    class Kind(Enum):
        EOF = 0
        SYMBOL = 1
        NUMBER = 2
        STRING = 3

        PLUS = 4
        MINUS = 5
        STAR = 6
        SLASH = 7

        EQUALS = 8
        ARROW = 9
        CARET = 10

        SEMICOLON = 11
        COMMA = 12

        LPAR = 13
        RPAR = 14

    def __init__(
        self, 
        kind: 'Token.Kind',
        span: Span,
        pos: Pos,
        lexeme: str
    ):
        self.lexeme = lexeme
        self.kind = kind
        self.span = span
        self.pos = pos

    def __str__(self):
        return f'({self.span}) | ({self.pos}) {self.kind.name} ({self.lexeme})' 
