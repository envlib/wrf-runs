#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 10:40:23 2025

@author: mike
"""
import os
import pathlib
import shlex
import subprocess
import pendulum
import sentry_sdk
import shutil

import params

############################################
### Parameters


###########################################
### Functions


def run_real():
    """

    """
    cmd_str = f'{params.real_exe}'
    cmd_list = shlex.split(cmd_str)
    p = subprocess.run(cmd_list, capture_output=False, text=False, check=False, cwd=params.data_path)

    real_log_path = params.data_path.joinpath('rsl.out.0000')
    with open(real_log_path, 'rt') as f:
        f.seek(0, os.SEEK_END)
        f.seek(f.tell() - 40, os.SEEK_SET)
        results_str = f.read()

    if 'SUCCESS COMPLETE REAL_EM INIT' in results_str:
        for path in params.data_path.glob('met_em.*.nc'):
            path.unlink()

        run_path = params.data_path.joinpath('run')
        run_path.mkdir(exist_ok=True)
        wrf_run_path = params.wrf_path.joinpath('run')
        cmd_str = f'ln -sf {wrf_run_path}/* .'
        # cmd_list = shlex.split(cmd_str)
        p = subprocess.run(cmd_str, shell=True, capture_output=False, text=False, check=False, cwd=run_path)
        for path in params.data_path.glob('wrf*'):
            file_name = path.name
            path.rename(run_path.joinpath(file_name))

        cmd_str = f'ln -sf {params.wrf_nml_path} .'
        p = subprocess.run(cmd_str, shell=True, capture_output=False, text=False, check=False, cwd=run_path)

        return True
    else:
        scope = sentry_sdk.get_current_scope()
        scope.add_attachment(path=real_log_path)
        raise ValueError(f'real.exe failed. Look at the rsl.out.0000 file for details: {results_str}')





