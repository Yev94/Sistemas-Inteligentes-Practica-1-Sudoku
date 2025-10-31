#########################################################################
# CURSO 25-25
# PRACTICA 1 DE SISTEMAS INTELIGENTES: RESOLUCION DE SUDOKUS
# m1 ym2 son de la plantilla
# m3 es el más difícil de resolver AI Escargot
# m4 es uno inconsistente
# m5 son todo 0s
#########################################################################   

import pygame
import copy
from tablero import *
from pygame.locals import *
import sys

# --------------------- Mis Imports --------------------------------
import backtracking
import forwardchecking
import ac3
from variable import Variable
# --------------------- !Mis Imports --------------------------------
# --------------------- Mi config  --------------------------------
ARCHIVO = 'm1.txt'
IMPRIMIR_DOMINIOS_AC3 = True
MOSTRAR_VALORES_AC3_TABLA = True
# --------------------- Mi config  --------------------------------

GREY=(220,220,220)
NEGRO=(10,10,10)
GRIS_ACTIVO=(245,245,245)
GRIS_NORMAL=(169,169,169)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_DERECHO=125 #ancho del margen derecho entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
N=9 # número de filas del sudoku
VACIA='0'

#########################################################################
# Crea la lista de variables a partir del tablero
#########################################################################
def crear_variables(tablero):
    variables = []
    for fila in range(9):
        for columna in range(9):
            valor = tablero.getCelda(fila, columna)
            variables.append(Variable(valor))
    return variables

#########################################################################
# Precomputamos indices de vecinos de las restricciones para usarlas en los algoritmos
#########################################################################
def obtener_vecinos(indice):
    vecinos = set()
    fila = indice // 9
    col = indice % 9

    # Mismos fila
    for c in range(9):
        idx = fila * 9 + c
        if idx != indice:
            vecinos.add(idx)

    # Misma columna
    for f in range(9):
        idx = f * 9 + col
        if idx != indice:
            vecinos.add(idx)

    # Mismo bloque
    fila_base = (fila // 3) * 3
    col_base = (col // 3) * 3
    for f in range(fila_base, fila_base + 3):
        for c in range(col_base, col_base + 3):
            idx = f * 9 + c
            if idx != indice:
                vecinos.add(idx)

    return list(vecinos)

#########################################################################
# Imprimimos los dominios de AC3
#########################################################################
# 🔹 Función auxiliar: imprime los dominios antes y después uno al lado del otro
def imprimir_dominios_lado_a_lado(dominios_antes, dominios_despues):
    print("\n{:<40}{}".format("DOMINIOS ANTES DEL AC3", "DOMINIOS DESPUÉS DEL AC3"))
    for i in range(len(dominios_antes)):
        fila, col = i // 9, i % 9
        antes_str = ", ".join(dominios_antes[i])
        despues_str = ", ".join(dominios_despues[i])
        print(f"{fila}{col:1}  Dominio: {antes_str:<30}    {fila}{col:1}  Dominio: {despues_str}")


#########################################################################
# Detecta si se pulsa un botón
#########################################################################   
def pulsaBoton(pos, boton):
    if boton.collidepoint(pos[0], pos[1]):    
        return True
    else:
        return False

#########################################################################
# Pintar un boton
#########################################################################   
def pintarBoton(screen, fuenteBot, boton, mensaje):
    if boton.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, GRIS_ACTIVO, boton, 0)        
    else:
        pygame.draw.rect(screen, GRIS_NORMAL, boton, 0)
        
    texto=fuenteBot.render(mensaje, True, NEGRO)
    screen.blit(texto, (boton.x+(boton.width-texto.get_width())/2, boton.y+(boton.height-texto.get_height())/2))         

#########################################################################
# Pintar el sudokuz
#########################################################################         
def pintarTablero(screen, fuenteSud, tablero, copTab):
    pygame.draw.rect(screen, GREY, [0, 0, N*(TAM+MARGEN)+MARGEN, N*(TAM+MARGEN)+MARGEN],0)
    for fil in range(9):
        for col in range(9):
            if tablero is None or tablero.getCelda(fil, col)==VACIA :
                pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)            
            else:
                pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                if tablero.getCelda(fil, col)==copTab.getCelda(fil, col):
                    color=NEGRO
                else:
                    color=GRIS_NORMAL                 
                texto= fuenteSud.render(tablero.getCelda(fil, col), True, color)            
                screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])
    
    #dibujar línea de cuadrícula     
    pygame.draw.line(screen, GRIS_NORMAL, (MARGEN, 3*(TAM+MARGEN)+2), (9*(TAM+MARGEN),3*(TAM+MARGEN)+2), 5)
    pygame.draw.line(screen, GRIS_NORMAL, (MARGEN, 6*(TAM+MARGEN)+2), (9*(TAM+MARGEN),6*(TAM+MARGEN)+2), 5)    
    pygame.draw.line(screen, GRIS_NORMAL, (3*(TAM+MARGEN)+2,MARGEN), (3*(TAM+MARGEN)+2,9*(TAM+MARGEN)), 5)
    pygame.draw.line(screen, GRIS_NORMAL, (6*(TAM+MARGEN)+2, MARGEN), (6*(TAM+MARGEN)+2,9*(TAM+MARGEN)), 5)
    pygame.draw.rect(screen, GRIS_NORMAL, [MARGEN, MARGEN, N*(TAM+MARGEN), N*(TAM+MARGEN)],5)


#########################################################################  
# Principal
#########################################################################
def main():    
    
    pygame.init()
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file=ARCHIVO
    else:
        file=sys.argv[-1]
    
    anchoVentana=N*(TAM+MARGEN)+MARGEN_DERECHO
    altoVentana= N*(TAM+MARGEN)+2*MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Sudoku") 
    
    fuenteBot=pygame.font.Font(None, 30)
    fuenteSud= pygame.font.Font(None, 70)
    
    botLoad=pygame.Rect(anchoVentana-95, 75, 70, 50)    
    botBK=pygame.Rect(anchoVentana-95, 203, 70, 50)
    botFC=pygame.Rect(anchoVentana-95, 333, 70, 50)
    botAC3=pygame.Rect(anchoVentana-95, 463, 70, 50)
    
    game_over=False
    tablero=None
    copTab=None
    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición                               
                pos=pygame.mouse.get_pos()
                if pulsaBoton(pos, botLoad):                                      
                    tablero=Tablero(file)
                    copTab=copy.deepcopy(tablero)
                    variables = crear_variables(tablero)
                    vecinos = [obtener_vecinos(i) for i in range(81)]                

                # Reemplazamos funcion botón BK           
                if pulsaBoton(pos, botBK):
                    if tablero is None:
                        print("Hay que cargar un sudoku")
                    else:
                        backtracking.contador_rec = 0
                        backtracking.contador_asig = 0

                        exito, tiempo = backtracking.resolverBK(tablero, variables, vecinos)

                        if exito:
                            print(f"✅ BK -> Recursiones: {backtracking.contador_rec} | Asignaciones: {backtracking.contador_asig} | Tiempo: {tiempo}s")
                        else:
                            print(f"❌ No se encontró solución con BK. | Tiempo: {tiempo}s")

                #  Reemplazamos función botón FC
                elif pulsaBoton(pos, botFC):
                    if tablero is None:
                        print("Hay que cargar un sudoku")
                    else:
                        forwardchecking.contador_rec = 0
                        forwardchecking.contador_asig = 0

                        exito, tiempo = forwardchecking.resolverFC(tablero, variables, vecinos)
                        if exito:
                            print(f"✅ FC -> Recursiones: {forwardchecking.contador_rec} | Asignaciones: {forwardchecking.contador_asig} | Tiempo: {tiempo}s")
                        else:
                            print(f"❌ No se encontró solución con FC. | Tiempo: {tiempo}s")


                elif pulsaBoton(pos, botAC3):
                    if tablero is None:
                        print('Hay que cargar un sudoku')
                    else:
                        # Ejecutar el algoritmo de consistencia
                        exito, tiempo, dominios_antes, dominios_despues = ac3.resolverAC3(variables, vecinos)

                        if exito:
                            if IMPRIMIR_DOMINIOS_AC3: imprimir_dominios_lado_a_lado(dominios_antes, dominios_despues)
                            print(f"✅ AC3 -> finalizado correctamente | Tiempo: {tiempo}s")
                        else:
                            print(f"❌ El Sudoku no es consistente (AC-3 detectó un conflicto) | Tiempo: {tiempo}s")

                        #Para visualizar tablero con los que solo tengan un valor en dominio 
                        if MOSTRAR_VALORES_AC3_TABLA:
                            for i, var in enumerate(variables):
                                if len(var.dominio) == 1:
                                    valor = next(iter(var.dominio))
                                    fila = i // 9
                                    col = i % 9
                                    tablero.setCelda(fila, col, valor)

        #limpiar pantalla
        screen.fill(GREY)
        #pintar cuadrícula del sudoku  
        pintarTablero(screen, fuenteSud, tablero, copTab)                   
        #pintar botones        
        pintarBoton(screen, fuenteBot, botLoad, "Re/Load")
        pintarBoton(screen, fuenteBot, botBK, "BK")
        pintarBoton(screen, fuenteBot, botFC, "FC")
        pintarBoton(screen, fuenteBot, botAC3, "AC3")        
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.delay(500)
    
    pygame.quit()
 
if __name__=="__main__":
    main()
 
