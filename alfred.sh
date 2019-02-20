#!/bin/bash
pipenv install > /dev/null 2>&1
pipenv run python ./main.py "$@"
