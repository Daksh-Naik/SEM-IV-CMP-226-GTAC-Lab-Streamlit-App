# # 12 February 2026
# # EXPERIMENT 03: SUBGRAPHS USING BUILT-IN NETWORKX FUNCTIONS
# import networkx as nx
# import matplotlib.pyplot as plt

# def create_complete_graph(num_nodes: int) -> nx.Graph:
#     """
#     Creates a complete graph explicitly using standard loops.
#     This mimics a standard C++/Java nested loop structure.
#     """
#     graph: nx.Graph = nx.Graph()
    
#     # Explicitly add nodes
#     for i in range(num_nodes):
#         graph.add_node(i)
        
#     # Explicitly add edges to connect every node to every other node
#     for i in range(num_nodes):
#         for j in range(i + 1, num_nodes):
#             graph.add_edge(i, j)
            
#     return graph

# def main() -> None:
#     # 1. Create the Original Graph
#     G: nx.Graph = create_complete_graph(8)

#     # Hardcoded positions for the 8 nodes (avoids complex trigonometry)
#     pos: dict[int, tuple[float, float]] = {
#         0: (0.382, 0.923),   # Top Right
#         1: (0.923, 0.382),   # Right Upper
#         2: (0.923, -0.382),  # Right Lower
#         3: (0.382, -0.923),  # Bottom Right
#         4: (-0.382, -0.923), # Bottom Left
#         5: (-0.923, -0.382), # Left Lower
#         6: (-0.923, 0.382),  # Left Upper
#         7: (-0.382, 0.923)   # Top Left
#     }

#     # ==========================================
#     # FINDING SUBGRAPHS USING NETWORKX FUNCTIONS
#     # ==========================================

#     # 2. Spanning Subgraph
#     # A spanning subgraph contains all vertices of the original graph.
#     # The minimum spanning tree function finds one such acyclic subgraph.
#     G_spanning: nx.Graph = nx.minimum_spanning_tree(G)

#     # 3. Vertex Induced Subgraph
#     # An induced subgraph consists of a subset of vertices and EVERY edge 
#     # from the original graph that connects those vertices.
#     nodes_to_keep: list[int] = [0, 1, 2, 4]
#     G_induced: nx.Graph = nx.induced_subgraph(G, nodes_to_keep)

#     # 4. Edge Deleted Subgraph
#     # Instead of the "shortcut" of copying the graph and manually popping edges,
#     # we use the formal Graph Theory operation: Graph Difference.
#     # We create a graph of the edges we want to remove, then subtract it.
#     G_edges_to_remove: nx.Graph = nx.Graph()
    
#     # The graph to subtract MUST have the same nodes as the original graph
#     for i in range(8):
#         G_edges_to_remove.add_node(i)
        
#     G_edges_to_remove.add_edge(0, 4)
#     G_edges_to_remove.add_edge(1, 5)
    
#     # nx.difference removes the edges of the second graph from the first graph
#     G_deleted: nx.Graph = nx.difference(G, G_edges_to_remove)

#     # ==========================================
#     # PLOTTING THE GRAPHS ON A SINGLE CANVAS
#     # ==========================================
    
#     # Create a 2x2 grid of subplots. 
#     # 'axes' acts like a 2D array: axes[row][column]
#     fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 12))
#     fig.suptitle("EXP 03: Subgraphs", fontsize=20, fontweight='bold')

#     # --- TOP ROW, LEFT COLUMN: Original Graph ---
#     ax_original = axes[0][0]
#     nx.draw_networkx_nodes(G, pos, ax=ax_original, node_color='lightgray', node_size=500, edgecolors='black')
#     nx.draw_networkx_labels(G, pos, ax=ax_original, font_size=12)
#     nx.draw_networkx_edges(G, pos, ax=ax_original, edge_color='black', width=2)
#     ax_original.set_title("Original Graph", fontsize=14, fontweight='bold')
#     ax_original.axis('off')

#     # --- TOP ROW, RIGHT COLUMN: Spanning Subgraph ---
#     ax_spanning = axes[0][1]
#     nx.draw_networkx_nodes(G_spanning, pos, ax=ax_spanning, node_color='white', node_size=500, edgecolors='green')
#     nx.draw_networkx_labels(G_spanning, pos, ax=ax_spanning, font_size=12)
#     nx.draw_networkx_edges(G_spanning, pos, ax=ax_spanning, edge_color='green', width=2)
#     ax_spanning.set_title("Spanning Subgraph\n(nx.minimum_spanning_tree)", fontsize=9, fontweight='bold')
#     ax_spanning.axis('off')

#     # --- BOTTOM ROW, LEFT COLUMN: Induced Subgraph ---
#     ax_induced = axes[1][0]
#     nx.draw_networkx_nodes(G_induced, pos, ax=ax_induced, node_color='white', node_size=500, edgecolors='red')
#     nx.draw_networkx_labels(G_induced, pos, ax=ax_induced, font_size=12)
#     nx.draw_networkx_edges(G_induced, pos, ax=ax_induced, edge_color='red', width=2)
#     ax_induced.set_title("Vertex Induced Subgraph\n(nx.induced_subgraph)", fontsize=9, fontweight='bold')
#     ax_induced.axis('off')

#     # --- BOTTOM ROW, RIGHT COLUMN: Edge Deleted Subgraph ---
#     ax_deleted = axes[1][1]
#     nx.draw_networkx_nodes(G_deleted, pos, ax=ax_deleted, node_color='white', node_size=500, edgecolors='orange')
#     nx.draw_networkx_labels(G_deleted, pos, ax=ax_deleted, font_size=12)
#     nx.draw_networkx_edges(G_deleted, pos, ax=ax_deleted, edge_color='orange', width=2)
#     ax_deleted.set_title("Edge Deleted Subgraph\n(nx.difference)", fontsize=9, fontweight='bold')
#     ax_deleted.axis('off')

#     # Adjust layout so titles do not overlap
#     plt.tight_layout()
#     plt.show()

# # Standard Python idiom to call the main function
# if __name__ == "__main__":
#     main()

# ---------------------------------------------------------------------------------------------------------------------------


# 12 February 2026
# EXPERIMENT 03: SUBGRAPHS USING BUILT-IN NETWORKX FUNCTIONS
import networkx as nx
import matplotlib.pyplot as plt

def create_original_graph() -> nx.Graph:
    """
    Creates a complete graph of 8 vertices using explicit loops.
    Returns the generated NetworkX Graph.
    """
    G: nx.Graph = nx.Graph()
    
    # Add nodes 0 through 7
    G.add_nodes_from(range(8))
    
    # Add edges to make it a complete graph
    # This nested loop is identical to how you would write it in C++ or Java
    for i in range(8):
        for j in range(i + 1, 8):
            G.add_edge(i, j)
            
    return G

def get_induced_subgraph_nodes() -> list[int]:
    """
    Takes user input to determine which vertices to keep for the induced subgraph.
    """
    nodes_to_keep: list[int] =[]
    
    print("--- Vertex Induced Subgraph ---")
    count_str: str = input("How many vertices do you want to keep? (e.g., 4): ")
    count: int = int(count_str)
    
    for i in range(count):
        vertex_str: str = input("Enter vertex number to keep (0 to 7): ")
        vertex: int = int(vertex_str)
        nodes_to_keep.append(vertex)
        
    return nodes_to_keep

def main() -> None:
    # 1. Create the original graph
    G: nx.Graph = create_original_graph()
    
    # Hardcoded positions to avoid complex math/trigonometry
    pos: dict[int, tuple[float, float]] = {
        0: (0.382, 0.923),   # Top Right
        1: (0.923, 0.382),   # Right Upper
        2: (0.923, -0.382),  # Right Lower
        3: (0.382, -0.923),  # Bottom Right
        4: (-0.382, -0.923), # Bottom Left
        5: (-0.923, -0.382), # Left Lower
        6: (-0.923, 0.382),  # Left Upper
        7: (-0.382, 0.923)   # Top Left
    }
    
    # 2. Get user inputs for subgraphs
    nodes_to_keep: list[int] = get_induced_subgraph_nodes()
    
    print("\n--- Edge Deleted Subgraph ---")
    a_str: str = input("Enter first vertex of edge to delete: ")
    a: int = int(a_str)
    
    b_str: str = input("Enter second vertex of edge to delete: ")
    b: int = int(b_str)
    
    # 3. Generate Subgraphs using built-in NetworkX functions
    
    # A. Spanning Subgraph (Minimum Spanning Tree)
    G_spanning: nx.Graph = nx.minimum_spanning_tree(G)
    
    # B. Vertex Induced Subgraph
    # G.subgraph() automatically creates a subgraph keeping only the specified nodes and their connecting edges
    G_induced: nx.Graph = G.subgraph(nodes_to_keep)
    
    # C. Edge Deleted Subgraph
    # We must copy the graph first so we don't modify the original graph 'G'
    G_deleted: nx.Graph = G.copy()
    if G_deleted.has_edge(a, b):
        G_deleted.remove_edge(a, b)
    else:
        print("Warning: The edge you entered does not exist in the graph.")

    # 4. Plotting in a single 2x2 canvas
    # fig represents the entire window, axes is a 2D array of the subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle("EXP 03: Subgraphs", fontsize=20, fontweight='bold')
    
    # ---------------------------------------------------------
    # Top-Left [0][0]: Original Graph
    # ---------------------------------------------------------
    ax_original = axes[0][0]
    nx.draw_networkx_nodes(G, pos, ax=ax_original, node_color='lightgray', node_size=500, edgecolors='black')
    nx.draw_networkx_labels(G, pos, ax=ax_original, font_size=12)
    nx.draw_networkx_edges(G, pos, ax=ax_original, edge_color='black', width=2)
    
    ax_original.set_title("Original Graph", fontsize=9)
    ax_original.axis('off')
    
    # ---------------------------------------------------------
    # Top-Right [0][1]: Spanning Subgraph
    # ---------------------------------------------------------
    ax_spanning = axes[0][1]
    nx.draw_networkx_nodes(G_spanning, pos, ax=ax_spanning, node_color='white', node_size=500, edgecolors='green')
    nx.draw_networkx_labels(G_spanning, pos, ax=ax_spanning, font_size=12)
    nx.draw_networkx_edges(G_spanning, pos, ax=ax_spanning, edge_color='green', width=2)
    
    ax_spanning.set_title("Spanning Subgraph\n(nx.minimum_spanning_tree)", fontsize=9)
    ax_spanning.axis('off')
    
    # ---------------------------------------------------------
    # Bottom-Left [1][0]: Vertex Induced Subgraph
    # ---------------------------------------------------------
    ax_induced = axes[1][0]
    nx.draw_networkx_nodes(G_induced, pos, ax=ax_induced, node_color='white', node_size=500, edgecolors='red')
    nx.draw_networkx_labels(G_induced, pos, ax=ax_induced, font_size=12)
    nx.draw_networkx_edges(G_induced, pos, ax=ax_induced, edge_color='red', width=2)
    
    ax_induced.set_title("Vertex Induced Subgraph\n(G.subgraph)", fontsize=9)
    ax_induced.axis('off')
    
    # ---------------------------------------------------------
    # Bottom-Right [1][1]: Edge Deleted Subgraph
    # ---------------------------------------------------------
    ax_deleted = axes[1][1]
    nx.draw_networkx_nodes(G_deleted, pos, ax=ax_deleted, node_color='white', node_size=500, edgecolors='orange')
    nx.draw_networkx_labels(G_deleted, pos, ax=ax_deleted, font_size=12)
    nx.draw_networkx_edges(G_deleted, pos, ax=ax_deleted, edge_color='orange', width=2)
    
    ax_deleted.set_title("Edge Deleted Subgraph\n(G.remove_edge)", fontsize=9)
    ax_deleted.axis('off')
    
    # Adjust layout so titles don't overlap, then display
    plt.tight_layout()
    plt.show()

# This is the standard Python way to call the main function, 
# similar to 'public static void main' in Java or 'int main()' in C++
if __name__ == "__main__":
    main()