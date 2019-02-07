from validator_collection import checkers
import subprocess
import io
import os


def clone_repo(repo_url, commit_id):
    """
    This function asserts that the url given is valid and clones it in a
    temporary folder
    """

    if not checkers.is_url(repo_url):
        raise ValueError('Url not valid')

    # If /tmp/mullemeck doesn't exist, creates it
    if not os.path.isdir('/tmp/mullemeck/'):
        subprocess.call('mkdir /tmp/mullemeck/', shell=True)
    # Sets up directory to clone the repo.
    directory = '/tmp/mullemeck/' + commit_id + '/'
    # Creates the folder and clones the repo in it.
    subprocess.call('mkdir ' + directory, shell=True)
    build = subprocess.Popen('cd ' + directory + ' && git clone ' + repo_url,
                             shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    build.wait(timeout=60)

    status = build.returncode

    lines = []
    for line in io.TextIOWrapper(build.stdout, encoding="utf-8"):
        lines.append(line)
    for line in io.TextIOWrapper(build.stderr, encoding="utf-8"):
        lines.append(line)
    logs = ' '.join(lines)

    success = False
    # If the shell command returns 0 it means that no errors occured. Every
    # other value sets status to False.
    if status == 0:
        success = True

    # If the clone couldn't be built we don't want to keep the directory.
    if not success:
        subprocess.call('rmdir '+directory, shell=True)

    return success, logs, directory


def build_static_checks(directory):
    """
    This function runs static checks using the pre-commit configuration of the
    directory given in argument, on the project.
    It assumes that pre-commit exists and that pre-commit-config.yaml exist in
    the path.
    """

    command1 = 'cd ' + directory
    # runs pre-commit on all the files with the local config, in poetry enviro-
    # nment
    command2 = 'poetry run pre-commit run -a -c ./.pre-commit-config.yaml'
    # Runs the build and gets the output in build object.
    build = subprocess.Popen(command1 + '&&' + command2, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Waits for the process to end
    build.wait()
    success = build.returncode

    # Reads the output and saves it in lines, then concatenates it in single
    # string logs.
    lines = []
    for line in io.TextIOWrapper(build.stdout, encoding="utf-8"):
        lines.append(line)
    for line in io.TextIOWrapper(build.stderr, encoding="utf-8"):
        lines.append(line)
    logs = ' '.join(lines)

    status = False
    # If the shell command returns 0 it means that no errors occured. Every
    # other value sets status to False.
    if success == 0:
        status = True

    return status, logs


def build_tests(directory):
    """
    This function runs pytest on a specific project located in `directory`.
    It assumes that the project is compatible with the usage of pytest.
    """

    # Runs the build and gets the output in build object.
    build = subprocess.Popen('poetry run pytest ' + directory,
                             shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    # Waits for the process to end
    build.wait()
    success = build.returncode

    # Reads the output and saves it in lines, then concatenates it in single
    # string logs.
    lines = []
    for line in io.TextIOWrapper(build.stdout, encoding="utf-8"):
        lines.append(line)
    for line in io.TextIOWrapper(build.stderr, encoding="utf-8"):
        lines.append(line)
    logs = ' '.join(lines)

    status = False
    # If the shell command returns 0 it means that no errors occured. Every
    # other value sets status to False.
    if success == 0:
        status = True

    return status, logs
