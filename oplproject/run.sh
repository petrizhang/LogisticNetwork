#!/usr/bin/env bash

dir=$OPLBIN_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$dir
$dir/oplrunjava -profile -p ./ default 
