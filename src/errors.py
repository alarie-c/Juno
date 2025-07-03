from enum import Enum
from src.common import Span, Pos
from typing import TypeVar

# helper function to map characters when being printed
def map_source_chars(ch: str) -> str:
    if ch in '\n\t\r':
        return ' '
    else:
        return ch

class Error(Exception):
    """
    Holds information for all kinds of diagnostics that might be created
    at any point in the interpreter's running of the code.

    Attributes:
        kind (Diagnostic.Kind): the class of error.
        msg (str): the diagnostic help message.
        path (str): the file this diagnostic is for.
        span (Span): where in the source code this points to.
        pos (Pos): line and column of the start of the diagnostic.
        code (int): internal exception code.
    """
    class Kind(Enum):
        SYNTAX_ERROR = 0
        PARSE_ERROR = 1
        ILLEGAL_CHAR = 2
    
    def __init__(
        self,
        kind: 'Error.Kind',
        msg: str,
        path: str,
        span: Span,
        pos: Pos,
        code=None
    ):
        super().__init__(msg)
        self.kind = kind
        self.path = path
        self.span = span
        self.pos = pos
        self.code = code
        self.msg = msg

    def show(self, src: str):
        # error: (SyntaxError) in (main.juno:1:5)
        print(f'error: ({self.kind.name}) in ({self.path}:{self.pos})')
        
        start, end = self.span.bounds()
        
        assert start < len(src)
        assert end <= end
        
        source = ''.join(map(map_source_chars, src[start:end]))
        carets = '^' + '~' * (self.span.length - 1)
        spaces = ' ' * len(str(self.pos.col))

        #.   |
        # ln | source_code
        #    | ^~~~~~~~~~~
        # helper message here
        print(f'{spaces} |')
        print(f'{self.pos.line} | ', end='')
        print(f'{source}')
        print(f'{spaces} | {carets}')
        print(f'{self.msg}')

# T = TypeVar("T")
# class Result[T]:
#     def __init__(self, val: T | None, err: Error | None):
#         self.val = val
#         self.err = err

#     def unwrap(self) -> T:
#         assert self.val is not None
#         return self.val



 
