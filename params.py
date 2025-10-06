#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 15:03:38 2025

@author: mike
"""
import tomllib
import os
import pathlib
import f90nml
import shlex
import subprocess

############################################
### Read params file

base_path = pathlib.Path(os.path.realpath(os.path.dirname(__file__)))

with open(base_path.joinpath("parameters.toml"), "rb") as f:
    file = tomllib.load(f)


##############################################
### Assign executables

if 'wrf_path' in file['executables']:
    wrf_path = pathlib.Path(file['executables']['wrf_path'])
else:
    wrf_path = pathlib.Path('/WRF')

wrf_exe = wrf_path.joinpath('main/wrf.exe')

real_exe = wrf_path.joinpath('main/real.exe')

if 'wps_path' in file['executables']:
    wps_path = pathlib.Path(file['executables']['wps_path'])
else:
    wps_path = pathlib.Path('/WPS')

geogrid_exe = wps_path.joinpath('geogrid.exe')

metgrid_exe = wps_path.joinpath('metgrid.exe')


###########################################
### Others

if 'data_path' in file:
    data_path = pathlib.Path(file['data_path'])
else:
    data_path = pathlib.Path('/data')

wps_nml_path = data_path.joinpath('namelist.wps')
wrf_nml_path = data_path.joinpath('namelist.input')

##########################################
### ERA5

# era5_file_names = [
#     'e5.oper.an.pl/{date}/e5.oper.an.pl.128_129_z.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.pl/{date}/e5.oper.an.pl.128_133_q.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.pl/{date}/e5.oper.an.pl.128_130_t.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.pl/{date}/e5.oper.an.pl.128_131_u.ll025uv.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.pl/{date}/e5.oper.an.pl.128_132_v.ll025uv.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_034_sstk.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_235_skt.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_039_swvl1.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_040_swvl2.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_041_swvl3.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_042_swvl4.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_139_stl1.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_170_stl2.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_183_stl3.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_236_stl4.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_031_ci.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_167_2t.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_168_2d.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_165_10u.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_166_10v.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_033_rsn.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_141_sd.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_151_msl.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.an.sfc/{date}/e5.oper.an.sfc.128_134_sp.ll025sc.{start_date_hour}_{end_date_hour}.nc',
#     'e5.oper.invariant/197901/e5.oper.invariant.128_172_lsm.ll025sc.1979010100_1979010100.nc',
#     'e5.oper.invariant/197901/e5.oper.invariant.128_172_z.ll025sc.1979010100_1979010100.nc',
#     ]


#######################################################
### Functions


def create_rclone_config(name, config_path, config_dict):
    """

    """
    type_ = config_dict['type']
    config_list = [f'{k}={v}' for k, v in config_dict.items() if k != 'type']
    config_str = ' '.join(config_list)
    config_path = config_path.joinpath('rclone.config')
    cmd_str = f'rclone config create {name} {type_} {config_str} --config={config_path} --non-interactive'
    cmd_list = shlex.split(cmd_str)
    p = subprocess.run(cmd_list, capture_output=True, text=True, check=True)

    return config_path




















