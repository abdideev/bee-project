import pygame
import os
from game.constants import *

class Abeja(pygame.sprite.Sprite):
    def __init__(self, mundo, pos_inicial):
        super().__init__()
        self.mundo = mundo
        self.r = pos_inicial[0]  # Fila inicial
        self.c = pos_inicial[1]  # Columna inicial
        self.sprites_animacion = self.cargar_sprites_animacion()
        self.image = self.sprites_animacion[0]
        self.rect = self.image.get_rect(center=self._obtener_posicion_pixel(self.r, self.c))

    def cargar_sprites_animacion(self):
        sprites = []
        for i in range(0, 6):
            path = os.path.join('assets', 'sprites', f'{i}.png')
            try:
                imagen = pygame.image.load(path).convert_alpha()
                scaled_image = pygame.transform.scale(imagen, (int(TAMANO_CELDA * 1), int(TAMANO_CELDA * 1)))
                sprites.append(scaled_image)
            except pygame.error:
                print(f"ERROR: No se pudo cargar sprite en {path}. Usando respaldo.")
        if not sprites:
            backup = pygame.Surface((int(TAMANO_CELDA * 1), int(TAMANO_CELDA * 1)), pygame.SRCALPHA)
            backup.fill((255, 255, 0))
            sprites.append(backup)
        return sprites
        
    def _obtener_posicion_pixel(self, r, c):
        x_pixel = c * TAMANO_CELDA + (TAMANO_CELDA // 2)
        y_pixel = r * TAMANO_CELDA + (TAMANO_CELDA // 2)
        return (x_pixel, y_pixel)

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)