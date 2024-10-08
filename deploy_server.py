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
TEMP_FILE_NAME = 'deploy_client_file_'

# Needs to be identical in the client
JSON_INVOKE_AFTER_PATH = 'Invoke After'
JSON_META_COLLECTION_NAME = 'Computed Items'


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

        collection_json_name = normalize_path(Path.joinpath(Path(SYNC_POINT_DIR), 'deploy_meta.json'))
        if Path(collection_json_name).is_file():
            with open(collection_json_name, 'r') as f:
                meta_data_json = json.load(f)
        else:
            meta_data_json = {JSON_META_COLLECTION_NAME: []}

        if JSON_META_COLLECTION_NAME in meta_data_json and file_abs_path in meta_data_json[JSON_META_COLLECTION_NAME]:
            return False
        if JSON_META_COLLECTION_NAME not in meta_data_json:
            meta_data_json[JSON_META_COLLECTION_NAME] = [file_abs_path]
        else:
            meta_data_json[JSON_META_COLLECTION_NAME].append(file_abs_path)

        with open(collection_json_name, 'w') as f:
            json.dump(meta_data_json, f)

        temp_dir_name = normalize_path(Path.joinpath(Path(SYNC_POINT_DIR).parent.absolute(), "deploy_client_temp_file_dir"))

        print('Unpacking archive to:', temp_dir_name)
        shutil.unpack_archive(file_abs_path, temp_dir_name, 'zip')

        temp_info_file_name = normalize_path(Path.joinpath(Path(temp_dir_name), 'deploy_client_info.json'))

        if not Path(temp_info_file_name).is_file():
            # If there is no info file the whole extracted archive is pretty useless for this deploy system
            # as it depending on server scripts, so clean up and exclude it
            for filename in os.listdir(temp_dir_name):
                file_path = os.path.join(temp_dir_name, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

            try:
                os.removedirs(temp_dir_name)
            except Exception as e:
                print('Failed to delete temp dir %s. Reason: %s' % (temp_dir_name, e))

            print('An archive without an info file got detected ... excluding it')
            return False

        with open(temp_info_file_name, 'r') as f:
            data = json.load(f)

        if Path(temp_info_file_name).is_file():
            os.remove(temp_info_file_name)

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
