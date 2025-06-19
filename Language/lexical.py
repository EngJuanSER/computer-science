import re

class Token:
    """
    This class represents the data structure of a token,
    it means: the type of the token and the value (lexema).
    """
    def __init__(self, type_: str, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type_}, {self.value})'

class LexicalAnalizer:
    """This class represents the behavior of a simple lexical analyzer for MacraScript."""

    @staticmethod
    def lex(code: str) -> list:
        """
        This method receives a line of MacraScript code, and returns
        a list of tokens.

        Args:
            code(str): The line of code to be analyzed.
        """

        tokens = []

        token_specification = [
            # Keywords (Order matters: more specific before general IDENTIFIER)
            ("KEYWORDS",            r'\b(START|END|PATTERN|ALPHA|NORMAL|THREADS|WIDTH|HEIGHT|COLORS|ROW|KNOT|LEFT|RIGHT|REPEAT)\b'),
            
            # Literals
            ("COLOR",               r'"[A-Fa-f0-9]{6}"'),  # Hex color codes like "FF0000"
            ("COLOR_NAME",          r'"[a-zA-Z]+"'),       # Color names like "red", "blue"
            ("INTEGER",             r'\d+'),               # Numbers
            ("IDENTIFIER",          r'[a-zA-Z_][a-zA-Z0-9_]*'),
            
            # Operators and Punctuation
            ("COLON",               r':'),
            ("COMMA",               r','),
            ("LBRACE",              r'{'),
            ("RBRACE",              r'}'),
            ("LPAREN",              r'\('),
            ("RPAREN",              r'\)'),
            
            # Others
            ("NEWLINE",             r'\n'),
            ("SKIP",                r'[ \t]+'),
            ("MISMATCH",            r'.')
        ]

        tok_regex = "|".join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()

            if kind == "MISMATCH":
                raise RuntimeError(f'Unexpected character: {value}')
            elif kind == "SKIP":
                continue
            tokens.append(Token(kind, value))
        return tokens

