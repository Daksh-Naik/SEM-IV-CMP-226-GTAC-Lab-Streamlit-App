# Experiment 08: 30 April 2026
# To implement gen of closed walks, trail and path in a connected graph.

import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.Graph()
G1.add_nodes_from(['A', 'B', 'E', 'D', 'C'])
pos1 = {'A': (0, 3), 'B': (2.5, 3), 'E': (0, 0), 'D': (2.5, 0), 'C': (4.5, 0)}
solid_edges1 = [('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D')]
G1.add_edges_from(solid_edges1)

# path for G1
path_nodes1 = nx.shortest_path(G1, source='B', target='C')
path_edges1 = list(nx.utils.pairwise(path_nodes1))

# trail for G1
trail_nodes1 = max(nx.all_simple_paths(G1, source='B', target='C'), key=len)
trail_edges1 = list(nx.utils.pairwise(trail_nodes1))

# closed Walk for G1
walk_edges1 = nx.find_cycle(G1, source='A')
walk_nodes1 = [u for u, v in walk_edges1] + [walk_edges1[-1][1]]

G2 = nx.Graph()
G2.add_nodes_from(['A', 'B', 'E', 'D', 'C'])
pos2 = {'A': (0, 3), 'B': (2.5, 3), 'E': (0, 0), 'D': (2.5, 0), 'C': (4.5, 0)}
solid_edges2 = [('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D'), ('B', 'C')]
G2.add_edges_from(solid_edges2)

# path for G2
path_nodes2 = nx.shortest_path(G2, source='A', target='C')
path_edges2 = list(nx.utils.pairwise(path_nodes2))

# trail for G2
trail_edges2 = list(nx.eulerian_path(G2, source='A'))
trail_nodes2 = [u for u, v in trail_edges2] + [trail_edges2[-1][1]]

# closed Walk
walk_edges2 = nx.find_cycle(G2, source='A')
walk_nodes2 = [u for u, v in walk_edges2] + [walk_edges2[-1][1]]

def draw_g1_quadrant(ax, highlight_edges=None, title="", sequence_nodes=None):
    nx.draw_networkx_nodes(G1, pos1, node_color='white', edgecolors='black', node_size=800, ax=ax)
    nx.draw_networkx_labels(G1, pos1, font_color='black', font_size=12, font_family='sans-serif', ax=ax)
    nx.draw_networkx_edges(G1, pos1, edgelist=solid_edges1, edge_color='gray', style='solid', width=2.0, ax=ax)
    
    nx.draw_networkx_edges(G1, pos1, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', edge_color='gray', style='solid', width=2.0, ax=ax, arrows=True, arrowstyle='-')
    
    edge_labels1 = {('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', ('E', 'D'): 'e4', ('D', 'C'): 'e5'}
    nx.draw_networkx_edge_labels(G1, pos1, edge_labels=edge_labels1, font_color='black', font_size=10, ax=ax)
    ax.text(1.25, -0.6, 'e6', fontsize=10, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')

    if highlight_edges:
        nx.draw_networkx_edges(G1, pos1, edgelist=highlight_edges, edge_color='red', width=3.0, ax=ax)
        nx.draw_networkx_nodes(G1, pos1, nodelist=sequence_nodes, node_color='lightcoral', edgecolors='black', node_size=800, ax=ax)

    ax.set_title(title, fontweight='bold')
    ax.set_xlim(-1, 5.5)
    ax.set_ylim(-1.5, 4.5)
    ax.axis('off')
    
    if sequence_nodes:
        seq_str = "Sequence: " + " -> ".join(sequence_nodes)
        ax.text(0.5, 0.02, seq_str, transform=ax.transAxes, ha='center', va='bottom', 
                fontsize=11, fontweight='bold', color='darkred', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.3'))


def draw_g2_quadrant(ax, highlight_edges=None, title="", sequence_nodes=None):
    nx.draw_networkx_nodes(G2, pos2, node_color='white', edgecolors='black', node_size=800, ax=ax)
    nx.draw_networkx_labels(G2, pos2, font_color='black', font_size=12, font_family='sans-serif', ax=ax)
    nx.draw_networkx_edges(G2, pos2, edgelist=solid_edges2, edge_color='gray', style='solid', width=2.0, ax=ax)
    
    nx.draw_networkx_edges(G2, pos2, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4',  edge_color='gray', style='solid', width=2.0, ax=ax, arrows=True, arrowstyle='-')
    nx.draw_networkx_edges(G2, pos2, edgelist=[('E', 'A')], connectionstyle='arc3, rad=-0.4',  edge_color='gray', style='solid', width=2.0, ax=ax, arrows=True, arrowstyle='-')
    
    edge_labels2 = {('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', ('E', 'D'): 'e4', ('D', 'C'): 'e5', ('B', 'C'): 'e8'}
    nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2, font_color='black', font_size=10, ax=ax)
    ax.text(1.25, -0.6, 'e6', fontsize=10, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')
    ax.text(-0.7, 1.5, 'e7', fontsize=10, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')

    if highlight_edges:
        nx.draw_networkx_edges(G2, pos2, edgelist=highlight_edges, edge_color='blue', width=3.0, ax=ax)
        nx.draw_networkx_nodes(G2, pos2, nodelist=sequence_nodes, node_color='lightblue', edgecolors='black', node_size=800, ax=ax)

    ax.set_title(title, fontweight='bold')
    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(-1.5, 4.5)
    ax.axis('off')
    
    if sequence_nodes:
        seq_str = "Sequence: " + " -> ".join(sequence_nodes)
        ax.text(0.5, 0.02, seq_str, transform=ax.transAxes, ha='center', va='bottom', fontsize=11, fontweight='bold', color='darkblue', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3'))


fig1, axs1 = plt.subplots(2, 2, figsize=(14, 10))
fig1.suptitle("Graph 1 Analysis: Walk, Trail, and Path", fontweight='bold', fontsize=16)

draw_g1_quadrant(axs1[0, 0], title="Original Graph 1")
draw_g1_quadrant(axs1[0, 1], highlight_edges=walk_edges1, sequence_nodes=walk_nodes1, title="Generated Closed Walk")
draw_g1_quadrant(axs1[1, 0], highlight_edges=trail_edges1, sequence_nodes=trail_nodes1, title="Generated Trail")
draw_g1_quadrant(axs1[1, 1], highlight_edges=path_edges1, sequence_nodes=path_nodes1, title="Generated Path")

plt.tight_layout()


fig2, axs2 = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle("Graph 2 Analysis: Walk, Trail, and Path", fontweight='bold', fontsize=16)

draw_g2_quadrant(axs2[0, 0], title="Original Graph 2")
draw_g2_quadrant(axs2[0, 1], highlight_edges=walk_edges2, sequence_nodes=walk_nodes2, title="Generated Closed Walk")
draw_g2_quadrant(axs2[1, 0], highlight_edges=trail_edges2, sequence_nodes=trail_nodes2, title="Generated Trail (Eulerian)")
draw_g2_quadrant(axs2[1, 1], highlight_edges=path_edges2, sequence_nodes=path_nodes2, title="Generated Path")

plt.tight_layout()

plt.show()