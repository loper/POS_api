#!/bin/bash

# determine if in docker container
grep -q docker /proc/1/cgroup && {
    # in docker
    # EXE=pylint --init-hook="import pylint_venv, sys; sys.path.insert(0, '/home/api/venv/lib/python3.8/site-packages/')"
    EXE='pylint'
} || {
    EXE='pylint'
}

for src in $(ls *.py); do
    $EXE --init-hook="import pylint_venv, sys; sys.path.insert(0, '/home/api/venv/lib/python3.8/site-packages/')" -j 0 -f colorized --errors-only $src || exit 1
done

for src in $(ls *.py); do
    $EXE --init-hook="import pylint_venv, sys; sys.path.insert(0, '/home/api/venv/lib/python3.8/site-packages/')" -j 0 -f colorized --disable=C0114 --disable=C0116 $src || exit 1
done
