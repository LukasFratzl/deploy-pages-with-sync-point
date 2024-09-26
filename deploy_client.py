import os
from pathlib import Path
from sys import argv
import shutil
import json
from datetime import datetime

# CONFIG -> Nextcloud or basically any root folder where you store your files
# this is the default dir if -r, --root is not defined
ROOT_DIR = '/No/Valid/Path/'
TARGET_SYNC_POINT = '/No/Valid/Path/'

TEMP_FILE_NAME = 'deploy_client_file_{0}'  # needs to be without extension and identical in the server

CONVERT_IGNORE_FOLDERS = ['']  # In this case it's '/ROOT_DIR/.../Ignore File Name

ROOT_DIR_ARG_SYN = ['-r', '--root']
SYNC_POINT_SYN = ['-s', '--sync_point']
# command needs to be a shell script on the server or anything which is like physical on the server callable
CMD_ARG_SYN = ['-c', '--command']

TARGET_CMD = ''

# Needs to be identical in the server
JSON_INVOKE_AFTER_PATH = 'Invoke After'

global file_sync


def normalize_path(path_str):
    path_str = os.path.normpath(path_str)
    path_str = os.path.normcase(path_str)
    return path_str


class FileSync:
    def __init__(self):
        pass

    def zip_root_dir(self):
        current_time = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        root_dir = Path(ROOT_DIR)
        zip_file_name = Path(normalize_path(Path.joinpath(root_dir.parent.absolute(), TEMP_FILE_NAME.format(current_time) + '.zip')))
        if zip_file_name.is_file():
            os.remove(zip_file_name)
        info_file_name = normalize_path(Path.joinpath(root_dir, 'deploy_client_info.json'))
        info_json = {JSON_INVOKE_AFTER_PATH: TARGET_CMD}
        with open(info_file_name, 'w') as f:
            json.dump(info_json, f)
        zip_file_base_name = Path(normalize_path(Path.joinpath(root_dir.parent.absolute(), TEMP_FILE_NAME.format(current_time))))
        shutil.make_archive(str(zip_file_base_name.absolute()), 'zip', root_dir.absolute())
        print('zip file created at:', zip_file_name.absolute())
        return zip_file_name


    def send_to_target(self, zip_file_name):
        if not zip_file_name.is_file():
            return False
        shutil.move(zip_file_name, TARGET_SYNC_POINT)
        return True


if __name__ == '__main__':
    args = argv[1:]
    if len(args) % 2 == 1:
        print('You called an arg but miss the value .. ')
    for argi in range(len(args)):
        # Needs to be just every periodic arg to check
        if argi % 2 == 0:
            arg_lower = args[argi].lower()
            for arg in ROOT_DIR_ARG_SYN:
                if arg_lower == arg:
                    path = args[argi + 1].replace('\'', '').replace('"', '')
                    if os.path.isdir(path):
                        ROOT_DIR = path

            for arg in SYNC_POINT_SYN:
                if arg_lower == arg:
                    sync_point = args[argi + 1].replace('\'', '').replace('"', '')
                    TARGET_SYNC_POINT = sync_point

            for arg in CMD_ARG_SYN:
                if arg_lower == arg:
                    cmd = args[argi + 1].replace('\'', '').replace('"', '')
                    TARGET_CMD = cmd

    ROOT_DIR = normalize_path(ROOT_DIR)
    TARGET_SYNC_POINT = normalize_path(TARGET_SYNC_POINT)

    print('Using root dir ->', ROOT_DIR)
    print('Using sync point ->', TARGET_SYNC_POINT)
    print('Using Target Command ->', TARGET_CMD)

    if not os.path.isdir(ROOT_DIR):
        print('No Valid Root Directory ... Please check your root path argument..., sometimes you may need to add "" or \'\' like "/Path/"')
        err = 'err'
        int(err)

    file_sync = FileSync()

    zip_file_path = file_sync.zip_root_dir()
    if file_sync.send_to_target(zip_file_path):
        print('Deploy finished')
