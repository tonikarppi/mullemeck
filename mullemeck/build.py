from validator_collection import checkers
import subprocess
import io


def clone_repo(repo_url, commit):
    """
    This function asserts that the url given is valid and clones it in a
    temporary folder
    """

    if not checkers.is_url(repo_url):
        raise ValueError('Url not valid')

    # Sets up directory to clone the repo.
    directory = '/tmp/mullemeck' + commit
    # Creates the folder and clones the repo in it.
    subprocess.call('mkdir ' + directory, shell=True)
    build = subprocess.Popen('cd ' + directory + ' && git clone ' + repo_url,
                             shell=True, stdout=subprocess.PIPE)

    build.wait()

    success = build.returncode

    lines = []
    for line in io.TextIOWrapper(build.stdout, encoding="utf-8"):
        lines.append(line)
    logs = ' '.join(lines)

    status = False
    # If the shell command returns 0 it means that no errors occured. Every
    # other value sets status to False.
    if success == 0:
        status = True

    return status, logs, directory


def build_static_checks(project):
    """
    This function runs static checks using the pre-commit configuration of the
    project given in argument, on this project.
    It assumes that the project will be cloned in projects/ and that the file
    is run from root level of the mullemeck project.
    """
    command1 = 'cd ./projects/' + project
    # runs pre-commit on all the files with the local config, in poetry enviro-
    # nment
    command2 = 'poetry run pre-commit run -a -c ./.pre-commit-config.yaml'
    # Runs the build and gets the output in build object.
    build = subprocess.Popen(command1 + '&&' + command2, shell=True,
                             stdout=subprocess.PIPE)
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
