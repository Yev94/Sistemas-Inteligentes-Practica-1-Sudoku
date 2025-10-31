import time

contador_rec = 0
contador_asig = 0

def comprobar(k, variables, vecinos):
    valorK = variables[k].get_valor()
    if valorK == '0':
            return True  # si está vacía, nada que comprobar

    for idx in vecinos[k]:  # solo recorre sus vecinos directos
        if variables[idx].get_valor() == valorK:
            return False
    return True


def backtracking(k, variables, vecinos):
    global contador_rec, contador_asig
    contador_rec += 1
    
    # Si ya pasamos el último índice, está resuelto
    if k >= len(variables): return variables

    variable_actual = variables[k]
    if variable_actual.fijo: return backtracking(k + 1, variables, vecinos) # Es una celda fija → saltar
    for valor_actual in variable_actual.dominio:
        contador_asig += 1
        variable_actual.asignar(valor_actual)
        if comprobar(k, variables, vecinos):
            resultado = backtracking(k + 1, variables, vecinos)
            if resultado:   return resultado 
    
    variable_actual.desasignar()
    return False

def resolverBK(tablero, variables, vecinos):
    inicio = time.perf_counter()
    bkResuelto = backtracking(0, variables, vecinos)
    fin = time.perf_counter()
    tiempo = fin - inicio  # medimos el tiempo total

    if not bkResuelto:
        return False, tiempo  # devolvemos False + tiempo
    
    for i in range(81):
        fila = i // 9
        columna = i % 9
        tablero.setCelda(fila, columna, bkResuelto[i].get_valor())  # sincronizar tablero
    return True, tiempo
