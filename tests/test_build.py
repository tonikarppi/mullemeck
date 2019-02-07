from mullemeck.build import clone_repo
from mullemeck.build import build_static_checks
from mullemeck.build import build_tests
import os
import subprocess
import pytest


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
    # asserts that the clone is successful (and checks that the path exists)
    success, logs, dir = clone_repo('https://github.com/hexadeciman/Snake.git',
                                    'latestSnake')
    assert success
    assert os.path.isdir(dir)
    # Remove the cloned repo to be able to run tests again. Otherwise throws
    # error because the path already exists and diretory not empty.
    subprocess.call('rm -rf /tmp/mullemeck/latestSnake', shell=True)


def test_build_static_checks():
    success, logs = build_static_checks('random/path/to/nowhere')
    assert not success
    assert logs != ''
    # runs on private repo. Should not work
    clone_repo('https://github.com/tonikarppi/dd2480-lab1.git', 'privaterepo')
    success, logs = build_static_checks('tmp/mullemeck/privatrepo')
    assert not success
    assert logs != ''


def test_build_tests():
    success, logs = build_tests('random/path/to/nowhere')
    assert not success
    assert logs != ''
