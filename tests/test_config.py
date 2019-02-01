import configparser
from mullemeck import config
from pathlib import Path
import subprocess

"""
    Verifies that config reads correctly,
    And that clone directory is created
"""

tmp_file = ".tmp_config"
original_file = ""


def setup_module(module):
    "Changes config file for testing"
    global original_file
    original_file = config.CONFIG_FILE_PATH
    config.CONFIG_FILE_PATH = tmp_file


def teardown_module(module):
    "reverts to old test file"
    subprocess.run(["rm", config.CONFIG_FILE_PATH])
    config.CONFIG_FILE_PATH = original_file


def test_create_config():
    config.read()
    assert Path(config.CONFIG_FILE_PATH).is_file()


def test_read_config():
    writtenConfig = configparser.ConfigParser()
    data = {
        "DBReadUser": "abc",
        "DBReadUserPassword": "123",
        "DBWriteUser": "cde",
        "DBWriteUserPassword": "123",
        "CloneDirectory": "/tmp/test",
        "DBName": "testdb"
    }
    writtenConfig["DEFAULT"] = data

    with open(tmp_file, 'w') as configfile:
        writtenConfig.write(configfile)

    config.CONFIG_FILE_PATH = tmp_file
    config.read()
    assert config.DB_READ_USER == data["DBReadUser"]
    assert config.DB_READ_USER_PASSWORD == data["DBReadUserPassword"]
    assert config.DB_WRITE_USER == data["DBWriteUser"]
    assert config.DB_WRITE_USER_PASSWORD == data["DBWriteUserPassword"]
    assert config.CLONE_DIRECTORY == data["CloneDirectory"]
    assert config.DB_NAME == data["DBName"]
