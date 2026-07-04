# Experiment 09: 30 April 2026
# custom implementation of Eulerian Check and fleury's algo

import networkx as nx
import matplotlib.pyplot as plt
import copy
import math
from collections import Counter

def get_adjacency_list(G):
    adj = {node: [] for node in G.nodes()}
    for u, v in G.edges():
        adj[u].append(v)
        adj[v].append(u)
    return adj

def check_eulerian(adj):
    # whether it has even deg?
    for node, neighbors in adj.items():
        if len(neighbors) % 2 != 0:
            return False, f"No Eulerian Circuit exists.\nVertex '{node}' has an odd degree ({len(neighbors)})."
    
    # does it have connectivity (but Ignore isolated vertices)?
    non_zero_degree_nodes = [n for n, neighbors in adj.items() if len(neighbors) > 0]
    if not non_zero_degree_nodes:
        return True, "Graph is empty but trivially Eulerian."
    
    start_node = non_zero_degree_nodes[0]
    visited = set()
    
    def dfs(v):
        visited.add(v)
        for neighbor in adj[v]:
            if neighbor not in visited:
                dfs(neighbor)
                
    dfs(start_node)
    
    for node in non_zero_degree_nodes:
        if node not in visited:
            return False, "No Eulerian Circuit exists.\nGraph is disconnected."
            
    return True, "Eulerian Circuit exists!"

def count_reachable(adj, u, visited):
    count = 1
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            count += count_reachable(adj, v, visited)
    return count

def is_valid_next_edge(adj, u, v):
    # Checks if edge (u, v) is a valid choice in Fleury's Algorithm (not a bridge unless necessary)
    if len(adj[u]) == 1:
        return True
        
    visited_before = set()
    count_before = count_reachable(adj, u, visited_before)
    
    adj[u].remove(v)
    adj[v].remove(u)
    
    visited_after = set()
    count_after = count_reachable(adj, u, visited_after)
    
    adj[u].append(v)
    adj[v].append(u)
    
    return count_before <= count_after

def fleury_algorithm(adj_original, start_node):
    # constructs an Eulerian circuit and records snapshots of the graph state at each step
    adj = copy.deepcopy(adj_original)
    circuit = [start_node]
    u = start_node
    
    # snapshot 0: Original state
    snapshots = [copy.deepcopy(adj)]
    
    total_edges = sum(len(neighbors) for neighbors in adj.values()) // 2
    
    while total_edges > 0:
        # sorted to ensure deterministic algorithm pathing
        for v in sorted(adj[u]):
            if is_valid_next_edge(adj, u, v):
                circuit.append(v)
                adj[u].remove(v)
                adj[v].remove(u)
                u = v
                total_edges -= 1
                
                # take snapshot of G of i
                snapshots.append(copy.deepcopy(adj))
                break 
                
    return circuit, snapshots

def draw_snapshot(ax, G_base, pos_dict, adj_snapshot, title):
    nx.draw_networkx_nodes(G_base, pos_dict, node_color='white', edgecolors='black', node_size=600, ax=ax)
    nx.draw_networkx_labels(G_base, pos_dict, font_color='black', font_size=10, font_family='sans-serif', ax=ax)

    # extract unique edges
    temp_adj = copy.deepcopy(adj_snapshot)
    edges = []
    for u in temp_adj:
        while temp_adj[u]:
            v = temp_adj[u].pop(0)
            temp_adj[v].remove(u)
            edges.append((u, v))

    # Count frequencies to handle the parallel edges cleanly
    edge_counts = Counter([tuple(sorted((u, v))) for u, v in edges])
    straight_edges = []
    curved_edges = []

    # map edges to their visual representation (straight vs curved)
    for edge, count in edge_counts.items():
        u, v = edge
        if edge == tuple(sorted(('E', 'D'))):
            if count == 2:
                straight_edges.append((u, v))
                curved_edges.append((('E', 'D'), 0.4))
            elif count == 1:
                straight_edges.append((u, v))
        elif edge == tuple(sorted(('A', 'E'))):
            if count == 2:
                straight_edges.append((u, v))
                curved_edges.append((('E', 'A'), -0.4))
            elif count == 1:
                straight_edges.append((u, v))
        else:
            straight_edges.append((u, v))

    # draw the specific remaining edges
    if straight_edges:
        nx.draw_networkx_edges(G_base, pos_dict, edgelist=straight_edges, edge_color='black', style='solid', width=2.0, ax=ax)
    for (u, v), rad in curved_edges:
        nx.draw_networkx_edges(G_base, pos_dict, edgelist=[(u, v)], connectionstyle=f'arc3, rad={rad}', edge_color='black', style='solid', width=2.0, ax=ax, arrows=True, arrowstyle='-')

    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(-1.5, 4)
    ax.axis('off')


fig1, (ax1, ax_res1) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1.2, 1]})
fig1.suptitle("EXPERIMENT 09", fontweight='bold', fontsize=16)

G1 = nx.MultiGraph()
G1.add_nodes_from(['A', 'B', 'E', 'D', 'C'])
pos1 = {'A': (0, 3), 'B': (2.5, 3), 'E': (0, 0), 'D': (2.5, 0), 'C': (4.5, 0)}

solid_edges1 = [('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D')]
G1.add_edges_from(solid_edges1)
G1.add_edge('E', 'D') 

nx.draw_networkx_nodes(G1, pos1, node_color='white', edgecolors='black', node_size=800, ax=ax1)
nx.draw_networkx_labels(G1, pos1, font_color='black', font_size=12, font_family='sans-serif', ax=ax1)
nx.draw_networkx_edges(G1, pos1, edgelist=solid_edges1, edge_color='black', style='solid', width=2.0, ax=ax1)
nx.draw_networkx_edges(G1, pos1, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', edge_color='black', style='solid', width=2.0, ax=ax1, arrows=True, arrowstyle='-')

edge_labels1 = {('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', ('E', 'D'): 'e4', ('D', 'C'): 'e5'}
nx.draw_networkx_edge_labels(G1, pos1, edge_labels=edge_labels1, font_color='black', font_size=12, ax=ax1)
ax1.text(1.25, -0.6, 'e6', fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')

ax1.set_title("Graph 1", fontweight='bold')
ax1.set_xlim(-1, 5.5)
ax1.set_ylim(-1.5, 4)
ax1.axis('off')

adj_G1 = get_adjacency_list(G1)
is_eulerian_G1, msg_G1 = check_eulerian(adj_G1)

res_text1 = f"Result\n\n{msg_G1}\n\n"
if is_eulerian_G1:
    circuit1, _ = fleury_algorithm(adj_G1, start_node='A')
    res_text1 += f"Circuit Path:\n{'  ->  '.join(circuit1)}"

ax_res1.text(0.5, 0.5, res_text1, fontsize=14, ha='center', va='center')
# bbox=dict(facecolor='#ffcccc' if not is_eulerian_G1 else '#ccffcc', alpha=0.5, boxstyle='round,pad=1')
ax_res1.set_title("Output", fontweight='bold')
ax_res1.axis('off')
fig1.tight_layout()


fig2, (ax2, ax_res2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1.2, 1]})
fig2.suptitle("EXPERIMENT 09", fontweight='bold', fontsize=16)

G2 = nx.MultiGraph()
G2.add_nodes_from(['A', 'B', 'E', 'D', 'C'])
pos2 = {'A': (0, 3), 'B': (2.5, 3), 'E': (0, 0), 'D': (2.5, 0), 'C': (4.5, 0)}

solid_edges2 = [('A', 'B'), ('A', 'E'), ('E', 'D'), ('D', 'C'), ('A', 'D'), ('B', 'C')]
G2.add_edges_from(solid_edges2)
G2.add_edge('E', 'D') 
G2.add_edge('E', 'A') 

nx.draw_networkx_nodes(G2, pos2, node_color='white', edgecolors='black', node_size=800, ax=ax2)
nx.draw_networkx_labels(G2, pos2, font_color='black', font_size=12, font_family='sans-serif', ax=ax2)
nx.draw_networkx_edges(G2, pos2, edgelist=solid_edges2, edge_color='black', style='solid', width=2.0, ax=ax2)
nx.draw_networkx_edges(G2, pos2, edgelist=[('E', 'D')], connectionstyle='arc3, rad=0.4', edge_color='black', style='solid', width=2.0, ax=ax2, arrows=True, arrowstyle='-')
nx.draw_networkx_edges(G2, pos2, edgelist=[('E', 'A')], connectionstyle='arc3, rad=-0.4', edge_color='black', style='solid', width=2.0, ax=ax2, arrows=True, arrowstyle='-')

edge_labels2 = {('A', 'B'): 'e1', ('A', 'E'): 'e2', ('A', 'D'): 'e3', ('E', 'D'): 'e4', ('D', 'C'): 'e5', ('B', 'C'): 'e8'}
nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2, font_color='black', font_size=12, ax=ax2)
ax2.text(1.25, -0.6, 'e6', fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')
ax2.text(-0.7, 1.5, 'e7', fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='none', pad=1.0), ha='center', va='center')

ax2.set_title("Graph 2", fontweight='bold')
ax2.set_xlim(-1.5, 5.5)
ax2.set_ylim(-1.5, 4)
ax2.axis('off')

adj_G2 = get_adjacency_list(G2)
is_eulerian_G2, msg_G2 = check_eulerian(adj_G2)

res_text2 = f"Result\n\n{msg_G2}\n\n"
if is_eulerian_G2:
    circuit2, snapshots2 = fleury_algorithm(adj_G2, start_node='A')
    res_text2 += f"Circuit Path:\n{'  ->  '.join(circuit2)}"

ax_res2.text(0.5, 0.5, res_text2, fontsize=14, ha='center', va='center')
ax_res2.set_title("Output", fontweight='bold')
ax_res2.axis('off')
fig2.tight_layout()


# step-by-stepp fleury (triggered only if eulerian)
if is_eulerian_G2:
    num_snapshots = len(snapshots2)
    cols = 3
    rows = math.ceil(num_snapshots / cols)

    fig3, axes3 = plt.subplots(rows, cols, figsize=(15, 4 * rows))
    fig3.suptitle("EXPERIMENT 09", fontweight='bold', fontsize=18)
    axes3 = axes3.flatten()

    for i, adj_snapshot in enumerate(snapshots2):
        ax = axes3[i]
        
        if i == 0:
            title = "G0: Original Graph"
        elif i == num_snapshots - 1:
            title = f"G{i}: Circuit Complete (Empty Graph)"
        else:
            prev_node = circuit2[i-1]
            curr_node = circuit2[i]
            title = f"G{i}: Traversed & Deleted ({prev_node} -> {curr_node})"
            
        draw_snapshot(ax, G2, pos2, adj_snapshot, title)

    for j in range(i + 1, len(axes3)):
        axes3[j].axis('off')
        
    circuit_str = "  ->  ".join(circuit2)
    fig3.text(0.5, 0.02, f"Final Eulerian Circuit: {circuit_str}", 
             ha='center', va='center', fontsize=16, fontweight='bold')
    # bbox=dict(facecolor='#e6f2ff', edgecolor='black', boxstyle='round,pad=0.5')

    fig3.tight_layout(rect=[0, 0.05, 1, 0.96])

plt.show()