# Simplified Grammar Definition for MacraScript (BNF-like)
#
# <program> ::= <statement_list>
# <statement_list> ::= <statement> | <statement> <newline_token> <statement_list>
#
# <statement> ::= <pattern_definition>
#               | <color_definition>
#               | <thread_initialization>
#
# <pattern_definition> ::= "PATTERN" <identifier> "{" <newline_token>
#                              <pattern_body_list>
#                          "}"
#
# <pattern_body_list> ::= <pattern_attribute>
#                       | <pattern_attribute> <newline_token> <pattern_body_list>
#
# <pattern_attribute> ::= <type_attribute>
#                       | <threads_attribute>
#                       | <background_color_attribute>
#                       | <grid_attribute>        # For ALPHA patterns
#                       | <data_attribute>        # For ALPHA patterns
#                       | <sequence_attribute>    # For NORMAL patterns
#
# <type_attribute> ::= "TYPE" ":" <pattern_type>
# <pattern_type> ::= "ALPHA" | "NORMAL"
#
# <threads_attribute> ::= "THREADS" ":" <integer>
#
# <background_color_attribute> ::= "BACKGROUND_COLOR" ":" <string_literal>
#
# <grid_attribute> ::= "GRID" ":" <integer> "x" <integer>
#
# <data_attribute> ::= "DATA" "{" <newline_token>
#                          <data_row_list>
#                      "}"
# <data_row_list> ::= <data_row>
#                   | <data_row> <newline_token> <data_row_list>
# <data_row> ::= <color_value_list_comma_separated>
#
# <sequence_attribute> ::= "SEQUENCE" ":" "{" <newline_token>
#                              <knot_instruction_list>
#                          "}"
#
# <knot_instruction_list> ::= <knot_instruction>
#                           | <knot_instruction> <newline_token> <knot_instruction_list>
#
# <knot_instruction> ::= <knot_type> <direction>? "ON" <thread_references_comma_separated> (<repeat_clause>)?
# <knot_type> ::= "KNOT_FESTON" | "KNOT_PLANE" | <identifier> # Identifier for future custom knots
# <direction> ::= "LEFT" | "RIGHT"
# <thread_references_comma_separated> ::= <thread_reference> | <thread_reference> "," <thread_references_comma_separated>
# <thread_reference> ::= <integer> | <integer> "-" <integer> # e.g., 1 or 1-4
# <repeat_clause> ::= "REPEAT" <integer> "TIMES"
#
# <color_definition> ::= "DEFINE_COLOR" <identifier> "=" <string_literal>
#
# <thread_initialization> ::= "INIT_THREADS" <integer> ("COLORS" <color_value_list_comma_separated>)?
#
# <color_value_list_comma_separated> ::= <color_value> | <color_value> "," <color_value_list_comma_separated>
# <color_value> ::= <string_literal> | <identifier> # String for hex/name, or identifier for a defined color
#
# # --- Terminal Tokens (from Lexer) ---
# # <identifier> ::= IDENTIFIER
# # <integer> ::= INTEGER
# # <string_literal> ::= STRING_LITERAL
# # <newline_token> ::= NEWLINE (explicitly handled by parser)
# # Keywords: PATTERN, TYPE, ALPHA, NORMAL, THREADS, BACKGROUND_COLOR, GRID, DATA, SEQUENCE,
# #           DEFINE_COLOR, INIT_THREADS, COLORS, KNOT_FESTON, KNOT_PLANE, LEFT, RIGHT, ON, REPEAT, TIMES
# # Punctuation: {, }, :, =, ,, x, -
#
# # Notes on Simplification:
# # 1. Indentation is not part of the grammar syntax itself but implied by NEWLINE and {} structure.
# #    The parser might enforce consistent indentation semantically if desired, but lexer provides NEWLINE.
# # 2. All statements are top-level for now. No complex nesting of control structures yet.
# # 3. Knot instructions are simplified.
# # 4. Alpha pattern data is a list of color value lists.
# # 5. Thread references are simple integers or ranges.
# # 6. Explicit NEWLINE tokens are used to structure lists within blocks.
#
# # Example of how a parser might use this:
# # A parser would consume tokens from the lexer.
# # When it sees "PATTERN", it expects an <identifier>, then "{", then <newline_token>,
# # then it tries to parse <pattern_body_list>, and finally "}".
# # <pattern_body_list> would recursively parse attributes separated by <newline_token>.
