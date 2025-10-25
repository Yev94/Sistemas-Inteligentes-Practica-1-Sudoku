
def es_consistente(k, variables, valor):
    """
    Comprueba si 'valor' puede colocarse en la posición k sin 
    violar las restricciones de fila, columna o bloque 3x3.
    """
    if valor == '0':
        return True  # nada que comprobar

    fila = k // 9
    columna = k % 9
    fila_base = fila * 9

    # --- Fila ---
    for i in range(9):
        idx = fila_base + i
        if idx != k and variables[idx].get_valor() == valor:
            return False

    # --- Columna ---
    for i in range(9):
        idx = 9 * i + columna
        if idx != k and variables[idx].get_valor() == valor:
            return False

    # --- Bloque 3x3 ---
    iFilaCuadrante = (fila // 3) * 3
    iColumnaCuadrante = (columna // 3) * 3
    for f in range(iFilaCuadrante, iFilaCuadrante + 3):
        base = 9 * f
        for c in range(iColumnaCuadrante, iColumnaCuadrante + 3):
            idx = base + c
            if idx != k and variables[idx].get_valor() == valor:
                return False

    return True


def forward(i, variables):
    dominio_vacio = False
    for j in range(i + 1, len(variables)):
        for b in variables[j].dominio[:]:
            if variables[j].fijo: continue
            variables[j].asignar(b)
            if not es_consistente(j, variables, b):
                variables[j].dominio.remove(b)
                variables[j].setPodado((i, b))
            variables[j].desasignar()
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
    if i >= len(variables): return variables
    variable = variables[i]
    if variable.fijo: return FC(i + 1, variables)

    for valor in variable.dominio:
        contador_asig += 1  # 🔹 contamos una asignación de valor
        variable.asignar(valor) # Xi ← a
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