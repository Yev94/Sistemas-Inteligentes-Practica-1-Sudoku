import time

def no_es_consistente(a, j, variables):
    return a in variables[j].dominio


def forward(i, variables, vecinos):
    cambios = [] # Lista de (j, valor) que se quitaron
    a = variables[i].get_valor()
    for j in vecinos[i]:
        if j <= i:
            continue  # solo mirar variables futuras

        # Si el valor asignado a Xi está en el dominio de Xj
        if no_es_consistente(a, j, variables):
            # Si Xj solo tiene ese valor → dominio vacío → inconsistente
            if len(variables[j].dominio) == 1:
                return False, cambios

            variables[j].dominio.remove(a)
            cambios.append((j, a))

    return True, cambios

def restaurar(cambios, variables):
    for j, val in cambios:
                variables[j].dominio.append(val)


def FC(i, variables, vecinos):
    global contador_rec, contador_asig
    contador_rec += 1  #  contamos una llamada recursiva

    # Caso base: Sudoku completo
    if i >= len(variables): 
        return variables
    variable = variables[i]

    for a in variable.dominio:
        contador_asig += 1  # contamos una asignación de a
        variable.asignar(a) # Xi ← a
        ok, cambios = forward(i, variables, vecinos)
        if ok:
            resultado = FC(i+1, variables, vecinos)
            if resultado:
                return resultado

        # Restaurar solo los cambios hechos en esta llamada
        restaurar(cambios, variables)

        variable.desasignar()
    return False


def resolverFC(tablero, variables, vecinos):
    inicio = time.perf_counter()
    fcResuelto = FC(0, variables, vecinos)
    fin = time.perf_counter()
    tiempo = fin - inicio

    if not fcResuelto:
        return False, tiempo
    
    for i in range(81):
        fila = i // 9
        columna = i % 9
        tablero.setCelda(fila, columna, fcResuelto[i].get_valor())  # sincronizar tablero
    return True, tiempo