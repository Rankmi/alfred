import os
import subprocess
from pathlib import Path


def uncompress(filepath, delete_after=False):
    subprocess.run(["echo", "Decompressing"])
    subprocess.run(
        ['tar',
         '-xjf',
         filepath,
         '--checkpoint=1', r"--checkpoint-action=ttyout=\r(%d sec): %{r}T"])
    if delete_after:
        delete(filepath)


def delete(filepath):
    if Path(filepath).is_file():
        os.remove(filepath)
    else:
        print(f"No existe el archivo {filepath}")
