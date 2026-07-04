import networkx as nx
import matplotlib.pyplot as plt

user_input = input("Enter a degree sequence separated by spaces: ")

sequence = list(map(int, user_input.split()))
if nx.is_graphical(sequence):
    print("Graphical sequence")

    G = nx.havel_hakimi_graph(sequence)
    print("Edges:", list(G.edges()))
    plt.figure(figsize=(6,6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels = True, node_size = 800, font_size = 9, font_weight='bold' )
    plt.title("Graph from Degree Sequence", fontsize = 9)
    plt.tight_layout()
    plt.show()
else:
    print("Not a graphical sequence")