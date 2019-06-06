import platform
import subprocess


def release_alfred(version):
    if platform.system() != "Darwin":
        print("You need to release alfred from a Mac machine.")
        return 403

    with open("_version.py", "w") as f:
        f.write("__version__ = '" + version + "'\n")

    print("Releasing binary for Mac systems.")
    subprocess.run(["./generator.sh", "ins", "gen"])
    subprocess.run(["./dist/alfred", "release", "new"])

    print("Releasing binary for Linux systems.")
    subprocess.call("cp ~/.alfred.conf .", shell=True)
    subprocess.run(["docker", "build", "-t", "alfredock:"+version, "."])
    subprocess.run(["rm", ".alfred.conf"])

    print("All binaries successfully uploaded.")
    return 201
