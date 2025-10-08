import random
import pygame
import os
from .constants import *

class Celda:
    def __init__(self, fila, columna):
        self.r = fila
        self.c = columna
        self.tipo = TIPO_VACIO
        self.en_ruta = False
        self.imagen_original_path = None

class Mundo:
    def __init__(self, N):
        self.N = N
        self.grid = []
        self.inicializar_grid_aleatorio()
        self.cargar_imagenes_flores()

    def inicializar_grid_aleatorio(self):
        self.grid = []
        PROB_OBSTACULO = 0.25
        PROB_FLOR = 0.10
        rutas_flores = [
            os.path.join('assets', 'objects', 'flor_1.png'),
            os.path.join('assets', 'objects', 'flor_2.png'),
            os.path.join('assets', 'objects', 'lata.png'),
            os.path.join('assets', 'objects', 'tenis.png')
        ]
        for fila_num in range(self.N):
            fila_actual = []
            for col_num in range(self.N):
                celda = Celda(fila_num, col_num)
                valor_aleatorio = random.random()
                if valor_aleatorio < PROB_OBSTACULO:
                    celda.tipo = TIPO_OBSTACULO
                elif valor_aleatorio < PROB_OBSTACULO + PROB_FLOR:
                    celda.tipo = TIPO_FLOR
                    # Se le asigna un path solo si es una flor
                    celda.imagen_original_path = random.choice(rutas_flores)
                fila_actual.append(celda)
            self.grid.append(fila_actual)

    def cargar_imagenes_flores(self):
        self.imagenes_sprites_flores = {}
        for fila in self.grid:
            for celda in fila:
                if celda.tipo == TIPO_FLOR and celda.imagen_original_path:
                    path = celda.imagen_original_path
                    if path not in self.imagenes_sprites_flores:
                        try:
                            img = pygame.image.load(path).convert_alpha()
                            self.imagenes_sprites_flores[path] = pygame.transform.scale(img, (int(TAMANO_CELDA * 0.9), int(TAMANO_CELDA * 0.9)))
                        except pygame.error as e:
                            print(f"Error cargando imagen de flor en {path}: {e}")

    def seleccionar_punto(self, pos_pixel, tipo_punto):
        columna = pos_pixel[0] // TAMANO_CELDA
        fila = pos_pixel[1] // TAMANO_CELDA
        if 0 <= fila < self.N and 0 <= columna < self.N:
            celda = self.grid[fila][columna]
            if celda.tipo not in [TIPO_OBSTACULO, TIPO_FLOR]:
                celda.tipo = tipo_punto
                return True
        return False
    
    def obtener_vecinos_validos(self, celda_actual):
        vecinos = []
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        r, c = celda_actual.r, celda_actual.c
        for dr, dc in movimientos:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.N and 0 <= nc < self.N:
                if self.grid[nr][nc].tipo != TIPO_OBSTACULO:
                    vecinos.append((nr, nc))
        return vecinos

    def dibujar(self, pantalla):
        for fila in self.grid:
            for celda in fila:
                x = celda.c * TAMANO_CELDA
                y = celda.r * TAMANO_CELDA
                rect_celda = pygame.Rect(x, y, TAMANO_CELDA, TAMANO_CELDA)

                
                pygame.draw.rect(pantalla, COLOR_FONDO_CELDA, rect_celda)
                if celda.en_ruta:
                    pygame.draw.rect(pantalla, COLOR_RUTA, rect_celda)

                if celda.tipo == TIPO_OBSTACULO:
                    pygame.draw.rect(pantalla, COLOR_OBSTACULO, rect_celda)
                elif celda.tipo == TIPO_FLOR:
                    sprite = self.imagenes_sprites_flores.get(celda.imagen_original_path)
                    if sprite:
                        pantalla.blit(sprite, sprite.get_rect(center=rect_celda.center))
                elif celda.tipo == TIPO_INICIO:
                    pygame.draw.rect(pantalla, COLOR_INICIO, rect_celda)
                elif celda.tipo == TIPO_ENJAMBRE:
                    pygame.draw.rect(pantalla, COLOR_META, rect_celda)
                
                # Asegúrate de tener COLOR_BORDE_CELDA en constants.py o usa un color
                pygame.draw.rect(pantalla, (80, 80, 80), rect_celda, 1)