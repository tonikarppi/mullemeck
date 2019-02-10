from mullemeck.build import clone_repo
from mullemeck.build import build_static_checks
from mullemeck.build import build_tests
from mullemeck.build import build_dependecies
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
    # repo with nothing but little dependecies to install
    suc, logs, dir = clone_repo('https://github.com/SandstormVR/\
                                mullemeck-unit-tests.git',
                                '7ffb0ac9fe3fe05abdf688501d047ce501849a40')
    directories['dir_dependecies_basics'] = dir
    # Repo with pre-commit satisfied and no tests.
    suc, logs, dir = clone_repo('https://github.com/SandstormVR/\
                                mullemeck-unit-tests.git',
                                'f676b450172207f1e65f5a7e0574c0cde7baba42')
    directories['dir_hello_world_no_tests'] = dir
    # Repo with pre_commit error and no tests
    suc, logs, dir = clone_repo('https://github.com/SandstormVR/\
                                mullemeck-unit-tests.git',
                                'a82b9b829d352901e0f37702f87186ca3234d35a')
    directories['dir_fail_hello_world_no_tests'] = dir
    # Repo with valid test. Pre-commit runs
    suc, logs, dir = clone_repo('https://github.com/SandstormVR/\
                                mullemeck-unit-tests.git',
                                '25e0e252636172a2d38b4ca8b3ada3c60b211596')
    directories['dir_hello_world_success_test'] = dir
    suc, logs, dir = clone_repo('https://github.com/SandstormVR/\
                                mullemeck-unit-tests.git',
                                '76bfd501cf59e6b9380abab5fc508208cf7a1692')
    directories['dir_hello_world_fail_test'] = dir

    return directories


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
    success, logs, dir = clone_repo('https://github.com/hexadeciman/Snake.git',
                                    'latestSnake')
    assert success
    assert os.path.isdir(dir)
    # Remove the cloned repo to be able to run tests again. Otherwise throws
    # error because the path already exists and diretory not empty.
    subprocess.call('rm -rf /tmp/mullemeck/latestSnake', shell=True)

    success, logs, dir = clone_repo('https://github.com/hexadeciman/Snake.git',
                                    'e36d474082a8bddb0f04d114a24bdbbfc429a41b')
    print(logs)
    assert success
    assert os.path.isdir(dir)
    subprocess.call('rm -rf ' + dir, shell=True)


def test_build_dependencies():
    success, logs = build_dependecies('random/path/to/nowhere')
    assert not success
    assert logs != ''


def test_build_static_checks():
    success, logs = build_static_checks('random/path/to/nowhere')
    assert not success
    assert logs != ''


def test_build_tests():
    success, logs = build_tests('random/path/to/nowhere')
    assert not success
    assert logs != ''
