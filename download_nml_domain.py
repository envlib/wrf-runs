#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 15:06:19 2025

@author: mike
"""
# import s3func
# import concurrent.futures
import pathlib
import shlex
import subprocess
import copy

import params



############################################
### Parameters

remote = copy.deepcopy(params.file['remote']['project'])


###########################################
### Functions


def dl_nml_domain():
    """

    """
    params.data_path.mkdir(parents=True, exist_ok=True)

    proj_path = pathlib.Path(remote.pop('path'))

    name = 'project'

    config_path = params.create_rclone_config(name, params.data_path, remote)

    src_str = f'{name}:{proj_path}/'
    cmd_str = f'rclone copy {src_str} {params.data_path} --config={config_path} --include "geo_em.*.nc" --include "namelist.*"'
    cmd_list = shlex.split(cmd_str)
    p = subprocess.run(cmd_list, capture_output=True, text=True, check=False)
    # for file_path in params.data_path.iterdir():
    #     if file_path.is_file():
    #         file_path.unlink()
    if p.stderr != '':
        raise ValueError(p.stderr)
    else:
        return True



    # dst_session = s3func.S3Session(remote['access_key_id'], remote['access_key'], remote['bucket'], remote['endpoint_url'], stream=False)



    # with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    #     futures = {}
    #     for file_path in params.data_path.iterdir():
    #         if file_path.is_file():
    #             print(file_path)
    #             key = str(proj_path.joinpath(file_path.name))
    #             f = executor.submit(upload_file, dst_session, key, file_path)
    #             futures[f] = key

    #     for future in concurrent.futures.as_completed(futures):
    #         key = futures[future]
    #         msg = future.result()
    #         if msg == 'success':
    #             print(f'success: {key}')
    #         else:
    #             print(f'failed: {key} - {msg}')


############################################
### Upload files








