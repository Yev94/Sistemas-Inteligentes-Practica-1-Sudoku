from variable import Variable

contador_rec = 0
contador_asig = 0

def comprobar(k, variables):
    """
    Comprueba si el valor de la celda k cumple las
    restricciones de fila, columna y bloque del Sudoku.
    """
    valorK = variables[k].getvalor()
    if valorK == '0':
        return True  # si está vacía, no hay nada que comprobar

    fila = k // 9
    columna = k % 9
    fila_base = fila * 9

    # --- Comprobar fila ---
    for i in range(9):
        idx = fila_base + i
        if idx != k and variables[idx].getvalor() == valorK:
            return False

    # --- Comprobar columna ---
    for i in range(9):
        idx = 9 * i + columna
        if idx != k and variables[idx].getvalor() == valorK:
            return False

    # --- Comprobar bloque 3x3 ---
    iFilaCuadrante = (fila // 3) * 3
    iColumnaCuadrante = (columna // 3) * 3
    for f in range(iFilaCuadrante, iFilaCuadrante + 3):
        base = 9 * f
        for c in range(iColumnaCuadrante, iColumnaCuadrante + 3):
            idx = base + c
            if idx != k and variables[idx].getvalor() == valorK:
                return False

    return True

def crear_variables(tablero):
    variables = []
    for fila in range(9):
        for columna in range(9):
            valor = tablero.getCelda(fila, columna)
            variables.append(Variable(valor))
    return variables


def backtracking(k, variables):
    global contador_rec, contador_asig
    contador_rec += 1
    # ✅ Si ya pasamos el último índice, está resuelto
    if k >= len(variables): return variables
    variable_actual = variables[k]

    if variable_actual.fijo: return backtracking(k + 1, variables) # Es una celda fija → saltar
    for valor_actual in variable_actual.dominio:
        contador_asig += 1
        variable_actual.asignar(valor_actual)
        if comprobar(k, variables):
            resultado = backtracking(k + 1, variables)
            if resultado:   return resultado 
    
    variable_actual.desasignar()
    return False

def resolverBK(tablero):
    variables = crear_variables(tablero)
    bkResuelto = backtracking(0, variables)

    for i in range(81):
        fila = i // 9
        columna = i % 9
        tablero.setCelda(fila, columna, bkResuelto[i].getvalor())  # sincronizar tablero
