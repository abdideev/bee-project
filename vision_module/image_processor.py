# vision_module/image_processor.py

import cv2
import numpy as np

def ecualizacion_histograma(imagen_subexpuesta):
    """Aplica Ecualización del Histograma a una imagen en escala de grises."""
    if imagen_subexpuesta is None:
        return np.array([])
        
    if len(imagen_subexpuesta.shape) == 3:
        imagen_gris = cv2.cvtColor(imagen_subexpuesta, cv2.COLOR_BGR2GRAY) 
    else:
        imagen_gris = imagen_subexpuesta
        
    imagen_mejorada = cv2.equalizeHist(imagen_gris)
    
    return imagen_mejorada