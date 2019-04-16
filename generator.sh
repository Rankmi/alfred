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
        # Let's asume the user is using a debian based distro
        ${LINUX})
            if [ "$1" == "ins" ]; then
                echo "Installing dependencies for Linux."
                echo "----------------------------------------------------"
                apt update
                apt install -y glibc libc-bin binutils
                pipenv install -d pyinstaller
                echo "----------------------------------------------------"
            fi

            if [ "$1" == "gen" ] || [ "$2" == "gen" ]; then
                echo "Generating binary for Linux machines."
                echo "----------------------------------------------------"
                pipenv run pyinstaller main.py -n alfred --onefile
                echo "----------------------------------------------------"
                echo "Self-contained binary generated on ./dist as alfred."
            fi;;
        ${MAC})
            if [ "$1" == "ins" ]; then
                echo "Installing dependecies for MacOS."
                echo "----------------------------------------------------"
                brew update
                pip3 install pipenv
                pipenv install -d pyinstaller
                echo "----------------------------------------------------"
            fi

            if [ "$1" == "gen" ] || [ "$2" == "gen" ]; then
                echo "Generating binary for MacOS machines."
                echo "----------------------------------------------------"
                pipenv run pyinstaller main.py -n alfred --onefile
                echo "----------------------------------------------------"
                echo "Self-contained binary generated on ./dist as alfred."
            fi;;
        *)
            echo "Operative system not supported.";;
esac