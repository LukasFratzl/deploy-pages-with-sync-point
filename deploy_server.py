import os
from pathlib import Path
import json
import shutil
from sys import argv
from time import sleep

SYNC_POINT_DIR = '/No/Valid/Path/'

CONVERT_IGNORE_FOLDERS = ['']  # In this case it's '/ROOT_DIR/.../Ignore File Name

SYNC_POINT_SYN = ['-s', '--sync_point']

# needs to be without extension and needs to be identical in the client except including {0}
TEMP_FILE_NAME = 'deploy_client_file_123454321_'

# Needs to be identical in the client
JSON_INVOKE_AFTER_PATH = 'Invoke After'


def run_command(cmd):
    process = os.popen(cmd)

    output = process.read()
    process.close()

    return output.strip()


def normalize_path(path_str):
    path_str = os.path.normpath(path_str)
    path_str = os.path.normcase(path_str)
    return str(path_str)


class FileSync:
    def __init__(self):
        self.ignore_path_folders = []
        for folder in CONVERT_IGNORE_FOLDERS:
            self.ignore_path_folders.append(normalize_path('/' + folder + '/'))
        self.files_mtimes = dict(file_path='', mtime=-1)

    def file_action(self, file_path):
        if not file_path.is_file():
            return False

        file_abs_path = str(file_path.absolute())

        if not file_abs_path.endswith('.zip'):
            return False

        file_mtime = os.path.getmtime(file_path)
        if file_abs_path in self.files_mtimes:
            if self.files_mtimes[file_abs_path] == file_mtime:
                return False
        self.files_mtimes[file_abs_path] = file_mtime

        for folder in self.ignore_path_folders:
            if folder in file_abs_path:
                return False

        if TEMP_FILE_NAME not in file_path.name:
            return False

        temp_dir_name = normalize_path(Path.joinpath(Path(SYNC_POINT_DIR).parent.absolute(), "deploy_client_temp_file_dir"))

        print('Unpacking archive to:', temp_dir_name)
        shutil.unpack_archive(file_abs_path, temp_dir_name, 'zip')

        os.remove(file_abs_path)

        temp_info_file_name = normalize_path(Path.joinpath(Path(temp_dir_name), 'deploy_client_info.json'))
        with open(temp_info_file_name, 'r') as f:
            data = json.load(f)

        if JSON_INVOKE_AFTER_PATH in data and data[JSON_INVOKE_AFTER_PATH] != '':
            cmd_file = data[JSON_INVOKE_AFTER_PATH]
            # Only run stuff if the file is actually on the server and is not inside the sync dir
            if Path(cmd_file).is_file() and SYNC_POINT_DIR not in cmd_file:
                print(run_command('"' + cmd_file + '"'))

        print('Finished deploy')

        return True

    def scan_files(self):
        for path in os.scandir(SYNC_POINT_DIR):
            if not path.is_dir():
                self.file_action(Path(path.path))


if __name__ == '__main__':

    args = argv[1:]
    if len(args) % 2 == 1:
        print('You called an arg but miss the value .. ')
    for argi in range(len(args)):
        # Needs to be just every periodic arg to check
        if argi % 2 == 0:
            arg_lower = args[argi].lower()

            for arg in SYNC_POINT_SYN:
                if arg_lower == arg:
                    dir = args[argi + 1].replace('\'', '').replace('"', '')
                    SYNC_POINT_DIR = dir

    print('Enable Sync Point at:', SYNC_POINT_DIR)

    file_sync = FileSync()

    try:
        while True:
            file_sync.scan_files()
            sleep(0.5)
    except KeyboardInterrupt:
        pass
