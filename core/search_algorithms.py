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
    Búsqueda en Amplitud (BFS). Siempre encuentra la ruta más corta.
    Versión original sin análisis de visión (retrocompatibilidad).
    """
    tiempo_inicio = time.time()
    
    cola = deque([inicio])
    visitados = {inicio}
    padres = {inicio: None}
    
    while cola:
        r_actual, c_actual = cola.popleft()
        
        if (r_actual, c_actual) == meta:
            ruta = reconstruir_ruta(padres, inicio, meta)
            return ruta
        
        celda_actual_obj = mundo.grid[r_actual][c_actual]
        for vecino in mundo.obtener_vecinos_validos(celda_actual_obj):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = (r_actual, c_actual)
                cola.append(vecino)
    
    return []


def dfs_panal(mundo, inicio, meta):
    """
    Búsqueda en Profundidad (DFS). Usa una pila en lugar de una cola.
    Versión original sin análisis de visión (retrocompatibilidad).
    """
    tiempo_inicio = time.time()
    
    pila = [inicio]
    visitados = {inicio}
    padres = {inicio: None}
    
    while pila:
        r_actual, c_actual = pila.pop()
        
        if (r_actual, c_actual) == meta:
            ruta = reconstruir_ruta(padres, inicio, meta)
            return ruta
        
        celda_actual_obj = mundo.grid[r_actual][c_actual]
        for vecino in mundo.obtener_vecinos_validos(celda_actual_obj):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = (r_actual, c_actual)
                pila.append(vecino)
    
    return []


def analizar_ruta_con_vision(ruta, mundo, sistema_vision, pantalla, tamano_celda, estadisticas):
    """
    Analiza cada celda de la ruta encontrada con visión por computadora.
    SOLO analiza las celdas que tienen tipo 'flor' (con imágenes).
    """
    # Contar cuántas flores hay en la ruta
    flores_en_ruta = sum(1 for r, c in ruta if mundo.grid[r][c].tipo == 'flor')
    
    print(f"\n🔍 Analizando {flores_en_ruta} flores en la ruta con visión por computadora...")
    
    # Mostrar resumen de tipos de celdas en la ruta
    tipos_contador = {}
    for r, c in ruta:
        tipo = mundo.grid[r][c].tipo
        tipos_contador[tipo] = tipos_contador.get(tipo, 0) + 1
    
    print(f"\n📊 Composición de la ruta:")
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
    Ejecuta un algoritmo de búsqueda y luego analiza la ruta con visión.
    
    Flujo:
    1. Ejecutar algoritmo de búsqueda (BFS o DFS)
    2. Obtener la ruta
    3. Analizar cada celda de la ruta con visión por computadora
    4. Generar estadísticas
    """
    from game.stats_system import EstadisticasAlgoritmo
    
    print(f"\n{'='*60}")
    print(f"🚀 Ejecutando {nombre}...")
    print(f"{'='*60}")
    
    estadisticas = EstadisticasAlgoritmo(nombre)
    
    # Paso 1: Ejecutar el algoritmo de búsqueda
    tiempo_inicio = time.time()
    
    if nombre == "BFS":
        ruta = bfs_panal(mundo, inicio, meta)
    elif nombre == "DFS":
        ruta = dfs_panal(mundo, inicio, meta)
    else:
        ruta = []
    
    tiempo_busqueda = time.time() - tiempo_inicio
    
    if not ruta:
        print(f"❌ No se encontró ruta")
        estadisticas.exito = False
        estadisticas.tiempo_ejecucion = tiempo_busqueda
        return ruta, estadisticas
    
    print(f"✓ Ruta encontrada: {len(ruta)} pasos")
    print(f"✓ Tiempo de búsqueda: {tiempo_busqueda:.4f}s")
    
    # Imprimir la ruta completa
    print(f"\n📍 RUTA COMPLETA (Coordenadas):")
    print("=" * 60)
    
    # Imprimir en líneas de 10 coordenadas
    for i in range(0, len(ruta), 10):
        linea_coords = []
        for j in range(i, min(i + 10, len(ruta))):
            r, c = ruta[j]
            linea_coords.append(f"({r},{c})")
        print(f"  {' → '.join(linea_coords)}")
    
    print("=" * 60)
    print(f"Total: {len(ruta)} pasos desde {ruta[0]} hasta {ruta[-1]}")
    
    # Paso 2: Analizar la ruta con visión por computadora
    tiempo_inicio_analisis = time.time()
    
    analizar_ruta_con_vision(
        ruta=ruta,
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
    estadisticas.longitud_ruta = len(ruta)
    estadisticas.ruta_completa = ruta
    estadisticas.exito = True
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DE ANÁLISIS:")
    print(f"  Tiempo total: {tiempo_busqueda + tiempo_analisis:.4f}s")
    print(f"  Longitud de ruta: {len(ruta)} pasos")
    print(f"  Flores analizadas: {estadisticas.celdas_analizadas}")
    print(f"  Flores confirmadas (VC): {estadisticas.flores_detectadas_vision}")
    print(f"  Imágenes no reconocidas: {estadisticas.no_flores}")
    print(f"  Score: {estadisticas.calcular_score()}")
    
    return ruta, estadisticas