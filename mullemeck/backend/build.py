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
