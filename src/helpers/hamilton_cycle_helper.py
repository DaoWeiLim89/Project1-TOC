import csv
import json
import os
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from src.helpers.constants import CONFIGURATION_FILE_PATH, RESULTS_FOLDER
from src.helpers.dmaics_parser import parse_cnf_instances_hamilton
from src.helpers.project_selection_enum import ProjectSelection, SubProblemSelection


class HamiltonCycleAbstractClass(ABC):
    def __init__(
        self,
        cnf_file_input_path: str,
        result_file_name: str = "graph_coloring_results",
        results_folder_path: str = RESULTS_FOLDER,
    ):
        self.cnf_file_input_path = cnf_file_input_path
        self.results_folder_path = results_folder_path
        self.result_file_name = result_file_name
        self.config_path = CONFIGURATION_FILE_PATH
        self.solution_instances = self.parse_input_file()
        print(
            f"Parsed {len(self.solution_instances)} instances from {self.cnf_file_input_path}"
        )
        self.sub_problems = self.set_config()

    def set_config(self):
        if not os.path.exists(self.config_path):
            raise Exception("Please make sure the configuration file exists!!!")
        with open(self.config_path, mode="r", encoding="utf-8") as conf_buffer:
            data = json.load(conf_buffer)
        data = data["Project Configuration"]
        selection = data["Selection"]
        sub_problem = data["Sub Problem"]
        sub_probs = []
        for sub_prob in sub_problem:
            if sub_prob["value"] == SubProblemSelection.brute_force.value:
                sub_probs.append(SubProblemSelection.brute_force)
            elif sub_prob["value"] == SubProblemSelection.btracking.value:
                sub_probs.append(SubProblemSelection.btracking)
            elif sub_prob["value"] == SubProblemSelection.simple.value:
                sub_probs.append(SubProblemSelection.simple)
            elif sub_prob["value"] == SubProblemSelection.best_case.value:
                sub_probs.append(SubProblemSelection.best_case)
        return sub_probs

    def parse_input_file(self):
        return parse_cnf_instances_hamilton(self.cnf_file_input_path)

    def save_results(self, run_results: List[Any], sub_problem):
        # Write to CSV
        dir_name, file_name = os.path.split(self.cnf_file_input_path)
        file_name_only, ext = os.path.splitext(file_name)
        temp_result = os.path.join(
            self.results_folder_path,
            f"{sub_problem}_{file_name_only}_{self.result_file_name}.csv",
        )
        with open(temp_result, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "Instance_ID",
                    "Num_Vertices",
                    "Num_Edges",
                    "Hamiltonian_Path",
                    "Hamiltonian_Cycle",
                    "Largest_Cycle_Size",
                    "Algorithm",
                    "Time",
                ]
            )
            w.writerows(run_results)
        print(f"\nResults written to {temp_result}")

    @abstractmethod
    def hamilton_backtracking(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    @abstractmethod
    def hamilton_bruteforce(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    @abstractmethod
    def hamilton_simple(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    @abstractmethod
    def hamilton_bestcase(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def run(self):
        results = []

        for inst in self.solution_instances:
            vertices: set = inst.get("vertices", set())
            edges: list[tuple[int]] = inst.get("edges", [])
            inst_id: int = inst.get("id", -1)
            n_vertices: int = len(vertices)

            if SubProblemSelection.brute_force in self.sub_problems:
                t0 = time.perf_counter()
                path_exists, path, cycle_exists, cycle, largest_cycle_size = (
                    self.hamilton_bruteforce(vertices, edges)
                )
                bt_time = time.perf_counter() - t0
                results.append(
                    [
                        inst_id,
                        n_vertices,
                        len(edges),
                        path if path_exists else "None",
                        cycle if cycle_exists else "None",
                        largest_cycle_size,
                        "BruteForce",
                        f"{bt_time:.6f}",
                    ]
                )

        if SubProblemSelection.brute_force in self.sub_problems:
            self.save_results(results, SubProblemSelection.brute_force.name)
            results = []

        for inst in self.solution_instances:
            vertices: set = inst.get("vertices", set())
            edges: list[tuple[int]] = inst.get("edges", [])
            inst_id: int = inst.get("id", -1)
            n_vertices: int = len(vertices)

            if SubProblemSelection.btracking in self.sub_problems:
                t0 = time.perf_counter()
                path_exists, path, cycle_exists, cycle, largest_cycle_size = (
                    self.hamilton_backtracking(vertices, edges)
                )
                bt_time = time.perf_counter() - t0
                results.append(
                    [
                        inst_id,
                        n_vertices,
                        len(edges),
                        path if path_exists else "None",
                        cycle if cycle_exists else "None",
                        largest_cycle_size,
                        "Backtracking",
                        f"{bt_time:.6f}",
                    ]
                )

        if SubProblemSelection.btracking in self.sub_problems:
            self.save_results(results, SubProblemSelection.btracking.name)
            results = []

        for inst in self.solution_instances:
            vertices: set = inst.get("vertices", set())
            edges: list[tuple[int]] = inst.get("edges", [])
            inst_id: int = inst.get("id", -1)
            n_vertices: int = len(vertices)

            if SubProblemSelection.simple in self.sub_problems:
                t0 = time.perf_counter()
                path_exists, path, cycle_exists, cycle, largest_cycle_size = (
                    self.hamilton_simple(vertices, edges)
                )
                bt_time = time.perf_counter() - t0
                results.append(
                    [
                        inst_id,
                        n_vertices,
                        len(edges),
                        path if path_exists else "None",
                        cycle if cycle_exists else "None",
                        largest_cycle_size,
                        f"{bt_time:.6f}",
                    ]
                )

        if SubProblemSelection.simple in self.sub_problems:
            self.save_results(results, SubProblemSelection.simple.name)
            results = []

        for inst in self.solution_instances:
            vertices: set = inst.get("vertices", set())
            edges: list[tuple[int]] = inst.get("edges", [])
            inst_id: int = inst.get("id", -1)
            n_vertices: int = len(vertices)

            if SubProblemSelection.best_case in self.sub_problems:
                t0 = time.perf_counter()
                path_exists, path, cycle_exists, cycle, largest_cycle_size = (
                    self.hamilton_bestcase(vertices, edges)
                )
                bt_time = time.perf_counter() - t0
                results.append(
                    [
                        inst_id,
                        n_vertices,
                        len(edges),
                        path if path_exists else "None",
                        cycle if cycle_exists else "None",
                        largest_cycle_size,
                        f"{bt_time:.6f}",
                    ]
                )

        if SubProblemSelection.best_case in self.sub_problems:
            self.save_results(results, SubProblemSelection.best_case.name)
            results = []
