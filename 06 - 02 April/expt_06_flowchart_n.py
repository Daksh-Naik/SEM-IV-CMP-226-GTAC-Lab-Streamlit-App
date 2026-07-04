import networkx as nx
import matplotlib.pyplot as plt
from typing import Any

def get_edge_weight(edge: tuple[str, str, int]) -> int:
    # here to extract the weight from an edge tuple we use this instead of a Python 'lambda' function to sort the edges
    weight: int = edge[2]
    return weight

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
        u_node: str = edge[0]
        v_node: str = edge[1]
        w: int = edge[2]
        G.add_edge(u_node, v_node, weight=w)
        
    pos: dict[str, tuple[int, int]] = {
        'A': (0, 1), 'B': (1, 2), 'C': (3, 2),
        'D': (5, 2), 'E': (1, 0), 'F': (2, 1),
        'G': (3, 0), 'H': (5, 0), 'J': (6, 1)
    }

    fig, axes_array = plt.subplots(nrows=3, ncols=3, figsize=(9, 6))
    fig.suptitle("Finding MST of Graph - Experiment 06 (02/04/2026)", fontsize=12, fontweight='bold')        
    axes: list[Any] = axes_array.flatten()
        
    # FLOWCHART START: Set S = empty, i = 0, j = 0
    S: list[tuple[str, str]] =[]
    i: int = 0
    j: int = 0
    
    mst_graph: nx.Graph = nx.Graph()    
    # we must add all nodes to our tracking graph first. 
    # if nodes don't exist in the graph, nx.has_path() will crash.
    for node in G.nodes:
        mst_graph.add_node(node)

    # FLOWCHART (1): sort edges in order of increasing weight (a1, a2, till ae)
    a: list[tuple[str, str, int]] =[]
    for edge in edges:
        a.append(edge)
        
    a.sort(key=get_edge_weight)        
    v: int = len(G.nodes)
    
    mst_edge_labels: dict[tuple[str, str], int] = {}

    # FLOWCHART LOOP
    while True:
        # FLOWCHART (2): the decision whether |S| = i = v - 1?
        if len(S) == v - 1:
            # YES then STOP: G[S] = T*
            break
            
        # if graph is disconnected?
        if j >= len(a):
            break
            
        # if NO then move down to test the current edge a of j
        current_edge: tuple[str, str, int] = a[j]
        node_u: str = current_edge[0]
        node_v: str = current_edge[1]
        edge_weight: int = current_edge[2]
        
        # FLOWCHART (3): decision: G[S U {a of j}] is acyclic?
        
        # if there is ALREADY a path between node_u and node_v in our MST graph, adding this edge would create a closed loop (cycle).
        path_exists: bool = nx.has_path(mst_graph, node_u, node_v)
        
        if path_exists == False:
            # YES (It is acyclic, no loop created because no prior path exists)            
            # Add the edge to our tracking graph so future path checks know about it
            mst_graph.add_edge(node_u, node_v)
            
            # S U {e_i+1} is to S?
            S.append((node_u, node_v))
            mst_edge_labels[(node_u, node_v)] = edge_weight            
            
            ax = axes[i]
            ax.set_title(f"Step {i+1}: Added ({node_u}, {node_v}), MST Cost: {edge_weight}", fontweight='bold')            
            
            nx.draw_networkx_nodes(G, pos, node_color='white', edgecolors='black', node_size=350, ax=ax)
            nx.draw_networkx_labels(G, pos, font_color='black', font_size=7, font_family='sans-serif', ax=ax)            
            nx.draw_networkx_edges(G, pos, edge_color='black', style='dotted', width=1.0, ax=ax)            
            nx.draw_networkx_edges(G, pos, edgelist=S, edge_color='black', width=3.0, ax=ax)
            
            # gather all edge labels for the background graph
            all_edge_labels: dict[tuple[str, str], int] = {}
            for e in G.edges(data=True):
                u_bg: str = e[0]
                v_bg: str = e[1]
                w_bg: int = e[2]['weight']
                all_edge_labels[(u_bg, v_bg)] = w_bg
                
            nx.draw_networkx_edge_labels(G, pos, edge_labels=all_edge_labels, font_color='black', font_size=7, ax=ax)
            
            ax.axis('off')            
            
            i = i + 1       # i + 1 -> i
            j = j + 1       # j + 1 -> j
        else:
            # NO (Path already exists, so adding this edge creates a loop. Reject it.)            
            j = j + 1       # j + 1 -> j
    
    ax_final = axes[8]
    ax_final.set_title("Final Minimum Spanning Tree", fontweight='bold', fontsize=14)

    nx.draw_networkx_nodes(G, pos, node_color='white', edgecolors='black', node_size=400, ax=ax_final)
    nx.draw_networkx_labels(G, pos, font_color='black', font_size=12, font_family='sans-serif', ax=ax_final)
    
    nx.draw_networkx_edges(G, pos, edgelist=S, edge_color='black', width=3.0, ax=ax_final)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=mst_edge_labels, font_color='black', font_size=7, ax=ax_final)

    ax_final.axis('off')

    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    plt.show()

if __name__ == '__main__':
    main()