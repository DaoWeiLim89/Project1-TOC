"""
Hamilton Cycle Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c INSTANCE 1
p edge 4 5
e 1 2
e 1 4
e 2 3
e 2 4
e 3 4

c INSTANCE 2
p edge 6 10
e 1 5
e 1 6
e 2 3
e 2 4
e 2 6
e 3 4
e 3 5
e 3 6
e 4 5
e 4 6

c INSTANCE 3
p edge 5 4
e 1 5
e 2 3
e 3 5
e 4 5


OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id, n_vertices, n_edges, k, method, colorable, time_seconds, coloring

EXAMPLE OUTPUT
--------------
Instance_ID,Num_Vertices,Num_Edges,Hamiltonian_Path,Hamiltonian_Cycle,Largest_Cycle_Size,Algorithm,Time
1,4,5,"[1, 2, 3, 4]","[1, 2, 3, 4, 1]",4,"BruteForce",0.000000
2,6,10,"[1, 5, 3, 2, 4, 6]","[1, 5, 3, 2, 4, 6, 1]",6,"BruteForce",0.000000
3,5,4,None,None,0,"BruteForce",0.000000

"""

import itertools
from typing import List, Tuple

from src.helpers.hamilton_cycle_helper import HamiltonCycleAbstractClass


class HamiltonCycleColoring(HamiltonCycleAbstractClass):
    """
    NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
    For this you dont need to save anything just make sure to return exact related output.

    For ease look at the Abstract Solver class and basically we are having the run method which does the saving
    of the CSV file just focus on the logic
    """


    def hamilton_backtracking(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:        
        # return (path_exists, path, cycle_exists, cycle, largest)
        Num_Vertices = len(vertices)
        Hamiltonian_Path = []
        Hamiltonian_Cycle = []
        Largest_Cycle_Size = 0

        def recurse(visited: List, cur_node):
            nonlocal Hamiltonian_Path, Hamiltonian_Cycle, Largest_Cycle_Size
            # Need at least 3 vertices for a valid cycle
            if len(visited) >= 3:
                if check_for_cycle(cur_node, visited[0]):
                    Largest_Cycle_Size = max(Largest_Cycle_Size, len(visited))
                
            # base case
            if Num_Vertices == len(visited):
                Hamiltonian_Path = visited[:]
                if check_for_cycle(cur_node, visited[0]):
                    Hamiltonian_Cycle = visited[:] + [visited[0]]
                    Largest_Cycle_Size = len(visited)
                return
                
            # Recurse
            for edge in edges:
                neighbor = None
                if edge[1] == cur_node and edge[0] not in visited:
                    neighbor = edge[0]
                elif edge[0] == cur_node and edge[1] not in visited:
                    neighbor = edge[1]
                
                if neighbor is not None:
                    visited.append(neighbor)
                    recurse(visited, neighbor)
                    visited.pop()
                    if Hamiltonian_Cycle != []:
                        return

        def check_for_cycle(cur_node, start_node):
            """Check if current path forms a cycle back to start"""
            # Check if there's an edge from current node back to start
            has_edge_to_start = any(
                (cur_node == e[0] and start_node == e[1]) or 
                (cur_node == e[1] and start_node == e[0]) 
                for e in edges
            )

            return has_edge_to_start
        
        for start in vertices:
            recurse([start], start)
            if Hamiltonian_Cycle != []:
                break
                
        return [Hamiltonian_Path != [], Hamiltonian_Path, Hamiltonian_Cycle != [], Hamiltonian_Cycle, Largest_Cycle_Size]

    def hamilton_bruteforce(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:

        vertices_list = list(vertices)
        n = len(vertices_list)

        # Build adjacency check
        edge_set = set()
        for u, v in edges:
            edge_set.add((u, v))
            edge_set.add((v, u))

        def has_edge(u, v):
            return (u, v) in edge_set

        def is_valid_path(perm):
            # Check if consecutive vertices in permutation have edges
            for i in range(len(perm) - 1):
                if not has_edge(perm[i], perm[i + 1]):
                    return False
            return True

        def generate_permutations(arr):
            # Generate all permutations of arr
            result = []

            def backtrack(current, remaining):
                if not remaining:
                    result.append(current[:])
                    return

                for i in range(len(remaining)):
                    current.append(remaining[i])
                    backtrack(current, remaining[:i] + remaining[i+1:])
                    current.pop()

            backtrack([], arr)
            return result

        def generate_subsets(arr):
            # Generate all subsets of arr with size >= 3
            result = []

            def backtrack_subset(start, current):
                if len(current) >= 3:
                    result.append(current[:])

                for i in range(start, len(arr)):
                    current.append(arr[i])
                    backtrack_subset(i + 1, current)
                    current.pop()

            backtrack_subset(0, [])
            return result

        hamiltonian_path = []
        hamiltonian_cycle = []
        largest_cycle_size = 0

        # First, check for Hamiltonian path/cycle (full permutations)
        all_perms = generate_permutations(vertices_list)
        for perm in all_perms:
            if is_valid_path(perm):
                # Found a valid path
                if not hamiltonian_path:
                    hamiltonian_path = list(perm)

                # Check if it forms a cycle
                if len(perm) >= 3 and has_edge(perm[-1], perm[0]):
                    cycle_size = len(perm)
                    largest_cycle_size = max(largest_cycle_size, cycle_size)

                    if cycle_size == n and not hamiltonian_cycle:
                        hamiltonian_cycle = list(perm) + [perm[0]]

        # check all subsets for largest cycle (if we haven't found a Hamiltonian cycle)
        if largest_cycle_size < n:
            all_subsets = generate_subsets(vertices_list)
            for subset in all_subsets:
                subset_perms = generate_permutations(subset)
                for perm in subset_perms:
                    if is_valid_path(perm) and has_edge(perm[-1], perm[0]):
                        cycle_size = len(perm)
                        largest_cycle_size = max(largest_cycle_size, cycle_size)

        path_exists = len(hamiltonian_path) > 0
        cycle_exists = len(hamiltonian_cycle) > 0

        # Format output to match expected format
        if not path_exists:
            hamiltonian_path = None
        if not cycle_exists:
            hamiltonian_cycle = None
            # Keep largest_cycle_size even if no Hamiltonian cycle

        return [path_exists, hamiltonian_path, cycle_exists, hamiltonian_cycle, largest_cycle_size]

    def hamilton_simple(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def hamilton_bestcase(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass
