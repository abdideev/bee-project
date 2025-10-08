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
        pygame.display.set_caption("🐝 Abeja Buscadora - Algoritmos de Búsqueda + IA")
        self.mundo = Mundo(TAMANO_N)
        self.estado_seleccion = 'inicio'
        self.agente_abeja = None
        self.reloj = pygame.time.Clock()
        
        # Sistemas
        self.sistema_vision = VisionSystem()
        self.comparador = ComparadorAlgoritmos()
        self.ui_manager = UIManager(ANCHO_PANTALLA, ALTO_PANTALLA)
        self.ui_manager.comparador = self.comparador
        
        # Control de estado
        self.mostrar_panel_comparacion = False
        self.ultimo_algoritmo_ejecutado = None
        self.estadisticas_actuales = None
        
        # Contador de tiempo en ejecución
        self.tiempo_inicio_movimiento = None
        self.tiempo_total_movimiento = 0.0
        self.movimiento_completado = False
        
        self.imprimir_instrucciones()
    
    def imprimir_instrucciones(self):
        """Imprime las instrucciones del juego en la consola."""
        print("\n" + "="*70)
        print("🐝 PROYECTO ABEJA BUSCADORA")
        print("   Algoritmos de Búsqueda Sin Información + Visión por Computadora")
        print("="*70)
        print("\n📋 INSTRUCCIONES:")
        print("-"*70)
        print("1️⃣  Click izquierdo → Seleccionar INICIO (verde)")
        print("2️⃣  Click izquierdo → Seleccionar META (rojo)")
        print("3️⃣  Presiona '1' → Ejecutar BFS (Breadth-First Search)")
        print("4️⃣  Presiona '2' → Ejecutar DFS (Depth-First Search)")
        print("5️⃣  Presiona '3' → Ejecutar AMBOS y COMPARAR")
        print("6️⃣  Presiona 'TAB' → Mostrar/Ocultar panel de estadísticas")
        print("7️⃣  Presiona 'S' → Guardar resultados en JSON")
        print("8️⃣  Presiona 'R' → Reiniciar juego")
        print("9️⃣  Presiona 'V' → Ver reporte del grid")
        print("🔟  Presiona 'ESC' → Salir")
        print("-"*70)
        print("\n💡 CONCEPTOS:")
        print("   • BFS: Explora nivel por nivel, garantiza camino MÁS CORTO")
        print("   • DFS: Explora en profundidad, NO garantiza camino óptimo")
        print("   • Ambos NO atraviesan obstáculos (celdas negras)")
        print("   • La abeja analiza flores con ViT (Vision Transformer)")
        print("="*70 + "\n")
    
    def ejecutar_busqueda(self, algoritmo_func, nombre_estrategia):
        """
        Ejecuta un algoritmo de búsqueda con análisis de visión completo.
        """
        # Obtener coordenadas de inicio y meta
        inicio = self.mundo.obtener_inicio()
        meta = self.mundo.obtener_meta()
        
        if not inicio or not meta:
            print("❌ ERROR: Debes seleccionar inicio y meta primero.")
            return
        
        if not self.agente_abeja:
            print("❌ ERROR: No se ha inicializado el agente abeja.")
            return
        
        print(f"\n{'═'*70}")
        print(f"🚀 Iniciando {nombre_estrategia}...")
        print(f"{'═'*70}")
        
        # Limpiar ruta anterior
        self.mundo.limpiar_ruta()
        self.movimiento_completado = False
        self.tiempo_total_movimiento = 0.0
        
        # Mostrar mensaje de carga
        self.ui_manager.dibujar_mensaje_cargando(
            self.pantalla, 
            f"🔍 Ejecutando {nombre_estrategia}..."
        )
        
        try:
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
            
            if ruta and len(ruta) > 0:
                # Asignar ruta a la abeja
                self.agente_abeja.asignar_ruta(ruta)
                
                # Iniciar contador de tiempo
                self.tiempo_inicio_movimiento = pygame.time.get_ticks() / 1000.0
                
                # Guardar estadísticas
                self.estadisticas_actuales = estadisticas
                self.ultimo_algoritmo_ejecutado = nombre_estrategia
                
                # Agregar al comparador
                self.comparador.agregar_estadistica(nombre_estrategia, estadisticas)
                
                print(f"\n✅ {nombre_estrategia} completado exitosamente")
                print(f"   La abeja comenzará a moverse...")
            else:
                print(f"\n❌ ERROR: No se encontró una ruta válida.")
                self.estadisticas_actuales = None
                
        except Exception as e:
            print(f"\n❌ ERROR durante la ejecución: {e}")
            import traceback
            traceback.print_exc()
            self.estadisticas_actuales = None
    
    def ejecutar_comparacion(self):
        """Ejecuta ambos algoritmos y realiza una comparación completa."""
        print(f"\n{'═'*70}")
        print("📊 MODO COMPARACIÓN: Ejecutando BFS y DFS")
        print(f"{'═'*70}")
        
        # Limpiar estadísticas anteriores
        self.comparador.limpiar()
        
        # Obtener coordenadas
        inicio = self.mundo.obtener_inicio()
        meta = self.mundo.obtener_meta()
        
        if not inicio or not meta:
            print("❌ ERROR: Debes seleccionar inicio y meta primero.")
            return
        
        # Ejecutar BFS
        print("\n" + "-"*70)
        print("🔹 Ejecutando BFS...")
        print("-"*70)
        
        self.ui_manager.dibujar_mensaje_cargando(self.pantalla, "🔍 Ejecutando BFS...")
        
        try:
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
            
            if ruta_bfs and len(ruta_bfs) > 0:
                self.comparador.agregar_estadistica("BFS", stats_bfs)
                print(f"✅ BFS completado - Score: {stats_bfs.calcular_score()}")
        except Exception as e:
            print(f"❌ Error en BFS: {e}")
            ruta_bfs = []
        
        # Ejecutar DFS
        print("\n" + "-"*70)
        print("🔹 Ejecutando DFS...")
        print("-"*70)
        
        self.ui_manager.dibujar_mensaje_cargando(self.pantalla, "🔍 Ejecutando DFS...")
        
        try:
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
            
            if ruta_dfs and len(ruta_dfs) > 0:
                self.comparador.agregar_estadistica("DFS", stats_dfs)
                print(f"✅ DFS completado - Score: {stats_dfs.calcular_score()}")
        except Exception as e:
            print(f"❌ Error en DFS: {e}")
            ruta_dfs = []
        
        # Realizar comparación
        if len(self.comparador.estadisticas) >= 2:
            comparacion = self.comparador.comparar_algoritmos()
            
            # Imprimir análisis en consola
            self.comparador.imprimir_comparacion()
            
            # Mostrar panel de comparación
            self.mostrar_panel_comparacion = True
            
            # Usar la ruta del algoritmo con menor longitud (BFS debería ser óptimo)
            mejor_algoritmo = comparacion['ganadores']['mejor_ruta']
            
            if mejor_algoritmo == "BFS" and ruta_bfs:
                self.agente_abeja.asignar_ruta(ruta_bfs)
                self.estadisticas_actuales = stats_bfs
                self.ultimo_algoritmo_ejecutado = "BFS"
            elif ruta_dfs:
                self.agente_abeja.asignar_ruta(ruta_dfs)
                self.estadisticas_actuales = stats_dfs
                self.ultimo_algoritmo_ejecutado = "DFS"
            
            # Iniciar contador de tiempo
            self.tiempo_inicio_movimiento = pygame.time.get_ticks() / 1000.0
            self.movimiento_completado = False
            
            print(f"\n🏆 Usando ruta de: {mejor_algoritmo}")
            print(f"   La abeja comenzará a moverse...")
        else:
            print("\n⚠️  No se pudieron ejecutar ambos algoritmos para comparar")
    
    def ver_reporte_grid(self):
        """Muestra un reporte detallado del grid."""
        try:
            from core.grid_validator import generar_reporte_grid
            generar_reporte_grid(self.mundo)
        except ImportError:
            # Si no existe el módulo, mostrar estadísticas básicas
            stats = self.mundo.obtener_estadisticas()
            print("\n" + "="*70)
            print("📊 ESTADÍSTICAS DEL GRID")
            print("="*70)
            print(f"Tamaño: {stats['tamano']}x{stats['tamano']}")
            print(f"Total de celdas: {stats['total_celdas']}")
            print(f"Vacías: {stats['vacias']} ({100-stats['porcentaje_obstaculos']-stats['porcentaje_flores']:.1f}%)")
            print(f"Obstáculos: {stats['obstaculos']} ({stats['porcentaje_obstaculos']:.1f}%)")
            print(f"Flores: {stats['flores']} ({stats['porcentaje_flores']:.1f}%)")
            print("="*70 + "\n")
    
    def reiniciar(self):
        """Reinicia el juego completamente."""
        print("\n" + "="*70)
        print("🔄 REINICIANDO JUEGO...")
        print("="*70)
        
        self.mundo = Mundo(TAMANO_N)
        self.estado_seleccion = 'inicio'
        self.agente_abeja = None
        self.comparador.limpiar()
        self.sistema_vision.limpiar_cache()
        self.mostrar_panel_comparacion = False
        self.estadisticas_actuales = None
        self.tiempo_inicio_movimiento = None
        self.tiempo_total_movimiento = 0.0
        self.movimiento_completado = False
        
        print("✅ Juego reiniciado exitosamente\n")

    def run(self):
        """Loop principal del juego."""
        juego_en_marcha = True
        
        while juego_en_marcha:
            # Procesar eventos
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
                            print("✅ Punto de INICIO seleccionado en ({}, {})".format(fila, col))

                    elif self.estado_seleccion == 'meta':
                        if self.mundo.seleccionar_punto(evento.pos, TIPO_ENJAMBRE):
                            self.estado_seleccion = 'listo'
                            fila = evento.pos[1] // TAMANO_CELDA
                            col = evento.pos[0] // TAMANO_CELDA
                            print("✅ Punto de META seleccionado en ({}, {})".format(fila, col))
                            print("\n💡 Ahora presiona 1, 2 o 3 para ejecutar algoritmos\n")

                if evento.type == pygame.KEYDOWN:
                    # Algoritmos (solo si está listo)
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
                        estado = "Visible" if self.mostrar_panel_comparacion else "Oculto"
                        print(f"🔄 Panel de comparación: {estado}")
                    
                    elif evento.key == pygame.K_s:
                        if len(self.comparador.estadisticas) > 0:
                            self.comparador.guardar_comparacion()
                        else:
                            print("⚠️  No hay estadísticas para guardar")
                    
                    elif evento.key == pygame.K_r:
                        self.reiniciar()
                    
                    elif evento.key == pygame.K_v:
                        self.ver_reporte_grid()
                    
                    elif evento.key == pygame.K_ESCAPE:
                        juego_en_marcha = False

            # Actualizar
            self.actualizar()
            
            # Dibujar
            self.dibujar()
            
            # Controlar FPS
            self.reloj.tick(FPS)
        
        print("\n" + "="*70)
        print("👋 ¡Gracias por usar Abeja Buscadora!")
        print("="*70 + "\n")

    def actualizar(self):
        """Actualiza el estado de todos los objetos del juego."""
        if self.agente_abeja:
            # Guardar estado anterior
            estaba_en_movimiento = self.agente_abeja.esta_en_movimiento
            
            # Actualizar abeja
            self.agente_abeja.actualizar()
            
            # Detectar cuando termina el movimiento
            if estaba_en_movimiento and not self.agente_abeja.esta_en_movimiento:
                if not self.movimiento_completado:
                    self.movimiento_completado = True
                    if self.tiempo_inicio_movimiento is not None:
                        self.tiempo_total_movimiento = (pygame.time.get_ticks() / 1000.0) - self.tiempo_inicio_movimiento
                        
                        print(f"\n{'='*70}")
                        print(f"🎯 ¡LA ABEJA HA LLEGADO A LA META!")
                        print(f"{'='*70}")
                        print(f"⏱️  Tiempo de llegada: {self.tiempo_total_movimiento:.2f} segundos")
                        print(f"📏 Distancia recorrida: {self.estadisticas_actuales.longitud_ruta if self.estadisticas_actuales else 'N/A'} pasos")
                        print(f"🏆 Score obtenido: {self.estadisticas_actuales.calcular_score() if self.estadisticas_actuales else 0} flores")
                        print(f"{'='*70}\n")

    def dibujar(self):
        """Dibuja todos los elementos del juego."""
        # 1. Dibujar el mundo
        self.mundo.dibujar(self.pantalla)

        # 2. Dibujar la abeja
        if self.agente_abeja:
            self.agente_abeja.dibujar(self.pantalla)

        # 3. Dibujar UI
        self.ui_manager.dibujar_instrucciones(self.pantalla, self.estado_seleccion)
        
        # 4. Panel de comparación si está activo
        if self.mostrar_panel_comparacion and len(self.comparador.estadisticas) > 0:
            self.ui_manager.dibujar_panel_comparacion(self.pantalla, self.comparador, self.agente_abeja)
        
        # 5. Resumen simple si hay estadísticas actuales
        elif self.estadisticas_actuales and not self.mostrar_panel_comparacion:
            self.ui_manager.dibujar_resumen_simple(
                self.pantalla, 
                self.estadisticas_actuales, 
                self.ultimo_algoritmo_ejecutado,
                self.agente_abeja
            )
        
        # 6. Mostrar tiempo de movimiento si está en progreso
        if self.agente_abeja and self.agente_abeja.esta_en_movimiento:
            if self.tiempo_inicio_movimiento is not None:
                tiempo_transcurrido = (pygame.time.get_ticks() / 1000.0) - self.tiempo_inicio_movimiento
                self.dibujar_contador_tiempo(tiempo_transcurrido)

        # 7. Actualizar pantalla
        pygame.display.flip()
    
    def dibujar_contador_tiempo(self, tiempo):
        """
        Dibuja un contador de tiempo en la esquina superior derecha.
        
        Args:
            tiempo: Tiempo transcurrido en segundos
        """
        # Crear superficie semi-transparente
        ancho_contador = 200
        alto_contador = 50
        superficie = pygame.Surface((ancho_contador, alto_contador))
        superficie.set_alpha(230)
        superficie.fill((30, 30, 40))
        
        # Borde
        pygame.draw.rect(superficie, (100, 200, 255), superficie.get_rect(), 3)
        
        # Texto del contador
        fuente_titulo = pygame.font.Font(None, 20)
        fuente_tiempo = pygame.font.Font(None, 32)
        
        titulo = fuente_titulo.render("⏱️ TIEMPO", True, (200, 200, 200))
        texto_tiempo = fuente_tiempo.render(f"{tiempo:.2f}s", True, (100, 255, 100))
        
        # Centrar textos
        superficie.blit(titulo, (ancho_contador // 2 - titulo.get_width() // 2, 5))
        superficie.blit(texto_tiempo, (ancho_contador // 2 - texto_tiempo.get_width() // 2, 22))
        
        # Posicionar en esquina superior derecha
        x = ANCHO_PANTALLA - ancho_contador - 10
        y = 40
        
        self.pantalla.blit(superficie, (x, y))


if __name__ == "__main__":
    try:
        juego = Juego()
        juego.run()
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()