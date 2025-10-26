import time

def crear_cola_par_variables(variables, vecinos):
    Q = []
    for i in range(len(variables)):
        for j in vecinos[i]:
            Q.append((i, j))
    return Q

def no_consistente(valor_k, dominio_m):
    for valor_m in dominio_m:
        if valor_k != valor_m: 
            return False  # tiene al menos un soporte → consistente
    return True  # no tiene ninguno → inconsistente



def ac3(variables, vecinos):

    # Línea 1: Q ← { (Vi, Vj) | ep ∈ E, i ≠ j }
    Q = crear_cola_par_variables(variables, vecinos)
    
    # 🟡 Guardar dominios iniciales antes de aplicar AC3
    dominios_antes = [v.dominio[:] for v in variables]

    while len(Q) > 0:

        # <Vk, Vm> ← seleccionar_y_borrar(Q)
        (k, m) = Q.pop(0)
        cambio = False

        # for all vk ∈ Dk do
        for valor_k in variables[k].dominio[:]:
            if no_consistente(valor_k, variables[m].dominio):
                variables[k].dominio.remove(valor_k)
                variables[k].setPodado((m, valor_k))
                cambio = True

        if len(variables[k].dominio) == 0:
            return False

        if cambio:
            for i in vecinos[k]:
                if i != m and i != k:
                    Q.append((i, k))

    # 🟢 Guardar dominios después del AC3
    dominios_despues = [v.dominio[:] for v in variables]

    # 👉 Devolver también los dominios (para imprimirlos luego si quieres)
    return True, dominios_antes, dominios_despues

def resolverAC3(variables, vecinos):
    inicio = time.time()
    exito, dominios_antes, dominios_despues = ac3(variables, vecinos)
    fin = time.time()
    tiempo = fin - inicio
    return exito, round(tiempo, 9), dominios_antes, dominios_despues