import subprocess
import io


def build_tests(project):
    """
    This function runs pytest on a specific project.
    It assumes that the project will be cloned in projects/ and that the file
    is run from root level of the mullemeck project.
    """

    # Runs the build and gets the output in build object.
    build = subprocess.Popen('poetry run pytest ./projects/'+project,
                             shell=True, stdout=subprocess.PIPE)
    # Waits for the process to end
    build.wait()
    success = build.returncode

    # Reads the output and saves it in lines, then concatenates it in single
    # string logs.
    lines = []
    for line in io.TextIOWrapper(build.stdout, encoding="utf-8"):
        lines.append(line)  # or another encoding
    logs = ' '.join(lines)

    status = False
    # If the shell command returns 0 it means that no errors occured. Every
    # other value sets status to False.
    if success == 0:
        status = True

    return status, logs
