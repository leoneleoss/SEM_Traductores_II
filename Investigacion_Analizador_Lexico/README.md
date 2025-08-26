# Analizador Léxico (Lexer)
## ¿Qué es un Analizador Léxico?
Un analizador léxico (también conocido como lexer o scanner) es la primera fase de un compilador o intérprete. Su función principal es convertir una secuencia de caracteres de entrada (código fuente) en una secuencia de tokens válidos. Estos tokens representan los componentes léxicos del lenguaje, como palabras clave, identificadores, operadores, literales y símbolos especiales.

## Funciones principales:
1. Eliminar caracteres irrelevantes como espacios en blanco, tabuladores y comentarios.

Identificar tokens mediante expresiones regulares o reglas definidas.

Reportar errores léxicos cuando se encuentran caracteres o secuencias no válidas.

Interactuar con el analizador sintáctico (parser) entregándole tokens para su posterior procesamiento.

## Componentes de un Analizador Léxico
Tabla de símbolos: Almacena identificadores y palabras reservadas para su rápido acceso.

Expresiones regulares: Definen patrones para reconocer tokens.

Autómatas finitos: Implementan la lógica para matching de tokens (determinísticos o no determinísticos).

## Ejemplo de Tokenización
Código fuente:

`python
x = 42 + y`
Tokens generados:

Token	Tipo
x	IDENTIFICADOR
=	OPERADOR
42	LITERAL_NUM
+	OPERADOR
y	IDENTIFICADOR
Implementación Básica en Python
python
import re

tokens = [
    (r'[ \n\t]+', None),           # Espacios en blanco (ignorar)
    (r'#[^\n]*', None),            # Comentarios (ignorar)
    (r'\d+', 'LITERAL_NUM'),       # Números
    (r'[a-zA-Z_]\w*', 'ID'),       # Identificadores
    (r'[=+*-]', 'OPERADOR'),       # Operadores
]

`
def lex(code):
    tokens_list = []
    pos = 0
    while pos < len(code):
        match = None
        for token_pattern, token_type in tokens:
            regex = re.compile(token_pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_type:  # Si no es None (ignorar)
                    tokens_list.append((token_type, value))
                break
        if not match:
            raise Exception(f'Carácter inválido: {code[pos]}')
        else:
            pos = match.end(0)
    return tokens_list
 `

# Prueba del analizador léxico
codigo_ejemplo = "x = 42 + y"
resultado = lex(codigo_ejemplo)
print("Tokens generados:")
for token in resultado:
    print(f"Tipo: {token[0]}, Valor: '{token[1]}'")
Resultado de la Ejecución
Al ejecutar el código anterior, se obtiene el siguiente resultado:

text
Tokens generados:
Tipo: ID, Valor: 'x'
Tipo: OPERADOR, Valor: '='
Tipo: LITERAL_NUM, Valor: '42'
Tipo: OPERADOR, Valor: '+'
Tipo: ID, Valor: 'y'
Este resultado muestra cómo el analizador léxico procesa la cadena de entrada "x = 42 + y" y la convierte en una secuencia de tokens con sus respectivos tipos y valores.

## Bibliografía
Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Addison-Wesley.

Grune, D., & Jacobs, C. J. H. (2008). Parsing Techniques: A Practical Guide (2nd ed.). Springer.

Appel, A. W. (2002). Modern Compiler Implementation in Java (2nd ed.). Cambridge University Press.

Cooper, K. D., & Torczon, L. (2011). Engineering a Compiler (2nd ed.). Morgan Kaufmann.

Levine, J. R. (2009). Flex & Bison: Text Processing Tools. O'Reilly Media.