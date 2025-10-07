import pygame

class UIManager:
    """Gestor de interfaz de usuario para mostrar estadísticas y información."""
    
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho = ancho_pantalla
        self.alto = alto_pantalla
        self.fuente_titulo = pygame.font.Font(None, 28)
        self.fuente_texto = pygame.font.Font(None, 20)
        self.fuente_pequena = pygame.font.Font(None, 16)
        
        # Panel de estadísticas (se muestra a la derecha o abajo)
        self.panel_activo = False
        self.comparador = None
        self.mostrar_panel_completo = False
        
    def dibujar_instrucciones(self, pantalla, estado_seleccion):
        """Dibuja las instrucciones en la parte superior."""
        instrucciones = {
            'inicio': 'Click para seleccionar INICIO (verde)',
            'meta': 'Click para seleccionar META/ENJAMBRE (rojo)',
            'listo': 'Presiona 1=BFS | 2=DFS | 3=Comparar'
        }
        
        texto = instrucciones.get(estado_seleccion, '')
        superficie_texto = self.fuente_texto.render(texto, True, (255, 255, 255))
        rect_texto = superficie_texto.get_rect(center=(self.ancho // 2, 15))
        
        # Fondo semi-transparente
        fondo = pygame.Surface((self.ancho, 30))
        fondo.set_alpha(200)
        fondo.fill((0, 0, 0))
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(superficie_texto, rect_texto)
    
    def dibujar_estadisticas_algoritmo(self, pantalla, stats, x, y, color_titulo):
        """Dibuja las estadísticas de un algoritmo en una posición específica."""
        if not stats:
            return
        
        offset_y = y
        
        # Título
        titulo = self.fuente_titulo.render(f"{stats.nombre}", True, color_titulo)
        pantalla.blit(titulo, (x, offset_y))
        offset_y += 30
        
        # SCORE destacado
        score_texto = self.fuente_titulo.render(f"🏆 SCORE: {stats.calcular_score()}", True, (255, 215, 0))
        pantalla.blit(score_texto, (x, offset_y))
        offset_y += 35
        
        # Líneas de estadísticas
        lineas = [
            f"⏱ Tiempo: {stats.tiempo_ejecucion:.4f}s",
            f"📏 Nodos explorados: {stats.longitud_ruta}",
            f"🔍 Flores encontradas: {stats.celdas_analizadas}",
            f"🌸 Confirmadas: {stats.flores_detectadas_vision}",
            f"❌ No reconocidas: {stats.no_flores}",
            f"📊 Eficiencia: {stats.calcular_eficiencia():.1f}%",
            f"🎯 Precisión VC: {stats.calcular_precision_deteccion():.1f}%"
        ]
        
        for linea in lineas:
            texto = self.fuente_pequena.render(linea, True, (200, 200, 200))
            pantalla.blit(texto, (x, offset_y))
            offset_y += 18
        
        return offset_y
    
    def dibujar_panel_comparacion(self, pantalla, comparador):
        """Dibuja un panel con la comparación de algoritmos."""
        if not comparador or len(comparador.estadisticas) == 0:
            return
        
        # Crear superficie para el panel
        ancho_panel = 350
        alto_panel = self.alto
        panel = pygame.Surface((ancho_panel, alto_panel))
        panel.set_alpha(240)
        panel.fill((20, 20, 30))
        
        # Borde del panel
        pygame.draw.rect(panel, (100, 100, 150), panel.get_rect(), 3)
        
        y_offset = 10
        
        # Título principal
        titulo = self.fuente_titulo.render("COMPARACIÓN", True, (255, 200, 0))
        panel.blit(titulo, (ancho_panel // 2 - titulo.get_width() // 2, y_offset))
        y_offset += 40
        
        # Dibujar estadísticas de cada algoritmo
        colores_algoritmos = {
            'BFS': (100, 200, 255),
            'DFS': (255, 150, 100)
        }
        
        for nombre, stats in comparador.estadisticas.items():
            color = colores_algoritmos.get(nombre, (200, 200, 200))
            
            # Título del algoritmo
            texto_algo = self.fuente_texto.render(f"━━ {nombre} ━━", True, color)
            panel.blit(texto_algo, (20, y_offset))
            y_offset += 25
            
            # SCORE GRANDE
            score_texto = self.fuente_titulo.render(f"SCORE: {stats.calcular_score()}", True, (255, 215, 0))
            panel.blit(score_texto, (30, y_offset))
            y_offset += 30
            
            # Estadísticas
            lineas = [
                f"⏱ Tiempo: {stats.tiempo_ejecucion:.4f}s",
                f"📏 Explorados: {stats.longitud_ruta} nodos",
                f"🔍 Flores: {stats.celdas_analizadas}",
                f"🌸 Confirmadas: {stats.flores_detectadas_vision}",
                f"❌ No reconocidas: {stats.no_flores}",
                f"📊 Eficiencia: {stats.calcular_eficiencia():.1f}%",
                f"🎯 Precisión VC: {stats.calcular_precision_deteccion():.1f}%"
            ]
            
            for linea in lineas:
                texto = self.fuente_pequena.render(linea, True, (220, 220, 220))
                panel.blit(texto, (30, y_offset))
                y_offset += 18
            
            y_offset += 15
        
        # Línea separadora
        pygame.draw.line(panel, (100, 100, 150), (10, y_offset), (ancho_panel - 10, y_offset), 2)
        y_offset += 20
        
        # Sección de ganadores
        if len(comparador.estadisticas) >= 2:
            comparacion = comparador.comparar_algoritmos()
            
            titulo_ganadores = self.fuente_texto.render("🏆 GANADORES", True, (255, 215, 0))
            panel.blit(titulo_ganadores, (ancho_panel // 2 - titulo_ganadores.get_width() // 2, y_offset))
            y_offset += 30
            
            ganadores = [
                f"⚡ Más Rápido: {comparacion['ganador_tiempo']}",
                f"🏆 Mayor Score: {comparacion['ganador_score']}",
                f"📊 Eficiente: {comparacion['ganador_eficiencia']}",
                f"🛤️ Mejor Ruta: {comparacion['mejor_ruta']}"
            ]
            
            for ganador in ganadores:
                texto = self.fuente_pequena.render(ganador, True, (150, 255, 150))
                panel.blit(texto, (20, y_offset))
                y_offset += 20
        
        # Instrucciones
        y_offset += 20
        instrucciones = [
            "Presiona TAB para",
            "ocultar/mostrar panel",
            "",
            "Presiona S para",
            "guardar resultados"
        ]
        
        for inst in instrucciones:
            texto = self.fuente_pequena.render(inst, True, (150, 150, 150))
            panel.blit(texto, (20, y_offset))
            y_offset += 16
        
        # Dibujar el panel en la pantalla
        pantalla.blit(panel, (self.ancho - ancho_panel, 0))
    
    def dibujar_resumen_simple(self, pantalla, stats, nombre):
        """Dibuja un resumen simple en la parte inferior de la pantalla."""
        if not stats:
            return
        
        # Crear barra inferior
        altura_barra = 70
        barra = pygame.Surface((self.ancho, altura_barra))
        barra.set_alpha(220)
        barra.fill((25, 25, 35))
        
        y_barra = self.alto - altura_barra
        
        # SCORE destacado
        score_texto = self.fuente_titulo.render(f"🏆 SCORE: {stats.calcular_score()}", True, (255, 215, 0))
        barra.blit(score_texto, (20, 8))
        
        # Información resumida
        resumen = f"{nombre} | Tiempo: {stats.tiempo_ejecucion:.3f}s | Explorados: {stats.longitud_ruta} nodos | Flores: {stats.celdas_analizadas} | Confirmadas: {stats.flores_detectadas_vision}"
        
        texto = self.fuente_pequena.render(resumen, True, (150, 255, 150))
        barra.blit(texto, (20, 38))
        
        # Tercera línea
        eficiencia = f"No reconocidas: {stats.no_flores} | Eficiencia: {stats.calcular_eficiencia():.1f}% | Precisión VC: {stats.calcular_precision_deteccion():.1f}%"
        texto2 = self.fuente_pequena.render(eficiencia, True, (200, 200, 200))
        barra.blit(texto2, (20, 53))
        
        pantalla.blit(barra, (0, y_barra))
    
    def dibujar_detalles_flores(self, pantalla, stats, x_inicio, y_inicio):
        """Dibuja detalles de las flores encontradas."""
        if not stats or len(stats.detalles_celdas) == 0:
            return
        
        y = y_inicio
        titulo = self.fuente_texto.render("Celdas Analizadas:", True, (255, 200, 100))
        pantalla.blit(titulo, (x_inicio, y))
        y += 25
        
        # Mostrar solo las primeras 10 celdas que son flores
        flores_mostradas = 0
        for detalle in stats.detalles_celdas:
            if flores_mostradas >= 10:
                break
            
            if detalle['es_flor_segun_vision']:
                pos = detalle['posicion']
                etiqueta = detalle['etiqueta_vision'][:15]
                prob = detalle['probabilidad']
                
                texto = f"🌸 ({pos[0]},{pos[1]}) {etiqueta} {prob:.2f}"
                color = (150, 255, 150)
                
                superficie = self.fuente_pequena.render(texto, True, color)
                pantalla.blit(superficie, (x_inicio, y))
                y += 18
                flores_mostradas += 1
            
            if y > self.alto - 100:
                break
    
    def dibujar_mensaje_cargando(self, pantalla, mensaje="Analizando con Visión por Computadora..."):
        """Muestra un mensaje de carga mientras se procesa."""
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0, 0))
        
        texto = self.fuente_titulo.render(mensaje, True, (255, 255, 100))
        rect = texto.get_rect(center=(self.ancho // 2, self.alto // 2))
        pantalla.blit(texto, rect)
        
        pygame.display.flip()
    
    def dibujar_error(self, pantalla, mensaje_error):
        """Muestra un mensaje de error."""
        altura_barra = 40
        barra = pygame.Surface((self.ancho, altura_barra))
        barra.set_alpha(220)
        barra.fill((150, 0, 0))
        
        texto = self.fuente_texto.render(f"⚠ {mensaje_error}", True, (255, 255, 255))
        barra.blit(texto, (20, 10))
        
        pantalla.blit(barra, (0, self.alto - altura_barra))
    
    def dibujar_info_vision(self, pantalla, celda_pos, resultado_vision):
        """Muestra información de visión sobre una celda específica."""
        if not resultado_vision:
            return
        
        # Crear tooltip pequeño
        ancho_tooltip = 200
        alto_tooltip = 80
        tooltip = pygame.Surface((ancho_tooltip, alto_tooltip))
        tooltip.set_alpha(230)
        tooltip.fill((40, 40, 60))
        pygame.draw.rect(tooltip, (100, 100, 150), tooltip.get_rect(), 2)
        
        # Información
        lineas = [
            f"Celda: ({celda_pos[0]}, {celda_pos[1]})",
            f"Clase: {resultado_vision['etiqueta'][:15]}",
            f"Prob: {resultado_vision['probabilidad']:.2f}",
            f"Es flor: {'Sí' if resultado_vision['es_flor'] else 'No'}"
        ]
        
        y = 5
        for linea in lineas:
            texto = self.fuente_pequena.render(linea, True, (220, 220, 220))
            tooltip.blit(texto, (10, y))
            y += 18
        
        # Posicionar cerca del mouse
        mouse_pos = pygame.mouse.get_pos()
        x = min(mouse_pos[0] + 10, self.ancho - ancho_tooltip - 10)
        y = min(mouse_pos[1] + 10, self.alto - alto_tooltip - 10)
        
        pantalla.blit(tooltip, (x, y))