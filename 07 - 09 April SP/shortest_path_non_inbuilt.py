import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any

def format_distance(dist: float) -> str:
    if dist == float('inf'):
        return "∞"
    else:
        return str(int(dist))

def format_set(s_list: List[int]) -> str:
    # Helper function to format a list of nodes into a set notation string. so that [0, 2, 1] becomes "{0, 2, 1}"
    result: str = "{"
    index: int = 0
    while index < len(s_list):
        result = result + str(s_list[index])
        if index < len(s_list) - 1:
            result = result + ", "
        index = index + 1
    result = result + "}"
    return result

def main() -> None:
    G: nx.Graph = nx.Graph()

    edges: List[Tuple[int, int, int]] =[
        (0, 1, 3), (0, 2, 1), (0, 3, 6), (1, 2, 5), (1, 4, 3),
        (2, 3, 5), (2, 4, 6), (2, 5, 4), (3, 5, 2), (4, 5, 6)
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
        0: (0.0, 2.0), 1: (-1.0, 1.0), 2: (0.0, 0.0),
        3: (1.0, 1.0), 4: (-1.0, -1.5), 5: (1.0, -1.5)
    }
    
    # FLOWCHART START BOX:
    # L(u of 0) = 0
    # L(v) = infinity, for all v != (u of 0)
    # S = {u of 0}
    # i = 0
    
    start_node: int = 0
    
    # L represents the shortest distance from start_node to each node
    L: Dict[int, float] = {
        0: float('inf'), 1: float('inf'), 2: float('inf'),
        3: float('inf'), 4: float('inf'), 5: float('inf')
    }
    L[start_node] = 0.0
    
    S: List[int] = [start_node]
    
    # S_bar represents S complement (nodes not yet visited)
    S_bar: List[int] =[1, 2, 3, 4, 5]
    
    i: int = 0
    u_i: int = start_node
    
    # We need to keep track of the edges we use to form the shortest paths so we can color them orange later. parent[v] = u means we reached v from u.
    parent: Dict[int, int] = {}
    
    table_data: List[List[str]] =[]

    # FLOWCHART CONDITION (1): S negbar == empty?
    while len(S_bar) > 0:
        
        # FLOWCHART STEP (2):
        # min { L(v), L(u of i) + w(u of i, v) } -> L(v) for all v in S negbar
        s_bar_index: int = 0
        while s_bar_index < len(S_bar):
            v: int = S_bar[s_bar_index]
            
            # check if there is an edge between u of i and v
            if G.has_edge(u_i, v):
                weight_uv: float = float(G[u_i][v]['weight'])
                new_distance: float = L[u_i] + weight_uv
                
                # if the new path is shorter, update L(v) and record the edge
                if new_distance < L[v]:
                    L[v] = new_distance
                    parent[v] = u_i
                    
            s_bar_index = s_bar_index + 1

        # FLOWCHART STEP (3):
        # Compute min { L(v) } for all v in S_bar to find u of {i+1}
        min_distance: float = float('inf')
        u_next: int = -1
        
        s_bar_index = 0
        while s_bar_index < len(S_bar):
            v: int = S_bar[s_bar_index]
            if L[v] < min_distance:
                min_distance = L[v]
                u_next = v
            s_bar_index = s_bar_index + 1
            
        row: List[str] =[
            str(i),
            str(u_i),
            format_set(S),
            format_distance(L[0]),
            format_distance(L[1]),
            format_distance(L[2]),
            format_distance(L[3]),
            format_distance(L[4]),
            format_distance(L[5]),
            str(u_next)
        ]
        table_data.append(row)

        # fLOWCHART UPDATE BOX:
        # S union {u of {i+1}} -> S
        # i + 1 -> i
        S.append(u_next)
        
        # remove u_next from S_bar
        S_bar.remove(u_next)
        
        u_i = u_next
        i = i + 1

    # fLOWCHART stop:
    # L(v) = d(u of 0, v) for all v in V.

    visited_edges: List[Tuple[int, int]] = []
    visited_nodes: List[int] = list(parent.keys())
    
    node_idx: int = 0
    while node_idx < len(visited_nodes):
        child_node: int = visited_nodes[node_idx]
        parent_node: int = parent[child_node]
        
        edge: Tuple[int, int] = (parent_node, child_node)
        visited_edges.append(edge)
        
        node_idx = node_idx + 1

    plt.figure(figsize=(6, 8))
    
    nx.draw(G, pos, with_labels=True, node_color='white', edgecolors='black', node_size=1000, font_size=16, font_color='black', font_weight='bold',  edge_color='black', width=2)
    
    edge_labels: Dict[Tuple[int, int], int] = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=14, font_color='black')
    
    nx.draw_networkx_edges(G, pos, edgelist=visited_edges, edge_color='orange', width=4)
    
    plt.title("Dijkstra's Shortest Path Tree (From Node 0)", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('off')
    
    columns: List[str] =[
        "Iteration (i)", "Selected Node (u_i)", "Set S", 
        "L(0)", "L(1)", "L(2)", "L(3)", "L(4)", "L(5)", 
        "Next Node (u_{i+1})"
    ]
    
    table: Any = ax.table(cellText=table_data, colLabels=columns, loc='center', cellLoc='center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.8)
    
    plt.title("Dijkstra's Algorithm Execution Trace", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    plt.show()

if __name__ == '__main__':
    main()