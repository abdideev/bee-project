"""
Módulo para validar la conectividad del grid y garantizar que existan caminos válidos.
"""

from collections import deque

def bfs_simple(mundo, inicio, meta):
    """
    BFS simplificado solo para verificar si existe un camino.
    Retorna True si existe camino, False si no.
    """
    if inicio == meta:
        return True
    
    visitados = set()
    cola = deque([inicio])
    
    while cola:
        nodo_actual = cola.popleft()
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        if nodo_actual == meta:
            return True
        
        r, c = nodo_actual
        celda = mundo.grid[r][c]
        vecinos = mundo.obtener_vecinos_validos(celda)
        
        for vecino in vecinos:
            if vecino not in visitados:
                cola.append(vecino)
    
    return False


def verificar_conectividad_grid(mundo):
    """
    Verifica que todas las celdas no-obstáculo estén conectadas.
    Útil para asegurar que el grid generado tenga sentido.
    
    Returns:
        tuple: (es_valido, mensaje, info)
    """
    # Encontrar la primera celda no-obstáculo como punto de partida
    punto_inicio = None
    celdas_validas = []
    
    for fila in mundo.grid:
        for celda in fila:
            if celda.tipo != 'obstaculo':
                celdas_validas.append((celda.r, celda.c))
                if punto_inicio is None:
                    punto_inicio = (celda.r, celda.c)
    
    if not celdas_validas:
        return False, "No hay celdas válidas (todas son obstáculos)", {}
    
    if len(celdas_validas) == 1:
        return True, "Solo hay una celda válida", {'celdas_validas': 1}
    
    # Ejecutar BFS desde el punto de inicio
    visitados = set()
    cola = deque([punto_inicio])
    
    while cola:
        nodo_actual = cola.popleft()
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        r, c = nodo_actual
        celda = mundo.grid[r][c]
        vecinos = mundo.obtener_vecinos_validos(celda)
        
        for vecino in vecinos:
            if vecino not in visitados:
                cola.append(vecino)
    
    # Verificar si todas las celdas válidas fueron alcanzadas
    celdas_alcanzables = len(visitados)
    total_celdas_validas = len(celdas_validas)
    
    es_conectado = celdas_alcanzables == total_celdas_validas
    
    info = {
        'celdas_validas': total_celdas_validas,
        'celdas_alcanzables': celdas_alcanzables,
        'porcentaje_conectado': (celdas_alcanzables / total_celdas_validas * 100) if total_celdas_validas > 0 else 0
    }
    
    if es_conectado:
        mensaje = f"Grid totalmente conectado ({total_celdas_validas} celdas accesibles)"
    else:
        mensaje = f"Grid desconectado: solo {celdas_alcanzables}/{total_celdas_validas} celdas alcanzables"
    
    return es_conectado, mensaje, info


def contar_componentes_conectadas(mundo):
    """
    Cuenta cuántas regiones desconectadas existen en el grid.
    Una región es un grupo de celdas conectadas entre sí.
    """
    visitados_global = set()
    componentes = []
    
    for fila in mundo.grid:
        for celda in fila:
            pos = (celda.r, celda.c)
            
            # Solo considerar celdas no-obstáculo
            if celda.tipo == 'obstaculo' or pos in visitados_global:
                continue
            
            # BFS para esta componente
            componente_actual = set()
            cola = deque([pos])
            
            while cola:
                nodo = cola.popleft()
                
                if nodo in componente_actual:
                    continue
                
                componente_actual.add(nodo)
                visitados_global.add(nodo)
                
                r, c = nodo
                celda_nodo = mundo.grid[r][c]
                vecinos = mundo.obtener_vecinos_validos(celda_nodo)
                
                for vecino in vecinos:
                    if vecino not in componente_actual:
                        cola.append(vecino)
            
            componentes.append(componente_actual)
    
    return componentes


def generar_reporte_grid(mundo):
    """
    Genera un reporte detallado sobre el estado del grid.
    """
    print("\n" + "="*70)
    print("📋 REPORTE DE GRID")
    print("="*70)
    
    # Contar tipos de celdas
    contador_tipos = {
        'vacio': 0,
        'obstaculo': 0,
        'flor': 0,
        'inicio': 0,
        'enjambre': 0
    }
    
    total_celdas = mundo.N * mundo.N
    
    for fila in mundo.grid:
        for celda in fila:
            tipo = celda.tipo
            contador_tipos[tipo] = contador_tipos.get(tipo, 0) + 1
    
    print(f"\n📊 Distribución de Celdas (Grid {mundo.N}x{mundo.N}):")
    print(f"  Total de celdas: {total_celdas}")
    print(f"  • Vacías: {contador_tipos['vacio']} ({contador_tipos['vacio']/total_celdas*100:.1f}%)")
    print(f"  • Obstáculos: {contador_tipos['obstaculo']} ({contador_tipos['obstaculo']/total_celdas*100:.1f}%)")
    print(f"  • Flores: {contador_tipos['flor']} ({contador_tipos['flor']/total_celdas*100:.1f}%)")
    print(f"  • Inicio: {contador_tipos['inicio']}")
    print(f"  • Meta/Enjambre: {contador_tipos['enjambre']}")
    
    # Verificar conectividad
    es_conectado, mensaje, info = verificar_conectividad_grid(mundo)
    
    print(f"\n🔗 Conectividad:")
    if es_conectado:
        print(f"  ✅ {mensaje}")
    else:
        print(f"  ⚠️  {mensaje}")
        print(f"     Porcentaje conectado: {info['porcentaje_conectado']:.1f}%")
    
    # Contar componentes
    componentes = contar_componentes_conectadas(mundo)
    
    print(f"\n🗺️  Componentes Conectadas:")
    print(f"  • Número de regiones: {len(componentes)}")
    
    if len(componentes) > 1:
        print(f"  • Tamaños de regiones:")
        for i, comp in enumerate(sorted(componentes, key=len, reverse=True)):
            print(f"    Región {i+1}: {len(comp)} celdas")
    
    # Verificar si inicio y meta están conectados
    inicio = None
    meta = None
    
    for fila in mundo.grid:
        for celda in fila:
            if celda.tipo == 'inicio':
                inicio = (celda.r, celda.c)
            elif celda.tipo == 'enjambre':
                meta = (celda.r, celda.c)
    
    if inicio and meta:
        existe_camino = bfs_simple(mundo, inicio, meta)
        print(f"\n🎯 Validación de Búsqueda:")
        if existe_camino:
            print(f"  ✅ Existe camino de inicio {inicio} a meta {meta}")
        else:
            print(f"  ❌ NO existe camino de inicio {inicio} a meta {meta}")
            print(f"     ¡Los algoritmos de búsqueda fallarán!")
    
    print("="*70 + "\n")
    
    return {
        'contador_tipos': contador_tipos,
        'es_conectado': es_conectado,
        'num_componentes': len(componentes),
        'existe_camino': existe_camino if (inicio and meta) else None
    }