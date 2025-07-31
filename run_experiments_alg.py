import os 
import pathlib 
import subprocess
import time
import json
import argparse

parser = argparse.ArgumentParser(description="Run BRB experiments with specified algorithm.")
parser.add_argument("--alg", type=str, default="bracha", help="Algorithm name (default: bracha)")
parser.add_argument("--ma", type=int, default=1, help="Message adversary type (default: 1)")
args = parser.parse_args()
algorithm = args.alg
ma = args.ma

path_makefile = pathlib.Path(__file__).parent / "makefile"
path_makefile_dir = pathlib.Path(__file__).parent / "makefiles"
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
    #total_tests = int(data["experiments"][0]["tests"])*len(data["experiments"])*int(data["experiments"][0]["rounds"])
    total_tests = int(data["experiments"][0]["tests"])*len(data["experiments"])
    
makefile_text = ""
with open(path_makefile, "r") as f:
    makefile_text = f.read()
    
def modify_line(arg_line, arg_makefile):
    with open(path_makefile_dir / arg_makefile,"r") as f:
        final_file = ""
        check = False
        lines = f.readlines()
        for line in lines:
            if check:
                final_file += arg_line + "\n"
                check = False
            elif "#-->" in line:
                check = True
                final_file += line
            else:
                final_file += line 
                
    with open(path_makefile_dir / arg_makefile,"w+") as f:
            f.write(final_file)


processes = []

""" for file in files:
    f = open(f"results_status/MA{str(ma)}_{algorithm}_{file}", "w+") """

for ma_type in [ma]:
        
    for i, exp in enumerate(experiments):
        
        exp_name = exp.split("topologies/")[1].replace(".json","")
        makefile_file_name = f"makefile_{algorithm}_MA{ma_type}_{exp_name}"
        f = open(f"results_status/MA{str(ma)}_{algorithm}_{exp_name}.txt", "w+")
        
        line = exp.replace("<x>",str(ma_type)).replace("<alg>",algorithm)
        
        with open(path_makefile_dir / makefile_file_name, "w+") as f:
            f.write(makefile_text)
            
        modify_line(line, makefile_file_name)
        
        p = subprocess.Popen(["make", "-f", str(path_makefile_dir / makefile_file_name), "run"], cwd=path_makefile.parent)
        processes.append(p)
        
        # Monitor and display progress until all processes finish
        while True:
            # count completed processes
            term_proc = sum(1 for p in processes if p.poll() is not None)
            
            # exit when done
            if term_proc >= len(processes):
                break

            time.sleep(2)

        # wait for all processes to ensure clean exit
        for p in processes:
            p.wait()
        