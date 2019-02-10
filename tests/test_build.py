from mullemeck.build import clone_repo
from mullemeck.build import build_static_checks
from mullemeck.build import build_tests
from mullemeck.build import build_dependencies
import os
import subprocess
import pytest


def create_repos_for_unit_tests():
    """
    This function clones simple repos to run unit tests on the build.
    It clones mullemeck-unit-tests repo and returns the directories in which
    each relevant repo state is.
    """
    directories = {}
    # repo with nothing but little dependencies to install
    suc, logs, dir = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        '7ffb0ac9fe3fe05abdf688501d047ce501849a40')
    directories['dir_dependencies_basics'] = dir
    # Repo with pre-commit satisfied and no tests.
    suc, logs, dir = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        'f676b450172207f1e65f5a7e0574c0cde7baba42')
    directories['dir_hello_world_no_tests'] = dir
    # Repo with pre_commit error and no tests
    suc, logs, dir = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        'a82b9b829d352901e0f37702f87186ca3234d35a')
    directories['dir_fail_hello_world_no_tests'] = dir
    # Repo with valid test. Pre-commit runs
    suc, logs, dir = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        '25e0e252636172a2d38b4ca8b3ada3c60b211596')
    directories['dir_hello_world_success_test'] = dir
    suc, logs, dir = clone_repo(
        'https://github.com/SandstormVR/mullemeck-unit-tests',
        '76bfd501cf59e6b9380abab5fc508208cf7a1692')
    directories['dir_hello_world_fail_test'] = dir
    print('Hello world')
    return directories


directories_unit_tests = create_repos_for_unit_tests()


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
    assert success
    assert os.path.isdir(dir)
    subprocess.call('rm -rf ' + dir, shell=True)


def test_build_dependencies():

    success, logs = build_dependencies('path/to/nowhere')
    assert not success
    assert logs != ''

    success, logs = build_dependencies(
        directories_unit_tests['dir_dependencies_basics'])
    assert success
    assert logs != ''


def test_build_static_checks():
    success, logs = build_static_checks('random/path/to/nowhere')
    assert not success
    assert logs != ''


def test_build_tests():
    success, logs = build_tests('random/path/to/nowhere')
    assert not success
    assert logs != ''


def test_remove_directories_unit_tests():
    """
    This function is executed in last as it removes all repos cloned for unit
    testing purposes
    """
    for x in directories_unit_tests:
        subprocess.call('rm -rf ' + directories_unit_tests[x], shell=True)
