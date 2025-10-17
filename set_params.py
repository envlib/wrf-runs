#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 17:21:47 2025

@author: mike
"""
import pathlib
import f90nml
from datetime import datetime, timedelta
import params


################################################
### Parameters

geogrid_arrays = ['parent_id', 'parent_grid_ratio', 'i_parent_start', 'j_parent_start', 'e_we', 'e_sn', 'geog_data_res']

# wps_array_fields = {
#     'geogrid': ['parent_id', 'parent_grid_ratio', 'i_parent_start', 'j_parent_start', 'e_we', 'e_sn', 'geog_data_res'],

#     }

# wrf_array_fields = {
#     'domains': ['grid_id', 'parent_id', 'parent_grid_ratio', 'i_parent_start', 'j_parent_start', 'e_we', 'e_sn', 'e_vert', 'parent_time_step_ratio'],

#     }

domain_array_fields = ('parent_id', 'parent_grid_ratio', 'i_parent_start', 'j_parent_start', 'e_we', 'e_sn', 'geog_data_res', 'e_vert', 'parent_time_step_ratio')

wps_date_format = '%Y-%m-%d_%H:%M:%S'


def check_set_params():

    ##############################################
    ### Assign and check executables

    if not params.wrf_path.exists():
        raise ValueError(f'wrf path does not exist: {params.wrf_path}')

    if not params.wrf_exe.exists():
        raise ValueError(f'wrf.exe does not exist: {params.wrf_exe}')

    if not params.real_exe.exists():
        raise ValueError(f'real.exe does not exist: {params.real_exe}')

    if not params.wps_path.exists():
        raise ValueError(f'wps path does not exist: {params.wps_path}')

    if not params.geogrid_exe.exists():
        raise ValueError(f'geogrid.exe does not exist: {params.geogrid_exe}')

    if not params.metgrid_exe.exists():
        raise ValueError(f'metgrid.exe does not exist: {params.metgrid_exe}')


    ##############################################
    ### Namelist checks

    wps_nml = f90nml.read(params.wps_nml_path)
    wrf_nml = f90nml.read(params.wrf_nml_path)

    n_domains = wps_nml['share']['max_dom']

    # ## domains
    # wps_domains = wps_nml['geogrid']
    # wrf_domains = wrf_nml['domains']

    # for k, v in wps_domains.items():
    #     if k in domain_array_fields:
    #         if len(v) != n_domains:
    #             raise ValueError(f'The field {k} must be an array with {n_domains} values.')
    #     if k in ('e_we', 'e_sn'):
    #         for i in v:
    #             if i < 100:
    #                 raise ValueError('The number of grid points in the domain must be greater than or equal to 100.')

    # for k, v in wrf_domains.items():
    #     if k in domain_array_fields:
    #         if len(v) != n_domains:
    #             raise ValueError(f'The field {k} must be an array with {n_domains} values.')

    # for k, v in wps_domains.items():
    #     if k in wrf_domains:
    #         wrf_v = wrf_domains[k]
    #         if wrf_v != v:
    #             raise ValueError(f'The field {k} in both the wps and wrf namelists are not the same.')


    #########################################
    ### Assign values in namelists

    data_path = params.data_path
    # if not data_path.exists():
    #     raise ValueError(f'data_path does not exist: {data_path}')

    # geog_data_path = pathlib.Path(params.file['input_data']['geog_data_path'])
    # if not geog_data_path.exists():
    #     raise ValueError(f'geog_data_path does not exist: {geog_data_path}')

    ## Paths
    wps_nml['share']['opt_output_from_geogrid_path'] = str(data_path)
    wps_nml['metgrid']['opt_output_from_metgrid_path'] = str(data_path)
    # wps_nml['geogrid']['geog_data_path'] = str(geog_data_path)
    wps_nml['geogrid']['opt_geogrid_tbl_path'] = str(params.geogrid_exe.parent.joinpath('geogrid'))
    wps_nml['metgrid']['opt_metgrid_tbl_path'] = str(params.metgrid_exe.parent.joinpath('metgrid'))

    ## Time control
    start_date = datetime.fromisoformat(params.file['time_control']['start_date'])
    end_date = datetime.fromisoformat(params.file['time_control']['end_date'])

    if start_date > end_date:
        raise ValueError(f'start_date ({start_date}) is greater than end_date ({end_date}).')

    # date_diff = end_date - start_date

    history_begin = wrf_nml['time_control']['history_begin'][0]

    # if date_diff.total_seconds()/60 < history_begin:
    #     raise ValueError('The date difference must be greater than the history_begin value.')

    start_date = start_date - timedelta(minutes=history_begin)

    wps_nml['share']['start_date'] = [start_date.strftime(wps_date_format)] * n_domains
    wps_nml['share']['end_date'] = [end_date.strftime(wps_date_format)] * n_domains

    wrf_nml['time_control']['start_year'] = [start_date.year] * n_domains
    wrf_nml['time_control']['start_month'] = [start_date.month] * n_domains
    wrf_nml['time_control']['start_day'] = [start_date.day] * n_domains
    wrf_nml['time_control']['start_hour'] = [start_date.hour] * n_domains
    wrf_nml['time_control']['end_year'] = [end_date.year] * n_domains
    wrf_nml['time_control']['end_month'] = [end_date.month] * n_domains
    wrf_nml['time_control']['end_day'] = [end_date.day] * n_domains
    wrf_nml['time_control']['end_hour'] = [end_date.hour] * n_domains

    outputs = ['wrfout']
    if wrf_nml['time_control']['output_diagnostics'] == 1:
        outputs.append('summ')
    if wrf_nml['diags']['z_lev_diags'] == 1:
        outputs.append('zlevel')

    #############################################
    ### Write namelists

    with open(params.wps_nml_path, 'w') as nml_file:
       wps_nml.write(nml_file)

    with open(params.wrf_nml_path, 'w') as nml_file:
       wrf_nml.write(nml_file)

    return start_date, end_date, int(wrf_nml['time_control']['interval_seconds']/(60*60)), outputs




















































