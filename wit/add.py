import logging
import os
import shutil
import distutils.dir_util
from init import FolderNotFound


def get_folder_path(folder_name: str):

    """return the path to certain folder in the folders tree, if not found
        in this directory, will search in father directories."""
    original_path = os.getcwd()

    while True:
        cwd = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))

        os.chdir(parent_dir)

        if cwd == parent_dir:
            raise FolderNotFound('.wit dir not found, exiting program..')

        for cur_file in os.listdir():
            if cur_file == folder_name:
                logging.debug(f'Found {folder_name} folder!')

                folder_to_seach_path = os.getcwd() + '\\' + folder_name
                os.chdir(original_path)

                return folder_to_seach_path


def is_father_dir_exist(filename_to_search: str):

    original_location = os.getcwd()

    logging.debug('Im in is_father_exist func')
    if os.path.isfile(filename_to_search):
        dir_path = get_file_dir_path(filename_to_search)
        os.chdir(dir_path)

    while True:
        cwd = os.getcwd()
        for cur_file in os.listdir():
            if cur_file == filename_to_search:
                os.chdir(original_location)
                return True

        parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))
        if cwd == parent_dir:
            raise FolderNotFound('.wit dir not found, exiting program..')

        os.chdir(parent_dir)


def get_file_dir_path(data_to_copy_path):
    path = data_to_copy_path.split('\\')
    path = path[:len(path) - 1]
    path = '\\'.join(path)
    return path


def get_folders_tree(data_to_copy_path: str):

    logging.debug('Im in get_folders_tree func.')

    original_location = os.getcwd()

    if os.path.isfile(data_to_copy_path):
        path = get_file_dir_path(data_to_copy_path)
        os.chdir(path)  # start looking from the folder of the file you want to copy

    else:
        try:
            os.chdir(data_to_copy_path)  # start looking from the folder you want to copy

        except OSError:
            raise NotADirectoryError(f'{data_to_copy_path}\n  is not a directory.')

    relative_folders_tree = []
    while True:

        cur_files = os.listdir()
        for cur_file in cur_files:
            if cur_file == '.wit':
                os.chdir(original_location)
                return relative_folders_tree

        cwd = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))
        dir_name = os.path.basename(cwd)
        relative_folders_tree.append(dir_name)

        if cwd == parent_dir:
            raise FolderNotFound('.wit dir not found, exiting program..')

        os.chdir(str(parent_dir))


def build_dir_tree(relative_folders_tree: list, backup_folder_path: str):

    os.chdir(backup_folder_path)
    os.makedirs(relative_folders_tree, exist_ok=True)


def get_dest(backup_folder_path, relative_folders_tree):

    if len(relative_folders_tree) > 0:
        dest = backup_folder_path + '\\' + relative_folders_tree

    else:
        dest = backup_folder_path

    return dest


def organize_folders_tree(relative_folders_tree: list) -> str:
    relative_folders_tree = relative_folders_tree[::-1]
    relative_folders_tree = '\\'.join(relative_folders_tree)
    return relative_folders_tree


def copy(data_to_copy_path, relative_folders_tree):

    backup_folder_path = get_folder_path('.wit') + '\\staging_area'

    if len(relative_folders_tree) > 0:
        relative_folders_tree = organize_folders_tree(relative_folders_tree)
        build_dir_tree(relative_folders_tree, backup_folder_path)

    dest = get_dest(backup_folder_path, relative_folders_tree)

    if os.path.isfile(data_to_copy_path):

        shutil.copy(data_to_copy_path, dest)
        logging.info('The file and its father dirs has been copied succussfully.')

    elif os.path.isdir(data_to_copy_path):

        distutils.dir_util.copy_tree(data_to_copy_path, dest)

        logging.info('The folder tree has been copied succussfully.')


def add(data_to_copy_path: str):

    if is_father_dir_exist('.wit') is False:
        return

    folders_tree = get_folders_tree(data_to_copy_path)

    copy(data_to_copy_path, folders_tree)