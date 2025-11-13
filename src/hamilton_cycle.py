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

            return None

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
        pass

    def hamilton_simple(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def hamilton_bestcase(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass
