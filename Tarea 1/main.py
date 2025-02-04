import re
import tkinter as tk
from tkinter import scrolledtext, ttk

# Especificación de tokens con valores ajustados para palabras reservadas
token_specification = [
    ('PALABRA_RESERVADA_IF', r'\bif\b', 19),
    ('PALABRA_RESERVADA_WHILE', r'\bwhile\b', 20),
    ('PALABRA_RESERVADA_RETURN', r'\breturn\b', 21),
    ('PALABRA_RESERVADA', r'\b(else|int|float|void)\b', 4),  # Otras palabras reservadas
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*', 0),
    ('REAL', r'\d+\.\d+', 2),
    ('ENTERO', r'\d+', 1),
    ('CADENA', r'".*?"', 3),
    ('OP_IGUALDAD', r'==|!=', 11),
    ('OP_RELAC', r'<=|>=|<|>', 7),
    ('OP_ASIGNACION', r'=', 18),
    ('OP_SUMA', r'[+-]', 5),
    ('OP_MUL', r'[*/]', 6),
    ('OP_AND', r'&&', 9),
    ('OP_OR', r'\|\|', 8),
    ('OP_NOT', r'!', 10),
    ('PARENTESIS', r'[()]', 14),
    ('LLAVE', r'[{}]', 16),
    ('COMA', r',', 13),
    ('PUNTO_Y_COMA', r';', 12),
    ('FIN_ARCHIVO', r'\$', 23),
    ('ESPACIO', r'\s+', None)  # Ignorar espacios
]

def analizador_lexico(codigo_fuente):
    tokens = []
    posicion = 0
    while posicion < len(codigo_fuente):
        match = None
        for token_nombre, token_patron, token_tipo in token_specification:
            regex = re.compile(token_patron)
            match = regex.match(codigo_fuente, posicion)
            if match:
                if token_tipo is not None:  # Ignorar espacios en blanco
                    tokens.append((token_nombre, match.group(), token_tipo))
                posicion = match.end()
                break
        if not match:
            tokens.append(("ERROR", codigo_fuente[posicion], "Error léxico"))
            posicion += 1  # Avanzar para evitar bucles infinitos
    return tokens

def analizar_codigo():
    codigo = entrada_texto.get("1.0", tk.END).strip()
    tokens = analizador_lexico(codigo)
    for row in tabla.get_children():
        tabla.delete(row)
    for token in tokens:
        tabla.insert("", tk.END, values=token)

# Interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico")

# Cambiar el tamaño de la ventana
root.geometry("800x600")

# Estilo educativo
root.configure(bg="#f0f0f0")

# Entrada de código
entrada_label = tk.Label(root, text="Ingrese el código fuente:", font=("Arial", 12), bg="#f0f0f0")
entrada_label.pack(pady=10)

entrada_texto = scrolledtext.ScrolledText(root, width=70, height=12, font=("Courier New", 10), wrap=tk.WORD)
entrada_texto.pack(padx=20, pady=10, expand=True, fill=tk.BOTH)

# Botón para analizar
boton_analizar = tk.Button(root, text="Analizar", command=analizar_codigo, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised")
boton_analizar.pack(pady=10)

# Tabla para mostrar tokens
salida_label = tk.Label(root, text="Tokens:", font=("Arial", 12), bg="#f0f0f0")
salida_label.pack(pady=10)

tabla = ttk.Treeview(root, columns=("Tipo", "Valor", "Código"), show="headings")
tabla.heading("Tipo", text="Tipo")
tabla.heading("Valor", text="Valor")
tabla.heading("Código", text="Código")
tabla.column("Tipo", anchor="w", width=120)
tabla.column("Valor", anchor="w", width=150)
tabla.column("Código", anchor="w", width=100)

# Estilo de la tabla
tabla.tag_configure("error", background="red", foreground="white")

tabla.pack(padx=20, pady=10, expand=True, fill=tk.BOTH)

# Hacer que la ventana sea dinámica
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
