from mullemeck.build import clone_repo
from mullemeck.build import build_static_checks
from mullemeck.build import build_tests
from mullemeck.build import build_dependencies
import os
import subprocess
import pytest
'''
    This file runs unit-tests on the build functions.
    It does so by cloning real and test repositories and
    then testing the functions on them.
    Test repository: 'https://github.com/SandstormVR/mullemeck-unit-tests'
'''


def test_clone_repo():
    """
    Tests the clone_repo() function with an invalid url, a valid url that is
    not a repo and finally a valid Url
    """
    # asserts that is catched ValueError 'Url not valid'
    with pytest.raises(ValueError):
        clone_repo('Not a URL', '215684ead')
    # Asserts that the clone was not successful and the clone path was erased
    # When a invalid url is given.
    success, logs, dir = clone_repo('https://google.com', 'commit')
    assert not success
    assert not os.path.isdir(dir)
    # asserts that with valid repo but invalid commit_id it won't be successful
    # (and checks that the path exists)
    success, logs, dir = clone_repo('https://github.com/hexadeciman/Snake',
                                    'latestSnake')
    assert success
    assert os.path.isdir(dir)
    # Remove the cloned repo to be able to run tests again. Otherwise throws
    # error because the path already exists and diretory not empty.
    subprocess.call('rm -rf /tmp/mullemeck/latestSnake', shell=True)

    success, logs, dir = clone_repo('https://github.com/hexadeciman/Snake',
                                    'e36d474082a8bddb0f04d114a24bdbbfc429a41b')
    print(logs)
    assert success
    assert os.path.isdir(dir)
    subprocess.call('rm -rf ' + dir, shell=True)


def test_build_dependencies():
    '''
        Clones a basic repo with nothing but some dependencies,
        and tries to run build_dependencies on it. Should pass.
    '''
    # Clone repo with nothing but some dependecies to install
    suc, logs, directory = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        '7ffb0ac9fe3fe05abdf688501d047ce501849a40')
    success, logs = build_dependencies(directory)

    # Remove the cloned repos before assertions to be able to run tests again.
    # Otherwise throw serror because the path
    # already exists and directory isn't empty.
    subprocess.call('rm -rf ' + directory, shell=True)

    assert success
    assert logs != ''


def test_build_static_checks():
    '''
        Tests if build_static_checks (pre-commit check) works as intended
    '''
    # Repo with pre-commit satisfied and no tests.
    suc, logs, success_directory = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        'f676b450172207f1e65f5a7e0574c0cde7baba42')

    # Repo with pre_commit error and no tests
    suc, logs, fail_directory = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        'a82b9b829d352901e0f37702f87186ca3234d35a')

    success1, logs1 = build_static_checks(success_directory)
    success2, logs2 = build_static_checks(fail_directory)

    # Remove the cloned repos before assertions to be able to run tests again.
    # Otherwise throw serror because the path
    # already exists and directory isn't empty.
    subprocess.call('rm -rf ' + success_directory, shell=True)
    subprocess.call('rm -rf ' + fail_directory, shell=True)

    assert success1
    assert logs1 != ''
    assert not success2
    assert logs2 != ''


def test_build_tests():
    '''
        Tests if build_tests (pytest) works as intended
    '''
    # Repo with valid test. Pre-commit runs
    suc, logs, success_directory = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        '25e0e252636172a2d38b4ca8b3ada3c60b211596')

    # Repo with invalid test. Pre-commit runs
    suc, logs, fail_directory = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        '76bfd501cf59e6b9380abab5fc508208cf7a1692')

    success1, logs1 = build_tests(success_directory)
    success2, logs2 = build_tests(fail_directory)

    # Remove the cloned repos before assertions to be able to run tests again.
    # Otherwise throw serror because the path
    # already exists and directory isn't empty.
    subprocess.call('rm -rf ' + success_directory, shell=True)
    subprocess.call('rm -rf ' + fail_directory, shell=True)

    assert success1
    assert logs1 != ''
    assert not success2
    assert logs2 != ''
