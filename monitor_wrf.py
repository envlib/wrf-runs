#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 15:41:48 2025

@author: mike
"""
import os
import pathlib
import shlex
import subprocess
import pendulum
import copy
import sentry_sdk
from time import sleep

import params

############################################
### Parameters



out_files_glob = ('wrfout_*',)


###########################################
### Functions


def read_last_line(file_path):
    """

    """
    cmd_str = f'tail -1 {file_path}'
    cmd_list = shlex.split(cmd_str)
    p = subprocess.run(cmd_list, capture_output=True, text=True, check=False)

    return p.stdout.strip('\n')


def query_out_files(run_path):
    """

    """
    out_files = {}
    for glob in out_files_glob:
        for file_path in run_path.glob(glob):
            file_name = file_path.name
            out_name, domain, datetime = file_name.split('_', 2)
            if (out_name, domain) in out_files:
                out_files[(out_name, domain)].append(str(file_path))
                out_files[(out_name, domain)].sort()
            else:
                out_files[(out_name, domain)] = [str(file_path)]

    return out_files


def select_files_to_dl(out_files, min_files):
    """

    """
    dl_files = []
    for grp, file_paths in out_files.items():
        n_files = len(file_paths)
        file_paths.sort(reverse=True)
        if n_files > min_files:
            dl_files.extend(file_paths[min_files:n_files])

    return dl_files


def dl_files(dl_files, run_path, name, out_path, config_path):
    """

    """
    dl_files_str = '\n'.join(dl_files)
    cmd_str = f'rclone copy {run_path} {name}:{out_path} --transfers=4 --config={config_path} --files-from-raw -'
    cmd_list = shlex.split(cmd_str)
    p = subprocess.run(cmd_list, input=dl_files_str, capture_output=True, text=True, check=False)
    if p.stderr == '':
        for dl_file in dl_files:
            os.remove(dl_file)



def monitor_wrf():
    """

    """
    remote = copy.deepcopy(params.file['remote']['output'])

    out_path = pathlib.Path(remote.pop('path'))

    name = 'output'
    config_path = params.create_rclone_config(name, params.data_path, remote)

    run_path = params.data_path.joinpath('run')

    n_cores = params.file['n_cores']

    cmd_str = f'mpirun -np {n_cores} ./wrf.exe'
    cmd_list = shlex.split(cmd_str)
    p = subprocess.Popen(cmd_list, cwd=run_path)

    check = p.poll()
    while check is None:
        out_files = query_out_files(run_path)

        dl_files = select_files_to_dl(out_files, 1)

        if dl_files:
            files_str = ', '.join([p.split('/')[-1] for p in dl_files])
            print(f'-- Uploading files: {files_str}')
            dl_files(dl_files, run_path, name, out_path, config_path)

        sleep(120)
        check = p.poll()

    wrf_log_path = run_path.joinpath('rsl.out.0000')
    results_str = read_last_line(wrf_log_path)

    if 'SUCCESS COMPLETE WRF' in results_str:
        out_files = query_out_files(run_path)

        dl_files = select_files_to_dl(out_files, 0)

        if dl_files:
            files_str = ', '.join([p.split('/')[-1] for p in dl_files])
            print(f'-- Uploading files: {files_str}')
            dl_files(dl_files, run_path, name, out_path, config_path)

        return True
    else:
        scope = sentry_sdk.get_current_scope()
        scope.add_attachment(path=wrf_log_path)
        raise ValueError(f'wrf.exe failed. Look at the rsl.out.0000 file for details: {results_str}')















































