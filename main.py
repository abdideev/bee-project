import pygame
import sys
from game.constants import *
from game.grid_model import *
from game.bee_agent import *
from core.search_algorithms import bfs_panal, dfs_panal

class Juego:
    def __init__(self):
        pygame.init()

        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Proyecto Abeja Buscadora (Simulación IA)")
        self.mundo = Mundo(TAMANO_N)
        self.estado_seleccion = 'inicio'
        self.agente_abeja = None
        self.reloj = pygame.time.Clock()
    
    def ejecutar_busqueda(self, algoritmo_func, nombre_estrategia):
        """
        Llama al algoritmo de búsqueda y le pasa la ruta encontrada a la abeja.
        """
        # Primero, necesitamos las coordenadas de inicio y meta desde el mundo
        inicio = None
        meta = None
        for fila in self.mundo.grid:
            for celda in fila:
                if celda.tipo == TIPO_INICIO: inicio = (celda.r, celda.c)
                elif celda.tipo == TIPO_ENJAMBRE: meta = (celda.r, celda.c)
        
        if inicio and meta and self.agente_abeja:
            print(f"--- Ejecutando {nombre_estrategia} ---")
            ruta = algoritmo_func(self.mundo, inicio, meta)
            
            if ruta:
                print(f"Ruta encontrada con {len(ruta)} pasos.")
                # Aquí conectamos el cerebro (algoritmo) con el cuerpo (abeja)
                self.agente_abeja.asignar_ruta(ruta) 
            else:
                print("ERROR: No se encontró una ruta.")
        else:
            print("ERROR: Debes seleccionar un punto de inicio y una meta primero.")   

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

                if evento.type == pygame.KEYDOWN:
                    # Si estamos listos (ya se eligió inicio y meta)
                    if self.estado_seleccion == 'listo':
                        if evento.key == pygame.K_1: # Tecla '1' para BFS
                            self.ejecutar_busqueda(bfs_panal, "BFS")
                        if evento.key == pygame.K_2: # Tecla '2' para DFS
                            self.ejecutar_busqueda(dfs_panal, "DFS")

            # Limpiar el bucle y llamar al método dibujar
            self.actualizar()
            self.dibujar() 
            self.reloj.tick(FPS)

    def actualizar(self):
        """Actualiza el estado de todos los objetos del juego."""
        if self.agente_abeja:
            self.agente_abeja.actualizar()

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