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
        matrix = []
        for i in range(n):
            row = list(map(int, input(f"Row {i+1}: ").strip().split()))            
            if len(row) != n:
                print(f"Error: Expected {n} values in row {i+1}, got {len(row)}.")
                return None
            matrix.append(row)
        return np.array(matrix)
    except ValueError:
        print("Invalid input. Please enter integers only.")
        return None

def main():
    adj_matrix = get_adjacency_matrix()
    if adj_matrix is None:
        print("To invalid input.")
        return

    print("\nAdjacency Matrix:\n", adj_matrix)
    G = nx.from_numpy_array(adj_matrix)
    L = nx.line_graph(G)
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    pos_g = nx.spring_layout(G) 
    nx.draw(G, pos_g, with_labels=True, node_color='lightblue', 
            node_size=700, font_weight='bold', edge_color='gray')
    plt.title("Original Graph")

    plt.subplot(1, 2, 2)
    pos_l = nx.spring_layout(L)
    nx.draw(L, pos_l, with_labels=True, node_color='lightgreen', 
            node_size=700, font_weight='bold', edge_color='gray')
    plt.title("Line Graph")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()