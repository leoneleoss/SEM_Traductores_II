
# Etapa del proyecto analizador léxico completo. 

Este proyecto es un **analizador léxico** que utiliza expresiones regulares para identificar diferentes tipos de tokens en un código fuente dado. La interfaz gráfica está construida con la biblioteca `Tkinter` y permite al usuario ingresar código fuente, analizarlo y ver los tokens identificados.

## Funcionalidad

El programa lee un código fuente, lo analiza utilizando un conjunto de expresiones regulares predefinidas y muestra los tokens clasificados en una tabla. Los tokens incluyen palabras reservadas, identificadores, números enteros, reales, cadenas de texto, operadores y símbolos de puntuación.

### Características

- **Análisis léxico**: Identifica varios tipos de tokens en el código fuente.
- **Interfaz gráfica**: Desarrollada con `Tkinter`, permite al usuario ingresar código y ver los resultados de manera visual.
- **Expresiones regulares**: Utiliza expresiones regulares para identificar palabras reservadas específicas (como `if`, `while`, `return` con valores específicos) y otros elementos del lenguaje.

## Instalación

1. Asegúrate de tener Python 3.x instalado.
2. Instala las dependencias necesarias (si las hubiera) utilizando el siguiente comando:
   ```bash
   pip install tk
   ```
3. Clona este repositorio o descarga el archivo `.py` para ejecutarlo.

## Uso

1. Ejecuta el archivo Python en tu entorno local.
2. Ingrese el código fuente en el área de texto y presiona el botón **"Analizar"**.
3. Los tokens del código ingresado se mostrarán en la tabla debajo del área de entrada.

## Ejemplo de funcionamiento

Para ilustrar cómo funciona el programa, sigue estos pasos:

![Image](https://github.com/user-attachments/assets/3ba164e4-a801-4b70-b072-19cd2e6ba9c6)

1. Ingresa el siguiente código fuente en el área de texto:

   ```c
   int x = 10;
   float y = 20.5;
   void funcion() {
       if (x >= y) {
           x = x + 1;
       } else {
           y = y * 2;
       }
       while (x != 0) {
           x = x - 1;
       }
       return;
   }
   ```

2. Haz clic en el botón **"Analizar"**.
3. Los resultados aparecerán en la tabla de tokens, como se muestra a continuación:

| Tipo                | Valor   | Código |
|---------------------|---------|--------|
| PALABRA_RESERVADA_INT | int     | 19     |
| IDENTIFICADOR        | x       | 0      |
| OP_ASIGNACION        | =       | 18     |
| ENTERO               | 10      | 1      |
| PUNTO_Y_COMA         | ;       | 12     |
| PALABRA_RESERVADA_FLOAT | float | 19     |
| IDENTIFICADOR        | y       | 0      |
| OP_ASIGNACION        | =       | 18     |
| REAL                 | 20.5    | 2      |
| PUNTO_Y_COMA         | ;       | 12     |
| PALABRA_RESERVADA_VOID | void  | 19     |
| IDENTIFICADOR        | funcion | 0      |
| PARENTESIS           | (       | 14     |
| PARENTESIS           | )       | 14     |
| LLAVE                | {       | 16     |
| PALABRA_RESERVADA_IF | if      | 19     |
| PARENTESIS           | (       | 14     |
| IDENTIFICADOR        | x       | 0      |
| OP_RELAC             | >=      | 7      |
| IDENTIFICADOR        | y       | 0      |
| PARENTESIS           | )       | 14     |
| LLAVE                | {       | 16     |
| IDENTIFICADOR        | x       | 0      |
| OP_ASIGNACION        | =       | 18     |
| IDENTIFICADOR        | x       | 0      |
| OP_SUMA              | +       | 5      |
| ENTERO               | 1       | 1      |
| PUNTO_Y_COMA         | ;       | 12     |
| LLAVE                | }       | 16     |
| PALABRA_RESERVADA_ELSE | else  | 19     |
| LLAVE                | {       | 16     |
| IDENTIFICADOR        | y       | 0      |
| OP_ASIGNACION        | =       | 18     |
| IDENTIFICADOR        | y       | 0      |
| OP_MUL               | *       | 6      |
| REAL                 | 2       | 2      |
| PUNTO_Y_COMA         | ;       | 12     |
| LLAVE                | }       | 16     |
| PALABRA_RESERVADA_WHILE | while | 19   |
| PARENTESIS           | (       | 14     |
| IDENTIFICADOR        | x       | 0      |
| OP_IGUALDAD          | !=      | 11     |
| ENTERO               | 0       | 1      |
| PARENTESIS           | )       | 14     |
| LLAVE                | {       | 16     |
| IDENTIFICADOR        | x       | 0      |
| OP_ASIGNACION        | =       | 18     |
| IDENTIFICADOR        | x       | 0      |
| OP_SUMA              | -       | 5      |
| ENTERO               | 1       | 1      |
| PUNTO_Y_COMA         | ;       | 12     |
| LLAVE                | }       | 16     |
| PALABRA_RESERVADA_RETURN | return | 21 |
| PUNTO_Y_COMA         | ;       | 12     |
| LLAVE                | }       | 16     |

## Personalización

- **Palabras Reservadas**: El código incluye palabras reservadas como `if`, `while` y `return` con valores personalizados.
- **Tokens**: Puedes modificar las expresiones regulares en el código para agregar más tipos de tokens según sea necesario.

