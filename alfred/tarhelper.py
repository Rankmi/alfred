import os
import subprocess


def uncompress(filepath):
    subprocess.run(["echo", "Decompressing"])
    subprocess.run(
        ['tar',
         '-xjf',
         filepath,
         '--checkpoint=1', r"--checkpoint-action=ttyout=\r(%d sec): %{r}T"])
