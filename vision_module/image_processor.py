# vision_module/image_processor.py
import cv2
import numpy as np

def ecualizacion_histograma(imagen_cv):
    if imagen_cv is None: return np.array([])
    if len(imagen_cv.shape) == 3:
        imagen_gris = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2GRAY) 
    else:
        imagen_gris = imagen_cv
    return cv2.equalizeHist(imagen_gris)