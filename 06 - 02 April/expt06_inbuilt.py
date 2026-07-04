import networkx as nx
import matplotlib.pyplot as plt
from typing import Any

def find_and_display_mst(graph: nx.Graph, positions: dict[str, tuple[int, int]]) -> None:
    # function displays only the final result, without showing the step-by-step iteration
    
    # data=True ensures that the edge weights are included in the output.
    mst_edges_generator = nx.minimum_spanning_edges(graph, algorithm='kruskal', data=True)
    
    mst_edges: list[tuple[str, str]] =[]
    
    # create an empty dictionary to store the weights of the MST edges, to be used later to draw the labels on the graph
    mst_edge_labels: dict[tuple[str, str], int] = {}
    
    for edge_tuple in mst_edges_generator:        
        u: str = edge_tuple[0]
        v: str = edge_tuple[1]
        edge_data: dict[str, Any] = edge_tuple[2]
                
        mst_edges.append((u, v))
        
        weight: int = edge_data['weight']
        mst_edge_labels[(u, v)] = weight
        
    plt.figure(figsize=(8, 6))
    plt.title("Final Minimum Spanning Tree", fontweight='bold', fontsize=14)
    
    nx.draw_networkx_nodes(graph, positions, node_color='white', edgecolors='black', node_size=400)
    
    nx.draw_networkx_labels(graph, positions, font_color='black', font_size=12, font_family='sans-serif')
    
    nx.draw_networkx_edges(graph, positions, edgelist=mst_edges, edge_color='black', width=3.0)
    
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=mst_edge_labels, font_color='black', font_size=10)
    
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()


def main() -> None:
    G: nx.Graph = nx.Graph()
    
    edges: list[tuple[str, str, int]] =[
        ('A', 'B', 4), ('A', 'E', 8),
        ('B', 'C', 8), ('B', 'E', 11),
        ('C', 'D', 7), ('C', 'F', 2), ('C', 'H', 4),
        ('D', 'H', 14), ('D', 'J', 9),
        ('E', 'F', 7), ('E', 'G', 1),
        ('F', 'G', 6),
        ('G', 'H', 2),
        ('H', 'J', 10)
    ]
    
    for edge in edges:
        node_u: str = edge[0]
        node_v: str = edge[1]
        edge_weight: int = edge[2]
        G.add_edge(node_u, node_v, weight=edge_weight)
        
    pos: dict[str, tuple[int, int]] = {
        'A': (0, 1), 'B': (1, 2), 'C': (3, 2),
        'D': (5, 2), 'E': (1, 0), 'F': (2, 1),
        'G': (3, 0), 'H': (5, 0), 'J': (6, 1)
    }
    
    find_and_display_mst(G, pos)

if __name__ == '__main__':
    main()