from src.common import *
from src.errors import Error
from src.node import *
from src.tokenizer import tokenize

BINARY_INFIX = {
    Token.Kind.PLUS,
    Token.Kind.MINUS,
    Token.Kind.STAR,
    Token.Kind.SLASH,
}

class Parser:
    def __init__(self, src: str, path: str):
        tokens, errs = tokenize(src, path)
        
        self.src = src
        self.path = path
        self.tokens = tokens
        self.errs = errs
        self.pos = 0

        print("\n".join(str(x) for x in self.tokens))

    def here(self) -> Token:
        return self.tokens[max(0, min(self.pos, len(self.tokens) - 1))]
    
    def peek(self) -> Token:
        return self.tokens[max(0, min(self.pos + 1, len(self.tokens) - 1))]
    
    def atom(self) -> Node:
        token = self.here()

        if token.kind == Token.Kind.SYMBOL:
            return Symbol(token.span, token.lexeme)
        
        elif token.kind == Token.Kind.NUMBER:
            try:
                value = float(token.lexeme)
                return Number(token.span, value)
            except ValueError:
                raise Error(
                    Error.Kind.PARSE_ERROR,
                    'error parsing literal',
                    self.path,
                    token.span,
                    token.pos,
                )
        else:
            raise Error(
                Error.Kind.SYNTAX_ERROR,
                'expected expression',
                self.path,
                token.span,
                token.pos,
            )
        
    def call(self) -> Node:
        token = self.here()
        expr = self.atom()

        if self.peek().kind == Token.Kind.LPAR:
            self.pos += 1 # move to LPAR
            args = []
            self.pos += 1 # move to start

            while True:
                args.append(self.node())
                
                if self.peek().kind == Token.Kind.COMMA:
                    self.pos += 1 # move to COMMA
                    self.pos += 1 # move to next arg
                    continue
                elif self.peek().kind == Token.Kind.RPAR:
                    self.pos += 1 # move to RPAR
                    break
                else:
                    raise Error(
                        Error.Kind.SYNTAX_ERROR,
                        "expected closing parenthesis",
                        self.path,
                        token.span,
                        token.pos,
                    )

            span = token.span + self.here().span
            return Call(span, expr, args)
        
        return expr
        
    def binary(self) -> Node:
        token = self.here()
        expr = self.call()

        if self.peek().kind in BINARY_INFIX:
            self.pos += 1 # consume EXPR
            op = self.here().kind
            self.pos += 1 # consume OP

            rhs = self.binary()
            span = token.span + self.here().span
            return Binary(span, expr, rhs, op)
        
        return expr
        
    def assign(self) -> Node:
        token = self.here()
        expr = self.binary()
        
        mutate = 0
        peek = self.peek()
        
        if peek.kind == Token.Kind.ARROW:
            mutate = 1
        elif peek.kind == Token.Kind.EQUALS:
            mutate = 2
        
        if mutate != 0:
            self.pos += 1 # consume EXPR
            self.pos += 1 # consume ARROW

            if expr.kind != Node.Kind.SYMBOL:
                raise Error(
                    Error.Kind.SYNTAX_ERROR,
                    'expected symbol',
                    self.path,
                    expr.span,
                    token.pos,
                )
            value = self.binary()
            span = token.span + self.here().span
            
            if mutate == 1:
                return Mutate(span, expr, value)
            else:
                return Assign(span, expr, value)

        return expr
    
    def node(self) -> Node:
        return self.assign()
        
    def parse(self) -> list[Node]:
        ast = []
        
        try:
            node = self.node()
            ast.append(node)
            
            self.pos += 1
        except Error as e:
            self.errs.append(e)

        return ast