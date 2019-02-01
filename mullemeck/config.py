import configparser
from pathlib import Path
from psycopg2 import connect
CONFIG_FILE_PATH = "mulle.cfg"

DB_READ_USER = ""
DB_READ_USER_PASSWORD = ""
DB_WRITE_USER = ""
DB_WRITE_USER_PASSWORD = ""
DB_NAME = "mulledb"

CLONE_DIRECTORY = "/tmp/mulle/"


def read():
    """
        Reads a config from `CONFIG_FILE_PATH`
        If it does not exist a default config is written
    """
    global DB_READ_USER
    global DB_READ_USER_PASSWORD
    global DB_WRITE_USER
    global DB_WRITE_USER_PASSWORD
    global CLONE_DIRECTORY
    global DB_NAME

    config = configparser.ConfigParser()
    config_file = Path(CONFIG_FILE_PATH)
    if not config_file.is_file():
        print("No config Found in {}. Writing defaults"
              .format(CONFIG_FILE_PATH))
        config["DEFAULT"] = {
            "DBReadUser": "",
            "DBReadUserPassword": "",
            "DBWriteUser": "",
            "DBWriteUserPassword": "",
            "CloneDirectory": CLONE_DIRECTORY,
            "DBName": DB_NAME
        }
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(CONFIG_FILE_PATH)
        DB_READ_USER = config["DEFAULT"]["DBReadUser"]
        DB_READ_USER_PASSWORD = config["DEFAULT"]["DBReadUserPassword"]
        DB_WRITE_USER = config["DEFAULT"]["DBWriteUser"]
        DB_WRITE_USER_PASSWORD = config["DEFAULT"]["DBWriteUserPassword"]
        CLONE_DIRECTORY = config["DEFAULT"]["CloneDirectory"]
        DB_NAME = config["DEFAULT"]["DBName"]

    return validate()


def validate():
    return True


def get_db_connection():
    """
        Returns a psycopg2 connection with read permission
    """
    return connect(f'DB_NAME={DB_NAME} \
        user={DB_READ_USER} password={DB_READ_USER_PASSWORD}')


def get_db_write_connection():
    """
        Returns a psycopg2 connection with write permission
    """
    return connect(f'DB_NAME={DB_NAME} \
        user={DB_WRITE_USER} password={DB_WRITE_USER_PASSWORD}')
