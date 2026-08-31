from typing import List, Tuple, Dict, Optional
import re, time, os, sys


# ---------- Jerarquía de la Pila (Práctica 3) ----------
class ElementoPila:
    """
    Clase base para cualquier elemento que pueda apilarse en la pila del
    analizador LR. No se instancia directamente: sirve de base para
    Terminal, NoTerminal y Estado (equivalente a la clase 'Alumno' del
    ejemplo de la práctica).
    """

    def muestra(self) -> str:
        """Representación en texto del elemento (equivalente a Alumno::muestra)."""
        return ""

    def __str__(self):
        return self.muestra()


class Estado(ElementoPila):
    """Representa un número de estado del autómata LR (equivalente al 'int' original)."""

    def __init__(self, numero: int):
        self.numero = numero

    def muestra(self) -> str:
        return f"${self.numero}"


class Terminal(ElementoPila):
    """Representa un símbolo terminal de la gramática (p. ej. 'id', '+')."""

    def __init__(self, simbolo: str):
        self.simbolo = simbolo

    def muestra(self) -> str:
        return self.simbolo


class NoTerminal(ElementoPila):
    """Representa un símbolo no terminal de la gramática (p. ej. 'E', "S'")."""

    def __init__(self, simbolo: str):
        self.simbolo = simbolo

    def muestra(self) -> str:
        return self.simbolo


# ---------- Modelo de la gramática ----------
class Produccion:
    """Representa una producción de la gramática: A -> beta"""

    def __init__(self, izquierda: str, derecha: List[str]):
        self.izquierda = izquierda
        self.derecha = derecha

    def __str__(self):
        cuerpo = " ".join(self.derecha) if self.derecha else "ε"
        return f"{self.izquierda} -> {cuerpo}"

    def __len__(self):
        return len(self.derecha)


class Accion:
    """Representa una acción de la tabla ACTION: shift, reduce o accept."""

    SHIFT = "s"
    REDUCE = "r"
    ACCEPT = "acc"

    def __init__(self, tipo: str, valor: Optional[int] = None):
        self.tipo = tipo
        self.valor = valor

    @classmethod
    def shift(cls, estado: int) -> "Accion":
        return cls(cls.SHIFT, estado)

    @classmethod
    def reduce(cls, indice_produccion: int) -> "Accion":
        return cls(cls.REDUCE, indice_produccion)

    @classmethod
    def accept(cls) -> "Accion":
        return cls(cls.ACCEPT, None)

    def es_shift(self) -> bool:
        return self.tipo == self.SHIFT

    def es_reduce(self) -> bool:
        return self.tipo == self.REDUCE

    def es_accept(self) -> bool:
        return self.tipo == self.ACCEPT

    def texto(self, producciones: List[Produccion]) -> str:
        if self.es_shift():
            return f"s{self.valor}"
        if self.es_reduce():
            prod = producciones[self.valor]
            return f"r{self.valor}: {prod}"
        if self.es_accept():
            return "r0 (aceptar)"
        return str(self.tipo)


# ---------- Utilidades ----------
class Tokenizador:
    """Convierte una cadena cruda en una lista de tokens para el analizador LR."""

    PATRON_ID = re.compile(r'[A-Za-z_]\w*')

    def tokenizar(self, raw: str) -> List[str]:
        s = raw.strip().replace('+', ' + ')
        tokens: List[str] = []
        for tok in s.split():
            if tok == '+':
                tokens.append('+')
            elif self.PATRON_ID.fullmatch(tok):
                tokens.append('id')
            else:
                tokens.append('id' if tok == 'id' else tok)
        tokens.append('$')
        return tokens


class Pantalla:
    """Encapsula la impresión en consola: encabezado, filas y limpieza de pantalla."""

    ANCHO_PASO = 5
    ANCHO_PILA = 35
    ANCHO_ENTRADA = 25
    ANCHO_SALIDA = 25

    def limpiar(self):
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_encabezado(self):
        print(f"{'Paso':^{self.ANCHO_PASO}} | {'Pila':^{self.ANCHO_PILA}} | "
              f"{'Entrada':^{self.ANCHO_ENTRADA}} | {'Salida':^{self.ANCHO_SALIDA}}")
        print("-" * 100)

    def mostrar_fila(self, paso: int, pila: str, entrada: str, salida: str):
        print(f"{paso:^{self.ANCHO_PASO}} | {pila:{self.ANCHO_PILA}} | "
              f"{entrada:{self.ANCHO_ENTRADA}} | {salida:{self.ANCHO_SALIDA}}")


# ---------- Pila LR (Práctica 3: pila de ElementoPila*) ----------
class PilaLR:
    """
    Pila del autómata LR, ahora implementada como una pila de objetos
    ElementoPila (Estado, Terminal, NoTerminal) en lugar de enteros/strings
    sueltos, tal como pide la práctica 3 (equivalente a la clase Pila del
    ejemplo, cuyos push/pop/top ahora reciben/retornan ElementoPila*).
    """

    def __init__(self, estado_inicial: int = 0):
        self._lista: List[ElementoPila] = [Estado(estado_inicial)]

    def push(self, elemento: ElementoPila):
        self._lista.append(elemento)

    def pop(self) -> ElementoPila:
        return self._lista.pop()

    def top(self) -> ElementoPila:
        return self._lista[-1]

    def estado_actual(self) -> int:
        """Devuelve el número de estado que está en el tope de la pila."""
        tope = self.top()
        assert isinstance(tope, Estado), "El tope de la pila debe ser un Estado"
        return tope.numero

    def apilar_desplazamiento(self, simbolo: str, es_no_terminal: bool, estado: int):
        """Apila el símbolo desplazado/reducido seguido de su nuevo estado."""
        elemento = NoTerminal(simbolo) if es_no_terminal else Terminal(simbolo)
        self.push(elemento)
        self.push(Estado(estado))

    def desapilar(self, cantidad: int):
        for _ in range(cantidad):
            self.pop()

    def muestra(self) -> str:
        """Equivalente a Pila::muestra(): concatena la representación de cada elemento."""
        return " ".join(elemento.muestra() for elemento in self._lista)


# ---------- Motor LR ----------
class SimuladorLR:
    """Ejecuta el algoritmo de análisis LR mostrando cada paso en pantalla."""

    def __init__(
        self,
        producciones: List[Produccion],
        action: Dict[int, Dict[str, Optional[Accion]]],
        goto: Dict[int, Dict[str, Optional[int]]],
        no_terminales: Optional[set] = None,
        pantalla: Optional[Pantalla] = None,
    ):
        self.producciones = producciones
        self.action = action
        self.goto = goto
        # Símbolos que deben apilarse como NoTerminal en lugar de Terminal
        self.no_terminales = no_terminales or {p.izquierda for p in producciones}
        self.pantalla = pantalla or Pantalla()

    def simular(
        self,
        tokens: List[str],
        pausa: float = 0.8,
        manual: bool = False,
        limpiar_cada_paso: bool = False,
    ):
        pila = PilaLR()
        entrada = tokens[:]
        paso = 0

        if limpiar_cada_paso:
            self.pantalla.limpiar()
        self.pantalla.mostrar_encabezado()

        while True:
            paso += 1
            estado = pila.estado_actual()
            simbolo = entrada[0] if entrada else '$'
            accion = self.action.get(estado, {}).get(simbolo, None)

            salida = accion.texto(self.producciones) if accion else "error"
            self.pantalla.mostrar_fila(paso, pila.muestra(), " ".join(entrada), salida)

            if manual:
                input()
            else:
                time.sleep(pausa)
            if limpiar_cada_paso:
                self.pantalla.limpiar()
                self.pantalla.mostrar_encabezado()

            if accion is None:
                print("\n❌ Error: no hay ACTION para", (estado, simbolo))
                return False

            if accion.es_shift():
                pila.apilar_desplazamiento(simbolo, es_no_terminal=False, estado=accion.valor)
                entrada.pop(0)
                continue

            if accion.es_reduce():
                prod = self.producciones[accion.valor]
                pila.desapilar(2 * len(prod))
                s = pila.estado_actual()
                estado_goto = self.goto.get(s, {}).get(prod.izquierda, None)
                if estado_goto is None:
                    print("\n❌ Error: no hay GOTO para", (s, prod.izquierda))
                    return False
                pila.apilar_desplazamiento(
                    prod.izquierda,
                    es_no_terminal=prod.izquierda in self.no_terminales,
                    estado=estado_goto,
                )
                continue

            if accion.es_accept():
                print("\n✅ Cadena aceptada")
                return True


# ---------- Gramáticas de los ejercicios ----------
class Ejercicio:
    """Agrupa producciones, tablas ACTION/GOTO y una cadena de ejemplo."""

    def __init__(self, nombre: str, descripcion: str,
                 producciones: List[Produccion],
                 action: Dict[int, Dict[str, Optional[Accion]]],
                 goto: Dict[int, Dict[str, Optional[int]]],
                 ejemplo: str):
        self.nombre = nombre
        self.descripcion = descripcion
        self.producciones = producciones
        self.action = action
        self.goto = goto
        self.ejemplo = ejemplo

    def crear_simulador(self) -> SimuladorLR:
        return SimuladorLR(self.producciones, self.action, self.goto)


def construir_ejercicio_1() -> Ejercicio:
    # 0: S' -> E
    # 1: E  -> id + id
    producciones = [
        Produccion("S'", ["E"]),
        Produccion("E", ["id", "+", "id"]),
    ]
    action = {
        0: {'id': Accion.shift(2), '+': None, '$': None},
        1: {'id': None, '+': None, '$': Accion.accept()},
        2: {'id': None, '+': Accion.shift(3), '$': None},
        3: {'id': Accion.shift(4), '+': None, '$': None},
        4: {'id': None, '+': None, '$': Accion.reduce(1)},
    }
    goto = {
        0: {'E': 1},
        1: {}, 2: {}, 3: {}, 4: {},
    }
    return Ejercicio("Ejercicio 1", "Gramática: E -> id + id",
                      producciones, action, goto, "a+b")


def construir_ejercicio_2() -> Ejercicio:
    # 0: S' -> E
    # 1: E  -> id + E
    # 2: E  -> id
    producciones = [
        Produccion("S'", ["E"]),
        Produccion("E", ["id", "+", "E"]),
        Produccion("E", ["id"]),
    ]
    action = {
        0: {'id': Accion.shift(2), '+': None, '$': None},
        1: {'id': None, '+': Accion.shift(3), '$': Accion.accept()},
        2: {'id': None, '+': Accion.reduce(2), '$': Accion.reduce(2)},
        3: {'id': Accion.shift(2), '+': None, '$': None},
        4: {'id': None, '+': Accion.reduce(1), '$': Accion.reduce(1)},
    }
    goto = {
        0: {'E': 1},
        3: {'E': 4},
        1: {}, 2: {}, 4: {},
    }
    return Ejercicio("Ejercicio 2", "Gramática: E -> id + E | id",
                      producciones, action, goto, "a+b+c")


# ---------- CLI ----------
class AplicacionCLI:
    """Interfaz de línea de comandos que orquesta la selección de ejercicio y ejecución."""

    def __init__(self):
        self.tokenizador = Tokenizador()
        self.ejercicios = {
            "1": construir_ejercicio_1(),
            "2": construir_ejercicio_2(),
        }

    def elegir_ejercicio(self) -> Ejercicio:
        print("=== Simulador LR paso a paso (POO - pila de objetos) ===")
        for clave, ej in self.ejercicios.items():
            print(f"{clave}) {ej.nombre}  | {ej.descripcion}")
        opcion = input("Elige ejercicio (1/2) [2]: ").strip() or "2"
        return self.ejercicios.get(opcion, self.ejercicios["2"])

    def pedir_cadena(self, ejercicio: Ejercicio) -> List[str]:
        cad = input(f"Cadena a analizar (ej. {ejercicio.ejemplo}): ").strip() or ejercicio.ejemplo
        return self.tokenizador.tokenizar(cad)

    def pedir_modo(self) -> Tuple[bool, float]:
        modo = (input("Modo: [A]utomático con sleep / [M]anual con Enter (A/M) [A]: ")
                .strip().lower() or "a")
        manual = modo.startswith('m')
        pausa = 0.8
        if not manual:
            try:
                pausa = float(input("Segundos de pausa entre pasos [0.8]: ").strip() or "0.8")
            except ValueError:
                pausa = 0.8
        return manual, pausa

    def pedir_limpieza(self) -> bool:
        return input("¿Limpiar pantalla en cada paso? (s/n) [n]: ").strip().lower() == 's'

    def ejecutar(self):
        ejercicio = self.elegir_ejercicio()
        tokens = self.pedir_cadena(ejercicio)
        manual, pausa = self.pedir_modo()
        limpiar_flag = self.pedir_limpieza()

        print("\nGramática y tabla cargadas. Analizando...\n")
        simulador = ejercicio.crear_simulador()
        simulador.simular(tokens, pausa=pausa, manual=manual, limpiar_cada_paso=limpiar_flag)


def main():
    app = AplicacionCLI()
    app.ejecutar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        sys.exit(0)