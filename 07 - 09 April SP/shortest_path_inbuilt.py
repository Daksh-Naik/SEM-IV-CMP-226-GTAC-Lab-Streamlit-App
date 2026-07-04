import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

def print_all_distances(distances: Dict[int, int], start_node: int) -> None:
    keys: List[int] = list(distances.keys())
    
    index: int = 0
    while index < len(keys):
        current_node: int = keys[index]
        current_distance: int = distances[current_node]
        
        print("Shortest distance from Node " + str(start_node) + " to Node " + str(current_node) + " is: " + str(current_distance))
        
        index = index + 1

def get_edges_from_path(path_nodes: List[int]) -> List[Tuple[int, int]]:
    # to converta a list of nodes into a list of edges (pairs of nodes).
    # for example so that a path [0, 2, 5] becomes [(0, 2), (2, 5)].
    # we need this because matplot colors edges, not just nodes.
    path_edges: List[Tuple[int, int]] =[]
    
    index: int = 0
    # stop at len - 1 because an edge requires a current node and a next node
    while index < len(path_nodes) - 1:
        node_u: int = path_nodes[index]
        node_v: int = path_nodes[index + 1]
        
        edge: Tuple[int, int] = (node_u, node_v)
        path_edges.append(edge)
        
        index = index + 1
        
    return path_edges

def main() -> None:
    G: nx.Graph = nx.Graph()

    edges: List[Tuple[int, int, int]] =[
        (0, 1, 3),
        (0, 2, 1),
        (0, 3, 6),
        (1, 2, 5),
        (1, 4, 3),
        (2, 3, 5),
        (2, 4, 6),
        (2, 5, 4),
        (3, 5, 2),
        (4, 5, 6)
    ]

    index: int = 0
    while index < len(edges):
        edge_tuple: Tuple[int, int, int] = edges[index]
        node_u: int = edge_tuple[0]
        node_v: int = edge_tuple[1]
        weight: int = edge_tuple[2]
        
        G.add_edge(node_u, node_v, weight=weight)
        index = index + 1

    pos: Dict[int, Tuple[float, float]] = {
        0: (0.0, 2.0),
        1: (-1.0, 1.0),
        2: (0.0, 0.0),
        3: (1.0, 1.0),
        4: (-1.0, -1.5),
        5: (1.0, -1.5)
    }

    start_node: int = 0
    target_node: int = 5

    all_distances: Dict[int, int] = nx.single_source_dijkstra_path_length(G, start_node, weight='weight')

    print("Shortest Distances from Node 0 to ALL Nodes: ")
    print_all_distances(all_distances, start_node)

    distance_to_target: int = all_distances[target_node]
    print("\nShortest distance from Node 0 to Node 5: ")
    print("The shortest distance from Node " + str(start_node) + " to Node " + str(target_node) + " is: " + str(distance_to_target))

    shortest_path_nodes: List[int] = nx.shortest_path(G, source=start_node, target=target_node, weight='weight')
    print("The sequence of nodes for the shortest path is: " + str(shortest_path_nodes))

    shortest_path_edges: List[Tuple[int, int]] = get_edges_from_path(shortest_path_nodes)

    plt.figure(figsize=(6, 8))

    nx.draw(G, pos, with_labels=True, node_color='white', edgecolors='black', node_size=1000, font_size=16, font_color='black', font_weight='bold', edge_color='black', width=2)

    edge_labels: Dict[Tuple[int, int], int] = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=14, font_color='black')

    nx.draw_networkx_edges(G, pos, edgelist=shortest_path_edges, edge_color='orange', width=4)

    plt.title("Dijkstra's Shortest Path (0 to 5)", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()