import time

def es_consistente(a, b):
    return a != b


def forward(i, variables, vecinos):
    dominio_vacio = False
    valor_i = variables[i].get_valor()
    for j in vecinos[i]:
        if j <= i:
            continue  # solo mirar variables futuras
        for b in variables[j].dominio[:]:
            if not es_consistente(valor_i, b):
                variables[j].dominio.remove(b)
                variables[j].setPodado((i, b))
            
        if variables[j].dominio == []: 
            dominio_vacio = True
            break
    if dominio_vacio: return False
    return True

def restaurar(i, variables, vecinos):
    
    for j in vecinos[i]:
        if j <= i:
            continue  # solo mirar variables futuras
        nuevos_podados = [] # Lo hacemos de esta manera porque con una copia
        # Recorremos cada valor podado de Xj
        for (responsable, valor) in variables[j].podado:
            if responsable == i:
                # Xi es responsable del filtrado → restaurar valor
                if valor not in variables[j].dominio:
                    variables[j].dominio.append(valor)
            else:
                # Otro responsable (no restauramos todavía)
                nuevos_podados.append((responsable, valor))

        # Actualizamos la lista de podados (quitamos los restaurados)
        variables[j].podado = nuevos_podados


def FC(i, variables, vecinos):
    global contador_rec, contador_asig
    contador_rec += 1  # 🔹 contamos una llamada recursiva

     # ✅ Caso base: Sudoku completo
    if i >= len(variables): 
        return variables
    variable = variables[i]

    for a in variable.dominio:
        contador_asig += 1  # 🔹 contamos una asignación de a
        variable.asignar(a) # Xi ← a
        if forward(i, variables, vecinos): 
            resultado = FC(i+1, variables, vecinos)
            if resultado: return resultado
        restaurar(i, variables, vecinos)
        variable.desasignar()
    return False


def resolverFC(tablero, variables, vecinos):
    inicio = time.time()
    fcResuelto = FC(0, variables, vecinos)
    fin = time.time()
    tiempo = fin - inicio

    if not fcResuelto:
        print("❌ No hay solución posible con Forward Checking")
        return False
    
    for i in range(81):
        fila = i // 9
        columna = i % 9
        tablero.setCelda(fila, columna, fcResuelto[i].get_valor())  # sincronizar tablero
    return True, round(tiempo, 9)