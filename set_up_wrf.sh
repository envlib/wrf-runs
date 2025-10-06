#!/bin/bash

file_path=$1
dest_path=$2
file_name=$(basename $file_path)
new_file_path=$dest_path/$file_name
ncks -O -4 -L 3 -d latitude,-60.0,-20.0 -d longitude,144.0,194.0 $file_path $new_file_path

