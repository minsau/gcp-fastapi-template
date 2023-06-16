#!/usr/bin/env bash
set -e

if [[ "${RUNTYPE}" == "bash" ]]; then
    printf "started Docker container as runtype \e[1;93mbash\e[0m\n"
    exec /bin/bash

else
    printf "Runing with port 80 and runtype no RUNTYPE\n"
    printf "Runing in path: $(pwd)\n"
    exec gunicorn --bind :$INTERNAL_PORT --worker-class uvicorn.workers.UvicornWorker main:app
fi
