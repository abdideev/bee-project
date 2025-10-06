import cv2
import numpy as np
from PIL import Image
from transformers import pipeline
import pygame

class VisionSystem:
    """Sistema de visión por computadora para identificar flores en el grid."""
    
    def __init__(self):
        """Inicializa el sistema de visión con el modelo ViT."""
        self.image_classifier = None
        self.inicializar_modelo()
        self.cache_clasificaciones = {}  # Cache para evitar reclasificar
        
    def inicializar_modelo(self):
        """Carga el modelo Vision Transformer."""
        try:
            self.image_classifier = pipeline(
                task="image-classification",
                model="google/vit-base-patch16-224"
            )
            print("✓ Modelo de visión cargado correctamente")
        except Exception as e:
            print(f"⚠ ERROR: No se pudo inicializar el Vision Transformer.")
            print(f"   Instale: pip install transformers torch pillow")
            print(f"   Error: {e}")
            self.image_classifier = None
    
    def ecualizacion_histograma(self, imagen):
        """Aplica ecualización del histograma para mejorar la imagen."""
        if imagen is None or imagen.size == 0:
            return None
            
        # Convertir a escala de grises si es necesario
        if len(imagen.shape) == 3:
            imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        else:
            imagen_gris = imagen
            
        # Aplicar ecualización
        imagen_mejorada = cv2.equalizeHist(imagen_gris)
        return imagen_mejorada
    
    def capturar_celda_desde_pantalla(self, pantalla, fila, columna, tamano_celda):
        """Captura la región de una celda desde la pantalla de Pygame."""
        x = columna * tamano_celda
        y = fila * tamano_celda
        
        # Obtener la superficie de la celda
        celda_surface = pantalla.subsurface((x, y, tamano_celda, tamano_celda))
        
        # Convertir de Pygame a formato OpenCV
        imagen_string = pygame.image.tostring(celda_surface, 'RGB')
        imagen_numpy = np.frombuffer(imagen_string, dtype=np.uint8)
        imagen_numpy = imagen_numpy.reshape((tamano_celda, tamano_celda, 3))
        
        # Convertir de RGB a BGR para OpenCV
        imagen_bgr = cv2.cvtColor(imagen_numpy, cv2.COLOR_RGB2BGR)
        
        return imagen_bgr
    
    def capturar_celda_desde_imagen(self, ruta_imagen):
        """Carga una imagen desde disco (para las flores guardadas)."""
        try:
            imagen = cv2.imread(ruta_imagen)
            return imagen
        except Exception as e:
            print(f"Error cargando imagen {ruta_imagen}: {e}")
            return None
    
    def clasificar_objeto(self, imagen):
        """Clasifica una imagen usando Vision Transformer."""
        if self.image_classifier is None or imagen is None or imagen.size == 0:
            return {
                'etiqueta': 'Clasificador_No_Disponible',
                'probabilidad': 0.0,
                'es_flor': False,
                'confianza': 'baja'
            }
        
        try:
            # Mejorar la imagen primero
            imagen_mejorada = self.ecualizacion_histograma(imagen)
            
            # Convertir a PIL Image en RGB
            if len(imagen_mejorada.shape) == 2:
                imagen_pil = Image.fromarray(imagen_mejorada).convert('RGB')
            else:
                imagen_rgb = cv2.cvtColor(imagen_mejorada, cv2.COLOR_BGR2RGB)
                imagen_pil = Image.fromarray(imagen_rgb)
            
            # Clasificar
            results = self.image_classifier(imagen_pil)
            
            if results and len(results) > 0:
                etiqueta = results[0]['label'].lower()
                probabilidad = results[0]['score']
                
                # Palabras clave para identificar flores
                palabras_clave_flores = [
                    'flower', 'daisy', 'rose', 'sunflower', 'tulip',
                    'plant', 'petal', 'blossom', 'bloom', 'orchid'
                ]

            
                
                es_flor = any(palabra in etiqueta for palabra in palabras_clave_flores)
                
                # Determinar nivel de confianza
                if probabilidad >= 0.7:
                    confianza = 'alta'
                elif probabilidad >= 0.4:
                    confianza = 'media'
                else:
                    confianza = 'baja'
                
                return {
                    'etiqueta': etiqueta,
                    'probabilidad': probabilidad,
                    'es_flor': es_flor,
                    'confianza': confianza
                }
            
            return {
                'etiqueta': 'Clasificación_Inconclusa',
                'probabilidad': 0.0,
                'es_flor': False,
                'confianza': 'baja'
            }
            
        except Exception as e:
            print(f"Error durante la clasificación: {e}")
            return {
                'etiqueta': 'Error_VC',
                'probabilidad': 0.0,
                'es_flor': False,
                'confianza': 'baja'
            }
    
    def analizar_celda_del_grid(self, mundo, fila, columna, pantalla, tamano_celda):
        """Analiza una celda específica del grid y determina si contiene una flor."""
        celda = mundo.grid[fila][columna]
        
        # Crear clave única para el cache
        cache_key = f"{fila}_{columna}"
        
        # Si ya la analizamos, devolver resultado del cache
        if cache_key in self.cache_clasificaciones:
            return self.cache_clasificaciones[cache_key]
        
        resultado = None
        
        # Si la celda tiene una imagen de flor asignada, usarla
        if celda.tipo == 'flor' and celda.imagen_original_path:
            imagen = self.capturar_celda_desde_imagen(celda.imagen_original_path)
            if imagen is not None:
                resultado = self.clasificar_objeto(imagen)
        else:
            # Capturar desde la pantalla
            imagen = self.capturar_celda_desde_pantalla(pantalla, fila, columna, tamano_celda)
            resultado = self.clasificar_objeto(imagen)
        
        # Guardar en cache
        if resultado:
            self.cache_clasificaciones[cache_key] = resultado
        
        return resultado
    
    def limpiar_cache(self):
        """Limpia el cache de clasificaciones."""
        self.cache_clasificaciones = {}