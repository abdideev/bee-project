import time
import json
import os
from datetime import datetime

class EstadisticasAlgoritmo:
    """Almacena las estadísticas completas de un algoritmo de búsqueda."""
    
    def __init__(self, nombre_algoritmo):
        self.nombre = nombre_algoritmo
        
        # Tiempos
        self.tiempo_ejecucion = 0.0  # Tiempo de búsqueda
        self.tiempo_analisis_vision = 0.0  # Tiempo de análisis VC
        self.tiempo_total = 0.0  # Suma de ambos
        
        # Métricas de búsqueda
        self.nodos_explorados = 0  # Total de nodos visitados
        self.longitud_ruta = 0  # Longitud del camino encontrado
        self.ruta_completa = []  # Camino completo
        self.exito = False  # ¿Se encontró la meta?
        
        # Métricas de visión
        self.celdas_analizadas = 0  # Flores encontradas en la ruta
        self.flores_detectadas_vision = 0  # Flores confirmadas por VC
        self.no_flores = 0  # Imágenes no reconocidas como flores
        
        # Detalles de cada celda analizada
        self.detalles_celdas = []
        
        # Score
        self.score = 0
        
    def registrar_celda_analizada(self, posicion, tipo_celda, es_flor_segun_vision, 
                                   etiqueta, probabilidad, confianza):
        """
        Registra el análisis de una celda de tipo 'flor' en la ruta.
        """
        self.celdas_analizadas += 1
        
        # Actualizar contadores según resultado de visión
        if es_flor_segun_vision:
            self.flores_detectadas_vision += 1
            self.score += 1
        else:
            self.no_flores += 1
        
        # Guardar detalles
        self.detalles_celdas.append({
            'posicion': posicion,
            'tipo_celda': tipo_celda,
            'es_flor_segun_vision': es_flor_segun_vision,
            'etiqueta_vision': etiqueta,
            'probabilidad': probabilidad,
            'confianza': confianza
        })
    
    def calcular_score(self):
        """Calcula el score total (flores detectadas por visión)."""
        return self.flores_detectadas_vision
    
    def calcular_eficiencia(self):
        """
        Calcula la eficiencia del camino encontrado.
        Ratio: (longitud_ruta / nodos_explorados) * 100
        """
        if self.nodos_explorados == 0:
            return 0.0
        return (self.longitud_ruta / self.nodos_explorados) * 100
    
    def calcular_precision_deteccion(self):
        """
        Calcula la precisión del detector de visión.
        (Flores confirmadas / Total de celdas analizadas) * 100
        """
        if self.celdas_analizadas == 0:
            return 0.0
        return (self.flores_detectadas_vision / self.celdas_analizadas) * 100
    
    def calcular_velocidad(self):
        """Calcula nodos explorados por segundo."""
        if self.tiempo_ejecucion == 0:
            return 0.0
        return self.nodos_explorados / self.tiempo_ejecucion
    
    def obtener_resumen_texto(self):
        """Genera un resumen detallado en texto."""
        self.tiempo_total = self.tiempo_ejecucion + self.tiempo_analisis_vision
        
        lineas = []
        lineas.append(f"\n{'='*70}")
        lineas.append(f"📊 ESTADÍSTICAS DETALLADAS: {self.nombre}")
        lineas.append(f"{'='*70}")
        
        # Estado de la búsqueda
        estado = "✅ EXITOSA" if self.exito else "❌ FALLIDA"
        lineas.append(f"Estado: {estado}")
        
        # Sección de tiempos
        lineas.append(f"\n⏱️  TIEMPOS:")
        lineas.append(f"  • Búsqueda: {self.tiempo_ejecucion:.4f}s")
        lineas.append(f"  • Análisis VC: {self.tiempo_analisis_vision:.4f}s")
        lineas.append(f"  • TOTAL: {self.tiempo_total:.4f}s")
        lineas.append(f"  • Velocidad: {self.calcular_velocidad():.2f} nodos/seg")
        
        # Sección de exploración
        lineas.append(f"\n📏 EXPLORACIÓN:")
        lineas.append(f"  • Nodos explorados: {self.nodos_explorados}")
        lineas.append(f"  • Longitud de ruta: {self.longitud_ruta}")
        lineas.append(f"  • Eficiencia: {self.calcular_eficiencia():.2f}%")
        
        if self.longitud_ruta > 0:
            overhead = self.nodos_explorados - self.longitud_ruta
            lineas.append(f"  • Nodos extra explorados: {overhead}")
            lineas.append(f"  • Ratio exploración: {(self.nodos_explorados / self.longitud_ruta):.2f}x")
        
        # Sección de análisis de flores
        lineas.append(f"\n🌸 ANÁLISIS DE FLORES:")
        lineas.append(f"  • Flores en ruta: {self.celdas_analizadas}")
        lineas.append(f"  • Confirmadas (VC): {self.flores_detectadas_vision}")
        lineas.append(f"  • No reconocidas: {self.no_flores}")
        lineas.append(f"  • Precisión VC: {self.calcular_precision_deteccion():.1f}%")
        
        # Score
        lineas.append(f"\n🏆 PUNTUACIÓN:")
        lineas.append(f"  • SCORE: {self.calcular_score()} puntos")
        
        # Mostrar flores detectadas
        if self.flores_detectadas_vision > 0:
            lineas.append(f"\n🌸 FLORES CONFIRMADAS:")
            for detalle in self.detalles_celdas:
                if detalle['es_flor_segun_vision']:
                    pos = detalle['posicion']
                    etiqueta = detalle['etiqueta_vision'][:25]
                    prob = detalle['probabilidad']
                    lineas.append(f"  ✓ ({pos[0]:2d},{pos[1]:2d}) → {etiqueta} ({prob:.2%})")
        
        # Mostrar no detectadas
        if self.no_flores > 0:
            lineas.append(f"\n❌ IMÁGENES NO RECONOCIDAS:")
            for detalle in self.detalles_celdas:
                if not detalle['es_flor_segun_vision']:
                    pos = detalle['posicion']
                    etiqueta = detalle['etiqueta_vision'][:25]
                    prob = detalle['probabilidad']
                    lineas.append(f"  ✗ ({pos[0]:2d},{pos[1]:2d}) → {etiqueta} ({prob:.2%})")
        
        lineas.append(f"{'='*70}\n")
        
        return "\n".join(lineas)
    
    def to_dict(self):
        """Convierte las estadísticas a diccionario para guardar en JSON."""
        return {
            'nombre': self.nombre,
            'exito': self.exito,
            'tiempos': {
                'busqueda': self.tiempo_ejecucion,
                'analisis_vision': self.tiempo_analisis_vision,
                'total': self.tiempo_ejecucion + self.tiempo_analisis_vision
            },
            'exploracion': {
                'nodos_explorados': self.nodos_explorados,
                'longitud_ruta': self.longitud_ruta,
                'eficiencia': self.calcular_eficiencia(),
                'velocidad_nodos_seg': self.calcular_velocidad()
            },
            'flores': {
                'encontradas': self.celdas_analizadas,
                'confirmadas': self.flores_detectadas_vision,
                'no_reconocidas': self.no_flores,
                'precision': self.calcular_precision_deteccion()
            },
            'score': self.calcular_score(),
            'detalles_celdas': self.detalles_celdas,
            'ruta': [list(coord) for coord in self.ruta_completa]
        }


class ComparadorAlgoritmos:
    """Sistema para comparar estadísticas entre diferentes algoritmos."""
    
    def __init__(self):
        self.estadisticas = {}  # {nombre_algoritmo: EstadisticasAlgoritmo}
        self.historial_comparaciones = []
        
    def agregar_estadistica(self, nombre_algoritmo, estadistica):
        """Agrega las estadísticas de un algoritmo."""
        self.estadisticas[nombre_algoritmo] = estadistica
        print(f"✓ Estadísticas de {nombre_algoritmo} agregadas al comparador")
        
    def obtener_estadistica(self, nombre_algoritmo):
        """Obtiene las estadísticas de un algoritmo específico."""
        return self.estadisticas.get(nombre_algoritmo)
    
    def comparar_algoritmos(self):
        """Genera un análisis comparativo entre todos los algoritmos."""
        if len(self.estadisticas) < 2:
            print("⚠️  Se necesitan al menos 2 algoritmos para comparar")
            return None
        
        comparacion = {
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'algoritmos': {},
            'ganadores': {},
            'diferencias': {}
        }
        
        # Recopilar todas las métricas
        for nombre, stats in self.estadisticas.items():
            comparacion['algoritmos'][nombre] = stats.to_dict()
        
        # Determinar ganadores
        nombres = list(self.estadisticas.keys())
        
        # Ganador por tiempo (menor es mejor)
        ganador_tiempo = min(nombres, key=lambda n: self.estadisticas[n].tiempo_ejecucion)
        comparacion['ganadores']['tiempo_busqueda'] = ganador_tiempo
        
        # Ganador por score (mayor es mejor)
        ganador_score = max(nombres, key=lambda n: self.estadisticas[n].calcular_score())
        comparacion['ganadores']['mayor_score'] = ganador_score
        
        # Ganador por eficiencia (mayor es mejor)
        ganador_eficiencia = max(nombres, key=lambda n: self.estadisticas[n].calcular_eficiencia())
        comparacion['ganadores']['mayor_eficiencia'] = ganador_eficiencia
        
        # Mejor ruta (menor longitud es mejor)
        ganador_ruta = min(nombres, key=lambda n: self.estadisticas[n].longitud_ruta if self.estadisticas[n].longitud_ruta > 0 else float('inf'))
        comparacion['ganadores']['mejor_ruta'] = ganador_ruta
        
        # Menos nodos explorados (más eficiente)
        menos_nodos = min(nombres, key=lambda n: self.estadisticas[n].nodos_explorados)
        comparacion['ganadores']['menos_nodos_explorados'] = menos_nodos
        
        # Calcular diferencias porcentuales
        if len(nombres) == 2:
            algo1, algo2 = nombres[0], nombres[1]
            stats1 = self.estadisticas[algo1]
            stats2 = self.estadisticas[algo2]
            
            comparacion['diferencias'] = {
                'tiempo': self._calcular_diferencia_porcentual(
                    stats1.tiempo_ejecucion, stats2.tiempo_ejecucion
                ),
                'nodos_explorados': self._calcular_diferencia_porcentual(
                    stats1.nodos_explorados, stats2.nodos_explorados
                ),
                'longitud_ruta': self._calcular_diferencia_porcentual(
                    stats1.longitud_ruta, stats2.longitud_ruta
                ),
                'score': self._calcular_diferencia_porcentual(
                    stats1.calcular_score(), stats2.calcular_score()
                )
            }
        
        # Análisis textual
        comparacion['analisis'] = self._generar_analisis_textual(comparacion)
        
        # Guardar en historial
        self.historial_comparaciones.append(comparacion)
        
        return comparacion
    
    def _calcular_diferencia_porcentual(self, valor1, valor2):
        """Calcula la diferencia porcentual entre dos valores."""
        if valor2 == 0:
            return 0
        return ((valor1 - valor2) / valor2) * 100
    
    def _generar_analisis_textual(self, comparacion):
        """Genera un análisis detallado en texto de la comparación."""
        lineas = []
        lineas.append("\n" + "=" * 70)
        lineas.append("🔬 ANÁLISIS COMPARATIVO DE ALGORITMOS")
        lineas.append("=" * 70)
        lineas.append(f"📅 Fecha: {comparacion['fecha']}")
        lineas.append("")
        
        # Tabla comparativa
        lineas.append("📊 TABLA COMPARATIVA:")
        lineas.append("-" * 70)
        
        # Encabezado
        algoritmos = list(comparacion['algoritmos'].keys())
        header = f"{'Métrica':<25} | " + " | ".join([f"{algo:>15}" for algo in algoritmos])
        lineas.append(header)
        lineas.append("-" * 70)
        
        # Filas de datos
        metricas = [
            ('Tiempo (s)', lambda s: f"{s['tiempos']['busqueda']:.4f}"),
            ('Nodos explorados', lambda s: f"{s['exploracion']['nodos_explorados']}"),
            ('Longitud ruta', lambda s: f"{s['exploracion']['longitud_ruta']}"),
            ('Eficiencia (%)', lambda s: f"{s['exploracion']['eficiencia']:.2f}"),
            ('Flores confirmadas', lambda s: f"{s['flores']['confirmadas']}"),
            ('Score', lambda s: f"{s['score']}"),
            ('Precisión VC (%)', lambda s: f"{s['flores']['precision']:.1f}")
        ]
        
        for nombre_metrica, extractor in metricas:
            valores = []
            for algo in algoritmos:
                stats = comparacion['algoritmos'][algo]
                valores.append(extractor(stats))
            
            fila = f"{nombre_metrica:<25} | " + " | ".join([f"{v:>15}" for v in valores])
            lineas.append(fila)
        
        lineas.append("-" * 70)
        
        # Sección de ganadores
        lineas.append("\n🏆 GANADORES POR CATEGORÍA:")
        lineas.append("=" * 70)
        
        ganadores = comparacion['ganadores']
        
        lineas.append(f"⚡ Más Rápido (tiempo): {ganadores['tiempo_busqueda']}")
        lineas.append(f"🌸 Mayor Score: {ganadores['mayor_score']}")
        lineas.append(f"📊 Mayor Eficiencia: {ganadores['mayor_eficiencia']}")
        lineas.append(f"🛤️  Mejor Ruta (más corta): {ganadores['mejor_ruta']}")
        lineas.append(f"🎯 Menos Nodos Explorados: {ganadores['menos_nodos_explorados']}")
        
        # Diferencias si hay dos algoritmos
        if 'diferencias' in comparacion and comparacion['diferencias']:
            lineas.append("\n📈 DIFERENCIAS PORCENTUALES:")
            lineas.append("-" * 70)
            algo1, algo2 = list(comparacion['algoritmos'].keys())
            difs = comparacion['diferencias']
            
            lineas.append(f"{algo1} vs {algo2}:")
            lineas.append(f"  • Tiempo: {difs['tiempo']:+.2f}%")
            lineas.append(f"  • Nodos explorados: {difs['nodos_explorados']:+.2f}%")
            lineas.append(f"  • Longitud ruta: {difs['longitud_ruta']:+.2f}%")
            lineas.append(f"  • Score: {difs['score']:+.2f}%")
        
        # Análisis cualitativo
        lineas.append("\n💡 ANÁLISIS:")
        lineas.append("=" * 70)
        
        # BFS vs DFS
        if 'BFS' in algoritmos and 'DFS' in algoritmos:
            bfs_stats = comparacion['algoritmos']['BFS']
            dfs_stats = comparacion['algoritmos']['DFS']
            
            lineas.append("🔍 BFS (Breadth-First Search):")
            lineas.append("   ✓ Garantiza el camino MÁS CORTO")
            lineas.append(f"   • Exploró {bfs_stats['exploracion']['nodos_explorados']} nodos")
            lineas.append(f"   • Encontró ruta de {bfs_stats['exploracion']['longitud_ruta']} pasos")
            lineas.append(f"   • Eficiencia: {bfs_stats['exploracion']['eficiencia']:.2f}%")
            
            lineas.append("\n🔍 DFS (Depth-First Search):")
            lineas.append("   ⚠️  NO garantiza el camino más corto")
            lineas.append(f"   • Exploró {dfs_stats['exploracion']['nodos_explorados']} nodos")
            lineas.append(f"   • Encontró ruta de {dfs_stats['exploracion']['longitud_ruta']} pasos")
            lineas.append(f"   • Eficiencia: {dfs_stats['exploracion']['eficiencia']:.2f}%")
            
            # Determinar cuál fue mejor
            if bfs_stats['exploracion']['longitud_ruta'] < dfs_stats['exploracion']['longitud_ruta']:
                lineas.append("\n   📌 BFS encontró un camino MÁS CORTO que DFS")
            elif bfs_stats['exploracion']['longitud_ruta'] > dfs_stats['exploracion']['longitud_ruta']:
                lineas.append("\n   📌 En este caso, DFS encontró un camino más corto (por suerte)")
            else:
                lineas.append("\n   📌 Ambos encontraron caminos de la misma longitud")
            
            if bfs_stats['exploracion']['nodos_explorados'] < dfs_stats['exploracion']['nodos_explorados']:
                lineas.append("   📌 BFS exploró MENOS nodos")
            else:
                lineas.append("   📌 DFS exploró MENOS nodos")
        
        lineas.append("=" * 70)
        
        return "\n".join(lineas)
    
    def guardar_comparacion(self, ruta_archivo="data/comparaciones.json"):
        """Guarda la comparación en un archivo JSON."""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
            
            # Cargar comparaciones existentes
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            
            # Agregar nueva comparación
            if self.historial_comparaciones:
                data.append(self.historial_comparaciones[-1])
            
            # Guardar
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Comparación guardada en: {ruta_archivo}")
            print(f"   Total de comparaciones en archivo: {len(data)}")
            
        except Exception as e:
            print(f"❌ Error guardando comparación: {e}")
    
    def cargar_historial(self, ruta_archivo="data/comparaciones.json"):
        """Carga el historial de comparaciones."""
        try:
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    self.historial_comparaciones = json.load(f)
                print(f"✅ Historial cargado: {len(self.historial_comparaciones)} comparaciones")
                return True
            else:
                print(f"ℹ️  No existe archivo de historial en: {ruta_archivo}")
                return False
        except Exception as e:
            print(f"❌ Error cargando historial: {e}")
            return False
    
    def limpiar(self):
        """Limpia las estadísticas actuales para una nueva comparación."""
        self.estadisticas = {}
        print("🧹 Estadísticas actuales limpiadas")
    
    def imprimir_comparacion(self):
        """Imprime la última comparación en consola."""
        if self.historial_comparaciones:
            print(self.historial_comparaciones[-1]['analisis'])
        else:
            print("⚠️  No hay comparaciones disponibles")
    
    def obtener_resumen_rapido(self):
        """Genera un resumen rápido de la última comparación."""
        if not self.estadisticas:
            return "No hay estadísticas disponibles"
        
        lineas = []
        for nombre, stats in self.estadisticas.items():
            lineas.append(f"{nombre}: {stats.longitud_ruta} pasos, "
                         f"{stats.nodos_explorados} nodos, "
                         f"{stats.calcular_score()} score")
        
        return " | ".join(lineas)