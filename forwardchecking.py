# forwardchecking.py

from copy import deepcopy

contador_rec = 0
contador_asig = 0

def comprobar(tablero, fila, col, valor):
    """Comprueba si se puede colocar 'valor' en la celda (fila, col)."""
    for c in range(9):
        if tablero.getCelda(fila, c) == valor:
            return False
    for f in range(9):
        if tablero.getCelda(f, col) == valor:
            return False
    start_row = (fila // 3) * 3
    start_col = (col // 3) * 3
    for f in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if tablero.getCelda(f, c) == valor:
                return False
    return True


# Contadores (para estadísticas)
contador_rec = 0
contador_asig = 0


def calcular_dominios(tablero):
    """Genera un diccionario con los dominios posibles para cada celda vacía."""
    dominios = {}
    for fila in range(9):
        for col in range(9):
            if tablero.getCelda(fila, col) == '0':
                posibles = []
                for valor in map(str, range(1, 10)):
                    if comprobar(tablero, fila, col, valor):
                        posibles.append(valor)
                dominios[(fila, col)] = posibles
    return dominios


def forward_checking(tablero, dominios=None):
    global contador_rec, contador_asig
    contador_rec += 1

    # Generar dominios iniciales si no se pasan
    if dominios is None:
        dominios = calcular_dominios(tablero)

    # Si no quedan celdas vacías → Sudoku resuelto
    if not dominios:
        return True

    # Seleccionar la variable con menor dominio (heurística MRV)
    celda = min(dominios, key=lambda x: len(dominios[x]))
    fila, col = celda

    for valor in dominios[celda]:
        contador_asig += 1
        if comprobar(tablero, fila, col, valor):
            tablero.setCelda(fila, col, valor)

            # Copiar dominios y hacer "forward checking"
            nuevos_dominios = deepcopy(dominios)
            del nuevos_dominios[celda]  # ya asignada

            # Eliminar 'valor' de los dominios de sus vecinos
            start_row = (fila // 3) * 3
            start_col = (col // 3) * 3
            vecinos = set()
            for i in range(9):
                vecinos.add((fila, i))  # misma fila
                vecinos.add((i, col))  # misma columna
            for f in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    vecinos.add((f, c))

            # Quitar 'valor' de dominios de vecinos
            for (f, c) in vecinos:
                if (f, c) in nuevos_dominios and valor in nuevos_dominios[(f, c)]:
                    nuevos_dominios[(f, c)].remove(valor)
                    # Si algún vecino se queda sin valores → inconsistente
                    if not nuevos_dominios[(f, c)]:
                        tablero.setCelda(fila, col, '0')
                        break
            else:
                # Si todo está bien, seguir recursivamente
                if forward_checking(tablero, nuevos_dominios):
                    return True

            # Si falló, retroceder
            tablero.setCelda(fila, col, '0')

    return False  # No hay valor válido → backtrack
