# Esempio di grafo iniziale. Ogni nodo rappresenta un router e i pesi sugli archi indicano i costi tra i nodi
graph = {
    'A': {'B': 2, 'C': 5},
    'B': {'A': 2, 'D': 8},
    'C': {'A': 5, 'D': 3, 'E': 7},
    'D': {'B': 8, 'C': 3, 'F': 2},
    'E': {'C': 7, 'F': 4, 'G': 6},
    'F': {'D': 2, 'E': 4, 'G': 1},
    'G': {'E': 6, 'F': 1}
}

# Inizializza le tabelle di routing per ogni nodo. 
# Ogni nodo inizialmente conosce solo la sua distanza (0) e la distanza dei suoi vicini diretti
def init_routing_tables(graph):
    routing_tables = {}
    for node in graph:
        routing_tables[node] = {neighbor: {'cost': float('inf'), 'path': []} for neighbor in graph}
        routing_tables[node][node] = {'cost': 0, 'path': [node]}  # Distanza da sé stesso è 0
        for neighbor, cost in graph[node].items():
            # Costo e percorso iniziale per ogni nodo verso ogni nodo vicino
            routing_tables[node][neighbor] = {'cost': cost, 'path': [node, neighbor]}
    return routing_tables

# Aggiorna la tabella di routing di un dato nodo in base alle tabelle dei suoi vicini.
# Ritorna True se la tabella è aggiornata, Falso altrimenti
def update_routing_table(node, graph, routing_tables):
    updated = False
    for neighbor in graph[node]:  # Itera sui vicini
        for dest, data in routing_tables[neighbor].items():
            new_cost = routing_tables[node][neighbor]['cost'] + data['cost']
            if new_cost < routing_tables[node][dest]['cost']:
                # Aggiorna costo e percorso
                routing_tables[node][dest]['cost'] = new_cost
                routing_tables[node][dest]['path'] = routing_tables[node][neighbor]['path'] + data['path'][1:]
                updated = True
    return updated

# Simula l'algoritmo (Bellman-Ford). 
# Stampa i risultati delle tabelle di ogni nodo (router) del grafo per ogni iterazione eseguita, fino a che la convergenza non venga raggiunta
def distance_vector_routing(graph, max_iterations=10):
    # Inizializza le tabelle di routing
    routing_tables = init_routing_tables(graph)
    print("\nRouting Tables iniziali:\n")
    print_routing_tables(routing_tables)

    # Esegue iterazioni per aggiornare le tabelle di routing
    for iteration in range(max_iterations):
        print(f"\nIterazione {iteration + 1}:")
        updates = 0
        for node in graph:
            if update_routing_table(node, graph, routing_tables):
                updates += 1
        print_routing_tables(routing_tables)

        if updates == 0:  # Una volta raggiunta la convergenza
            print("Convergenza raggiunta.")
            break
    else:
        print("ATTENZIONE: Numero massimo di iterazioni, convergenza non raggiunta.")

    return routing_tables

# Stampa le tabelle di routing per ogni nodo del grafo
def print_routing_tables(routing_tables):
    for node, table in routing_tables.items():
        print(f"Routing Table per il Nodo {node}:")
        for dest, data in table.items():
            cost_display = data['cost'] if data['cost'] != float('inf') else "∞"
            path_display = " -> ".join(data['path']) if data['path'] else "N/A"
            print(f"  To {dest}: Cost = {cost_display}, Path = {path_display}")
        print()

# Riga di codice che fa partire l'algoritmo
execute_program = distance_vector_routing(graph)
