# vision_module/classifier_vit.py

from transformers import pipeline
import numpy as np
from PIL import Image

# Inicialización del Modelo ViT (una sola vez)
try:
    image_classifier = pipeline(
        task="image-classification",
        model="google/vit-base-patch16-224"
    )
except Exception as e:
    print(f"ERROR: No se pudo inicializar el Vision Transformer. Instale PyTorch o TensorFlow. Error: {e}")
    image_classifier = None 

def clasificar_objeto(imagen_mejorada):
    """Clasifica una imagen usando el Vision Transformer (ViT)."""
    if image_classifier is None or imagen_mejorada.size == 0:
        return "Clasificador_No_Disponible", 0.0, False
        
    try:
        # El modelo ViT espera una imagen RGB
        imagen_pil = Image.fromarray(imagen_mejorada.astype(np.uint8), 'L').convert('RGB')

        results = image_classifier(imagen_pil)
        
        if results and results[0]['score'] > 0.0:
            etiqueta = results[0]['label'].lower()
            probabilidad = results[0]['score']
            
            # Lógica para determinar si es una flor
            palabras_clave_flores = ['flower', 'daisy', 'rose', 'sunflower', 'plant']
            es_flor = any(palabra in etiqueta for palabra in palabras_clave_flores)
            
            return etiqueta, probabilidad, es_flor
        
        return "Clasificación_Inconclusa", 0.0, False

    except Exception as e:
        print(f"Error durante la clasificación: {e}")
        return "Error_VC", 0.0, False