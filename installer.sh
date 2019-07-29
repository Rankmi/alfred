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
            echo "Linux detected, installing dependencies using apt"
            apt update
            apt install -y python3.7 python3-pip
			      python3.7 -m pip install pipenv;;
        ${MAC})
            echo "MacOs detected, installing dependencies using brew"
            brew update
            brew install python3 pipenv gnu-tar;;
        *)
            echo "Your system is not supported, I'm sorry";;
esac

pipenv install
chmod +x ./alfred.sh

if [ "$1" == "gbin" ]; then 
    pipenv run pyinstaller main.py -n alfred --onefile
fi