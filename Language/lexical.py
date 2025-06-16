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
            ("PATTERN_KEYWORD",             r'PATTERN'),
            ("TYPE_KEYWORD",                r'TYPE'),
            ("ALPHA_KEYWORD",               r'ALPHA'),
            ("NORMAL_KEYWORD",              r'NORMAL'),
            ("THREADS_KEYWORD",             r'THREADS'),
            ("BACKGROUND_COLOR_KEYWORD",    r'BACKGROUND_COLOR'),
            ("DEFINE_COLOR_KEYWORD",        r'DEFINE_COLOR'),
            ("INIT_THREADS_KEYWORD",        r'INIT_THREADS'),
            ("COLORS_KEYWORD",              r'COLORS'),
            ("KNOT_FESTON_KEYWORD",         r'KNOT_FESTON'),
            ("KNOT_PLANE_KEYWORD",          r'KNOT_PLANE'),
            ("LEFT_KEYWORD",                r'LEFT'),
            ("RIGHT_KEYWORD",               r'RIGHT'),
            ("ON_KEYWORD",                  r'ON'),
            ("REPEAT_KEYWORD",              r'REPEAT'),
            ("TIMES_KEYWORD",               r'TIMES'),
            ("SEQUENCE_KEYWORD",            r'SEQUENCE'),
            ("GRID_KEYWORD",                r'GRID'),
            ("DATA_KEYWORD",                r'DATA'),

            # Literals
            ("STRING_LITERAL",      r'"[^"]*"'), # Corrected: Simple quotes, no internal escaped quotes
            ("INTEGER",             r'\\d+'),    # Corrected: For one or more digits
            ("IDENTIFIER",          r'[a-zA-Z_][a-zA-Z0-9_]*'),

            # Operators and Punctuation
            ("COLON",               r':'),
            ("EQUALS",              r'='),
            ("LBRACE",              r'{'),
            ("RBRACE",              r'}'),
            ("COMMA",               r','),
            ("X_SEPARATOR",         r'x'), # For GRID definition like 10x12
            ("MINUS_OPERATOR",      r'-'), # Added for ranges like 1-4

            # Others
            ("NEWLINE",             r'\\n'),    # Corrected: For newline character
            ("SKIP",                r'[ \\t]+'), # Corrected: For spaces and tabs
            ("MISMATCH",            r'.')     # Catches any other character
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

# Example Usage (optional, for testing)
# if __name__ == '__main__':
#     analyzer = LexicalAnalizer()
#     test_code = """
# PATTERN MyPattern {
#     TYPE: ALPHA
#     THREADS: 10
#     BACKGROUND_COLOR: "white"
#     GRID: 8x8
#     DATA {
#         "R", "R", "B"
#         "G", "G", "Y"
#     }
# }
#
# DEFINE_COLOR Red = "FF0000"
#
# INIT_THREADS 12 COLORS "Red", "Blue"
#
# PATTERN AnotherPattern {
#     TYPE: NORMAL
#     THREADS: 4
#     SEQUENCE: {
#         KNOT_FESTON LEFT ON 1,2
#         KNOT_PLANE ON 1,2,3,4 REPEAT 2 TIMES
#     }
# }
# """
#     all_tokens = []
#     for line in test_code.split('\\n'):
#         if line.strip(): # Avoid processing empty lines directly if not needed
#             line_tokens = analyzer.lex(line + '\\n') # Add newline back if split removed it and it's significant
#             all_tokens.extend(line_tokens)
#
#     for token in all_tokens:
#         print(token)

