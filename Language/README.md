# MacraScript - Language for Macrame Bracelet Patterns

MacraScript is a simplified language designed to describe macrame bracelet patterns in a natural and easy-to-understand way.

## Language Features

### Supported Pattern Types

1. **ALPHA**: Pixel-type patterns, similar to friendship bracelets with geometric designs or letters
2. **NORMAL**: Patterns based on specific knots, typical of traditional macrame

### Basic Syntax

Every MacraScript must follow this structure:

```
START <PATTERN_TYPE>
    <CONFIGURATION>
    <PATTERN_DATA>
END
```

## Language Components

### 1. Basic Configuration

#### Threads (THREADS)
Defines how many threads will be used:
```
THREADS: 8
```

#### Dimensions
Defines the width and height of the pattern:
```
WIDTH: 8
HEIGHT: 10
```

#### Colors
Defines the color palette to use:
```
COLORS: ("red", "blue", "white")
```
or with hexadecimal codes:
```
COLORS: ("FF0000", "0000FF", "FFFFFF")
```

### 2. ALPHA Patterns

ALPHA patterns define each row using color indices:

```
START ALPHA
THREADS: 8
WIDTH: 8
HEIGHT: 4
COLORS: ("red", "blue", "white")
PATTERN {
    ROW: (0, 1, 0, 1, 0, 1, 0, 1)
    ROW: (1, 0, 1, 0, 1, 0, 1, 0)
    ROW: (0, 2, 2, 2, 2, 2, 2, 0)
    ROW: (2, 2, 1, 1, 1, 1, 2, 2)
}
END
```

- Numbers in ROW correspond to color indices (0=first color, 1=second color, etc.)
- Each ROW represents a horizontal row of the pattern

### 3. NORMAL Patterns

NORMAL patterns define sequences of knots per row, indicating the direction of each knot.

```
START NORMAL
THREADS: 8
COLORS: ("red", "blue", "yellow", "green", "magenta", "cyan", "orange", "purple")

PATTERN {
    ROW: (RIGHT, RIGHT, RIGHT, RIGHT)
    ROW: (LEFT, LEFT, LEFT)
    ROW: (RIGHT, RIGHT, RIGHT, RIGHT)
    ROW: (LEFT, LEFT, LEFT)
    ROW: (RIGHT, RIGHT, RIGHT, RIGHT)
}
END
```

- `ROW: (DIRECTION, ...)`: Defines a row of knots. Each `DIRECTION` can be `LEFT` or `RIGHT`.
- The number of knots per row depends on the number of threads (`THREADS`) and the row's parity.
- Knots are formed between adjacent threads, and the direction indicates which thread "acts" on the other.

## Language Tokens

### Keywords (KEYWORDS)
- `START`, `END`: Script delimiters
- `ALPHA`, `NORMAL`: Pattern types
- `THREADS`, `WIDTH`, `HEIGHT`: Dimension configuration
- `COLORS`: Color definition
- `PATTERN`: Start of pattern data
- `ROW`: Pattern data row (for ALPHA or NORMAL)
- `LEFT`, `RIGHT`: Knot directions (for NORMAL patterns)

### Literals
- `COLOR`: Hexadecimal codes like `"FF0000"`
- `COLOR_NAME`: Color names like `"red"`
- `INTEGER`: Integers
- `IDENTIFIER`: Identifiers (variable names)

### Punctuation
- `:`: Type/value separator
- `,`: Element separator in lists
- `{`, `}`: Block delimiters
- `(`, `)`: Parameter delimiters

## Complete Examples

### Example 1: Stripe Pattern (ALPHA)
```
START ALPHA
THREADS: 6
WIDTH: 6
HEIGHT: 8
COLORS: ("red", "white", "blue")
PATTERN {
    ROW: (0, 0, 0, 0, 0, 0)
    ROW: (1, 1, 1, 1, 1, 1)
    ROW: (2, 2, 2, 2, 2, 2)
    ROW: (0, 0, 0, 0, 0, 0)
    ROW: (1, 1, 1, 1, 1, 1)
    ROW: (2, 2, 2, 2, 2, 2)
    ROW: (0, 0, 0, 0, 0, 0)
    ROW: (1, 1, 1, 1, 1, 1)
}
END
```

### Example 2: Complex Knot Pattern (NORMAL)
```
START NORMAL
THREADS: 8
COLORS: ("red", "blue", "yellow", "green", "magenta", "cyan", "orange", "purple")

PATTERN {
    ROW: (RIGHT, RIGHT, RIGHT, RIGHT)
    ROW: (LEFT, LEFT, LEFT)
    ROW: (RIGHT, RIGHT, RIGHT, RIGHT)
    ROW: (LEFT, LEFT, LEFT)
    ROW: (RIGHT, RIGHT, RIGHT, RIGHT)
}
END
```

## Analyzer Usage

To use the lexical and syntactic analyzer:

```python
from lexical import LexicalAnalizer
from sintactic import SintacticAnalyzer

# Your MacraScript code
script = """
START ALPHA
THREADS: 4
WIDTH: 4
HEIGHT: 2
COLORS: ("red", "blue")
PATTERN {
    ROW: (0, 1, 0, 1)
    ROW: (1, 0, 1, 0)
}
END
"""

# Lexical analysis
tokens = LexicalAnalizer.lex(script)

# Syntactic analysis
parser = SintacticAnalyzer(tokens)
result = parser.parse()

print(result)
```

## Analyzer Output

The syntactic analyzer returns a dictionary with:
- `type`: Pattern type ("ALPHA" or "NORMAL")
- `threads`: Number of threads
- `width`: Pattern width
- `height`: Pattern height
- `colors`: List of colors
- `pattern_data`: Pattern data (rows for ALPHA, knots for NORMAL)

This structure can later be used by a renderer to generate the graphical visualization of the macrame pattern.
