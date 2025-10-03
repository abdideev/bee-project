import random
import pygame
from game.constants import *

class Celda:
    def __init__(self, fila, columna):
        self.r = fila
        self.c = columna
        self.tipo = TIPO_VACIO

class Mundo:
    def __init__(self, N):
        self.N = N
        self.grid = []  # La cuadrícula final (la pared)
        # Bucle exterior para cada FILA
        for fila_num in range(N):
            fila_actual = []  # 1. Crea una nueva fila vacía
            # Bucle interior para cada COLUMNA de esta fila

            for col_num in range(N):
                # 2. Crea una celda y añádela a la fila actual
                celda = Celda(fila_num, col_num)

                valor_aleatorio = random.random()
                if valor_aleatorio < 0.25:
                    celda.tipo = TIPO_OBSTACULO
                elif valor_aleatorio < 0.35:
                    celda.tipo = TIPO_FLOR

                fila_actual.append(celda)
            
            # 3. Cuando la fila está llena, añádela a la cuadrícula principal
            self.grid.append(fila_actual)

    def seleccionar_punto(self, pos_pixel, tipo_punto):
        # Convierte coordenadas de píxeles, valida y cambia el tipo de una celda.
        columna = pos_pixel[0] // TAMANO_CELDA
        fila = pos_pixel[1] // TAMANO_CELDA
        if 0 <= fila < self.N and 0 <= columna < self.N:
            celda = self.grid[fila][columna]
            # Verificamos que no sea un obstáculo o una flor
            if celda.tipo != TIPO_OBSTACULO and celda.tipo != TIPO_FLOR:
                celda.tipo = tipo_punto 
                return True # Devolvemos True para saber que el clic fue exitoso
        return False # Devolvemos False para saber que el clic NO fue exitoso

                
    # Bucle anidado para visitar cada celda
    def dibujar(self, pantalla):
        for fila in self.grid:
            for celda in fila:
                 # 2. Calcula la posición en píxeles
                x = celda.c * TAMANO_CELDA
                y = celda.r * TAMANO_CELDA

                # 3. Crea el rectángulo
                rect_celda = pygame.Rect(x, y, TAMANO_CELDA, TAMANO_CELDA)

                # Dibuja el fondo y el borde
                pygame.draw.rect(pantalla, COLOR_FONDO_CELDA, rect_celda)
                if celda.tipo == TIPO_OBSTACULO:
                    pygame.draw.rect(pantalla, COLOR_OBSTACULO, rect_celda)
                elif celda.tipo == TIPO_FLOR:
                    # Usaremos un círculo rosa simple para la flor por ahora
                    pygame.draw.circle(pantalla, (255, 0, 255), rect_celda.center, TAMANO_CELDA // 4)
                # --- CORRECCIÓN 2: Dibujar rectángulos para inicio y meta ---
                elif celda.tipo == TIPO_INICIO:
                    pygame.draw.rect(pantalla, COLOR_INICIO, rect_celda)
                elif celda.tipo == TIPO_ENJAMBRE:
                    pygame.draw.rect(pantalla, COLOR_META, rect_celda)

                # Dibujamos el borde al final para que siempre se vea
                pygame.draw.rect(pantalla, COLOR_BORDE_CELDA, rect_celda, 1)


