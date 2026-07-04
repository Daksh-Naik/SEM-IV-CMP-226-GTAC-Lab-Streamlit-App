# 05 February 2026 - Experiment 02 - No Readymade NetworkX Funcs
# To Verify if two Graphs are Isomorphic or not
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class GraphIsoChecker:
    def __init__(self, name, edges, node_labels):
        self.name = name
        self.node_labels = node_labels
        self.num_nodes = len(node_labels)
        self.edges = edges
        self.adj_list = defaultdict(list)
        self.adj_matrix = [[0] * self.num_nodes for _ in range(self.num_nodes)]
        self._build_graph()

    def _build_graph(self):
        for u, v in self.edges:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            self.adj_matrix[u][v] = 1
            self.adj_matrix[v][u] = 1

    def get_degree_sequence(self):
        degrees = [len(self.adj_list[i]) for i in range(self.num_nodes)]
        return sorted(degrees, reverse=True)

    def get_num_edges(self):
        return len(self.edges)

    def find_cycles(self):
        def dfs_cycle_visit(u, visited_stack, path, cycles_found):
            visited_stack.add(u)
            path.append(u)

            for v in self.adj_list[u]:
                if len(path) >= 2 and v == path[-2]:
                    continue
                
                if v in visited_stack:
                    if v in path:
                        cycle_start_index = path.index(v)
                        raw_cycle = path[cycle_start_index:]
                        min_node = min(raw_cycle)
                        idx = raw_cycle.index(min_node)
                        rotated = raw_cycle[idx:] + raw_cycle[:idx]
                        if len(rotated) > 2:
                            if rotated[1] > rotated[-1]:
                                rotated = [rotated[0]] + rotated[1:][::-1]                                
                        cycles_found.add(tuple(rotated))
                else:
                    dfs_cycle_visit(v, visited_stack, path, cycles_found)
            
            path.pop()
            visited_stack.remove(u)

        all_unique_cycles = set()
        for i in range(self.num_nodes):
            dfs_cycle_visit(i, set(), [], all_unique_cycles)

        real_cycles = [c for c in all_unique_cycles if len(c) > 2]
        
        if not real_cycles:
             return 0, 0
             
        max_len = max(len(c) for c in real_cycles)
        return len(real_cycles), max_len

    def check_adjacency(self, u, v):
        return self.adj_matrix[u][v] == 1

def check_isomorphism(g1, g2):
    print(f"Isomorphism check: {g1.name} vs {g2.name}\n")
    
    print(f"1. Node Count Check:")
    if g1.num_nodes!= g2.num_nodes:
        print(f"   [FAIL] {g1.num_nodes}!= {g2.num_nodes}")
        return False
    print(f"   Both have {g1.num_nodes} nodes.")

    print(f"2. Edge Count Check:")
    e1, e2 = g1.get_num_edges(), g2.get_num_edges()
    if e1!= e2:
        print(f"   [FAIL] {e1}!= {e2}")
        return False
    print(f"   Both have {e1} edges.")

    print(f"3. Degree Sequence Check:")
    deg1 = g1.get_degree_sequence()
    deg2 = g2.get_degree_sequence()
    if deg1!= deg2:
        print(f"   [FAIL] Sequences do not match.")
        print(f"   {g1.name}: {deg1}")
        print(f"   {g2.name}: {deg2}")
        return False
    print(f"   Both have sequence: {deg1}")

    print(f"5. Cycle Analysis (DFS):")
    c1_count, c1_max = g1.find_cycles()
    c2_count, c2_max = g2.find_cycles()
    print(f"   {g1.name}: {c1_count} cycles found. Max Length: {c1_max}")
    print(f"   {g2.name}: {c2_count} cycles found. Max Length: {c2_max}")
    
    if c1_max!= c2_max:
        print(f"   Max cycle lengths differ! Isomorphism unlikely.")
    if c1_count!= c2_count:
        print(f"   Total cycle counts differ! Isomorphism unlikely.")

    print(f"4. Brute-Force Permutation Mapping:")
    nodes = range(g1.num_nodes)
    
    permutation_generator = itertools.permutations(nodes)
    valid_mapping = None
    
    for perm in permutation_generator:
        mapping_works = True        
        for i in range(g1.num_nodes):
            for j in range(g1.num_nodes):
                is_adj_g1 = g1.adj_matrix[i][j]                
                u_mapped = perm[i]
                v_mapped = perm[j]
                is_adj_g2 = g2.adj_matrix[u_mapped][v_mapped]
                
                if is_adj_g1!= is_adj_g2:
                    mapping_works = False
                    break 
            if not mapping_works:
                break
        
        if mapping_works:
            valid_mapping = perm
            break 
            
    if valid_mapping:
        print(f"   Isomorphism Found!")
        print(f"   Mapping ({g1.name} -> {g2.name}):")
        mapping_dict = {g1.node_labels[i]: g2.node_labels[valid_mapping[i]] for i in nodes}
        print(f"   {mapping_dict}")
        return True
    else:
        print(f"   [FAIL] Checked all permutations. No isomorphism exists.")
        return False

def main():
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.title("Graph 1")
    G1 = nx.Graph()
    nodes_G1 = [1, 2, 3, 4, 5, 6]
    G1.add_nodes_from(nodes_G1)
    G1_edges = [
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
    edges_G1_int = [(nodes_G1.index(u), nodes_G1.index(v)) for u, v in G1_edges]    
    plt.subplot(1, 2, 2)
    plt.title("Graph 2")

    G2 = nx.Graph()
    nodes_G2 = [1, 2, 3, 4, 5, 6]
    G2.add_nodes_from(nodes_G2)

    G2_edges = [
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
    edges_G2_int = [(nodes_G2.index(u), nodes_G2.index(v)) for u, v in G2_edges]
    checker_G1 = GraphIsoChecker("Graph 1", edges_G1_int, nodes_G1)
    checker_G2 = GraphIsoChecker("Graph 2", edges_G2_int, nodes_G2)
    are_isomorphic = check_isomorphism(checker_G1, checker_G2)
    plt.suptitle(f"Isomorphism Result: {'Isomorphic' if are_isomorphic else 'Not Isomorphic'}", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

