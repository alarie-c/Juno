from src.common import *
from src.errors import Error

def peek(src: str, i: int) -> str:
    return src[max(0, min(i + 1, len(src) - 1))]

def tokenize(src: str, path: str) -> tuple[list[Token], list[Error]]:
    """
    Tokenizes the source code and creates any erros that we made need as well.

    Parameters:
        src (str): the source code.
        path (str): the source code file path.
    """

    i, x, y = 0, 1, 1
    tokens, errs = [], []

    while i < len(src):
        ch = src[i]

        if ch in '\t\r ':
            i += 1
            x += 1
            continue

        elif ch == '\n':
            i += 1
            x = 1
            y += 1
            continue

        elif ch.isdigit():
            begin, number = i, ch
            while i + 1 < len(src):
                n = peek(src, i)
                if n.isdigit() or n == '.':
                    number += n
                    i += 1
                    x += 1
                else:
                    break
            span = Span(begin, len(number))
            pos = Pos(y, x)
            tokens.append(Token(Token.Kind.NUMBER, span, pos, number))

        elif ch.isalpha():
            begin, ident = i, ch
            while i + 1 < len(src):
                n = peek(src, i)
                if n.isalnum() or n == '.':
                    ident += n
                    i += 1
                    x += 1
                else:
                    break
            span = Span(begin, len(ident))
            pos = Pos(y, x)
            tokens.append(Token(Token.Kind.SYMBOL, span, pos, ident))

        elif ch == '"':
            begin, string = i, ''
            while True:
                if i + 1 >= len(src):
                    errs.append(Error(
                        Error.Kind.SYNTAX_ERROR,
                        'unterminated string literal',
                        path,
                        Span(begin, i),
                        Pos(y, x)))
                    break

                if peek(src, i) == '"':
                    i += 1
                    x += 1
                    break  
                string += peek(src, i)
                i += 1
                x += 1

            span = Span(begin, len(string) + 1)
            pos = Pos(y, x)
            tokens.append(Token(Token.Kind.STRING, span, pos, string))

        elif ch == '(':
            tokens.append(Token(Token.Kind.LPAR, Span(i, 1), Pos(y, x), ch))
        elif ch == ')':
            tokens.append(Token(Token.Kind.RPAR, Span(i, 1), Pos(y, x), ch))
        
        elif ch == '=':
            tokens.append(Token(Token.Kind.EQUALS, Span(i, 1), Pos(y, x), ch))
        elif ch == '+':
            tokens.append(Token(Token.Kind.PLUS, Span(i, 1), Pos(y, x), ch))
        elif ch == '-':
            if peek(src, i) == '>':
                i += 1
                x += 1
                tokens.append(Token(Token.Kind.ARROW, Span(i - 1, 2), Pos(y, x), '->'))
            else:
                tokens.append(Token(Token.Kind.MINUS, Span(i, 1), Pos(y, x), ch))
        elif ch == '*':
            tokens.append(Token(Token.Kind.STAR, Span(i, 1), Pos(y, x), ch))
        elif ch == '/':
            tokens.append(Token(Token.Kind.SLASH, Span(i, 1), Pos(y, x), ch))
        elif ch == ';':
            tokens.append(Token(Token.Kind.SEMICOLON, Span(i, 1), Pos(y, x), ch))
        elif ch == '^':
            tokens.append(Token(Token.Kind.CARET, Span(i, 1), Pos(y, x), ch))
        elif ch == ',':
            tokens.append(Token(Token.Kind.COMMA, Span(i, 1), Pos(y, x), ch))
        else:
            print(f'illegal: {ch}')
        
        i += 1
        x += 1
    
    tokens.append(Token(Token.Kind.EOF, Span(i, 0), Pos(y, x), ''))
    return tokens, errs 
    