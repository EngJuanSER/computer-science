"""This module represents the behavior of a semantic analyzer for MacraScript.

MacraScript allows for defining macrame bracelet patterns in two modes:
- ALPHA: Pixel-based patterns (similar to friendship bracelets)
- NORMAL: Traditional macrame knot-based patterns

Author: Juan Serrano
"""


class MacraPattern:
    """A class representing a processed MacraScript pattern."""

    def __init__(self):
        self.pattern_type = None  # "ALPHA" or "NORMAL"
        self.thread_count = 0
        self.width = 0
        self.height = 0
        self.colors = []  # List of colors by index (not dictionary)
        self.rows = []    # For ALPHA patterns (list of integer lists)
        self.knots = []   # For NORMAL patterns (sequence of knot instructions)
        self.is_valid = False
        self.errors = []
    
    def to_dict(self):
        """
        Convert the pattern to a dictionary format compatible with the sintactic analyzer output.
        """
        result = {
            "type": self.pattern_type,
            "threads": self.thread_count,
            "width": self.width,
            "height": self.height,
            "colors": self.colors,
        }
        
        if self.rows:
            result["pattern_data"] = self.rows
        elif self.knots:
            result["pattern_data"] = self.knots
            
        return result
    
    def __str__(self):
        """Returns a string representation of the pattern."""
        result = f"MacraPattern ({self.pattern_type})\n"
        result += f"  Threads: {self.thread_count}\n"
        result += f"  Dimensions: {self.width}x{self.height}\n"
        result += f"  Colors: {len(self.colors)} {self.colors}\n"
        
        if self.pattern_type == "ALPHA":
            result += f"  Rows: {len(self.rows)}\n"
            # Display a small preview of the pattern
            if self.rows:
                result += "  Preview:\n"
                for i, row in enumerate(self.rows[:3]):
                    result += f"    {row[:10]}{'...' if len(row) > 10 else ''}\n"
                if len(self.rows) > 3:
                    result += "    ...\n"
        else:  # NORMAL
            result += f"  Knots: {len(self.knots)}\n"
            # Display a small preview of knot instructions
            if self.knots:
                result += "  Preview:\n"
                for i, knot in enumerate(self.knots[:5]):
                    result += f"    {knot}\n"
                if len(self.knots) > 5:
                    result += "    ...\n"
                    
        return result


# pylint: disable=too-few-public-methods
class SemanticAnalyzer:
    """This class represents the behavior of a semantic analyzer for MacraScript."""

    def __init__(self, tokens_input: list):
        """
        Initialize the semantic analyzer with a list of tokens.
        
        Args:
            tokens_input (list): List of tokens from the lexical analyzer
        """
        self.tokens = tokens_input
        self.current_index = 0
        self.pattern = MacraPattern()
        
        # Valid knot types for NORMAL patterns (direction LEFT/RIGHT)
        self.valid_directions = ["LEFT", "RIGHT"]
        
    def analyze(self):
        """
        Analyzes the tokens and returns a MacraPattern object.
        
        Returns:
            MacraPattern: The processed pattern with all semantic information
            
        Raises:
            Exception: If there are semantic errors in the pattern
        """
        try:
            # Process tokens and build a semantic representation
            self._process_tokens()
            
            # Validate the pattern after processing
            self._validate_pattern()
                
            self.pattern.is_valid = len(self.pattern.errors) == 0
            
            if not self.pattern.is_valid:
                raise Exception(f"Semantic errors found: {'; '.join(self.pattern.errors)}")
                
            return self.pattern
            
        except Exception as e:
            self.pattern.errors.append(str(e))
            self.pattern.is_valid = False
            return self.pattern
            
    def _process_tokens(self):
        """
        Process all tokens and build a semantic representation of the pattern.
        This method follows the token stream and constructs the pattern as it goes.
        """
        # Verify the program starts with START
        if self.current_index >= len(self.tokens) or self.tokens[self.current_index].type_ != "KEYWORDS" or self.tokens[self.current_index].value != "START":
            raise Exception("Program must start with START keyword")
        
        self._advance()
        
        # Get pattern type (ALPHA or NORMAL)
        if self.current_index < len(self.tokens) and self.tokens[self.current_index].type_ == "KEYWORDS" and self.tokens[self.current_index].value in ["ALPHA", "NORMAL"]:
            self.pattern.pattern_type = self.tokens[self.current_index].value
            self._advance()
        else:
            raise Exception("Pattern type must be ALPHA or NORMAL")
        
        # Process configuration and pattern data
        self._process_configuration()
        self._process_pattern_data()
        
        # Verify the program ends with END
        if self.current_index >= len(self.tokens) or self.tokens[self.current_index].type_ != "KEYWORDS" or self.tokens[self.current_index].value != "END":
            raise Exception("Program must end with END keyword")
    
    def _process_configuration(self):
        """Process configuration section: THREADS, WIDTH, HEIGHT, COLORS"""
        config_found = {"THREADS": False, "WIDTH": False, "HEIGHT": False, "COLORS": False}
        
        while self.current_index < len(self.tokens):
            token = self._current_token()
            
            if token.type_ != "KEYWORDS":
                break
            
            if token.value == "THREADS":
                self._process_threads_def()
                config_found["THREADS"] = True
            elif token.value == "WIDTH":
                self._process_width_def()
                config_found["WIDTH"] = True
            elif token.value == "HEIGHT":
                self._process_height_def()
                config_found["HEIGHT"] = True
            elif token.value == "COLORS":
                self._process_colors_def()
                config_found["COLORS"] = True
            elif token.value == "PATTERN":
                # Beginning of pattern data
                break
            elif token.value == "END":
                # End of program
                break
            else:
                # Unknown keyword
                self._advance()
        
        # Check required configuration
        if self.pattern.pattern_type == "ALPHA":
            required_configs = ["THREADS", "WIDTH", "HEIGHT", "COLORS"]
        else:  # NORMAL
            required_configs = ["THREADS", "COLORS"]
            
        for config in required_configs:
            if not config_found[config]:
                self.pattern.errors.append(f"Missing required {config} configuration for {self.pattern.pattern_type} pattern")
    
    def _process_threads_def(self):
        """Process THREADS configuration."""
        # Skip THREADS keyword
        self._advance()
        
        # Expect COLON
        if self._current_token().type_ != "COLON":
            self.pattern.errors.append("Expected ':' after THREADS")
            self._advance()
            return
            
        self._advance()
        
        # Expect INTEGER
        if self._current_token().type_ != "INTEGER":
            self.pattern.errors.append("Expected integer value after THREADS:")
            self._advance()
            return
            
        thread_count = int(self._current_token().value)
        if thread_count <= 0:
            self.pattern.errors.append(f"Thread count must be positive, got {thread_count}")
            
        self.pattern.thread_count = thread_count
        self._advance()
    
    def _process_width_def(self):
        """Process WIDTH configuration."""
        # Skip WIDTH keyword
        self._advance()
        
        # Expect COLON
        if self._current_token().type_ != "COLON":
            self.pattern.errors.append("Expected ':' after WIDTH")
            self._advance()
            return
            
        self._advance()
        
        # Expect INTEGER
        if self._current_token().type_ != "INTEGER":
            self.pattern.errors.append("Expected integer value after WIDTH:")
            self._advance()
            return
            
        width = int(self._current_token().value)
        if width <= 0:
            self.pattern.errors.append(f"Width must be positive, got {width}")
            
        self.pattern.width = width
        self._advance()
    
    def _process_height_def(self):
        """Process HEIGHT configuration."""
        # Skip HEIGHT keyword
        self._advance()
        
        # Expect COLON
        if self._current_token().type_ != "COLON":
            self.pattern.errors.append("Expected ':' after HEIGHT")
            self._advance()
            return
            
        self._advance()
        
        # Expect INTEGER
        if self._current_token().type_ != "INTEGER":
            self.pattern.errors.append("Expected integer value after HEIGHT:")
            self._advance()
            return
            
        height = int(self._current_token().value)
        if height <= 0:
            self.pattern.errors.append(f"Height must be positive, got {height}")
            
        self.pattern.height = height
        self._advance()
    
    def _process_colors_def(self):
        """Process COLORS configuration."""
        # Skip COLORS keyword
        self._advance()
        
        # Expect COLON
        if self._current_token().type_ != "COLON":
            self.pattern.errors.append("Expected ':' after COLORS")
            self._advance()
            return
            
        self._advance()
        
        # Expect LPAREN
        if self._current_token().type_ != "LPAREN":
            self.pattern.errors.append("Expected '(' after COLORS:")
            self._advance()
            return
            
        self._advance()
        
        # Process color list
        colors = self._process_color_list()
        self.pattern.colors = colors
        
        # Expect RPAREN
        if self._current_token().type_ != "RPAREN":
            self.pattern.errors.append("Expected ')' after color list")
            return
            
        self._advance()
        
    def _process_color_list(self):
        """Process a list of colors."""
        colors = []
        
        # Get first color
        if self._current_token().type_ in ["COLOR", "COLOR_NAME"]:
            colors.append(self._current_token().value.strip('"'))
            self._advance()
        else:
            self.pattern.errors.append(f"Expected color, got {self._current_token().type_}")
            self._advance()
            return colors
            
        # Process additional colors
        while self._current_token().type_ == "COMMA":
            self._advance()
            if self._current_token().type_ in ["COLOR", "COLOR_NAME"]:
                colors.append(self._current_token().value.strip('"'))
                self._advance()
            else:
                self.pattern.errors.append(f"Expected color after comma, got {self._current_token().type_}")
                self._advance()
                break
                
        return colors
    
    def _process_pattern_data(self):
        """Process pattern data section based on pattern type."""
        # Look for PATTERN keyword
        if self._current_token().type_ != "KEYWORDS" or self._current_token().value != "PATTERN":
            self.pattern.errors.append("Expected PATTERN keyword")
            return
            
        self._advance()
        
        # Expect LBRACE
        if self._current_token().type_ != "LBRACE":
            self.pattern.errors.append("Expected '{' after PATTERN")
            return
            
        self._advance()
        
        # Process pattern data based on type
        if self.pattern.pattern_type == "ALPHA":
            self._process_alpha_pattern()
        else:  # NORMAL
            self._process_normal_pattern()
        
        # Expect RBRACE
        if self._current_token().type_ != "RBRACE":
            self.pattern.errors.append("Expected '}' after pattern data")
            return
            
        self._advance()
    
    def _process_alpha_pattern(self):
        """Process ALPHA pattern data with rows of color indices."""
        rows = []
        row_count = 0
        
        # Process rows until we find RBRACE or end of tokens
        while self._current_token().type_ == "KEYWORDS" and self._current_token().value == "ROW":
            # Process row definition
            row = self._process_row()
            rows.append(row)
            row_count += 1
            
            # Check row length
            if self.pattern.width > 0 and len(row) != self.pattern.width:
                self.pattern.errors.append(f"Row {row_count} has {len(row)} colors, but pattern width is {self.pattern.width}")
        
        # Check total row count
        if self.pattern.height > 0 and row_count != self.pattern.height:
            self.pattern.errors.append(f"Pattern has {row_count} rows, but height is {self.pattern.height}")
            
        self.pattern.rows = rows
    
    def _process_row(self):
        """Process a single ROW definition for either ALPHA or NORMAL patterns."""
        # Skip ROW keyword
        self._advance()
        
        # Expect COLON
        if self._current_token().type_ != "COLON":
            self.pattern.errors.append("Expected ':' after ROW")
            self._advance()
            return []
            
        self._advance()
        
        # Expect LPAREN
        if self._current_token().type_ != "LPAREN":
            self.pattern.errors.append("Expected '(' after ROW:")
            self._advance()
            return []
            
        self._advance()
        
        # Process sequence based on pattern type
        if self.pattern.pattern_type == "ALPHA":
            sequence = self._process_color_sequence()
        else: # NORMAL
            sequence = self._process_direction_sequence()

        # Expect RPAREN
        if self._current_token().type_ != "RPAREN":
            self.pattern.errors.append("Expected ')' after sequence")
        else:
            self._advance()
            
        return sequence
    
    def _process_color_sequence(self):
        """Process a sequence of color indices in a row."""
        indices = []
        
        # Get first index
        if self._current_token().type_ == "INTEGER":
            color_index = int(self._current_token().value)
            
            # Validate color index
            if color_index < 0 or (self.pattern.colors and color_index >= len(self.pattern.colors)):
                self.pattern.errors.append(f"Color index {color_index} is out of range")
                
            indices.append(color_index)
            self._advance()
        else:
            self.pattern.errors.append(f"Expected integer for color index, got {self._current_token().type_}")
            self._advance()
            return indices
            
        # Process additional indices
        while self._current_token().type_ == "COMMA":
            self._advance()
            
            if self._current_token().type_ == "INTEGER":
                color_index = int(self._current_token().value)
                
                # Validate color index
                if color_index < 0 or (self.pattern.colors and color_index >= len(self.pattern.colors)):
                    self.pattern.errors.append(f"Color index {color_index} is out of range")
                    
                indices.append(color_index)
                self._advance()
            else:
                self.pattern.errors.append(f"Expected integer for color index, got {self._current_token().type_}")
                self._advance()
                break
                
        return indices
    
    def _process_direction_sequence(self):
        """Process a sequence of knot directions in a row."""
        directions = []
        
        # Get first direction
        if self._current_token().type_ == "KEYWORDS" and self._current_token().value in self.valid_directions:
            directions.append(self._current_token().value)
            self._advance()
        else:
            self.pattern.errors.append(f"Expected a direction (LEFT/RIGHT), got {self._current_token().type_}")
            self._advance()
            return directions
            
        # Process additional directions
        while self._current_token().type_ == "COMMA":
            self._advance()
            
            if self._current_token().type_ == "KEYWORDS" and self._current_token().value in self.valid_directions:
                directions.append(self._current_token().value)
                self._advance()
            else:
                self.pattern.errors.append(f"Expected a direction after comma, got {self._current_token().type_}")
                self._advance()
                break
                
        return directions

    def _process_normal_pattern(self):
        """Process NORMAL pattern data by generating knots from rows of directions."""
        all_knots = []
        row_index = 0
        
        while self._current_token().type_ == "KEYWORDS" and self._current_token().value == "ROW":
            directions = self._process_row()
            
            # Determine the starting thread for this row (1 for even rows, 2 for odd rows)
            start_thread = 1 if row_index % 2 == 0 else 2
            
            # Validate row length
            expected_knots = (self.pattern.thread_count - (start_thread - 1)) // 2
            if len(directions) != expected_knots:
                self.pattern.errors.append(f"Row {row_index + 1} has {len(directions)} knots, but {expected_knots} were expected.")
            
            # Generate knot instructions for the current row
            for i, direction in enumerate(directions):
                thread1 = start_thread + i * 2
                thread2 = thread1 + 1
                
                if thread2 > self.pattern.thread_count:
                    self.pattern.errors.append(f"Knot in row {row_index + 1} involves a non-existent thread.")
                    continue

                knot = {
                    "direction": direction,
                    "threads": [thread1, thread2],
                    "repeat": 1
                }
                all_knots.append(knot)
            
            row_index += 1
        
        self.pattern.knots = all_knots
        
        if not all_knots:
            self.pattern.errors.append("NORMAL pattern must contain at least one ROW instruction.")

    def _validate_pattern(self):
        """Validate the pattern after all tokens have been processed."""
        # Check if pattern type is set
        if not self.pattern.pattern_type:
            self.pattern.errors.append("Missing pattern type")
            
        # Check thread count
        if self.pattern.thread_count <= 0:
            self.pattern.errors.append("Thread count must be positive")
            
        # Check dimensions for ALPHA patterns
        if self.pattern.pattern_type == "ALPHA":
            if self.pattern.width <= 0:
                self.pattern.errors.append("Width must be positive")
            
            if self.pattern.height <= 0:
                self.pattern.errors.append("Height must be positive")
                
        # Check colors
        if not self.pattern.colors:
            self.pattern.errors.append("Colors must be defined")
            
        # Check pattern data
        if self.pattern.pattern_type == "ALPHA" and not self.pattern.rows:
            self.pattern.errors.append("ALPHA pattern must contain rows")
            
        if self.pattern.pattern_type == "NORMAL" and not self.pattern.knots:
            self.pattern.errors.append("NORMAL pattern must contain knot instructions")
            
    def _current_token(self):
        """Returns the current token or a dummy token if at the end of tokens."""
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        
        # Return a dummy token to prevent errors
        from lexical import Token
        return Token("EOF", "EOF")
        
    def _advance(self):
        """Advances to the next token."""
        self.current_index += 1
