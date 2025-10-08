import time
import json
import os
from datetime import datetime

class EstadisticasAlgoritmo:
    """Almacena las estadísticas de un algoritmo de búsqueda."""
    
    def __init__(self, nombre_algoritmo):
        self.nombre = nombre_algoritmo
        self.tiempo_ejecucion = 0.0
        self.tiempo_analisis_vision = 0.0
        self.longitud_ruta = 0
        self.ruta_completa = []
        self.exito = False
        
        # Contadores principales (solo de celdas en la ruta)
        self.celdas_analizadas = 0
        self.flores_detectadas_vision = 0  # Flores confirmadas por visión
        self.no_flores = 0  # Celdas que NO son flores según visión
        
        # Detalles de cada celda analizada
        self.detalles_celdas = []  # Lista con info de cada celda en la ruta
        
        # Score (flores detectadas)
        self.score = 0
        
    def registrar_celda_analizada(self, posicion, tipo_celda, es_flor_segun_vision, 
                                   etiqueta, probabilidad, confianza):
        """
        Registra el análisis de una celda de tipo 'flor' en la ruta.
        Solo se llama para celdas que tienen imágenes de flores.
        """
        self.celdas_analizadas += 1
        
        # Actualizar contadores según resultado de visión
        if es_flor_segun_vision:
            self.flores_detectadas_vision += 1
            self.score += 1  # Aumentar score por cada flor encontrada
        else:
            self.no_flores += 1  # La imagen NO fue reconocida como flor
        
        # Guardar detalles
        self.detalles_celdas.append({
            'posicion': posicion,
            'tipo_celda': tipo_celda,  # Siempre será 'flor'
            'es_flor_segun_vision': es_flor_segun_vision,
            'etiqueta_vision': etiqueta,
            'probabilidad': probabilidad,
            'confianza': confianza
        })
    
    def calcular_score(self):
        """Calcula el score total (flores detectadas por visión)."""
        return self.flores_detectadas_vision
    
    def calcular_eficiencia(self):
        """Calcula el porcentaje de flores encontradas respecto a la longitud de ruta."""
        if self.longitud_ruta == 0:
            return 0.0
        return (self.flores_detectadas_vision / self.longitud_ruta) * 100
    
    def calcular_precision_deteccion(self):
        """
        Calcula qué tan bien el modelo detectó las flores reales.
        (Celdas con imágenes que fueron correctamente identificadas como flores)
        """
        if self.celdas_analizadas == 0:
            return 0.0
        
        return (self.flores_detectadas_vision / self.celdas_analizadas) * 100
    
    def obtener_resumen_texto(self):
        """Genera un resumen en texto del análisis."""
        lineas = []
        lineas.append(f"\n{'='*50}")
        lineas.append(f"📊 ESTADÍSTICAS: {self.nombre} (Sin Información)")
        lineas.append(f"{'='*50}")
        lineas.append(f"✓ Meta encontrada: {'SÍ' if self.exito else 'NO'}")
        lineas.append(f"⏱  Tiempo búsqueda: {self.tiempo_ejecucion:.4f}s")
        lineas.append(f"🔍 Tiempo análisis VC: {self.tiempo_analisis_vision:.4f}s")
        lineas.append(f"📏 Nodos explorados: {self.longitud_ruta}")
        lineas.append(f"\n🎯 ANÁLISIS DE FLORES EN LA EXPLORACIÓN:")
        lineas.append(f"  • Flores encontradas: {self.celdas_analizadas}")
        lineas.append(f"  • 🌸 Flores confirmadas (VC): {self.flores_detectadas_vision}")
        lineas.append(f"  • ❌ Imágenes no reconocidas: {self.no_flores}")
        lineas.append(f"  • 🏆 SCORE: {self.calcular_score()}")
        
        # Mostrar coordenadas de flores detectadas
        if self.flores_detectadas_vision > 0:
            lineas.append(f"\n🌸 FLORES DETECTADAS (Coordenadas):")
            for detalle in self.detalles_celdas:
                if detalle['es_flor_segun_vision']:
                    pos = detalle['posicion']
                    etiqueta = detalle['etiqueta_vision']
                    prob = detalle['probabilidad']
                    lineas.append(f"  ✓ ({pos[0]},{pos[1]}) - {etiqueta} (confianza: {prob:.2%})")
        
        # Mostrar coordenadas de imágenes no reconocidas
        if self.no_flores > 0:
            lineas.append(f"\n❌ IMÁGENES NO RECONOCIDAS (Coordenadas):")
            for detalle in self.detalles_celdas:
                if not detalle['es_flor_segun_vision']:
                    pos = detalle['posicion']
                    etiqueta = detalle['etiqueta_vision']
                    prob = detalle['probabilidad']
                    lineas.append(f"  ✗ ({pos[0]},{pos[1]}) - {etiqueta} (confianza: {prob:.2%})")
        
        lineas.append(f"\n📈 MÉTRICAS:")
        lineas.append(f"  • Eficiencia: {self.calcular_eficiencia():.2f}% (flores/exploración)")
        lineas.append(f"  • Precisión VC: {self.calcular_precision_deteccion():.2f}%")
        lineas.append(f"{'='*50}")
        
        return "\n".join(lineas)
    
    def to_dict(self):
        """Convierte las estadísticas a diccionario para guardar."""
        return {
            'nombre': self.nombre,
            'tiempo_ejecucion': self.tiempo_ejecucion,
            'tiempo_analisis_vision': self.tiempo_analisis_vision,
            'longitud_ruta': self.longitud_ruta,
            'celdas_analizadas': self.celdas_analizadas,
            'flores_detectadas': self.flores_detectadas_vision,
            'no_flores': self.no_flores,
            'score': self.calcular_score(),
            'eficiencia': self.calcular_eficiencia(),
            'precision': self.calcular_precision_deteccion(),
            'detalles_celdas': self.detalles_celdas,
            'exito': self.exito
        }


class ComparadorAlgoritmos:
    """Sistema para comparar estadísticas entre diferentes algoritmos."""
    
    def __init__(self):
        self.estadisticas = {}  # {nombre_algoritmo: EstadisticasAlgoritmo}
        self.historial_comparaciones = []
        
    def agregar_estadistica(self, nombre_algoritmo, estadistica):
        """Agrega las estadísticas de un algoritmo."""
        self.estadisticas[nombre_algoritmo] = estadistica
        
    def obtener_estadistica(self, nombre_algoritmo):
        """Obtiene las estadísticas de un algoritmo específico."""
        return self.estadisticas.get(nombre_algoritmo)
    
    def comparar_algoritmos(self):
        """Genera un análisis comparativo entre todos los algoritmos."""
        if len(self.estadisticas) < 2:
            return None
        
        comparacion = {
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'algoritmos': {},
            'ganador_tiempo': None,
            'ganador_score': None,
            'ganador_eficiencia': None,
            'mejor_ruta': None
        }
        
        # Recopilar todas las métricas
        for nombre, stats in self.estadisticas.items():
            comparacion['algoritmos'][nombre] = stats.to_dict()
        
        # Determinar ganadores
        nombres = list(self.estadisticas.keys())
        
        # Ganador por tiempo (menor es mejor)
        ganador_tiempo = min(nombres, key=lambda n: self.estadisticas[n].tiempo_ejecucion)
        comparacion['ganador_tiempo'] = ganador_tiempo
        
        # Ganador por score/flores (mayor es mejor)
        ganador_score = max(nombres, key=lambda n: self.estadisticas[n].calcular_score())
        comparacion['ganador_score'] = ganador_score
        
        # Ganador por eficiencia (mayor es mejor)
        ganador_eficiencia = max(nombres, key=lambda n: self.estadisticas[n].calcular_eficiencia())
        comparacion['ganador_eficiencia'] = ganador_eficiencia
        
        # Mejor ruta (menor longitud es mejor)
        mejor_ruta = min(nombres, key=lambda n: self.estadisticas[n].longitud_ruta)
        comparacion['mejor_ruta'] = mejor_ruta
        
        # Análisis textual
        comparacion['analisis'] = self._generar_analisis_textual(comparacion)
        
        # Guardar en historial
        self.historial_comparaciones.append(comparacion)
        
        return comparacion
    
    def _generar_analisis_textual(self, comparacion):
        """Genera un análisis en texto de la comparación."""
        lineas = []
        lineas.append("\n" + "=" * 70)
        lineas.append("📊 ANÁLISIS COMPARATIVO DE ALGORITMOS")
        lineas.append("=" * 70)
        
        for nombre, datos in comparacion['algoritmos'].items():
            lineas.append(f"\n🤖 {nombre.upper()}:")
            lineas.append(f"  ⏱  Tiempo: {datos['tiempo_ejecucion']:.4f}s")
            lineas.append(f"  📏 Longitud de ruta: {datos['longitud_ruta']} pasos")
            lineas.append(f"  🌸 Flores detectadas: {datos['flores_detectadas']}")
            lineas.append(f"  ❌ No-flores: {datos['no_flores']}")
            lineas.append(f"  🏆 SCORE: {datos['score']}")
            lineas.append(f"  📊 Eficiencia: {datos['eficiencia']:.2f}%")
            lineas.append(f"  🎯 Precisión: {datos['precision']:.2f}%")
        
        lineas.append("\n" + "=" * 70)
        lineas.append("🏆 GANADORES POR CATEGORÍA:")
        lineas.append("=" * 70)
        lineas.append(f"⚡ Más Rápido: {comparacion['ganador_tiempo']}")
        lineas.append(f"🌸 Mayor Score: {comparacion['ganador_score']} "
                     f"({comparacion['algoritmos'][comparacion['ganador_score']]['score']} flores)")
        lineas.append(f"📊 Más Eficiente: {comparacion['ganador_eficiencia']}")
        lineas.append(f"🛤️  Mejor Ruta: {comparacion['mejor_ruta']}")
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
                
            print(f"✓ Comparación guardada en {ruta_archivo}")
            
        except Exception as e:
            print(f"⚠ Error guardando comparación: {e}")
    
    def cargar_historial(self, ruta_archivo="data/comparaciones.json"):
        """Carga el historial de comparaciones."""
        try:
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    self.historial_comparaciones = json.load(f)
                print(f"✓ Historial cargado: {len(self.historial_comparaciones)} comparaciones")
        except Exception as e:
            print(f"⚠ Error cargando historial: {e}")
    
    def limpiar(self):
        """Limpia las estadísticas actuales para una nueva comparación."""
        self.estadisticas = {}
    
    def imprimir_comparacion(self):
        """Imprime la última comparación en consola."""
        if self.historial_comparaciones:
            print(self.historial_comparaciones[-1]['analisis'])