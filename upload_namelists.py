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
import copy

import params, utils

############################################
### Parameters


###########################################
### Functions



def upload_namelists(run_uuid):
    """

    """
    remote = copy.deepcopy(params.file['remote']['output'])

    if 'path' in remote:
        out_path = pathlib.Path(remote.pop('path'))

        name = 'output'
        config_path = utils.create_rclone_config(name, params.data_path, remote)

        dest_str = f'{name}:{out_path}/namelists/{run_uuid}/'
        cmd_str = f'rclone copy {params.data_path} {dest_str} --config={config_path} --include "namelist.*"'
        cmd_list = shlex.split(cmd_str)
        p = subprocess.run(cmd_list, capture_output=True, text=True, check=False)

        if p.stderr != '':
            raise ValueError(p.stderr)
        else:
            return True















































