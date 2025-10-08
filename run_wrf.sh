#!/bin/bash

uv run main.py

n_cores=$(toml get --toml-path parameters.toml n_cores)
wrf_exe_path=$(toml get --toml-path parameters.toml executables.wrf_path)/main/wrf.exe

cd $(toml get --toml-path parameters.toml data_path)

# echo $n_cores $wrf_exe_path
mpirun -np $n_cores $wrf_exe_path

uv run monitor_wrf.py
