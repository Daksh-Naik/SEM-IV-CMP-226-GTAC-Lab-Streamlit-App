import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph()

G = nx.complete_graph(7)
G = nx.relabel_nodes(G, {i: i+1 for i in range(7)})

G.remove_edge(2, 7)
G.remove_edge(4, 6)

pos = {
    1: (0, 1),
    2: (-0.5, 0.7),
    3: (-0.7, 0),
    4: (-0.25, -0.7),
    5: (0.25, -0.7),
    6: (0.7, 0),
    7: (0.5, 0.7)
}

# def order_strategy(G, colors):
#     uncolored = [n for n in G.nodes() if n not in colors]
#     return sorted(uncolored)
coloring = nx.coloring.greedy_color(G, strategy='connected_sequential_bfs')
# coloring = nx.coloring.greedy_color(G, strategy=order_strategy)

color_list = ['blue', 'red', 'green', 'black', 'yellow']
node_colors = [color_list[coloring[node]] for node in G.nodes()]
num_colors = max(coloring.values()) + 1

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.canvas.manager.set_window_title('Canvas 1')
fig.suptitle("Graph: Original and Greedy Coloured", fontsize=16, fontweight='bold')

nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightgray', 
        edge_color='gray', node_size=800, font_size=14, font_weight='bold')
ax1.set_title("Original Graph", fontsize=14)

nx.draw(G, pos, ax=ax2, with_labels=True, node_color=node_colors, font_color='white',
        edge_color='gray', node_size=800, font_size=14, font_weight='bold')
ax2.set_title(f"Greedy Coloring\n(Chromatic Number: {num_colors})", fontsize=14)

plt.tight_layout()
plt.show()