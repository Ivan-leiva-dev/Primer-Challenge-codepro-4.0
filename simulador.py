#primer paso crear tablero
#RECORDAR QUE MIENTRAS MAS SENCILLO SEA MEJOR
#definir entidades
#definir movimientos 

 
import copy

def crear_tablero(filas=5, columnas=5):
    """ Aca se crea el tablero y sus dimensiones, donde el gato inicia en la ezquina sup. izquierda
    y el raton en la parte inferior derecha"""
    return{
        "filas": filas,
        "columnas": columnas,
        "pos_gato": (0,0), #esto es una tupla con fila y columna, donde es la pos inicial del gato
        "pos_raton": (filas-1, columnas-1) #y aca indicamos la posicion inicial del raton
    }

def mostrar_tablero(tablero):
    """ aca se muestra el tablero con las posiciones de las entidades"""
    for i in range(tablero["filas"]):
        for j in range(tablero["columnas"]):
            if (i, j) == tablero["pos_gato"]:
                print("G", end=" ")
            elif (i, j) == tablero["pos_raton"]:
                print("R", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

def mov_posibles(tablero, posicion):
    """Aca calculamos los movimientos que se pueden hacer """
    fila, columna = posicion
    movimientos =[]
    direciones = [(-1, 0), (1,0), (0, -1), (0, 1)] #arriba,abajo.izq. y derecha

    for df, dc in direciones: 
        nueva_fila = fila + df
        nueva_columna = columna + dc

        #Se agrega la condicion para que no se salga del tablero
        if 0 <= nueva_fila < tablero["filas"] and 0 <= nueva_columna < tablero["columnas"]:
            movimientos.append((nueva_fila, nueva_columna))
    
    return movimientos

def evaluar_tablero(tablero):
    """Aca usamos la heuristica para evaluar el tablero,
    la distancia manhattan entre las entidades,
    donde el gato quiere minimixzar la distancia hacia e raton,
    y el raton quiere maximizar"""

    distancia = abs(tablero["pos_gato"][0] - tablero["pos_raton"][0]) + \
                abs(tablero["pos_gato"][1] - tablero["pos_raton"][1])
    #el abs significa que no importa si es negatico o positivo, solo nos interesa el valor absoluto
    return -distancia #-distancia para que el gato minimice la distancia y el raton la maximce

def minimax(tablero, profundidad, es_turno_gato):
    """el algoritmo minimaz se usa para que l gato y el raton jueguen de manera optima,
    """

    #si la profundidad es 0, o el gato atrapa al raton
    if profundidad == 0 or tablero["pos_gato"] == tablero["pos_raton"]:
        return evaluar_tablero(tablero), None
    
    if es_turno_gato: #maximiza el gato
        mejor_valor = float("-inf")
        mejor_movimiento = None

        for movimiento in mov_posibles(tablero, tablero["pos_gato"]):
            tablero_simulado = copy.deepcopy(tablero)
            tablero_simulado["pos_gato"] = movimiento 

            valor, _ = minimax(tablero_simulado, profundidad - 1, False)

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento

            return mejor_valor, mejor_movimiento
   #minimiza el raton
    else:
        mejor_valor = float("inf")
        mejor_movimiento = None

        for movimiento in mov_posibles(tablero, tablero["pos_raton"]):
            tablero_simulado = copy.deepcopy(tablero)
            tablero_simulado["pos_raton"] = movimiento

            valor, _ = minimax(tablero_simulado, profundidad - 1, True)

            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento

        return mejor_valor, mejor_movimiento
            
def jugar(tablero, max_turnos=20, profundidad_minimax=3): 
    """Aca se ejecuta el juego, donde se define el maximo de turbnos y la profnidad minimax,
    el juego termina cuando el gato atrapa al raton o se alcanza el maximo de turnos"""

    turno = 0

    while turno < max_turnos:
                print(f"\n--- Turno {turno + 1} ---")
                mostrar_tablero(tablero)

                #revisa si el gato gano
                if tablero["pos_gato"] == tablero["pos_raton"]:
                    print("¡El gato atrapó al ratón!")
                    return "gato"
                
                #movimiento del gato con minimax
                _, movimiento_gato = minimax(tablero, profundidad_minimax, True)
                if movimiento_gato:
                    tablero["pos_gato"] = movimiento_gato
                    print(f"G Gato se mueve  a {movimiento_gato}")
                
                #vuelve a rebisar si el gato atrapo al raton
                if tablero["pos_gato"] == tablero["pos_raton"]:
                    mostrar_tablero(tablero)
                    print("¡El gato atrapó al ratón!")
                    return "gato"
                
                #aca se define el movimiento del raton
                _, movimiento_raton = minimax(tablero, profundidad_minimax, False)
                if movimiento_raton:
                    tablero["pos_raton"] = movimiento_raton
                    print(f"R Ratón se mueve a {movimiento_raton}")

                turno += 1

    print("¡El ratón escapó!")
    return "raton"
        
if __name__ == "__main__":
    tablero = crear_tablero(filas=5, columnas=5)
    ganador = jugar(tablero, max_turnos=20, profundidad_minimax=3)
    print(f"\nGanador: {ganador}")


                

