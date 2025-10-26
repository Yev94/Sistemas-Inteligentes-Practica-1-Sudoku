def es_consistente(i, a, j, b):
    # Solo importa si están en la misma fila, columna o cuadrante
    fila_i = i // 9
    col_i = i % 9
    fila_j = j // 9
    col_j = j % 9
    mismo_cuadrante = (fila_i // 3 == fila_j // 3) and (col_i // 3 == col_j // 3)

    # Si son vecinos y tienen el mismo valor, hay conflicto
    if (fila_i == fila_j or col_i == col_j or mismo_cuadrante) and a == b:
        return False
    return True


def forward(i, variables):
    dominio_vacio = False
    valor_i = variables[i].get_valor()
    for j in range(i + 1, len(variables)):
        for b in variables[j].dominio[:]:
            # if variables[j].fijo: continue
            
            if not es_consistente(i, valor_i, j, b):
                variables[j].dominio.remove(b)
                variables[j].setPodado((i, b))
            
        if variables[j].dominio == []: 
            dominio_vacio = True
            break
    if dominio_vacio: return False
    return True

def restaurar(i, variables):
    
    for j in range(i + 1, len(variables)):
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


def FC(i, variables):
    global contador_rec, contador_asig
    contador_rec += 1  # 🔹 contamos una llamada recursiva

     # ✅ Caso base: Sudoku completo
    if i >= len(variables): 
        return variables
    variable = variables[i]
    # if variable.fijo: return FC(i + 1, variables)

    for a in variable.dominio:
        contador_asig += 1  # 🔹 contamos una asignación de a
        variable.asignar(a) # Xi ← a
        if forward(i, variables): 
            resultado = FC(i+1, variables)
            if resultado: return resultado
        restaurar(i, variables)
        variable.desasignar()
    return False


def resolverFC(tablero, variables):
    
    fcResuelto = FC(0, variables)

    if not fcResuelto:
        print("❌ No hay solución posible con Forward Checking")
        return False
    
    for i in range(81):
        fila = i // 9
        columna = i % 9
        tablero.setCelda(fila, columna, fcResuelto[i].get_valor())  # sincronizar tablero
    return True