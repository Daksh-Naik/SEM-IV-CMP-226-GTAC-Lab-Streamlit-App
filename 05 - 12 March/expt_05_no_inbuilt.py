import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def get_adjacency_matrix():
    try:
        n = int(input("Enter the number of vertices in the original graph: "))
        if n <= 0:
            print("Number of vertices must be greater than 0.")
            return None
            
        print(f"Enter the {n}x{n} adjacency matrix row by row (space-separated values):")
        matrix =[]
        for i in range(n):
            row = list(map(int, input(f"Row {i+1}: ").strip().split()))
            if len(row) != n:
                print(f"Error: Expected {n} values, but got {len(row)}.")
                return None
            matrix.append(row)
            
        return np.array(matrix)
    except ValueError:
        print("Invalid input. Please enter integers only.")
        return None

def construct_line_graph(adj_matrix):
    n = len(adj_matrix)
    
    G = nx.Graph(adj_matrix)
    
    edges =[]
    for i in range(n):
        for j in range(i, n):
            if adj_matrix[i][j] != 0:
                edges.append((i, j))
                
    L_G = nx.Graph()
    
    L_G.add_nodes_from(edges)
    
    # for every pair of edges in G: If they share a common vertex, then they are adjacent in L(G).
    # for each pair of adjacent edges in G, add an edge between their corresponding vertices in L(G).
    num_edges = len(edges)
    for i in range(num_edges):
        for j in range(i + 1, num_edges):
            edge1 = edges[i]
            edge2 = edges[j]
            if (edge1[0] == edge2[0] or edge1[0] == edge2[1] or 
                edge1[1] == edge2[0] or edge1[1] == edge2[1]):
                L_G.add_edge(edge1, edge2)
                
    return G, L_G

def main():
    adj_matrix = get_adjacency_matrix()
    
    if adj_matrix is not None:
        G, L_G = construct_line_graph(adj_matrix)
        
        print("\nOriginal Graph Edges:", list(G.edges()))
        print("Line Graph Vertices (Edges of G):", list(L_G.nodes()))
        print("Line Graph Edges:", list(L_G.edges()))
        
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.title("Original Graph (G)")
        pos_G = nx.spring_layout(G)
        nx.draw(G, pos_G, with_labels=True, node_color='lightblue', 
                node_size=700, font_weight='bold', edge_color='gray')
        
        plt.subplot(1, 2, 2)
        plt.title("Line Graph L(G)")
        pos_L_G = nx.spring_layout(L_G)
        labels = {node: f"{node[0]}-{node[1]}" for node in L_G.nodes()}
        nx.draw(L_G, pos_L_G, labels=labels, with_labels=True, node_color='lightgreen', 
                node_size=1000, font_weight='bold', edge_color='black')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()