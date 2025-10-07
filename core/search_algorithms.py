from collections import deque
import time

def reconstruir_ruta(padres, inicio, meta):
    """
    Sigue el diccionario de 'padres' hacia atrás desde la meta
    hasta el inicio para construir la ruta final.
    """
    ruta = []
    nodo_actual = meta
    while nodo_actual is not None:
        ruta.append(nodo_actual)
        nodo_actual = padres.get(nodo_actual)
    
    # La ruta está al revés (meta -> inicio), así que la invertimos
    return ruta[::-1]


def bfs_panal(mundo, inicio, meta):
    """
    Búsqueda en Amplitud (BFS) SIN INFORMACIÓN.
    Explora nodo por nodo hasta encontrar la meta.
    Retorna el CAMINO DE EXPLORACIÓN completo (no solo la ruta óptima).
    """
    tiempo_inicio = time.time()
    
    visitados = []  # Lista de nodos visitados EN ORDEN
    cola = deque([inicio])
    padres = {inicio: None}
    
    while cola:
        nodo_actual = cola.popleft()
        
        # Si ya lo visitamos, saltar
        if nodo_actual in visitados:
            continue
        
        # Marcar como visitado
        visitados.append(nodo_actual)
        r_actual, c_actual = nodo_actual
        
        # Si encontramos la meta, DETENERSE
        if nodo_actual == meta:
            print(f"✓ Meta encontrada en posición {len(visitados)} de la exploración")
            # Retornar el camino de exploración completo
            return visitados
        
        # Explorar vecinos
        celda_actual_obj = mundo.grid[r_actual][c_actual]
        for vecino in mundo.obtener_vecinos_validos(celda_actual_obj):
            if vecino not in visitados and vecino not in cola:
                padres[vecino] = nodo_actual
                cola.append(vecino)
    
    return visitados  # Si no encuentra meta, devuelve lo explorado


def dfs_panal(mundo, inicio, meta):
    """
    Búsqueda en Profundidad (DFS) SIN INFORMACIÓN.
    Explora en profundidad hasta encontrar la meta.
    Retorna el CAMINO DE EXPLORACIÓN completo (no solo la ruta óptima).
    """
    tiempo_inicio = time.time()
    
    visitados = []  # Lista de nodos visitados EN ORDEN
    pila = [inicio]
    padres = {inicio: None}
    
    while pila:
        nodo_actual = pila.pop()
        
        # Si ya lo visitamos, saltar
        if nodo_actual in visitados:
            continue
        
        # Marcar como visitado
        visitados.append(nodo_actual)
        r_actual, c_actual = nodo_actual
        
        # Si encontramos la meta, DETENERSE
        if nodo_actual == meta:
            print(f"✓ Meta encontrada en posición {len(visitados)} de la exploración")
            # Retornar el camino de exploración completo
            return visitados
        
        # Explorar vecinos (en orden inverso para mantener lógica DFS)
        celda_actual_obj = mundo.grid[r_actual][c_actual]
        vecinos = mundo.obtener_vecinos_validos(celda_actual_obj)
        
        for vecino in reversed(vecinos):
            if vecino not in visitados:
                if vecino not in padres:
                    padres[vecino] = nodo_actual
                pila.append(vecino)
    
    return visitados  # Si no encuentra meta, devuelve lo explorado


def analizar_ruta_con_vision(ruta, mundo, sistema_vision, pantalla, tamano_celda, estadisticas):
    """
    Analiza cada celda de la ruta encontrada con visión por computadora.
    SOLO analiza las celdas que tienen tipo 'flor' (con imágenes).
    """
    # Contar cuántas flores hay en la ruta
    flores_en_ruta = sum(1 for r, c in ruta if mundo.grid[r][c].tipo == 'flor')
    
    print(f"\n🔍 Analizando {flores_en_ruta} flores en el camino de exploración...")
    
    # Mostrar resumen de tipos de celdas en la ruta
    tipos_contador = {}
    for r, c in ruta:
        tipo = mundo.grid[r][c].tipo
        tipos_contador[tipo] = tipos_contador.get(tipo, 0) + 1
    
    print(f"\n📊 Composición del camino de exploración:")
    for tipo, cantidad in sorted(tipos_contador.items()):
        icono = {
            'vacio': '⬜',
            'flor': '🌸',
            'obstaculo': '🧱',
            'inicio': '🟢',
            'enjambre': '🔴'
        }.get(tipo, '❓')
        print(f"  {icono} {tipo.capitalize()}: {cantidad} celdas")
    
    print(f"\n🔬 Iniciando análisis de visión...\n")
    
    flores_analizadas = 0
    
    for i, (r, c) in enumerate(ruta):
        celda = mundo.grid[r][c]
        
        # SOLO analizar si la celda es de tipo 'flor'
        if celda.tipo == 'flor':
            flores_analizadas += 1
            
            # Analizar con visión por computadora
            resultado_vc = sistema_vision.analizar_celda_del_grid(
                mundo, r, c, pantalla, tamano_celda
            )
            
            # Registrar en estadísticas
            estadisticas.registrar_celda_analizada(
                posicion=(r, c),
                tipo_celda=celda.tipo,
                es_flor_segun_vision=resultado_vc['es_flor'],
                etiqueta=resultado_vc['etiqueta'],
                probabilidad=resultado_vc['probabilidad'],
                confianza=resultado_vc['confianza']
            )
            
            # Mostrar progreso
            if flores_analizadas % 3 == 0 or flores_analizadas == flores_en_ruta:
                print(f"  Progreso: {flores_analizadas}/{flores_en_ruta} flores analizadas")


def ejecutar_busqueda_con_analisis(algoritmo, nombre, mundo, inicio, meta, 
                                   sistema_vision, pantalla, tamano_celda):
    """
    Ejecuta un algoritmo de búsqueda SIN INFORMACIÓN y luego analiza el camino con visión.
    
    Flujo:
    1. Ejecutar algoritmo de búsqueda (BFS o DFS)
    2. Obtener el CAMINO DE EXPLORACIÓN (no solo ruta óptima)
    3. Analizar cada flor en el camino con visión por computadora
    4. Generar estadísticas
    """
    from game.stats_system import EstadisticasAlgoritmo
    
    print(f"\n{'='*60}")
    print(f"🚀 Ejecutando {nombre} (Búsqueda Sin Información)...")
    print(f"{'='*60}")
    
    estadisticas = EstadisticasAlgoritmo(nombre)
    
    # Paso 1: Ejecutar el algoritmo de búsqueda
    tiempo_inicio = time.time()
    
    if nombre == "BFS":
        camino_exploracion = bfs_panal(mundo, inicio, meta)
    elif nombre == "DFS":
        camino_exploracion = dfs_panal(mundo, inicio, meta)
    else:
        camino_exploracion = []
    
    tiempo_busqueda = time.time() - tiempo_inicio
    
    if not camino_exploracion:
        print(f"❌ No se encontró camino a la meta")
        estadisticas.exito = False
        estadisticas.tiempo_ejecucion = tiempo_busqueda
        return camino_exploracion, estadisticas
    
    print(f"✓ Exploración completada: {len(camino_exploracion)} nodos visitados")
    print(f"✓ Tiempo de búsqueda: {tiempo_busqueda:.4f}s")
    
    # Imprimir el camino de exploración completo
    print(f"\n📍 CAMINO DE EXPLORACIÓN (Coordenadas):")
    print("=" * 60)
    print("La abeja explorará en este orden hasta encontrar la meta:\n")
    
    # Imprimir en líneas de 10 coordenadas
    for i in range(0, len(camino_exploracion), 10):
        linea_coords = []
        for j in range(i, min(i + 10, len(camino_exploracion))):
            r, c = camino_exploracion[j]
            linea_coords.append(f"({r},{c})")
        print(f"  {' → '.join(linea_coords)}")
    
    print("=" * 60)
    print(f"Total: {len(camino_exploracion)} nodos explorados")
    print(f"Inicio: {camino_exploracion[0]} | Meta: {camino_exploracion[-1]}")
    
    # Paso 2: Analizar el camino con visión por computadora
    tiempo_inicio_analisis = time.time()
    
    analizar_ruta_con_vision(
        ruta=camino_exploracion,
        mundo=mundo,
        sistema_vision=sistema_vision,
        pantalla=pantalla,
        tamano_celda=tamano_celda,
        estadisticas=estadisticas
    )
    
    tiempo_analisis = time.time() - tiempo_inicio_analisis
    
    # Paso 3: Completar estadísticas
    estadisticas.tiempo_ejecucion = tiempo_busqueda
    estadisticas.tiempo_analisis_vision = tiempo_analisis
    estadisticas.longitud_ruta = len(camino_exploracion)
    estadisticas.ruta_completa = camino_exploracion
    estadisticas.exito = True
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DE ANÁLISIS:")
    print(f"  Tiempo total: {tiempo_busqueda + tiempo_analisis:.4f}s")
    print(f"  Nodos explorados: {len(camino_exploracion)}")
    print(f"  Flores analizadas: {estadisticas.celdas_analizadas}")
    print(f"  Flores confirmadas (VC): {estadisticas.flores_detectadas_vision}")
    print(f"  Imágenes no reconocidas: {estadisticas.no_flores}")
    print(f"  Score: {estadisticas.calcular_score()}")
    
    return camino_exploracion, estadisticas