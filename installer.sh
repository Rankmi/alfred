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
            sudo apt update
            sudo apt install python python-pip
            pip install boto3;;
        ${MAC})
            echo "MacOs detected, installing dependencies using brew"
            brew update
            brew install python3
            pip3 install boto3;;
        *)
            echo "Your system is not supported, I'm sorry";;
esac

