from commit_module import get_commit_id
import logging
import os
import pathlib
from status import get_changes_not_staged_for_commit, get_files_to_be_commited
from add import get_folder_path, is_father_dir_exist
import distutils.dir_util
from distutils.errors import DistutilsFileError


def is_ok_for_checkout():

    """return False if
        1.There are changes to be commited.
        2.There are changes not staged for commit.

        this function prevent to do checkout in situations that might lead to information loss.

        return True otherwise.
    """
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

    return len(changes_to_be_commited) == 0 and len(changes_not_staged_for_commit) == 0


def update_head(wit_dir_path: str, branch_commit_id: str) -> None:

    ref_path = wit_dir_path + '\\references.txt'
    head = 'HEAD=' + branch_commit_id + '\n'

    with open(ref_path, 'r') as references_file:
        content = references_file.readlines()[1:]
        content = ''.join(content)

    content = head + content
    with open(ref_path, 'w') as references_file:
        references_file.write(content)

def update_original_dir_wit_according_to_checkout(wit_dir_path: str, parameter: str) -> None:

    original_dir_path = str(pathlib.Path(wit_dir_path).parents[0])
    commit_id_path = wit_dir_path + '\\images\\' + parameter

    try:
        distutils.dir_util.copy_tree(commit_id_path, original_dir_path)

    except DistutilsFileError:
        logging.error('commit id dir does not exist')
        raise FileNotFoundError

    else:
        logging.info('Checkout was succeeded')


def change_staging_area_content(wit_dir_path: str, parameter :str) -> None:

    staging_area_path = os.path.join(wit_dir_path, 'staging_area')

    commit_id_path = wit_dir_path + '\\images\\' + parameter

    distutils.dir_util.remove_tree(staging_area_path)
    distutils.dir_util.copy_tree(commit_id_path, staging_area_path)
    logging.info('Staging_area dir now have the content of the last commit id dir.')


def erase_activated_file(wit_dir_path: str) -> None:

    activated_file_path = os.path.join(wit_dir_path, 'activated.txt')
    with open(activated_file_path, 'w') as activated_file:
        activated_file.write('')


def is_branch_name_exist(parameter: str) -> bool:
    wit_dir_path = get_folder_path('.wit')

    ref_file_path = os.path.join(wit_dir_path, 'references.txt')

    with open(ref_file_path, 'r') as ref_file:

        content = ref_file.readlines()
        i = 0
        while i < len(content):
            content[i] = content[i].split('=')
            i += 1

        content = dict(content)
        print(content)

        return parameter in content



def get_activated_branch_name() -> str:
    """returns the name of the activated branch form the references file
        if not exist returns None."""
    wit_dir_path = get_folder_path('.wit')

    activated_file_path = os.path.join(wit_dir_path, 'activated.txt')
    with open(activated_file_path, 'r') as activated_file:

        activated_name = activated_file.read()
        return activated_name


def write_to_activated_file(activated_branch: str) -> None:

    wit_dir_path = get_folder_path('.wit')
    activated_file_path = os.path.join(wit_dir_path, 'activated.txt')
    with open(activated_file_path, 'w') as activated_file:
        activated_file.write(activated_branch)

def get_commit_id_from_activated_branch():

    activated_branch = get_activated_branch_name()

    if activated_branch == '':
        print('There is no activated branch.')
        return None
    wit_dir_path = get_folder_path('.wit')
    ref_file_path = os.path.join(wit_dir_path, 'references.txt')

    with open(ref_file_path, 'r') as ref_file:

        content = ref_file.readlines()
        i = 0
        while i < len(content):
            content[i] = content[i].split('=')
            i += 1

        dict_content = dict(content)

        try:
            commit_id_of_activated_branch = dict_content[activated_branch].strip()

        except KeyError:
            print('%s does not exist in the references file.', activated_branch)
            raise KeyError

        else:
            return commit_id_of_activated_branch

def checkout(parameter: str):

    COMMIT_ID_LENGTH = 40

    if is_father_dir_exist('.wit') is False:
        return

    if is_ok_for_checkout() is False:
        logging.error("""
        There are changes to be commited
        or there are changes_staged_for commit, checkout failed""")
        return

    wit_dir_path = get_folder_path('.wit')

    if parameter == 'master':
        parameter = get_commit_id(wit_dir_path)

    if len(parameter) == COMMIT_ID_LENGTH:  # checkout commit_id

        update_head(wit_dir_path, parameter)
        erase_activated_file(wit_dir_path)

    else:  # checkout branch_name

        if is_branch_name_exist(parameter):
            write_to_activated_file(parameter)
            # update_head(wit_dir_path, parameter)

            # branch_commit_id = get_commit_id_from_activated_branch()
            # if branch_commit_id != None:
        else:
            print('%s does not appear in references file.', parameter)

    temp =  get_commit_id_from_activated_branch()

    if temp != None:
        parameter = temp

    update_original_dir_wit_according_to_checkout(wit_dir_path, parameter)

    change_staging_area_content(wit_dir_path, parameter)


    activated_branch_name = get_activated_branch_name()

    if activated_branch_name is None:
        logging.info('There is no activated branch right now.')
        return
