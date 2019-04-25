import platform
import subprocess
from services.githubservice import get_token


def release_alfred(version):
    if platform.system() != "Darwin":
        print("You need to release alfred from a Mac machine.")
        return 403

    subprocess.run(["git", "checkout", "master"])
    subprocess.run(["git", "hf", "update"])
    subprocess.run(["git", "hf", "release", "start", version])
    subprocess.run(["echo", "__version__ = " + version, ">", "_version.py"])
    subprocess.run(["git", "hf", "release", "finish", version])

    print("Releasing binary for Mac systems.")
    subprocess.run(["./generator.sh", "ins", "gen"])
    subprocess.run(["alfred", "release", "new"])

    print("Releasing binary for Linux systems.")
    gh_token = get_token()
    subprocess.run(["docker", "build", "--build-arg", gh_token, "-t", "alfredock:"+version, "."])

    print("All binaries successfully uploaded.")
    return 201
