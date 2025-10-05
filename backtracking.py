import pygame
import time

def comprobar(tablero, fila, col, valor):
    # 1️⃣ Comprobar la FILA
        # Comprobamos los valores de todas las celdas de la fila
        # Si alguna es igual al valor que nosotros queremos meter  →  ❌ NO nos vale el valor
    for c in range(9):
        if tablero.getCelda(fila, c) == valor:
            return False

    # 2️⃣ Comprobar la COLUMNA
        # Comprobamos los valores de todas las celdas de la columna
        # Si alguna es igual al valor que nosotros queremos meter  →  ❌ NO nos vale el valor
    for f in range(9):
        if tablero.getCelda(f, col) == valor:
            return False

    # 3️⃣ Comprobar el CUADRANTE 3x3
        # Calculamos el inicio de cada cuadrante 
        # Los recorremos hasta la ultima celda en fila y columna de cada cuadrante
        # Hacemos lo mismo que en fila y columna
    start_row = (fila // 3) * 3
    start_col = (col // 3) * 3
    for f in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if tablero.getCelda(f, c) == valor:
                return False

    return True  # ✅ Si pasa todas, es válido


def resolverBK(tablero):
    for fila in range(9): # fila del 0 al 8
        for col in range(9): # fila del 0 al 8
            if tablero.getCelda(fila, col) == '0':  # Celda vacía
                for valor in map(str, range(1, 10)):  # Probar valores del 1 al 9 en formato string (str)
                    if comprobar(tablero, fila, col, valor):  # Si es válido
                        tablero.setCelda(fila, col, valor)  # Asignar
                        if resolverBK(tablero):   return True  # ✅ si valor correcto → siguiente con tablero actualizado con mi nuevo valor
                        tablero.setCelda(fila, col, '0')   # ❌ Si Falló → deshacer
                return False  # No hay número válido → retroceder
    return True  # ✅ Tablero completo
