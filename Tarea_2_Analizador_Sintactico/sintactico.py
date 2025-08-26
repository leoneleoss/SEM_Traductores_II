
from typing import List, Tuple, Dict, Optional
import re, time, os, sys

# ---------- Utilidades ----------
def limpiar():

    os.system("cls" if os.name == "nt" else "clear")

def tokenize(raw: str) -> List[str]:
    """
    Convierte letras/números/guiones_bajos en 'id'; deja '+' como '+'. Agrega '$' al final.
    Soporta entradas como: 'a+b', 'id + id + id', 'hola+mund0'
    """
    s = raw.strip()
    # separa '+' con espacios
    s = s.replace('+', ' + ')
    # tokeniza palabras y '+'
    tokens = []
    for tok in s.split():
        if tok == '+':
            tokens.append('+')
        else:
            # cualquier identificador -> 'id'
            if re.fullmatch(r'[A-Za-z_]\w*', tok):
                tokens.append('id')
            else:
                # si ya escribiste 'id' literal, también vale
                tokens.append('id' if tok == 'id' else tok)
    tokens.append('$')
    return tokens

def mostrar_encabezado():
    print(f"{'Paso':^5} | {'Pila':^35} | {'Entrada':^25} | {'Salida':^25}")
    print("-"*100)

def formatea_pila(stack: List):
    """
    La pila alterna: estado0, 'sym', estado, 'sym', estado, ...
    La mostramos como: $0 sym $s sym $s ...
    """
    out = []
    if stack and isinstance(stack[0], int):
        out.append(f"${stack[0]}")
    i = 1
    while i < len(stack):
        sym = stack[i]
        st = stack[i+1] if i+1 < len(stack) else "?"
        out.append(f"{sym} ${st}")
        i += 2
    return " ".join(out)

# ---------- Motor LR ----------
def simulate_lr(
    productions: List[Tuple[str, List[str]]],
    action: Dict[int, Dict[str, Optional[Tuple[str, Optional[int]]]]],
    goto: Dict[int, Dict[str, Optional[int]]],
    input_tokens: List[str],
    pausa: float = 0.8,
    manual: bool = False,
    limpiar_cada_paso: bool = False,
):
    stack: List = [0]
    inp = input_tokens[:]
    paso = 0

    if limpiar_cada_paso:
        limpiar()
    mostrar_encabezado()

    while True:
        paso += 1
        estado = stack[-1]
        a = inp[0] if inp else '$'
        act = action.get(estado, {}).get(a, None)

        # Texto de salida
        if act is None:
            salida = "error"
        elif act[0] == 's':
            salida = f"s{act[1]}"
        elif act[0] == 'r':
            i = act[1]
            A, beta = productions[i]
            salida = f"r{i}: {A} -> {' '.join(beta) if beta else 'ε'}"
        elif act[0] == 'acc':
            salida = "r0 (aceptar)"
        else:
            salida = str(act)

        print(f"{paso:^5} | {formatea_pila(stack):35} | {' '.join(inp):25} | {salida:25}")

        # Avance controlado
        if manual:
            input()  # Enter para continuar
        else:
            time.sleep(pausa)
        if limpiar_cada_paso:
            # reimprime encabezado para sensación de “animación”
            limpiar()
            mostrar_encabezado()

        # Transición
        if act is None:
            print("\n❌ Error: no hay ACTION para", (estado, a))
            return

        if act[0] == 's':
            nuevo = act[1]
            stack.append(a)
            stack.append(nuevo)
            inp.pop(0)
            continue

        if act[0] == 'r':
            i = act[1]
            A, beta = productions[i]
            k = 2 * len(beta)
            for _ in range(k):
                stack.pop()
            s = stack[-1]
            stack.append(A)
            goto_estado = goto.get(s, {}).get(A, None)
            if goto_estado is None:
                print("\n❌ Error: no hay GOTO para", (s, A))
                return
            stack.append(goto_estado)
            continue

        if act[0] == 'acc':
            print("\n✅ Cadena aceptada")
            return

# ---------- Tablas de los ejercicios ----------

# EJERCICIO 1: E -> id + id
# Producciones (índice):
# 0: S' -> E
# 1: E  -> id + id
PROD_1 = [
    ("S'", ["E"]),
    ("E", ["id", "+", "id"]),
]
ACTION_1 = {
    0: {'id': ('s', 2), '+': None, '$': None},
    1: {'id': None, '+': None, '$': ('acc', None)},
    2: {'id': None, '+': ('s', 3), '$': None},
    3: {'id': ('s', 4), '+': None, '$': None},
    4: {'id': None, '+': None, '$': ('r', 1)},
}
GOTO_1 = {
    0: {'E': 1},
    1: {},
    2: {},
    3: {},
    4: {},
}

# EJERCICIO 2: E -> id + E | id
# Producciones:
# 0: S' -> E
# 1: E  -> id + E
# 2: E  -> id
PROD_2 = [
    ("S'", ["E"]),
    ("E", ["id", "+", "E"]),
    ("E", ["id"]),
]
# Tabla LR(1)/SLR válida para esta gramática
ACTION_2 = {
    0: {'id': ('s', 2), '+': None, '$': None},
    1: {'id': None, '+': ('s', 3), '$': ('acc', None)},
    2: {'id': None, '+': ('r', 2), '$': ('r', 2)},
    3: {'id': ('s', 2), '+': None, '$': None},
    4: {'id': None, '+': ('r', 1), '$': ('r', 1)},
}
GOTO_2 = {
    0: {'E': 1},
    3: {'E': 4},
    1: {},
    2: {},
    4: {},
}

# ---------- CLI ----------
def main():
    print("=== Simulador LR paso a paso ===")
    print("1) Ejercicio 1  | Gramática: E -> id + id")
    print("2) Ejercicio 2  | Gramática: E -> id + E | id")
    ej = input("Elige ejercicio (1/2) [2]: ").strip() or "2"

    if ej == "1":
        prods, action, go = PROD_1, ACTION_1, GOTO_1
        ejemplo = "a+b"
    else:
        prods, action, go = PROD_2, ACTION_2, GOTO_2
        ejemplo = "a+b+c"

    cad = input(f"Cadena a analizar (ej. {ejemplo}): ").strip() or ejemplo
    tokens = tokenize(cad)

    modo = (input("Modo: [A]utomático con sleep / [M]anual con Enter (A/M) [A]: ")
            .strip().lower() or "a")
    manual = modo.startswith('m')

    pausa = 0.8
    if not manual:
        try:
            pausa = float(input("Segundos de pausa entre pasos [0.8]: ").strip() or "0.8")
        except:
            pausa = 0.8

    limpiar_flag = (input("¿Limpiar pantalla en cada paso? (s/n) [n]: ").strip().lower() == 's')

    print("\nGramática y tabla cargadas. Analizando...\n")
    simulate_lr(prods, action, go, tokens, pausa=pausa, manual=manual, limpiar_cada_paso=limpiar_flag)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        sys.exit(0)
