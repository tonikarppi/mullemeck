import subprocess


def build_static_checks(project):
    """
    This function runs static checks using the pre-commit configuration of the
    project given in argument, on this project.
    It assumes that the project will be cloned in projects/ and that the file
    is run from root level of the mullemeck project.
    """
    # Change directory to the project
    command1 = 'cd ./projects/' + project
    # runs pre-commit on all the files with the local configuration
    command2 = 'pre-commit run -a -c ./.pre-commit-config.yaml'
    # Saves the results of the combine two previous commands in pre-commit.log
    subprocess.call('touch pre-commit.log', shell=True)
    subprocess.call(command1 + '&&' + command2 +
                    '>../../pre-commit.log', shell=True)
    # Reads the log file
    with open('pre-commit.log') as file:
        lines = file.readlines()

    # Creates a single string variable for all the logs
    logs = ' '.join(lines)

    # If a test is not succesfuly run, 'failde' appears in the last line of the
    # logs.
    status = True
    if 'Failed' in logs:
        status = False

    return status, logs
