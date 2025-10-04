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
        self.indice_sprite = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 4
        self.image = self.sprites_animacion[self.indice_sprite]
        self.rect = self.image.get_rect(center=self.obtener_posicion_pixel(self.r, self.c))
        self.ruta_planificada = [] # para guardar la lista de coordenadas
        self.paso_actual = 0 # para saber en qué punto de la ruta vamos
        self.esta_en_movimiento = False # un interruptor para iniciar/detener el movimiento
        self.posicion_objetivo = self.rect.center # las coordenadas en píxeles de la siguiente celda a la que queremos llegar
        self.velocidad_movimiento = TAMANO_CELDA // 8 # Píxeles que se mueve por frame

    def cargar_sprites_animacion(self):
        sprites = []
        for i in range(0, 6):
            path = os.path.join('assets', 'sprites', f'{i}.png')
            try:
                imagen = pygame.image.load(path).convert_alpha()
                scaled_image = pygame.transform.scale(imagen, (int(TAMANO_CELDA * 0.8), int(TAMANO_CELDA * 0.8)))
                sprites.append(scaled_image)
            except pygame.error:
                print(f"ERROR: No se pudo cargar sprite en {path}. Usando respaldo.")
        if not sprites:
            backup = pygame.Surface((int(TAMANO_CELDA * 0.8), int(TAMANO_CELDA * 0.8)), pygame.SRCALPHA)
            backup.fill((255, 255, 0))
            sprites.append(backup)
        return sprites
        
    def obtener_posicion_pixel(self, r, c):
        x_pixel = c * TAMANO_CELDA + (TAMANO_CELDA // 2)
        y_pixel = r * TAMANO_CELDA + (TAMANO_CELDA // 2)
        return (x_pixel, y_pixel)
    
    def asignar_ruta(self, ruta):
        """Recibe una ruta del algoritmo y prepara a la abeja para moverse."""
        if not ruta:
            self.esta_en_movimiento = False
            return
        
        # 1. Limpiamos cualquier ruta anterior
        for fila in self.mundo.grid:
            for celda in fila:
                celda.en_ruta = False

        # 2. Marcar las celdas de la nueva ruta
        for r, c in ruta:
            self.mundo.grid[r][c].en_ruta = True
            
        self.ruta_planificada = ruta
        self.paso_actual = 0
        self.esta_en_movimiento = True
        # Asegurarse de que la abeja comience en el primer punto de la ruta
        self.r, self.c = self.ruta_planificada[self.paso_actual]
        self.rect.center = self.obtener_posicion_pixel(self.r, self.c)
        self.actualizar_siguiente_objetivo()

    def actualizar(self):
        if not self.esta_en_movimiento:
            return 
        
        self.animar_sprite()
        self.mover_hacia_objetivo()
        
    def animar_sprite(self):
        """Cambia la imagen de la abeja para simular que vuela."""
        self.contador_animacion += 1
        if self.contador_animacion >= self.velocidad_animacion:
            self.contador_animacion = 0
            self.indice_sprite = (self.indice_sprite + 1) % len(self.sprites_animacion)
            self.image = self.sprites_animacion[self.indice_sprite]
        
    def llegar_a_celda(self):
        """Se ejecuta cuando la abeja llega al centro de una celda."""
        self.r, self.c = self.ruta_planificada[self.paso_actual]

        # Comprobar si hemos llegado al final de la ruta
        if self.paso_actual >= len(self.ruta_planificada) - 1:
            self.esta_en_movimiento = False
            print("¡He llegado a la meta!")
        else:
            self.actualizar_siguiente_objetivo()

    def actualizar_siguiente_objetivo(self):
        """Avanza al siguiente paso de la ruta y actualiza el objetivo en píxeles."""
        self.paso_actual += 1
        siguiente_paso = self.ruta_planificada[self.paso_actual]
        self.posicion_objetivo = self.obtener_posicion_pixel(siguiente_paso[0], siguiente_paso[1])

    def mover_hacia_objetivo(self):
        """Mueve la abeja unos píxeles hacia la celda objetivo."""
        if self.rect.center == self.posicion_objetivo:
            # Si hemos llegado, decidimos cuál es el siguiente objetivo
            self.llegar_a_celda()
        else:
            # Si no hemos llegado, nos movemos un poco
            dx = self.posicion_objetivo[0] - self.rect.centerx
            dy = self.posicion_objetivo[1] - self.rect.centery
            
            if abs(dx) > self.velocidad_movimiento:
                self.rect.x += self.velocidad_movimiento if dx > 0 else -self.velocidad_movimiento
            else:
                self.rect.centerx = self.posicion_objetivo[0]
                
            if abs(dy) > self.velocidad_movimiento:
                self.rect.y += self.velocidad_movimiento if dy > 0 else -self.velocidad_movimiento
            else:
                self.rect.centery = self.posicion_objetivo[1]

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)