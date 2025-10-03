import os

# --- Configuración del Tablero ---
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 600
FPS = 60
TAMANO_N = 20
TAMANO_CELDA = ANCHO_PANTALLA // TAMANO_N # Divide el ancho para obtener el tamaño de cada celda

# --- Colores (RGB) ---
COLOR_NEGRO = (0, 0, 0)
COLOR_FONDO_CELDA = (0x0d1b2a)
COLOR_BORDE_CELDA = (0x01161e)
COLOR_FONDO = (30, 30, 30)
COLOR_OBSTACULO = (0x000814)
COLOR_INICIO = (0, 200, 0)
COLOR_META = (200, 0, 0)
COLOR_RUTA = (255, 255, 0) # Amarillo
COLOR_VISITADO = (50, 50, 150) # Azul oscuro

# --- Tipos de Celda ---
TIPO_VACIO = 'vacio'
TIPO_OBSTACULO = 'obstaculo'
TIPO_FLOR = 'flor'
TIPO_ENJAMBRE = 'enjambre'
TIPO_INICIO = 'inicio'


# --- Rutas de Sonidos (con los nombres correctos) ---
SOUND_FLOWER_FOUND = os.path.join('assets', 'sounds', 'point.mp3')
SOUND_BEE_STEP = os.path.join('assets', 'sounds', 'fly.mp3')