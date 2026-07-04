import networkx as nx
import matplotlib.pyplot as plt

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

def custom_greedy_coloring(graph, nodes_order, colors_order):
    coloring = {}
    
    for node in nodes_order:
        neighbor_colors = set()
        for neighbor in graph.neighbors(node):
            if neighbor in coloring:
                neighbor_colors.add(coloring[neighbor])
        
        assigned_color = None
        for color in colors_order:
            if color not in neighbor_colors:
                assigned_color = color
                break
                
        if assigned_color is not None:
            coloring[node] = assigned_color
        else:
            raise ValueError(f"Not enough colors provided to color node {node}")
            
    return coloring

ordered_vertices = [1, 2, 3, 4, 5, 6, 7]
ordered_colors = ['blue', 'red', 'green', 'black', 'yellow']

coloring = custom_greedy_coloring(G, ordered_vertices, ordered_colors)

node_colors = [coloring[node] for node in G.nodes()]
num_colors = len(set(coloring.values()))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.canvas.manager.set_window_title('Canvas 1')
fig.suptitle("Graph: Original and Custom Greedy Coloured", fontsize=16, fontweight='bold')

nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightgray', edge_color='gray', node_size=800, font_size=14, font_weight='bold')
ax1.set_title("Original Graph", fontsize=14)

nx.draw(G, pos, ax=ax2, with_labels=True, node_color=node_colors, font_color='white',
        edge_color='gray', node_size=800, font_size=14, font_weight='bold')
ax2.set_title(f"Custom Greedy Coloring\n(Chromatic Number: {num_colors})", fontsize=14)

plt.tight_layout()
plt.show()