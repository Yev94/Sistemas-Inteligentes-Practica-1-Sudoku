
def obtener_vecinos(indice, variables):
    vecinos = set() # Para no repetir vecinos 

    fila = indice // 9
    columna = indice % 9

    # --- Mismos fila ---
    for i in range(9):
        idx = fila * 9 + i
        if idx != indice:
            vecinos.add(variables[idx])

    # --- Misma columna ---
    for i in range(9):
        idx = 9 * i + columna
        if idx != indice:
            vecinos.add(variables[idx])

    # --- Mismo bloque 3x3 ---
    iFilaCuadrante = (fila // 3) * 3
    iColumnaCuadrante = (columna // 3) * 3
    for f in range(iFilaCuadrante, iFilaCuadrante + 3):
        base = 9 * f
        for c in range(iColumnaCuadrante, iColumnaCuadrante + 3):
            idx = base + c
            if idx != indice:
                vecinos.add(variables[idx])

    return list(vecinos)

def crear_cola_par_variables(variables):
    Q = []
    for i in range(len(variables)):
        Vi = variables[i]
        if Vi.fijo: continue  # ❌ No meter arcos que parten de variables fijas
        for Vj in obtener_vecinos(i, variables):
            if Vi != Vj: Q.append((Vi, Vj))  # 👈 guardamos objetos Variable
    return Q

def obtener_vecinos_por_variable(variable, variables):
    indice = variables.index(variable)
    return obtener_vecinos(indice, variables)

def no_consistente(valor_k, dominio_m):
    for valor_m in dominio_m:
        if valor_k != valor_m: return False  # tiene al menos un soporte → consistente
    return True  # no tiene ninguno → inconsistente


def ac3(variables):

    Q = crear_cola_par_variables(variables)

    while len(Q) > 0:

        # <Vk, Vm> ← seleccionar_y_borrar(Q)
        (Vk, Vm) = Q.pop(0)
        cambio = False

        # for all vk ∈ Dk do
        for valor_k in Vk.dominio[:]:
            if no_consistente(valor_k, Vm.dominio):
                Vk.dominio.remove(valor_k)
                Vk.setPodado((Vm, valor_k))
                cambio = True

        if len(Vk.dominio) == 0:
            return False

        if cambio:
            for Vi in obtener_vecinos_por_variable(Vk, variables):
                if Vi != Vm and Vi != Vk:
                    Q.append((Vi, Vk))

    return True