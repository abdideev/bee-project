import pygame
import sys
from game.constants import *
from game.grid_model import *
from game.bee_agent import *

class Juego:
    def __init__(self):
        pygame.init()
        self.mundo = Mundo(TAMANO_N)
        self.estado_seleccion = 'inicio'
        self.agente_abeja = None
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Proyecto Abeja Buscadora (Simulación IA)")
        self.reloj = pygame.time.Clock()

    def run(self):
        juego_en_marcha = True
        while juego_en_marcha:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    juego_en_marcha = False

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado_seleccion == 'inicio':
                        # Calcular fila y columna correctamente
                        col = evento.pos[0] // TAMANO_CELDA
                        fila = evento.pos[1] // TAMANO_CELDA
                        
                        if self.mundo.seleccionar_punto(evento.pos, TIPO_INICIO):
                            # Usamos las variables calculadas, no evento.pos
                            self.agente_abeja = Abeja(self.mundo, (fila, col))
                            self.estado_seleccion = 'meta'

                    elif self.estado_seleccion == 'meta':
                        if self.mundo.seleccionar_punto(evento.pos, TIPO_ENJAMBRE):
                            self.estado_seleccion = 'listo'

            # Limpiar el bucle y llamar al método dibujar
            self.dibujar()  
            # ----------------------------------------------------------------

            self.reloj.tick(FPS)

    def dibujar(self):
        # 1. Dibuja el mundo
        self.mundo.dibujar(self.pantalla)

        # 2. Dibuja la abeja si existe
        if self.agente_abeja:
            self.agente_abeja.dibujar(self.pantalla)

        # 3. Actualiza toda la pantalla
        pygame.display.flip()

if __name__ == "__main__":
    juego = Juego()
    juego.run()
    pygame.quit()
    sys.exit()