import re
import tkinter as tk
from tkinter import ttk, scrolledtext

# Versión precompilada de las especificaciones de tokens
token_specification = [
    ('PALABRA_RESERVADA_IF', r'\bif\b', 19),
    ('PALABRA_RESERVADA_WHILE', r'\bwhile\b', 20),
    ('PALABRA_RESERVADA_RETURN', r'\breturn\b', 21),
    ('PALABRA_RESERVADA', r'\b(else|int|float|void)\b', 4),
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*', 0),
    ('REAL', r'\d+\.\d+', 2),
    ('ENTERO', r'\d+', 1),
    ('CADENA', r'"([^"\\]|\\.)*?"', 3),  # Manejo de caracteres escapados
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
    ('ESPACIO', r'\s+', None)
]

# Precompilar todas las expresiones regulares
compiled_token_specs = [
    (nombre, re.compile(patron), tipo) 
    for nombre, patron, tipo in token_specification
]

def analizador_lexico(codigo_fuente):
    tokens = []
    posicion = 0
    while posicion < len(codigo_fuente):
        match = None
        for token_nombre, token_regex, token_tipo in compiled_token_specs:
            match = token_regex.match(codigo_fuente, posicion)
            if match:
                if token_tipo is not None:
                    valor = match.group()
                    # Manejo especial para cadenas (quitar comillas)
                    if token_nombre == 'CADENA':
                        valor = valor[1:-1]
                    tokens.append((token_nombre, valor, token_tipo))
                posicion = match.end()
                break
        if not match:
            # Calcular posición del error
            linea = codigo_fuente.count('\n', 0, posicion) + 1
            columna = posicion - codigo_fuente.rfind('\n', 0, posicion)
            error_char = codigo_fuente[posicion]
            tokens.append(("ERROR", f"Carácter inválido '{error_char}' en línea {linea}, columna {columna}", "Error léxico"))
            posicion += 1
    return tokens

class InterfazAnalizador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico Mejorado")
        self.geometry("1000x800")
        self.configure(bg="#f0f0f0")
        
        self.crear_componentes()
        self.configurar_estilos()
        
    def crear_componentes(self):
        # Panel de entrada
        entrada_frame = ttk.Frame(self)
        entrada_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(entrada_frame, text="Ingrese el código fuente:").pack(side=tk.TOP, anchor=tk.W)
        
        self.entrada_texto = scrolledtext.ScrolledText(
            entrada_frame, width=100, height=15, 
            font=("Consolas", 10), wrap=tk.WORD
        )
        self.entrada_texto.pack(padx=20, pady=5, fill=tk.BOTH)
        
        # Botón de análisis
        ttk.Button(
            self, text="Analizar", 
            command=self.analizar_codigo
        ).pack(pady=5)
        
        # Panel de resultados
        resultados_frame = ttk.Frame(self)
        resultados_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(resultados_frame, text="Tokens:").pack(side=tk.TOP, anchor=tk.W)
        
        # Tabla con scrollbar
        self.tabla = ttk.Treeview(
            resultados_frame, 
            columns=("Tipo", "Valor", "Código"), 
            show="headings",
            selectmode="browse"
        )
        
        vsb = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tabla.yview)
        hsb = ttk.Scrollbar(resultados_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configurar columnas
        self.tabla.heading("Tipo", text="Tipo", anchor=tk.W)
        self.tabla.heading("Valor", text="Valor", anchor=tk.W)
        self.tabla.heading("Código", text="Código", anchor=tk.W)
        
        self.tabla.column("Tipo", width=200, anchor=tk.W)
        self.tabla.column("Valor", width=300, anchor=tk.W)
        self.tabla.column("Código", width=100, anchor=tk.W)
        
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.map("Treeview", background=[('selected', '#0078D7')])
        
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("TLabel", font=("Arial", 11), background="#f0f0f0")
        
    def analizar_codigo(self):
        codigo = self.entrada_texto.get("1.0", tk.END).strip()
        tokens = analizador_lexico(codigo)
        
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        
        # Insertar nuevos tokens
        for token in tokens:
            tag = "error" if token[0] == "ERROR" else ""
            self.tabla.insert("", tk.END, values=token, tags=(tag,))
        
        # Configurar colores para errores
        self.tabla.tag_configure("error", background="#ffdddd", foreground="red")

if __name__ == "__main__":
    app = InterfazAnalizador()
    app.mainloop()