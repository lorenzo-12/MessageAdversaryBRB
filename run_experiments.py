import os 
import pathlib 
import subprocess
import time
import json

path_makefile = pathlib.Path(__file__).parent / "makefile"
path_ma1 = pathlib.Path(__file__).parent / "quantas" / "BRBPeer" / "topologies_bracha" /"MA1_topologies"

experiments = [
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/generalized_wheel_byz_center_n100_k6.json",
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/generalized_wheel_n100_k6.json",
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/multipartite_wheel_n99_k6.json",
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/random_graph_n100_k6.json",
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/random_graph_n100_k6_e500.json",
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/random_graph_n100_k6_e600.json",
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/random_graph_n100_k6_e700.json",
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/random_graph_pruned_n100_k6.json",
    "INPUTFILE := /topologies_<alg>/MA<x>_topologies/random_graph_byz_high_conn_n100_k6.json"
]

files = [
    "generalized_wheel_byz_center_n100_k6.txt",
    "generalized_wheel_n100_k6.txt",
    "multipartite_wheel_n99_k6.txt",
    "random_graph_byz_high_conn_n100_k6.txt",
    "random_graph_n100_k6_e500.txt",
    "random_graph_n100_k6_e600.txt",
    "random_graph_n100_k6_e700.txt",
    "random_graph_n100_k6.txt",
    "random_graph_pruned_n100_k6.txt"
]


file = os.listdir(path_ma1)[0]
with open(path_ma1/file,"r") as f:
    data = json.load(f)
    total_tests = 100*len(data["experiments"])


algorithm = "bracha"
processes = []

for ma_type in [1,2,3]:
    # reset files to empty
    for file in files:
        f = open("results_status/"+file, "w+")
    
    for i, exp in enumerate(experiments):
        final_file = ""
        check = False
        with open(path_makefile,"r") as f:
            lines = f.readlines()
            for line in lines:
                if check:
                    exp = exp.replace("<x>",str(ma_type)).replace("<alg>",algorithm)
                    final_file += exp + "\n"
                    check = False
                elif "#-->" in line:
                    check = True
                    final_file += line
                else:
                    final_file += line 

        with open(path_makefile,"w") as f:
            f.write(final_file)
        

        p = subprocess.Popen(["make", "run"], cwd=path_makefile.parent)
        processes.append(p)
        time.sleep(3)  # slight delay to avoid potential race conditions

    # Monitor and display progress until all processes finish
    while True:
        # count completed processes
        term_proc = sum(1 for p in processes if p.poll() is not None)
        # clear terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # build progress text
        text = ""
        for file in files:
            try:
                with open("results_status/"+file, "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                lines = []
            x = len(lines)
            perc = min(int(x * 100 / total_tests),100)
            y = len(str(total_tests))
            text += f"[{'#' * perc:<100}]{perc:>3}%  {x:>{y}}/{total_tests}   {file}\n"
        print(text, end="", flush=True)

        # exit when done
        if term_proc >= len(processes):
            break

        time.sleep(1)

    # wait for all processes to ensure clean exit
    for p in processes:
        p.wait()