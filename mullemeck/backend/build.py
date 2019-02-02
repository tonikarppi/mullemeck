import pytest


def build_tests(folder):
    """
    This function runs pytest on a specific folder.
    We assume that the project will be cloned in projects/
    """
    logs = pytest.main(['../../projects/'+folder])
    logs = pytest.main(['../../../dd2480-lab1/'+folder])
    return logs


print(build_tests('tests/'))
