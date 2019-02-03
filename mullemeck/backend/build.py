import subprocess


def build_tests(project):
    """
    This function runs pytest on a specific project.
    It assumes that the project will be cloned in projects/ and that the file
    is run from root level of the mullemeck project.
    """
    # Initates the test and saves it in a log file.
    subprocess.call('pytest ./projects/'+project+'>pytest.log', shell=True)

    # Reads the log file
    with open('pytest.log') as file:
        lines = file.readlines()

    # Creates a single string variable for all the logs
    logs = ' '.join(lines)
    last_line = lines[-1]

    # If a test is not succesfuly run, 'failde' appears in the last line of the
    # logs.
    status = True
    if 'failed' in last_line:
        status = False

    return status, logs
