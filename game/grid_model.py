import random
import pygame
import os
from .constants import *

class Celda:
    """Representa una celda individual del grid."""
    
    def __init__(self, fila, columna):
        self.r = fila
        self.c = columna
        self.tipo = TIPO_VACIO
        self.en_ruta = False
        self.imagen_original_path = None
    
    def __repr__(self):
        return f"Celda({self.r}, {self.c}, {self.tipo})"


class Mundo:
    """Representa el grid del juego con todas sus celdas."""
    
    def __init__(self, N):
        self.N = N
        self.grid = []
        self.inicializar_grid_aleatorio()
        self.cargar_imagenes_flores()
    
    def inicializar_grid_aleatorio(self):
        """
        Genera un grid aleatorio con validación de conectividad.
        Intenta hasta 10 veces generar un grid donde todas las celdas
        estén conectadas.
        """
        PROB_OBSTACULO = 0.25
        PROB_FLOR = 0.10
        MAX_INTENTOS = 10
        
        rutas_flores = [
            os.path.join('assets', 'objects', 'flor_1.png'),
            os.path.join('assets', 'objects', 'flor_2.png'),
            os.path.join('assets', 'objects', 'lata.png'),
            os.path.join('assets', 'objects', 'tenis.png')
        ]
        
        print(f"\n🎲 Generando grid {self.N}x{self.N}...")
        
        for intento in range(MAX_INTENTOS):
            self.grid = []
            
            # Generar grid básico
            for fila_num in range(self.N):
                fila_actual = []
                for col_num in range(self.N):
                    celda = Celda(fila_num, col_num)
                    valor_aleatorio = random.random()
                    
                    if valor_aleatorio < PROB_OBSTACULO:
                        celda.tipo = TIPO_OBSTACULO
                    elif valor_aleatorio < PROB_OBSTACULO + PROB_FLOR:
                        celda.tipo = TIPO_FLOR
                        celda.imagen_original_path = random.choice(rutas_flores)
                    
                    fila_actual.append(celda)
                self.grid.append(fila_actual)
            
            # Verificar conectividad
            if self._verificar_conectividad_basica():
                print(f"✅ Grid generado exitosamente (intento {intento + 1})")
                self._imprimir_estadisticas_grid()
                return
            else:
                print(f"   ⚠️  Intento {intento + 1}: Grid desconectado, regenerando...")
        
        # Si después de MAX_INTENTOS no se logró, generar grid simple garantizado
        print(f"⚠️  No se pudo generar grid conectado, creando grid simple...")
        self._generar_grid_simple(PROB_FLOR, rutas_flores)
        print(f"✅ Grid simple generado (conectividad garantizada)")
        self._imprimir_estadisticas_grid()
    
    def _verificar_conectividad_basica(self):
        """
        Verifica que al menos el 90% de las celdas no-obstáculo estén conectadas.
        """
        from collections import deque
        
        # Encontrar primera celda no-obstáculo
        punto_inicio = None
        celdas_validas = 0
        
        for fila in self.grid:
            for celda in fila:
                if celda.tipo != TIPO_OBSTACULO:
                    celdas_validas += 1
                    if punto_inicio is None:
                        punto_inicio = (celda.r, celda.c)
        
        if celdas_validas == 0:
            return False
        
        # BFS para contar celdas alcanzables
        visitados = set()
        cola = deque([punto_inicio])
        
        while cola:
            r, c = cola.popleft()
            
            if (r, c) in visitados:
                continue
            
            visitados.add((r, c))
            
            # Explorar vecinos
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.N and 0 <= nc < self.N:
                    if self.grid[nr][nc].tipo != TIPO_OBSTACULO:
                        if (nr, nc) not in visitados:
                            cola.append((nr, nc))
        
        # Verificar que al menos 90% de celdas válidas sean alcanzables
        porcentaje_conectado = len(visitados) / celdas_validas
        return porcentaje_conectado >= 0.90
    
    def _generar_grid_simple(self, prob_flor, rutas_flores):
        """
        Genera un grid simple sin obstáculos (conectividad garantizada).
        """
        self.grid = []
        
        for fila_num in range(self.N):
            fila_actual = []
            for col_num in range(self.N):
                celda = Celda(fila_num, col_num)
                
                # Solo flores con cierta probabilidad, sin obstáculos
                if random.random() < prob_flor:
                    celda.tipo = TIPO_FLOR
                    celda.imagen_original_path = random.choice(rutas_flores)
                
                fila_actual.append(celda)
            self.grid.append(fila_actual)
    
    def _imprimir_estadisticas_grid(self):
        """Imprime estadísticas básicas del grid generado."""
        contador = {
            TIPO_VACIO: 0,
            TIPO_OBSTACULO: 0,
            TIPO_FLOR: 0
        }
        
        total = self.N * self.N
        
        for fila in self.grid:
            for celda in fila:
                contador[celda.tipo] = contador.get(celda.tipo, 0) + 1
        
        print(f"   📊 Estadísticas:")
        print(f"      • Celdas vacías: {contador[TIPO_VACIO]} ({contador[TIPO_VACIO]/total*100:.1f}%)")
        print(f"      • Obstáculos: {contador[TIPO_OBSTACULO]} ({contador[TIPO_OBSTACULO]/total*100:.1f}%)")
        print(f"      • Flores: {contador[TIPO_FLOR]} ({contador[TIPO_FLOR]/total*100:.1f}%)")
    
    def cargar_imagenes_flores(self):
        """Carga y cachea las imágenes de las flores."""
        self.imagenes_sprites_flores = {}
        
        for fila in self.grid:
            for celda in fila:
                if celda.tipo == TIPO_FLOR and celda.imagen_original_path:
                    path = celda.imagen_original_path
                    
                    if path not in self.imagenes_sprites_flores:
                        try:
                            img = pygame.image.load(path).convert_alpha()
                            self.imagenes_sprites_flores[path] = pygame.transform.scale(
                                img, 
                                (int(TAMANO_CELDA * 0.9), int(TAMANO_CELDA * 0.9))
                            )
                        except pygame.error as e:
                            print(f"❌ Error cargando imagen de flor en {path}: {e}")
    
    def seleccionar_punto(self, pos_pixel, tipo_punto):
        """
        Selecciona un punto (inicio o meta) en el grid basado en la posición del click.
        
        Args:
            pos_pixel: Tupla (x, y) de la posición del click en píxeles
            tipo_punto: Tipo de punto a colocar (TIPO_INICIO o TIPO_ENJAMBRE)
        
        Returns:
            bool: True si se pudo colocar el punto, False si no
        """
        columna = pos_pixel[0] // TAMANO_CELDA
        fila = pos_pixel[1] // TAMANO_CELDA
        
        if 0 <= fila < self.N and 0 <= columna < self.N:
            celda = self.grid[fila][columna]
            
            # No permitir colocar puntos en obstáculos o flores
            if celda.tipo not in [TIPO_OBSTACULO, TIPO_FLOR]:
                # Si es un punto de inicio, limpiar el anterior
                if tipo_punto == TIPO_INICIO:
                    self._limpiar_tipo(TIPO_INICIO)
                
                # Si es un punto de meta, limpiar el anterior
                if tipo_punto == TIPO_ENJAMBRE:
                    self._limpiar_tipo(TIPO_ENJAMBRE)
                
                celda.tipo = tipo_punto
                return True
        
        return False
    
    def _limpiar_tipo(self, tipo):
        """Limpia todas las celdas de un tipo específico."""
        for fila in self.grid:
            for celda in fila:
                if celda.tipo == tipo:
                    celda.tipo = TIPO_VACIO
    
    def obtener_inicio(self):
        """Retorna la posición del punto de inicio o None si no existe."""
        for fila in self.grid:
            for celda in fila:
                if celda.tipo == TIPO_INICIO:
                    return (celda.r, celda.c)
        return None
    
    def obtener_meta(self):
        """Retorna la posición del punto de meta o None si no existe."""
        for fila in self.grid:
            for celda in fila:
                if celda.tipo == TIPO_ENJAMBRE:
                    return (celda.r, celda.c)
        return None
    
    def obtener_vecinos_validos(self, celda_actual):
        """
        Obtiene los vecinos válidos (no obstáculos) de una celda.
        
        Args:
            celda_actual: Objeto Celda
        
        Returns:
            list: Lista de tuplas (fila, columna) de vecinos válidos
        """
        vecinos = []
        movimientos = [
            (-1, 0),  # Arriba
            (1, 0),   # Abajo
            (0, -1),  # Izquierda
            (0, 1)    # Derecha
        ]
        
        r, c = celda_actual.r, celda_actual.c
        
        for dr, dc in movimientos:
            nr, nc = r + dr, c + dc
            
            # Verificar que está dentro del grid
            if 0 <= nr < self.N and 0 <= nc < self.N:
                # Verificar que NO es un obstáculo
                if self.grid[nr][nc].tipo != TIPO_OBSTACULO:
                    vecinos.append((nr, nc))
        
        return vecinos
    
    def limpiar_ruta(self):
        """Limpia todas las marcas de ruta del grid."""
        for fila in self.grid:
            for celda in fila:
                celda.en_ruta = False
    
    def dibujar(self, pantalla):
        """
        Dibuja el grid completo en la pantalla.
        
        Args:
            pantalla: Superficie de Pygame donde dibujar
        """
        for fila in self.grid:
            for celda in fila:
                x = celda.c * TAMANO_CELDA
                y = celda.r * TAMANO_CELDA
                rect_celda = pygame.Rect(x, y, TAMANO_CELDA, TAMANO_CELDA)
                
                # Fondo de la celda
                pygame.draw.rect(pantalla, COLOR_FONDO_CELDA, rect_celda)
                
                # Resaltar si está en la ruta
                if celda.en_ruta:
                    pygame.draw.rect(pantalla, COLOR_RUTA, rect_celda)
                
                # Dibujar contenido según el tipo
                if celda.tipo == TIPO_OBSTACULO:
                    pygame.draw.rect(pantalla, COLOR_OBSTACULO, rect_celda)
                
                elif celda.tipo == TIPO_FLOR:
                    sprite = self.imagenes_sprites_flores.get(celda.imagen_original_path)
                    if sprite:
                        pantalla.blit(sprite, sprite.get_rect(center=rect_celda.center))
                
                elif celda.tipo == TIPO_INICIO:
                    pygame.draw.rect(pantalla, COLOR_INICIO, rect_celda)
                    # Agregar texto "START"
                    fuente = pygame.font.Font(None, 20)
                    texto = fuente.render("START", True, (255, 255, 255))
                    texto_rect = texto.get_rect(center=rect_celda.center)
                    pantalla.blit(texto, texto_rect)
                
                elif celda.tipo == TIPO_ENJAMBRE:
                    pygame.draw.rect(pantalla, COLOR_META, rect_celda)
                    # Agregar texto "GOAL"
                    fuente = pygame.font.Font(None, 20)
                    texto = fuente.render("GOAL", True, (255, 255, 255))
                    texto_rect = texto.get_rect(center=rect_celda.center)
                    pantalla.blit(texto, texto_rect)
                
                # Borde de la celda (más visible)
                pygame.draw.rect(pantalla, COLOR_BORDE_CELDA, rect_celda, 1)
    
    def contar_flores(self):
        """Cuenta el número total de flores en el grid."""
        contador = 0
        for fila in self.grid:
            for celda in fila:
                if celda.tipo == TIPO_FLOR:
                    contador += 1
        return contador
    
    def obtener_estadisticas(self):
        """
        Retorna un diccionario con estadísticas del grid.
        """
        contador = {
            TIPO_VACIO: 0,
            TIPO_OBSTACULO: 0,
            TIPO_FLOR: 0,
            TIPO_INICIO: 0,
            TIPO_ENJAMBRE: 0
        }
        
        for fila in self.grid:
            for celda in fila:
                contador[celda.tipo] = contador.get(celda.tipo, 0) + 1
        
        total = self.N * self.N
        
        return {
            'tamano': self.N,
            'total_celdas': total,
            'vacias': contador[TIPO_VACIO],
            'obstaculos': contador[TIPO_OBSTACULO],
            'flores': contador[TIPO_FLOR],
            'inicio': contador[TIPO_INICIO],
            'meta': contador[TIPO_ENJAMBRE],
            'porcentaje_obstaculos': (contador[TIPO_OBSTACULO] / total * 100) if total > 0 else 0,
            'porcentaje_flores': (contador[TIPO_FLOR] / total * 100) if total > 0 else 0
        }