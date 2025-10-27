import time
from collections import deque

def crear_cola_par_variables(variables, vecinos):
    Q = deque()
    for i in range(len(variables)):
        for j in vecinos[i]:
            Q.append((i, j))
    return Q

def consistente(valor_k, dominio_m):
    """Devuelve True si valor_k tiene al menos un soporte en dominio_m"""
    for valor_m in dominio_m:
        if valor_k != valor_m: 
            return True
    return False  # ← ¡Aquí estaba el error!

def ac3(variables, vecinos):
    Q = crear_cola_par_variables(variables, vecinos)
    dominios_antes = [v.dominio.copy() for v in variables]

    while Q:
        (k, m) = Q.popleft()  # O(1)
        cambio = False

        # Iterar sobre una copia del dominio de k
        for valor_k in variables[k].dominio.copy():
            if not consistente(valor_k, variables[m].dominio):
                variables[k].dominio.discard(valor_k)
                cambio = True

        if len(variables[k].dominio) == 0:
            return False, None, None

        if cambio:
            for i in vecinos[k]:
                if i != m and i != k:
                    Q.append((i, k))

    dominios_despues = [v.dominio.copy() for v in variables]
    return True, dominios_antes, dominios_despues

def resolverAC3(variables, vecinos):
    inicio = time.perf_counter()
    exito, dominios_antes, dominios_despues = ac3(variables, vecinos)
    fin = time.perf_counter()
    tiempo = fin - inicio
    return exito, tiempo, dominios_antes, dominios_despues