# MacraScript - Lenguaje para Patrones de Pulseras de Macramé

MacraScript es un lenguaje simplificado diseñado para describir patrones de pulseras de macramé de una manera natural y fácil de entender.

## Características del Lenguaje

### Tipos de Patrones Soportados

1. **ALPHA**: Patrones tipo píxel, similares a las pulseras de la amistad con diseños geométricos o letras
2. **NORMAL**: Patrones basados en nudos específicos, típicos del macramé tradicional

### Sintaxis Básica

Todo script de MacraScript debe seguir esta estructura:

```
START <TIPO_DE_PATRON>
    <CONFIGURACION>
    <DATOS_DEL_PATRON>
END
```

## Componentes del Lenguaje

### 1. Configuración Básica

#### Hilos (THREADS)
Define cuántos hilos se utilizarán:
```
THREADS: 8
```

#### Dimensiones
Define el ancho y alto del patrón:
```
WIDTH: 8
HEIGHT: 10
```

#### Colores
Define la paleta de colores a utilizar:
```
COLORS: ("red", "blue", "white")
```
o con códigos hexadecimales:
```
COLORS: ("FF0000", "0000FF", "FFFFFF")
```

### 2. Patrones ALPHA

Los patrones ALPHA definen cada fila usando índices de colores:

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

- Los números en ROW corresponden a los índices de colores (0=primer color, 1=segundo color, etc.)
- Cada ROW representa una fila horizontal del patrón

### 3. Patrones NORMAL

Los patrones NORMAL definen secuencias de nudos:

```
START NORMAL
THREADS: 6
WIDTH: 4
HEIGHT: 8
COLORS: ("FF0000", "0000FF")
PATTERN {
    KNOT LEFT (1, 2)
    KNOT RIGHT (2, 3) REPEAT 2
    KNOT LEFT (3, 4)
    KNOT RIGHT (4, 5)
}
END
```

- `KNOT LEFT/RIGHT (hilo1, hilo2)`: Define un nudo hacia la izquierda o derecha entre dos hilos
- `REPEAT N`: Opcional, repite el nudo N veces
- Los números de hilos van de 1 a N (según THREADS)

## Tokens del Lenguaje

### Palabras Clave (KEYWORDS)
- `START`, `END`: Delimitadores del script
- `ALPHA`, `NORMAL`: Tipos de patrón
- `THREADS`, `WIDTH`, `HEIGHT`: Configuración de dimensiones
- `COLORS`: Definición de colores
- `PATTERN`: Inicio de datos del patrón
- `ROW`: Fila en patrones ALPHA
- `KNOT`: Nudo en patrones NORMAL
- `LEFT`, `RIGHT`: Direcciones de nudos
- `REPEAT`: Repetición de instrucciones

### Literales
- `COLOR`: Códigos hexadecimales como `"FF0000"`
- `COLOR_NAME`: Nombres de colores como `"red"`
- `INTEGER`: Números enteros
- `IDENTIFIER`: Identificadores (nombres de variables)

### Puntuación
- `:`: Separador tipo/valor
- `,`: Separador de elementos en listas
- `{`, `}`: Delimitadores de bloques
- `(`, `)`: Delimitadores de parámetros

## Ejemplos Completos

### Ejemplo 1: Patrón de Rayas (ALPHA)
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

### Ejemplo 2: Patrón de Nudos Simple (NORMAL)
```
START NORMAL
THREADS: 4
WIDTH: 2
HEIGHT: 6
COLORS: ("0000FF", "FFFF00")
PATTERN {
    KNOT LEFT (1, 2)
    KNOT RIGHT (3, 4)
    KNOT LEFT (2, 3)
    KNOT RIGHT (1, 4) REPEAT 2
    KNOT LEFT (1, 3)
    KNOT RIGHT (2, 4)
}
END
```

## Uso del Analizador

Para usar el analizador léxico y sintáctico:

```python
from lexical import LexicalAnalizer
from sintactic import SintacticAnalyzer

# Tu script de MacraScript
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

# Análisis léxico
tokens = LexicalAnalizer.lex(script)

# Análisis sintáctico
parser = SintacticAnalyzer(tokens)
result = parser.parse()

print(result)
```

## Salida del Analizador

El analizador sintáctico devuelve un diccionario con:
- `type`: Tipo de patrón ("ALPHA" o "NORMAL")
- `threads`: Número de hilos
- `width`: Ancho del patrón
- `height`: Alto del patrón
- `colors`: Lista de colores
- `pattern_data`: Datos del patrón (filas para ALPHA, nudos para NORMAL)

Esta estructura puede ser utilizada posteriormente por un renderizador para generar la visualización gráfica del patrón de macramé.
