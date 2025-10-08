from collections import deque
import time

def reconstruir_ruta(padres, inicio, meta):
    """
    Reconstruye la ruta óptima desde inicio hasta meta usando el diccionario de padres.
    
    Args:
        padres: Diccionario {nodo: nodo_padre}
        inicio: Tupla (fila, columna) del inicio
        meta: Tupla (fila, columna) de la meta
    
    Returns:
        Lista de tuplas representando la ruta [inicio, ..., meta]
    """
    if meta not in padres:
        return []
    
    ruta = []
    nodo_actual = meta
    
    while nodo_actual is not None:
        ruta.append(nodo_actual)
        nodo_actual = padres.get(nodo_actual)
    
    return ruta[::-1]  # Invertir para tener inicio -> meta


def validar_puntos(mundo, inicio, meta):
    """
    Valida que los puntos de inicio y meta sean válidos.
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if inicio is None or meta is None:
        return False, "Debe seleccionar inicio y meta"
    
    if inicio == meta:
        return False, "Inicio y meta no pueden ser el mismo punto"
    
    r_inicio, c_inicio = inicio
    r_meta, c_meta = meta
    
    # Validar que estén dentro del grid
    if not (0 <= r_inicio < mundo.N and 0 <= c_inicio < mundo.N):
        return False, "Punto de inicio fuera del grid"
    
    if not (0 <= r_meta < mundo.N and 0 <= c_meta < mundo.N):
        return False, "Punto de meta fuera del grid"
    
    # Validar que no sean obstáculos
    if mundo.grid[r_inicio][c_inicio].tipo == 'obstaculo':
        return False, "El inicio no puede ser un obstáculo"
    
    if mundo.grid[r_meta][c_meta].tipo == 'obstaculo':
        return False, "La meta no puede ser un obstáculo"
    
    return True, ""


def bfs_panal(mundo, inicio, meta):
    """
    Búsqueda en Amplitud (BFS) - Algoritmo SIN INFORMACIÓN.
    
    Características:
    - Explora nivel por nivel (como ondas en el agua)
    - Garantiza encontrar el camino más corto
    - Usa cola FIFO (First In, First Out)
    - NO atraviesa obstáculos
    
    Args:
        mundo: Objeto Mundo con el grid
        inicio: Tupla (fila, columna) del punto inicial
        meta: Tupla (fila, columna) del objetivo
    
    Returns:
        tuple: (ruta_optima, informacion_busqueda)
            - ruta_optima: Lista con el camino más corto [inicio, ..., meta]
            - informacion_busqueda: Diccionario con estadísticas de la búsqueda
    """
    print(f"\n{'='*70}")
    print(f"🔍 EJECUTANDO BFS (Breadth-First Search)")
    print(f"{'='*70}")
    print(f"📍 Inicio: {inicio}")
    print(f"🎯 Meta: {meta}")
    
    # Validar puntos
    es_valido, mensaje = validar_puntos(mundo, inicio, meta)
    if not es_valido:
        print(f"❌ ERROR: {mensaje}")
        return [], {
            'exito': False,
            'mensaje': mensaje,
            'nodos_explorados': 0,
            'tiempo_busqueda': 0.0,
            'longitud_ruta': 0
        }
    
    tiempo_inicio = time.time()
    
    # Estructuras de datos
    visitados = set()  # Set para O(1) en búsquedas
    cola = deque([inicio])  # Cola FIFO
    padres = {inicio: None}  # Diccionario para reconstruir ruta
    orden_exploracion = []  # Para visualización
    
    nodos_explorados = 0
    meta_encontrada = False
    
    print(f"\n🔄 Iniciando exploración BFS...")
    print(f"{'─'*70}")
    
    while cola:
        nodo_actual = cola.popleft()
        
        # Si ya visitamos este nodo, continuar
        if nodo_actual in visitados:
            continue
        
        # Marcar como visitado
        visitados.add(nodo_actual)
        orden_exploracion.append(nodo_actual)
        nodos_explorados += 1
        
        r_actual, c_actual = nodo_actual
        
        # Mostrar progreso cada 50 nodos
        if nodos_explorados % 50 == 0:
            print(f"   📊 Nodos explorados: {nodos_explorados} | En cola: {len(cola)}")
        
        # ¿Llegamos a la meta?
        if nodo_actual == meta:
            meta_encontrada = True
            tiempo_busqueda = time.time() - tiempo_inicio
            
            print(f"{'─'*70}")
            print(f"✅ ¡META ENCONTRADA!")
            print(f"   • Nodos explorados: {nodos_explorados}")
            print(f"   • Tiempo de búsqueda: {tiempo_busqueda:.4f}s")
            
            # Reconstruir ruta óptima
            ruta_optima = reconstruir_ruta(padres, inicio, meta)
            
            print(f"   • Longitud de ruta óptima: {len(ruta_optima)} pasos")
            print(f"   • Eficiencia: {(len(ruta_optima) / nodos_explorados * 100):.2f}%")
            print(f"{'='*70}\n")
            
            return ruta_optima, {
                'exito': True,
                'mensaje': 'Meta encontrada exitosamente',
                'nodos_explorados': nodos_explorados,
                'tiempo_busqueda': tiempo_busqueda,
                'longitud_ruta': len(ruta_optima),
                'orden_exploracion': orden_exploracion,
                'nodos_en_frontera': len(cola)
            }
        
        # Explorar vecinos (arriba, abajo, izquierda, derecha)
        celda_actual = mundo.grid[r_actual][c_actual]
        vecinos = mundo.obtener_vecinos_validos(celda_actual)
        
        for vecino in vecinos:
            # Solo agregar si no está visitado y no está en la cola
            if vecino not in visitados and vecino not in padres:
                padres[vecino] = nodo_actual
                cola.append(vecino)
    
    # No se encontró camino
    tiempo_busqueda = time.time() - tiempo_inicio
    
    print(f"{'─'*70}")
    print(f"❌ NO SE ENCONTRÓ CAMINO A LA META")
    print(f"   • Nodos explorados: {nodos_explorados}")
    print(f"   • Tiempo de búsqueda: {tiempo_busqueda:.4f}s")
    print(f"   • El objetivo está bloqueado o no existe camino válido")
    print(f"{'='*70}\n")
    
    return [], {
        'exito': False,
        'mensaje': 'No existe camino válido hacia la meta',
        'nodos_explorados': nodos_explorados,
        'tiempo_busqueda': tiempo_busqueda,
        'longitud_ruta': 0,
        'orden_exploracion': orden_exploracion,
        'nodos_en_frontera': 0
    }


def dfs_panal(mundo, inicio, meta):
    """
    Búsqueda en Profundidad (DFS) - Algoritmo SIN INFORMACIÓN.
    
    Características:
    - Explora en profundidad antes que en amplitud
    - NO garantiza el camino más corto
    - Usa pila LIFO (Last In, First Out)
    - NO atraviesa obstáculos
    - Puede explorar caminos muy largos antes de encontrar la meta
    
    Args:
        mundo: Objeto Mundo con el grid
        inicio: Tupla (fila, columna) del punto inicial
        meta: Tupla (fila, columna) del objetivo
    
    Returns:
        tuple: (ruta_encontrada, informacion_busqueda)
            - ruta_encontrada: Lista con un camino válido [inicio, ..., meta]
            - informacion_busqueda: Diccionario con estadísticas de la búsqueda
    """
    print(f"\n{'='*70}")
    print(f"🔍 EJECUTANDO DFS (Depth-First Search)")
    print(f"{'='*70}")
    print(f"📍 Inicio: {inicio}")
    print(f"🎯 Meta: {meta}")
    
    # Validar puntos
    es_valido, mensaje = validar_puntos(mundo, inicio, meta)
    if not es_valido:
        print(f"❌ ERROR: {mensaje}")
        return [], {
            'exito': False,
            'mensaje': mensaje,
            'nodos_explorados': 0,
            'tiempo_busqueda': 0.0,
            'longitud_ruta': 0
        }
    
    tiempo_inicio = time.time()
    
    # Estructuras de datos
    visitados = set()  # Set para O(1) en búsquedas
    pila = [inicio]  # Pila LIFO (usamos lista con append/pop)
    padres = {inicio: None}  # Diccionario para reconstruir ruta
    orden_exploracion = []  # Para visualización
    
    nodos_explorados = 0
    meta_encontrada = False
    
    print(f"\n🔄 Iniciando exploración DFS...")
    print(f"{'─'*70}")
    
    while pila:
        nodo_actual = pila.pop()  # LIFO: saca el último elemento
        
        # Si ya visitamos este nodo, continuar
        if nodo_actual in visitados:
            continue
        
        # Marcar como visitado
        visitados.add(nodo_actual)
        orden_exploracion.append(nodo_actual)
        nodos_explorados += 1
        
        r_actual, c_actual = nodo_actual
        
        # Mostrar progreso cada 50 nodos
        if nodos_explorados % 50 == 0:
            print(f"   📊 Nodos explorados: {nodos_explorados} | En pila: {len(pila)}")
        
        # ¿Llegamos a la meta?
        if nodo_actual == meta:
            meta_encontrada = True
            tiempo_busqueda = time.time() - tiempo_inicio
            
            print(f"{'─'*70}")
            print(f"✅ ¡META ENCONTRADA!")
            print(f"   • Nodos explorados: {nodos_explorados}")
            print(f"   • Tiempo de búsqueda: {tiempo_busqueda:.4f}s")
            
            # Reconstruir ruta encontrada
            ruta_encontrada = reconstruir_ruta(padres, inicio, meta)
            
            print(f"   • Longitud de ruta: {len(ruta_encontrada)} pasos")
            print(f"   • ⚠️  DFS NO garantiza el camino más corto")
            print(f"   • Eficiencia: {(len(ruta_encontrada) / nodos_explorados * 100):.2f}%")
            print(f"{'='*70}\n")
            
            return ruta_encontrada, {
                'exito': True,
                'mensaje': 'Meta encontrada exitosamente',
                'nodos_explorados': nodos_explorados,
                'tiempo_busqueda': tiempo_busqueda,
                'longitud_ruta': len(ruta_encontrada),
                'orden_exploracion': orden_exploracion,
                'nodos_en_frontera': len(pila)
            }
        
        # Explorar vecinos en orden INVERSO para mantener consistencia
        # (DFS explora en profundidad, el orden afecta qué rama explora primero)
        celda_actual = mundo.grid[r_actual][c_actual]
        vecinos = mundo.obtener_vecinos_validos(celda_actual)
        
        # Invertir para explorar en orden: arriba, derecha, abajo, izquierda
        for vecino in reversed(vecinos):
            if vecino not in visitados:
                if vecino not in padres:
                    padres[vecino] = nodo_actual
                pila.append(vecino)
    
    # No se encontró camino
    tiempo_busqueda = time.time() - tiempo_inicio
    
    print(f"{'─'*70}")
    print(f"❌ NO SE ENCONTRÓ CAMINO A LA META")
    print(f"   • Nodos explorados: {nodos_explorados}")
    print(f"   • Tiempo de búsqueda: {tiempo_busqueda:.4f}s")
    print(f"   • El objetivo está bloqueado o no existe camino válido")
    print(f"{'='*70}\n")
    
    return [], {
        'exito': False,
        'mensaje': 'No existe camino válido hacia la meta',
        'nodos_explorados': nodos_explorados,
        'tiempo_busqueda': tiempo_busqueda,
        'longitud_ruta': 0,
        'orden_exploracion': orden_exploracion,
        'nodos_en_frontera': 0
    }


def analizar_ruta_con_vision(ruta, mundo, sistema_vision, pantalla, tamano_celda, estadisticas):
    """
    Analiza SOLO las celdas de tipo 'flor' en la ruta con visión por computadora.
    
    Args:
        ruta: Lista de tuplas (fila, columna) de la ruta
        mundo: Objeto Mundo
        sistema_vision: Sistema de visión por computadora
        pantalla: Superficie de Pygame
        tamano_celda: Tamaño de cada celda en píxeles
        estadisticas: Objeto EstadisticasAlgoritmo
    """
    if not ruta:
        return
    
    # Contar flores en la ruta
    flores_en_ruta = sum(1 for r, c in ruta if mundo.grid[r][c].tipo == 'flor')
    
    print(f"\n{'='*70}")
    print(f"🔬 ANÁLISIS DE VISIÓN POR COMPUTADORA")
    print(f"{'='*70}")
    print(f"🌸 Flores encontradas en la ruta: {flores_en_ruta}")
    
    if flores_en_ruta == 0:
        print(f"   ℹ️  No hay flores en la ruta para analizar")
        print(f"{'='*70}\n")
        return
    
    print(f"\n🔍 Analizando cada flor con el modelo ViT...")
    print(f"{'─'*70}")
    
    flores_analizadas = 0
    
    for i, (r, c) in enumerate(ruta):
        celda = mundo.grid[r][c]
        
        # SOLO analizar celdas de tipo 'flor'
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
            
            # Mostrar resultado
            icono = "🌸" if resultado_vc['es_flor'] else "❌"
            print(f"   {icono} Celda ({r},{c}): {resultado_vc['etiqueta'][:20]} "
                  f"({resultado_vc['probabilidad']:.2%})")
            
            # Mostrar progreso
            if flores_analizadas % 5 == 0 or flores_analizadas == flores_en_ruta:
                print(f"   📊 Progreso: {flores_analizadas}/{flores_en_ruta} flores analizadas")
    
    print(f"{'─'*70}")
    print(f"✅ Análisis completado:")
    print(f"   • Flores confirmadas: {estadisticas.flores_detectadas_vision}")
    print(f"   • No reconocidas: {estadisticas.no_flores}")
    print(f"   • Precisión: {estadisticas.calcular_precision_deteccion():.1f}%")
    print(f"{'='*70}\n")


def ejecutar_busqueda_con_analisis(algoritmo, nombre, mundo, inicio, meta, 
                                   sistema_vision, pantalla, tamano_celda):
    """
    Ejecuta un algoritmo de búsqueda y analiza el resultado con visión por computadora.
    
    Flujo completo:
    1. Validar entrada
    2. Ejecutar algoritmo (BFS o DFS)
    3. Analizar flores en la ruta con VC
    4. Generar estadísticas completas
    
    Args:
        algoritmo: Función de búsqueda (bfs_panal o dfs_panal)
        nombre: Nombre del algoritmo ("BFS" o "DFS")
        mundo: Objeto Mundo
        inicio: Tupla (fila, columna) del inicio
        meta: Tupla (fila, columna) de la meta
        sistema_vision: Sistema de visión
        pantalla: Superficie de Pygame
        tamano_celda: Tamaño de celda
    
    Returns:
        tuple: (ruta, estadisticas)
    """
    from game.stats_system import EstadisticasAlgoritmo
    
    print(f"\n{'═'*70}")
    print(f"🚀 EJECUCIÓN COMPLETA: {nombre}")
    print(f"{'═'*70}")
    
    estadisticas = EstadisticasAlgoritmo(nombre)
    
    # PASO 1: Ejecutar algoritmo de búsqueda
    ruta, info_busqueda = algoritmo(mundo, inicio, meta)
    
    # Registrar información de búsqueda
    estadisticas.tiempo_ejecucion = info_busqueda['tiempo_busqueda']
    estadisticas.nodos_explorados = info_busqueda['nodos_explorados']
    estadisticas.exito = info_busqueda['exito']
    
    if not info_busqueda['exito']:
        estadisticas.longitud_ruta = 0
        estadisticas.ruta_completa = []
        print(f"\n⚠️  Búsqueda sin éxito: {info_busqueda['mensaje']}")
        return [], estadisticas
    
    # PASO 2: Analizar ruta con visión
    tiempo_inicio_vision = time.time()
    
    analizar_ruta_con_vision(
        ruta=ruta,
        mundo=mundo,
        sistema_vision=sistema_vision,
        pantalla=pantalla,
        tamano_celda=tamano_celda,
        estadisticas=estadisticas
    )
    
    estadisticas.tiempo_analisis_vision = time.time() - tiempo_inicio_vision
    
    # PASO 3: Completar estadísticas
    estadisticas.longitud_ruta = len(ruta)
    estadisticas.ruta_completa = ruta
    
    # PASO 4: Mostrar resumen final
    print(f"\n{'═'*70}")
    print(f"📊 RESUMEN FINAL - {nombre}")
    print(f"{'═'*70}")
    print(f"⏱️  Tiempos:")
    print(f"   • Búsqueda: {estadisticas.tiempo_ejecucion:.4f}s")
    print(f"   • Análisis VC: {estadisticas.tiempo_analisis_vision:.4f}s")
    print(f"   • Total: {estadisticas.tiempo_ejecucion + estadisticas.tiempo_analisis_vision:.4f}s")
    print(f"\n📏 Exploración:")
    print(f"   • Nodos explorados: {estadisticas.nodos_explorados}")
    print(f"   • Longitud de ruta: {estadisticas.longitud_ruta}")
    print(f"   • Ratio: {(estadisticas.longitud_ruta / estadisticas.nodos_explorados * 100):.2f}%")
    print(f"\n🌸 Flores:")
    print(f"   • Encontradas: {estadisticas.celdas_analizadas}")
    print(f"   • Confirmadas (VC): {estadisticas.flores_detectadas_vision}")
    print(f"   • No reconocidas: {estadisticas.no_flores}")
    print(f"\n🏆 Métricas:")
    print(f"   • SCORE: {estadisticas.calcular_score()}")
    print(f"   • Eficiencia: {estadisticas.calcular_eficiencia():.2f}%")
    print(f"   • Precisión VC: {estadisticas.calcular_precision_deteccion():.2f}%")
    print(f"{'═'*70}\n")
    
    return ruta, estadisticas