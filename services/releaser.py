import platform
import subprocess


def release_alfred(version):
    if platform.system() != "Darwin":
        print("You need to release alfred from a Mac machine.")
        return 403

    subprocess.run(["echo", "__version__ = " + version, ">", "_version.py"])

    print("Releasing binary for Mac systems.")
    subprocess.run(["./generator.sh", "ins", "gen"])
    subprocess.run(["alfred", "release", "new"])

    print("Releasing binary for Linux systems.")
    subprocess.run(["cp", "~/.alfred.conf", "."])
    subprocess.run(["docker", "build", "-t", "alfredock:"+version, "."])
    subprocess.run(["rm", ".alfred.conf"])

    print("All binaries successfully uploaded.")
    return 201
