import logging
from commit_module import get_commit_id
import pathlib
from add import get_folder_path, is_father_dir_exist
import filecmp
import os
from typing import List, Tuple


def get_files(path_to_dir):

    for _root, _dirs, files in os.walk(path_to_dir):
        return files


def get_files_to_be_commited(dir1: str, dir2: str, files_to_be_commited: List[str]) -> list:

    """Compare between two dirs and returns recursively the names of the files that:
    1.appears only in the left dir.
    2.have same name but different content.
    """

    dir_cmp_object = filecmp.dircmp(dir1, dir2)

    for file in dir_cmp_object.diff_files:
        files_to_be_commited.append(file)

    for file in dir_cmp_object.left_only:
        if os.path.isdir(file):
            path_to_dir = os.path.join(dir1, file)
            files_to_be_commited += get_files(path_to_dir)

        else:
            files_to_be_commited.append(file)

    for common_file in dir_cmp_object.common_dirs:

        subdir1 = os.path.join(dir1, common_file)
        subdir2 = os.path.join(dir2, common_file)

        get_files_to_be_commited(subdir1, subdir2, files_to_be_commited)

    return files_to_be_commited


def get_changes_not_staged_for_commit(dir1: str, dir2: str, files_not_staged_for_commit: List[str]) -> list:

    """Returns recursively the names of the files that
        have same names but different content and appear in both dirs.
    """

    dir_cmp_object = filecmp.dircmp(dir1, dir2)

    for file in (dir_cmp_object.diff_files):
        files_not_staged_for_commit.append(file)

    for common_file in dir_cmp_object.common_dirs:

        subdir1 = os.path.join(dir1, common_file)
        subdir2 = os.path.join(dir2, common_file)

        get_changes_not_staged_for_commit(subdir1, subdir2, files_not_staged_for_commit)

    return files_not_staged_for_commit


def get_untraecked_files(dir1: str, dir2: str, untracked_files: List[str]) -> list:

    """Returns recursively the names of the files that
        apears only in dir1 and it's subdirs.
    """

    dir_cmp_object = filecmp.dircmp(dir1, dir2)

    for file in (dir_cmp_object.left_only):
        untracked_files.append(file)

    for common_file in dir_cmp_object.common_dirs:

        subdir1 = os.path.join(dir1, common_file)
        subdir2 = os.path.join(dir2, common_file)

        get_untraecked_files(subdir1, subdir2, untracked_files)

    return untracked_files


def print_status(commit_id: str, changes_to_be_commited: List[str],
                changes_not_staged_for_commit: List[str],
                untracked_files: List[str]) -> Tuple[List, List]:

    print(f'\n\nCurrent commit id(Head):\t {commit_id}')

    print('*' * 90)
    print('Changes_to_be_commited:\n')

    for file in changes_to_be_commited:
        print(file)

    print('*' * 90)
    print('Changes_not_staged_for_commit:\n')

    for file in changes_not_staged_for_commit:
        print(file)
    print('*' * 90)

    print('Untracked_files:\n')

    for file in untracked_files:
        print(file)

    print('*' * 90)



def status():

    if is_father_dir_exist('.wit') is False:
        return

    wit_dir_path = get_folder_path('.wit')

    data_to_copy_path = pathlib.Path(wit_dir_path).parent

    commit_id = get_commit_id(wit_dir_path)

    if commit_id is None:
        logging.error('There was no commit yet. exiting program..')
        return

    staging_area_path = wit_dir_path + '\\staging_area'
    commit_id_path = wit_dir_path + '\\images\\' + commit_id

    files = []

    changes_to_be_commited = get_files_to_be_commited(staging_area_path, commit_id_path, files.copy())

    changes_not_staged_for_commit = get_changes_not_staged_for_commit(staging_area_path, data_to_copy_path, files.copy())

    untracked_files = get_untraecked_files(data_to_copy_path, staging_area_path, files.copy())

    print_status(commit_id, changes_to_be_commited, changes_not_staged_for_commit, untracked_files)

    return changes_to_be_commited, changes_not_staged_for_commit
