# Experiment 08: 30 April 2026
# To implement gen of closed walks, trail and path in a connected graph, no readymade networkx

import networkx as nx
import matplotlib.pyplot as plt


def manual_bfs_path(graph_dict, source, target):
    # finds a path (no repeated nodes) using bfs
    queue = [[source]]
    visited = {source}
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        
        if node == target:
            return path
            
        for neighbor in graph_dict[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return []

def manual_longest_trail(graph_dict, start):
    # find a trail (no repeated edges) using backtracking dfs
    best_trail = []
    
    def dfs(current, path, visited_edges):
        nonlocal best_trail
        if len(path) > len(best_trail):
            best_trail = list(path)
            
        for neighbor in graph_dict[current]:
            # use frozenset to treat (A,B) and (B,A) as the same undirected edge
            edge = frozenset([current, neighbor])
            if edge not in visited_edges:
                visited_edges.add(edge)
                path.append(neighbor)
                dfs(neighbor, path, visited_edges)
                path.pop()
                visited_edges.remove(edge)
                
    dfs(start, [start], set())
    return best_trail

def manual_closed_walk(graph_dict, start):
    # find a closed walk (cycle) starting and ending at the target node
    stack = [(start, [start])]
    
    while stack:
        curr, path = stack.pop()
        for neighbor in graph_dict[curr]:
            # if we hit the start node again and the path is valid (length > 2 to avoid A->B->A trivial walk)
            if neighbor == path[0] and len(path) > 2:
                return path + [neighbor]
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))
                
    # if no cycle is found (a trivial closed walk traversing one edge back and forth)
    neighbor = graph_dict[start][0]
    return [start, neighbor, start]

def nodes_to_edges(node_list):
    return [(node_list[i], node_list[i+1]) for i in range(len(node_list)-1)]


G1 = nx.Graph()
G1.add_nodes_from(['A', 'B', 'E', 'D', 'C'])
pos1 = {'A': (0, 3), 'B': (2.5, 3), 'E': (0, 0), 'D': (2.5, 0), 'C': (4.5, 0)}
solid_edges1 = [('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D')]
G1.add_edges_from(solid_edges1)

adj_G1 = {node: list(G1.neighbors(node)) for node in G1.nodes()}

path_nodes1 = manual_bfs_path(adj_G1, source='B', target='C')
path_edges1 = nodes_to_edges(path_nodes1)

trail_nodes1 = manual_longest_trail(adj_G1, start='B')
trail_edges1 = nodes_to_edges(trail_nodes1)

walk_nodes1 = manual_closed_walk(adj_G1, start='A')
walk_edges1 = nodes_to_edges(walk_nodes1)


G2 = nx.Graph()
G2.add_nodes_from(['A', 'B', 'E', 'D', 'C'])
pos2 = {'A': (0, 3), 'B': (2.5, 3), 'E': (0, 0), 'D': (2.5, 0), 'C': (4.5, 0)}
solid_edges2 = [('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D'), ('B', 'C')]
G2.add_edges_from(solid_edges2)

adj_G2 = {node: list(G2.neighbors(node)) for node in G2.nodes()}

path_nodes2 = manual_bfs_path(adj_G2, source='A', target='C')
path_edges2 = nodes_to_edges(path_nodes2)


trail_nodes2 = manual_longest_trail(adj_G2, start='A')
trail_edges2 = nodes_to_edges(trail_nodes2)


walk_nodes2 = manual_closed_walk(adj_G2, start='A')
walk_edges2 = nodes_to_edges(walk_nodes2)


def draw_g1_quadrant(ax, highlight_edges=None, title="", sequence_nodes=None):
    nx.draw_networkx_nodes(G1, pos1, node_color='white', edgecolors='black', node_size=800, ax=ax)
    nx.draw_networkx_labels(G1, pos1, font_color='black', font_size=12, font_family='sans-serif', ax=ax)
    nx.draw_networkx_edges(G1, pos1, edgelist=solid_edges1, edge_color='black', style='solid', width=2.0, ax=ax)
    
    nx.draw_networkx_edges(G1, pos1, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', edge_color='black', style='solid', width=2.0, ax=ax, arrows=True, arrowstyle='-')
    
    edge_labels1 = {('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', ('E', 'D'): 'e4', ('D', 'C'): 'e5'}
    nx.draw_networkx_edge_labels(G1, pos1, edge_labels=edge_labels1, font_color='black', font_size=10, ax=ax)
    ax.text(1.25, -0.6, 'e6', fontsize=10, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')

    if highlight_edges:
        normalized_highlights = []
        for u, v in highlight_edges:
            if (u, v) in G1.edges():
                normalized_highlights.append((u, v))
            elif (v, u) in G1.edges():
                normalized_highlights.append((v, u))
                
        nx.draw_networkx_edges(G1, pos1, edgelist=normalized_highlights, edge_color='red', width=4.0, ax=ax)
        nx.draw_networkx_nodes(G1, pos1, nodelist=sequence_nodes, node_color='lightcoral', edgecolors='black', node_size=800, ax=ax)

    ax.set_title(title, fontweight='bold')
    ax.set_xlim(-1, 5.5)
    ax.set_ylim(-1.5, 4.5)
    ax.axis('off')
    
    if sequence_nodes:
        seq_str = "Sequence: " + " -> ".join(sequence_nodes)
        ax.text(0.5, 0.02, seq_str, transform=ax.transAxes, ha='center', va='bottom', fontsize=11, fontweight='bold', color='darkred', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.3'))


def draw_g2_quadrant(ax, highlight_edges=None, title="", sequence_nodes=None):
    nx.draw_networkx_nodes(G2, pos2, node_color='white', edgecolors='black', node_size=800, ax=ax)
    nx.draw_networkx_labels(G2, pos2, font_color='black', font_size=12, font_family='sans-serif', ax=ax)
    nx.draw_networkx_edges(G2, pos2, edgelist=solid_edges2, edge_color='black', style='solid', width=2.0, ax=ax)
    
    nx.draw_networkx_edges(G2, pos2, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', edge_color='black', style='solid', width=2.0, ax=ax, arrows=True, arrowstyle='-')
    
    nx.draw_networkx_edges(G2, pos2, edgelist=[('E', 'A')], connectionstyle='arc3, rad=-0.4', edge_color='black', style='solid', width=2.0, ax=ax, arrows=True, arrowstyle='-')
    
    edge_labels2 = {('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', ('E', 'D'): 'e4', ('D', 'C'): 'e5', ('B', 'C'): 'e8'}
    nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2, font_color='black', font_size=10, ax=ax)
    ax.text(1.25, -0.6, 'e6', fontsize=10, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')
    ax.text(-0.7, 1.5, 'e7', fontsize=10, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')

    if highlight_edges:
        normalized_highlights = []
        for u, v in highlight_edges:
            if (u, v) in G2.edges():
                normalized_highlights.append((u, v))
            elif (v, u) in G2.edges():
                normalized_highlights.append((v, u))
                
        nx.draw_networkx_edges(G2, pos2, edgelist=normalized_highlights, edge_color='blue', width=4.0, ax=ax)
        nx.draw_networkx_nodes(G2, pos2, nodelist=sequence_nodes, node_color='lightblue', edgecolors='black', node_size=800, ax=ax)

    ax.set_title(title, fontweight='bold')
    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(-1.5, 4.5)
    ax.axis('off')
    
    if sequence_nodes:
        seq_str = "Sequence: " + " -> ".join(sequence_nodes)
        ax.text(0.5, 0.02, seq_str, transform=ax.transAxes, ha='center', va='bottom', fontsize=11, fontweight='bold', color='darkblue', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3'))

fig1, axs1 = plt.subplots(2, 2, figsize=(14, 10))
fig1.suptitle("Graph 1 Analysis: Walk, Trail, and Path (Manual Algo)", fontweight='bold', fontsize=16)

draw_g1_quadrant(axs1[0, 0], title="Original Graph 1")
draw_g1_quadrant(axs1[0, 1], highlight_edges=walk_edges1, sequence_nodes=walk_nodes1, title="Generated Closed Walk")
draw_g1_quadrant(axs1[1, 0], highlight_edges=trail_edges1, sequence_nodes=trail_nodes1, title="Generated Trail")
draw_g1_quadrant(axs1[1, 1], highlight_edges=path_edges1, sequence_nodes=path_nodes1, title="Generated Path")

plt.tight_layout()


fig2, axs2 = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle("Graph 2 Analysis: Walk, Trail, and Path (Manual Algo)", fontweight='bold', fontsize=16)

draw_g2_quadrant(axs2[0, 0], title="Original Graph 2")
draw_g2_quadrant(axs2[0, 1], highlight_edges=walk_edges2, sequence_nodes=walk_nodes2, title="Generated Closed Walk")
draw_g2_quadrant(axs2[1, 0], highlight_edges=trail_edges2, sequence_nodes=trail_nodes2, title="Generated Trail")
draw_g2_quadrant(axs2[1, 1], highlight_edges=path_edges2, sequence_nodes=path_nodes2, title="Generated Path")

plt.tight_layout()

plt.show()