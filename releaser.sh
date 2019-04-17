#!/bin/bash
MAC=Mac
LINUX=Linux

UNAME_OUT="$(uname -s)"

case "${UNAME_OUT}" in
    Linux*)     machine=${LINUX};;
    Darwin*)    machine=${MAC};;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

case ${machine} in

    ${LINUX})
        echo "You need to use a Mac machine.";;
    ${MAC})
        git hf update
        git hf release start "$1"
        echo "__version__ = '$1'" > _version.py
        git hf release finish "$1"

        echo "Releasing binary for Mac systems."
        ./generator.sh ins gen
        alfred release new

        echo "Releasing binary for Linux systems."
        docker build -t alfredock:"$1";;
esac
