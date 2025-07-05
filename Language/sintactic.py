"""This module represents the behavior of a syntactic analyzer for MacraScript.

Author: MacraScript Language Team
"""

# SIMPLIFIED GRAMMAR DEFINITION FOR MACRAMÉ BRACELET PATTERNS:
# 
# <S>               -> "START" <PATTERN_TYPE> <PATTERN_BODY> "END"
# <PATTERN_TYPE>    -> "ALPHA" | "NORMAL"
# <PATTERN_BODY>    -> <PATTERN_CONFIG> <PATTERN_DATA>
# <PATTERN_CONFIG>  -> <THREADS_DEF> <DIMENSIONS_DEF> <COLORS_DEF>
# <THREADS_DEF>     -> "THREADS" ":" <INTEGER>
# <DIMENSIONS_DEF>  -> "WIDTH" ":" <INTEGER> | "HEIGHT" ":" <INTEGER> | <DIMENSIONS_DEF> <DIMENSIONS_DEF>
# <COLORS_DEF>      -> "COLORS" ":" "(" <COLOR_LIST> ")"
# <COLOR_LIST>      -> <COLOR> | <COLOR> "," <COLOR_LIST>
# <COLOR>           -> <COLOR_NAME> | <COLOR>
# <PATTERN_DATA>    -> <ALPHA_DATA> | <NORMAL_DATA>
# <ALPHA_DATA>      -> "PATTERN" "{" <ROW_LIST> "}"
# <ROW_LIST>        -> <ROW> | <ROW> <ROW_LIST>
# <ROW>             -> "ROW" ":" "(" (<COLOR_SEQUENCE> | <DIRECTION_SEQUENCE>) ")"
# <COLOR_SEQUENCE>  -> <INTEGER> | <INTEGER> "," <COLOR_SEQUENCE>
# <NORMAL_DATA>     -> "PATTERN" "{" <ROW_LIST> "}"
# <DIRECTION_SEQUENCE> -> <DIRECTION> | <DIRECTION> "," <DIRECTION_SEQUENCE>
# <DIRECTION>       -> "LEFT" | "RIGHT"


class SintacticAnalyzer:
    """This class represents the behavior of a syntactic analyzer for MacraScript."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.pattern_type = None
        self.pattern_data = {}
        self.advance()

    def advance(self):
        """This method advances the current token to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        """This method starts the parsing process following the grammar structure."""
        self.start()
        self.pattern_type_def()
        self.pattern_body()
        self.end()
        return self.pattern_data

    def start(self):
        """This method checks if the first token is 'START'."""
        if (
            self.current_token 
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "START"
        ):
            self.advance()
        else:
            self.error("START")

    def end(self):
        """This method checks if the last token is 'END'."""
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "END"
        ):
            self.advance()
            if self.current_token is not None:
                self.error("No extra tokens expected after END")
        else:
            self.error("END")

    def pattern_type_def(self):
        """This method processes the pattern type: ALPHA or NORMAL."""
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value in ["ALPHA", "NORMAL"]
        ):
            self.pattern_type = self.current_token.value
            self.pattern_data["type"] = self.pattern_type
            self.advance()
        else:
            self.error("ALPHA or NORMAL")

    def pattern_body(self):
        """This method processes the pattern configuration and data."""
        self.pattern_config()
        self.pattern_data_section()

    def pattern_config(self):
        """This method processes the pattern configuration (threads, dimensions, colors)."""
        self.threads_def()
        self.dimensions_def()
        self.colors_def()

    def threads_def(self):
        """This method processes the threads definition."""
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "THREADS"
        ):
            self.advance()
            if self.current_token and self.current_token.type_ == "COLON":
                self.advance()
                if self.current_token and self.current_token.type_ == "INTEGER":
                    threads_count = int(self.current_token.value)
                    self.pattern_data["threads"] = threads_count
                    self.advance()
                else:
                    self.error("INTEGER after THREADS:")
            else:
                self.error("':' after THREADS")
        else:
            self.error("THREADS")

    def dimensions_def(self):
        """This method processes width and height definitions."""
        # Process WIDTH
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "WIDTH"
        ):
            self.advance()
            if self.current_token and self.current_token.type_ == "COLON":
                self.advance()
                if self.current_token and self.current_token.type_ == "INTEGER":
                    width = int(self.current_token.value)
                    self.pattern_data["width"] = width
                    self.advance()
                else:
                    self.error("INTEGER after WIDTH:")
            else:
                self.error("':' after WIDTH")

        # Process HEIGHT
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "HEIGHT"
        ):
            self.advance()
            if self.current_token and self.current_token.type_ == "COLON":
                self.advance()
                if self.current_token and self.current_token.type_ == "INTEGER":
                    height = int(self.current_token.value)
                    self.pattern_data["height"] = height
                    self.advance()
                else:
                    self.error("INTEGER after HEIGHT:")
            else:
                self.error("':' after HEIGHT")

    def colors_def(self):
        """This method processes the colors definition."""
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "COLORS"
        ):
            self.advance()
            if self.current_token and self.current_token.type_ == "COLON":
                self.advance()
                if self.current_token and self.current_token.type_ == "LPAREN":
                    self.advance()
                    colors = self.color_list()
                    self.pattern_data["colors"] = colors
                    if self.current_token and self.current_token.type_ == "RPAREN":
                        self.advance()
                    else:
                        self.error("')' after color list")
                else:
                    self.error("'(' after COLORS:")
            else:
                self.error("':' after COLORS")
        else:
            self.error("COLORS")

    def color_list(self):
        """This method processes a list of colors."""
        colors = []
        
        # Get first color
        if self.current_token and (self.current_token.type_ == "COLOR" or self.current_token.type_ == "COLOR_NAME"):
            colors.append(self.current_token.value.strip('"'))
            self.advance()
        else:
            self.error("COLOR or COLOR_NAME")
        
        # Get additional colors
        while self.current_token and self.current_token.type_ == "COMMA":
            self.advance()
            if self.current_token and (self.current_token.type_ == "COLOR" or self.current_token.type_ == "COLOR_NAME"):
                colors.append(self.current_token.value.strip('"'))
                self.advance()
            else:
                self.error("COLOR or COLOR_NAME after comma")
        
        return colors

    def pattern_data_section(self):
        """This method processes the pattern data based on the pattern type."""
        if self.pattern_type == "ALPHA":
            self.alpha_data()
        elif self.pattern_type == "NORMAL":
            self.normal_data()

    def alpha_data(self):
        """This method processes ALPHA pattern data."""
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "PATTERN"
        ):
            self.advance()
            if self.current_token and self.current_token.type_ == "LBRACE":
                self.advance()
                rows = self.row_list()
                self.pattern_data["pattern_data"] = rows
                if self.current_token and self.current_token.type_ == "RBRACE":
                    self.advance()
                else:
                    self.error("'}' after pattern data")
            else:
                self.error("'{' after PATTERN")
        else:
            self.error("PATTERN")

    def row_list(self):
        """This method processes a list of rows for ALPHA patterns."""
        rows = []
        
        while (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "ROW"
        ):
            row = self.row()
            rows.append(row)
        
        return rows

    def row(self):
        """This method processes a single row definition."""
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "ROW"
        ):
            self.advance()
            if self.current_token and self.current_token.type_ == "COLON":
                self.advance()
                if self.current_token and self.current_token.type_ == "LPAREN":
                    self.advance()
                    
                    # Depending on the pattern type, parse color indices or knot directions
                    if self.pattern_type == "ALPHA":
                        sequence = self.color_sequence()
                    else: # NORMAL
                        sequence = self.direction_sequence()

                    if self.current_token and self.current_token.type_ == "RPAREN":
                        self.advance()
                        return sequence
                    else:
                        self.error("')' after color sequence")
                else:
                    self.error("'(' after ROW:")
            else:
                self.error("':' after ROW")
        else:
            self.error("ROW")

    def color_sequence(self):
        """This method processes a sequence of color indices."""
        sequence = []
        
        if self.current_token and self.current_token.type_ == "INTEGER":
            sequence.append(int(self.current_token.value))
            self.advance()
        else:
            self.error("INTEGER")
        
        while self.current_token and self.current_token.type_ == "COMMA":
            self.advance()
            if self.current_token and self.current_token.type_ == "INTEGER":
                sequence.append(int(self.current_token.value))
                self.advance()
            else:
                self.error("INTEGER after comma")
        
        return sequence

    def direction_sequence(self):
        """This method processes a sequence of knot directions (LEFT/RIGHT)."""
        sequence = []
        
        if self.current_token and self.current_token.type_ == "KEYWORDS" and self.current_token.value in ["LEFT", "RIGHT"]:
            sequence.append(self.current_token.value)
            self.advance()
        else:
            self.error("LEFT or RIGHT direction")
        
        while self.current_token and self.current_token.type_ == "COMMA":
            self.advance()
            if self.current_token and self.current_token.type_ == "KEYWORDS" and self.current_token.value in ["LEFT", "RIGHT"]:
                sequence.append(self.current_token.value)
                self.advance()
            else:
                self.error("LEFT or RIGHT direction after comma")
        
        return sequence

    def normal_data(self):
        """This method processes NORMAL pattern data using ROW definitions."""
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "PATTERN"
        ):
            self.advance()
            if self.current_token and self.current_token.type_ == "LBRACE":
                self.advance()
                rows = self.row_list() # Re-use row_list for the new structure
                self.pattern_data["pattern_data"] = rows
                if self.current_token and self.current_token.type_ == "RBRACE":
                    self.advance()
                else:
                    self.error("'}' after pattern data")
            else:
                self.error("'{' after PATTERN")
        else:
            self.error("PATTERN")

    def error(self, expected):
        """This method raises an exception if the current token is not the expected one.

        Args:
            expected (str): The expected token.
        """
        current = self.current_token.value if self.current_token else "EOF"
        current_type = self.current_token.type_ if self.current_token else "None"
        
        # Mostrar información adicional para depuración
        raise SyntaxError(
            f"Syntax error at position {self.pos}: expected {expected}, found '{current}'"
        )
