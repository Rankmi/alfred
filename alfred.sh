#!/bin/bash
pipenv install
pipenv run python ./alfred/main.py "$@"
