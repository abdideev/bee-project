from collections import deque

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
    """Búsqueda en Amplitud (BFS). Siempre encuentra la ruta más corta."""
    
    # 1. Estructuras de datos
    # Una cola para gestionar los nodos a visitar (primero en entrar, primero en salir)
    cola = deque([inicio]) 
    # Un conjunto para no visitar el mismo nodo dos veces
    visitados = {inicio}
    # Un diccionario para reconstruir la ruta al final (hijo: padre)
    padres = {inicio: None}

    # 2. Bucle de búsqueda
    while cola:
        # Sacamos el nodo más antiguo de la cola
        r_actual, c_actual = cola.popleft()
        
        # Si llegamos a la meta, reconstruimos la ruta y terminamos
        if (r_actual, c_actual) == meta:
            return reconstruir_ruta(padres, inicio, meta)
        
        # 3. Exploración de vecinos
        # Pedimos al mundo los movimientos válidos desde nuestra posición actual
        celda_actual_obj = mundo.grid[r_actual][c_actual]
        for vecino in mundo.obtener_vecinos_validos(celda_actual_obj):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = (r_actual, c_actual)
                cola.append(vecino)
                
    return [] # Si la cola se vacía y no encontramos la meta, no hay ruta

def dfs_panal(mundo, inicio, meta):
    """Búsqueda en Profundidad (DFS). Usa una pila en lugar de una cola."""
    
    # 1. La única diferencia con BFS es que usamos una lista como PILA
    # (último en entrar, primero en salir)
    pila = [inicio]
    visitados = {inicio}
    padres = {inicio: None}

    # 2. Bucle de búsqueda
    while pila:
        # Sacamos el nodo más reciente de la pila
        r_actual, c_actual = pila.pop()
        
        if (r_actual, c_actual) == meta:
            return reconstruir_ruta(padres, inicio, meta)
        
        # 3. Exploración (idéntica a BFS)
        celda_actual_obj = mundo.grid[r_actual][c_actual]
        for vecino in mundo.obtener_vecinos_validos(celda_actual_obj):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = (r_actual, c_actual)
                pila.append(vecino)
    
    return []