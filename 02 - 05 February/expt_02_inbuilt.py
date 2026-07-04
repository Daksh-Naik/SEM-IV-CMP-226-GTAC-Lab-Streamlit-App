# 05 February 2026 - Experiment 02
# Using Inbuilt Functions to Verify if two Graphs are Isomorphic or not
# To Verify if two Graphs are Isomorphic or not
import networkx as nx
import matplotlib.pyplot as plt

def print_graph_properties(G, graph_name):
    print(f"{graph_name}")
    
    num_vertices = G.number_of_nodes()
    print(f"Number of Vertices : {num_vertices}")
    
    num_edges = G.number_of_edges()
    print(f"Number of Edges    : {num_edges}")
    
    adj_matrix = nx.to_numpy_array(G, nodelist=sorted(G.nodes()), dtype=int)
    print("Adjacency Matrix   :")
    print(adj_matrix)
    
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    print(f"Degree Sequence    : {degree_sequence}")
    
    cycles = nx.cycle_basis(G)
    cycle_lengths =[len(c) for c in cycles]
    print(f"Number of Cycles   : {len(cycles)}")
    print(f"Cycle Lengths      : {cycle_lengths}")
    print(f"Basic Cycles       : {cycles}\n")


def main():
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.title("Graph 1")

    G1 = nx.Graph()
    nodes_G1 =[1, 2, 3, 4, 5, 6]
    G1.add_nodes_from(nodes_G1)
    
    G1_edges =[
        (1, 6), (1, 5), (1, 3),  
        (6, 4),                  
        (2, 5), (2, 3),          
        (5, 3),                   
        (3, 4)                   
    ]
    G1.add_edges_from(G1_edges)

    pos1 = {
        6: (-2, 0),    
        1: (-1, 2),    
        5: (2, 2),     
        4: (0.5, -1.3),    
        2: (-1, -2),   
        3: (2, -2)     
    }

    nx.draw(G1, pos1, with_labels=True, node_color='lightgray', edgecolors='black', node_size=700, font_weight='bold')

    plt.subplot(1, 2, 2)
    plt.title("Graph 2")

    G2 = nx.Graph()
    nodes_G2 =[1, 2, 3, 4, 5, 6]
    G2.add_nodes_from(nodes_G2)

    G2_edges =[
        (1, 2), (1, 5), (1, 4),  
        (2, 6),                  
        (5, 4),                  
        (3, 6), (3, 4),          
        (6, 4)                   
    ]
    G2.add_edges_from(G2_edges)

    pos2 = {
        2: (-2, 1),     
        1: (0, 3),      
        5: (2, 1),      
        3: (-0.5, 0.7), 
        6: (-1.2, -0.8),
        4: (0, -3)      
    }

    nx.draw(G2, pos2, with_labels=True, node_color='lightgray', edgecolors='black', node_size=700, font_weight='bold')

    print_graph_properties(G1, "Graph 1")
    print_graph_properties(G2, "Graph 2")

    is_iso = nx.is_isomorphic(G1, G2)    
    if is_iso:
        print("Result: The graphs ARE isomorphic.")
        plt.suptitle("Graphs are ISOMORPHIC", fontsize=16, fontweight='bold', color='green')
    else:
        print("Result: The graphs ARE NOT isomorphic.")
        plt.suptitle("Graphs are NOT ISOMORPHIC", fontsize=16, fontweight='bold', color='red')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()