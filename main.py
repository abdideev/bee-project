import pygame
import sys
from game.constants import *
from game.grid_model import *
from game.bee_agent import *
from core.search_algorithms import bfs_panal, dfs_panal, ejecutar_busqueda_con_analisis
from vision.vision_system import VisionSystem
from game.stats_system import ComparadorAlgoritmos, EstadisticasAlgoritmo
from game.ui_manager import UIManager

class Juego:
    def __init__(self):
        pygame.init()

        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Proyecto Abeja Buscadora (IA + Visión por Computadora)")
        self.mundo = Mundo(TAMANO_N)
        self.estado_seleccion = 'inicio'
        self.agente_abeja = None
        self.reloj = pygame.time.Clock()
        
        # Nuevos sistemas
        self.sistema_vision = VisionSystem()
        self.comparador = ComparadorAlgoritmos()
        self.ui_manager = UIManager(ANCHO_PANTALLA, ALTO_PANTALLA)
        self.ui_manager.comparador = self.comparador
        
        # Control de estado
        self.mostrar_panel_comparacion = False
        self.ultimo_algoritmo_ejecutado = None
        self.estadisticas_actuales = None
        
        print("=" * 60)
        print("🐝 PROYECTO ABEJA BUSCADORA")
        print("=" * 60)
        print("Instrucciones:")
        print("  1. Click para seleccionar INICIO (verde)")
        print("  2. Click para seleccionar META/ENJAMBRE (rojo)")
        print("  3. Presiona '1' para ejecutar BFS")
        print("  4. Presiona '2' para ejecutar DFS")
        print("  5. Presiona '3' para ejecutar AMBOS y comparar")
        print("  6. Presiona 'TAB' para mostrar/ocultar panel")
        print("  7. Presiona 'S' para guardar resultados")
        print("  8. Presiona 'R' para reiniciar")
        print("=" * 60)
    
    def ejecutar_busqueda(self, algoritmo_func, nombre_estrategia):
        """
        Ejecuta un algoritmo de búsqueda con análisis de visión completo.
        """
        # Obtener coordenadas de inicio y meta
        inicio = None
        meta = None
        for fila in self.mundo.grid:
            for celda in fila:
                if celda.tipo == TIPO_INICIO: 
                    inicio = (celda.r, celda.c)
                elif celda.tipo == TIPO_ENJAMBRE: 
                    meta = (celda.r, celda.c)
        
        if inicio and meta and self.agente_abeja:
            print(f"\n{'='*60}")
            print(f"🔍 Ejecutando {nombre_estrategia}...")
            print(f"{'='*60}")
            
            # Mostrar mensaje de carga
            self.ui_manager.dibujar_mensaje_cargando(
                self.pantalla, 
                f"Ejecutando {nombre_estrategia}..."
            )
            
            # Ejecutar búsqueda con análisis completo
            ruta, estadisticas = ejecutar_busqueda_con_analisis(
                algoritmo=algoritmo_func,
                nombre=nombre_estrategia,
                mundo=self.mundo,
                inicio=inicio,
                meta=meta,
                sistema_vision=self.sistema_vision,
                pantalla=self.pantalla,
                tamano_celda=TAMANO_CELDA
            )
            
            if ruta:
                print(estadisticas.obtener_resumen_texto())
                
                # Asignar ruta a la abeja
                self.agente_abeja.asignar_ruta(ruta)
                
                # Guardar estadísticas
                self.estadisticas_actuales = estadisticas
                self.ultimo_algoritmo_ejecutado = nombre_estrategia
                
                # Agregar al comparador
                self.comparador.agregar_estadistica(nombre_estrategia, estadisticas)
            else:
                print("✗ ERROR: No se encontró una ruta.")
                self.estadisticas_actuales = None
        else:
            print("✗ ERROR: Debes seleccionar inicio y meta primero.")
    
    def ejecutar_comparacion(self):
        """Ejecuta ambos algoritmos y realiza una comparación completa."""
        print(f"\n{'='*60}")
        print("📊 MODO COMPARACIÓN: Ejecutando BFS y DFS")
        print(f"{'='*60}")
        
        # Limpiar estadísticas anteriores
        self.comparador.limpiar()
        
        # Obtener coordenadas
        inicio = None
        meta = None
        for fila in self.mundo.grid:
            for celda in fila:
                if celda.tipo == TIPO_INICIO: 
                    inicio = (celda.r, celda.c)
                elif celda.tipo == TIPO_ENJAMBRE: 
                    meta = (celda.r, celda.c)
        
        if not inicio or not meta:
            print("✗ ERROR: Debes seleccionar inicio y meta primero.")
            return
        
        # Ejecutar BFS
        self.ui_manager.dibujar_mensaje_cargando(self.pantalla, "Ejecutando BFS...")
        ruta_bfs, stats_bfs = ejecutar_busqueda_con_analisis(
            algoritmo=bfs_panal,
            nombre="BFS",
            mundo=self.mundo,
            inicio=inicio,
            meta=meta,
            sistema_vision=self.sistema_vision,
            pantalla=self.pantalla,
            tamano_celda=TAMANO_CELDA
        )
        
        if ruta_bfs:
            self.comparador.agregar_estadistica("BFS", stats_bfs)
            print(f"✓ BFS completado: Score {stats_bfs.calcular_score()}")
            print(stats_bfs.obtener_resumen_texto())
        
        # Ejecutar DFS
        self.ui_manager.dibujar_mensaje_cargando(self.pantalla, "Ejecutando DFS...")
        ruta_dfs, stats_dfs = ejecutar_busqueda_con_analisis(
            algoritmo=dfs_panal,
            nombre="DFS",
            mundo=self.mundo,
            inicio=inicio,
            meta=meta,
            sistema_vision=self.sistema_vision,
            pantalla=self.pantalla,
            tamano_celda=TAMANO_CELDA
        )
        
        if ruta_dfs:
            self.comparador.agregar_estadistica("DFS", stats_dfs)
            print(f"✓ DFS completado: Score {stats_dfs.calcular_score()}")
            print(stats_dfs.obtener_resumen_texto())
        
        # Realizar comparación
        if len(self.comparador.estadisticas) >= 2:
            comparacion = self.comparador.comparar_algoritmos()
            
            # Imprimir análisis en consola
            self.comparador.imprimir_comparacion()
            
            # Mostrar panel de comparación
            self.mostrar_panel_comparacion = True
            
            # Usar la ruta del algoritmo con mayor score
            mejor_algoritmo = comparacion['ganador_score']
            if mejor_algoritmo == "BFS":
                self.agente_abeja.asignar_ruta(ruta_bfs)
                self.estadisticas_actuales = stats_bfs
            else:
                self.agente_abeja.asignar_ruta(ruta_dfs)
                self.estadisticas_actuales = stats_dfs
            
            print(f"\n🏆 Usando ruta de: {mejor_algoritmo} (Mayor score)")
    
    def reiniciar(self):
        """Reinicia el juego."""
        print("\n🔄 Reiniciando juego...")
        self.mundo = Mundo(TAMANO_N)
        self.estado_seleccion = 'inicio'
        self.agente_abeja = None
        self.comparador.limpiar()
        self.sistema_vision.limpiar_cache()
        self.mostrar_panel_comparacion = False
        self.estadisticas_actuales = None
        print("✓ Juego reiniciado")

    def run(self):
        juego_en_marcha = True
        while juego_en_marcha:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    juego_en_marcha = False

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado_seleccion == 'inicio':
                        col = evento.pos[0] // TAMANO_CELDA
                        fila = evento.pos[1] // TAMANO_CELDA
                        
                        if self.mundo.seleccionar_punto(evento.pos, TIPO_INICIO):
                            self.agente_abeja = Abeja(self.mundo, (fila, col))
                            self.estado_seleccion = 'meta'
                            print("✓ Inicio seleccionado")

                    elif self.estado_seleccion == 'meta':
                        if self.mundo.seleccionar_punto(evento.pos, TIPO_ENJAMBRE):
                            self.estado_seleccion = 'listo'
                            print("✓ Meta seleccionada")

                if evento.type == pygame.KEYDOWN:
                    if self.estado_seleccion == 'listo':
                        if evento.key == pygame.K_1:  # BFS
                            self.ejecutar_busqueda(bfs_panal, "BFS")
                        elif evento.key == pygame.K_2:  # DFS
                            self.ejecutar_busqueda(dfs_panal, "DFS")
                        elif evento.key == pygame.K_3:  # Comparación
                            self.ejecutar_comparacion()
                    
                    # Controles globales
                    if evento.key == pygame.K_TAB:
                        self.mostrar_panel_comparacion = not self.mostrar_panel_comparacion
                        print(f"Panel comparación: {'Visible' if self.mostrar_panel_comparacion else 'Oculto'}")
                    
                    elif evento.key == pygame.K_s:
                        if len(self.comparador.estadisticas) > 0:
                            self.comparador.guardar_comparacion()
                        else:
                            print("⚠ No hay estadísticas para guardar")
                    
                    elif evento.key == pygame.K_r:
                        self.reiniciar()

            # Actualizar y dibujar
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

        # 3. Dibuja UI
        self.ui_manager.dibujar_instrucciones(self.pantalla, self.estado_seleccion)
        
        # 4. Panel de comparación si está activo
        if self.mostrar_panel_comparacion and len(self.comparador.estadisticas) > 0:
            self.ui_manager.dibujar_panel_comparacion(self.pantalla, self.comparador)
        
        # 5. Resumen simple si hay estadísticas actuales
        elif self.estadisticas_actuales and not self.mostrar_panel_comparacion:
            self.ui_manager.dibujar_resumen_simple(
                self.pantalla, 
                self.estadisticas_actuales, 
                self.ultimo_algoritmo_ejecutado
            )

        # 6. Actualiza toda la pantalla
        pygame.display.flip()

if __name__ == "__main__":
    juego = Juego()
    juego.run()
    pygame.quit()
    sys.exit()