#primer paso crear tablero
#RECORDAR QUE MIENTRAS MAS SENCILLO SEA MEJOR
#definir entidades
#definir movimientos 

import random 
import copy

class Tablero:
    def __init__(self, filas=5, columnas=5):
        '''Aca es donde definimos el tablero con el __init__'''
        self.filas = filas
        self.columnas = columnas
        self.pos_gato = (0,0)
        self.pos_raton = (filas-1, columnas-1)

    def mostrar(self):
        '''ACA DEFINIMOS LAS POSICIONES INCIALES DE LAS ENTIDADES'''
        for i in range(self.filas):
            for j in range(self.columnas):
                if (i, j) == self.pos_gato:
                    print('G', end=' ')
                elif (i, j) == self.pos_raton:
                    print('R', end=' ')
                else:
                    print('.', end=' ')
            print()
        print()

    def movimientos_posibles(self, posicion):
        '''ACA SE DEFINEN MOVIMIENTOS BASICOS RANDOM'''
        fila, columna = posicion
        movimientos = []

        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for df, dc in direcciones:
            nueva_fila = fila + df
            nueva_col = columna + dc

            if 0 <= nueva_fila < self.filas and 0 <= nueva_col < self.columnas:
                movimientos.append((nueva_fila, nueva_col))
        return movimientos

    def evaluar(self):
        '''ACA SE CALCULA LA POSICION DE AMBAS ENTIDADES Y LA DISTANCIA ENTRE AMBAS'''
        distancia = abs(self.pos_gato[0] - self.pos_raton[0]) +\
                    abs(self.pos_gato[1] - self.pos_raton[1])

        return -distancia

    def minimax(self, profundidad, es_turno_gato):
        '''ACA ENTRA EN ACCION EL MINIMAX PARA CALCULAR EL TURNO DE CADA ENTIDAD
        Y TAMBIEN CALCULA LOS POSIBLES MOVIMIENTOS Y ELIJE EL MEJOR MOVIMIENTO
        TAMBIEN CALCULA LA PROFUNDIDAD AL MIRAR 3 TURNOS ADELANTE'''

        if profundidad == 0 or self.pos_gato == self.pos_raton:
            return self.evaluar(), None

        if es_turno_gato:
            mejor_valor = float('-inf')
            mejor_movimiento = None

            for movimiento in self.movimientos_posibles(self.pos_gato):
                tablero_simulado = copy.deepcopy(self)
                tablero_simulado.pos_gato = movimiento

                valor, _ = tablero_simulado.minimax(profundidad -1, False)

                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento

            return mejor_valor, mejor_movimiento
        else:
            mejor_valor = float('inf')
            mejor_movimiento = None

            for movimiento in self.movimientos_posibles(self.pos_raton):
                tablero_simulado = copy.deepcopy(self)
                tablero_simulado.pos_raton = movimiento

                valor, _ = tablero_simulado.minimax(profundidad -1, True)

                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento
            
            return mejor_valor, mejor_movimiento

    def jugar(self, max_turnos= 20, profundidad_minimax=3):
        '''ACA SE EJECUTA EL JUEGO COMPLETO '''
        
        turno = 0

        while turno < max_turnos:
            print(f'\n--- Turno {turno + 1} ---')
            self.mostrar()

            if self.pos_gato == self.pos_raton:
                print('El GATO ATRAPO AL RATON!')
                return 'gato'

            _, movimiento_gato = self.minimax(profundidad_minimax, True)
            if movimiento_gato:
                self.pos_gato = movimiento_gato
                print(f'G Gato se mieve a {movimiento_gato}')

            if self.pos_gato == self.pos_raton:
                self.mostrar()
                print('El gato atrapo al raton!')
                return 'gato'

            _, movimiento_raton = self.minimax(profundidad_minimax, False)
            if movimiento_raton:
                self.pos_raton = movimiento_raton
                print(f'R Ranton se mueve a {movimiento_raton}')
            
            turno += 1

        print('\n Se acabo el tiempo! El raton escapo!')
        return 'raton'

if __name__ == "__main__":
    juego = Tablero(filas=5, columnas=5)
    ganador = juego.jugar(max_turnos=20, profundidad_minimax=3)
    print(f"\nGanador: {ganador}")