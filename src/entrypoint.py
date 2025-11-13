import os
from src.helpers.project_selection_enum import ProjectSelection
from src.helpers.constants import CONFIGURATION_FILE_PATH, parse_config, INPUT_FILE
from src.sat import SatSolver
from src.bin_packing import BinPacking
from src.graph_coloring import GraphColoring
from src.hamilton_cycle_Dunne322 import HamiltonCycleColoring
from src.helpers.automation_helpers import brief_about_project

def main():
    """
    Entry point for the project1_toc package.
    """

    if not os.path.exists(CONFIGURATION_FILE_PATH):
        brief_about_project()
    selection, sub_problem = parse_config(CONFIGURATION_FILE_PATH)


    if selection["name"] == ProjectSelection.sat.name:
        solver = SatSolver(INPUT_FILE)
    elif selection["name"] == ProjectSelection.bin_packing.name:
        solver = BinPacking(INPUT_FILE)
    elif selection["name"] == ProjectSelection.hamiltonian.name:
        solver = HamiltonCycleColoring(INPUT_FILE)
    elif selection["name"] == ProjectSelection.graph_coloring.name:
        solver = GraphColoring(INPUT_FILE)
    
    if solver:
        solver.run()


    
    
