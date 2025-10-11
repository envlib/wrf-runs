#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 10:40:23 2025

@author: mike
"""
import pathlib
import shlex
import subprocess
import pendulum
import shutil

import params



############################################
### Parameters


###########################################
### Functions


def run_era5_to_int(start_date, end_date, hour_interval, del_old=True):
    """

    """
    era5_path = params.data_path.joinpath('era5')

    cmd_str = f'era5_to_int -h {hour_interval} -i {era5_path} "{start_date}" "{end_date}"'
    cmd_list = shlex.split(cmd_str)
    p = subprocess.run(cmd_list, capture_output=True, text=True, check=False, cwd=params.data_path)

    if p.stderr != '':
        raise ValueError(p.stderr)
    else:
        if del_old:
            shutil.rmtree(era5_path)
        return True




