from commit_module import get_commit_id
from checkout import get_activated_branch_name
from add import get_folder_path, is_father_dir_exist
import datetime
import logging
import random
import os
import distutils.dir_util


def get_rand_nums(char_length):

    rand_nums = ""
    i = 0
    while i < char_length:
        cur_num = chr(random.randint(48, 57))
        rand_nums += cur_num
        i += 1

    return rand_nums


def get_rand_letter(char_length):

    rand_letterS = ""
    i = 0
    while i < char_length:
        cur_char = chr(random.randint(97, 102))
        rand_letterS += cur_char
        i += 1

    return rand_letterS


def create_commit_id_dir(wit_dir_path: str):
    NUMBER_OF_CHARS = 20
    commit_id = get_rand_letter(NUMBER_OF_CHARS) + get_rand_nums(NUMBER_OF_CHARS)
    images_dir_path = wit_dir_path + '\\images'
    os.mkdir(images_dir_path + '\\' + commit_id)
    logging.debug(f'commit_id {commit_id} created.')

    return commit_id


def create_metadata_file(commit_id: str, message: str, wit_dir_path: str) -> None:

    former_commit_id = get_former_commit_id(wit_dir_path)

    commit_id_meta_file = os.path.join(wit_dir_path, 'images', commit_id) + '.txt'
    with open(commit_id_meta_file, 'w') as metadata_file:
        parent = str(former_commit_id)

        time = str(datetime.datetime.now())

        content = 'Parent=' + parent + '\nTime=' + time + '\nMessage=' + message + '\n'
        metadata_file.write(content)
        logging.info('Metadata file has been created')


def copy_from_staging_area(wit_dir_path, commit_id):

    staging_area_path = os.path.join(wit_dir_path, 'staging_area')
    commit_id_path = os.path.join(wit_dir_path, 'images', commit_id)
    distutils.dir_util.copy_tree(staging_area_path, commit_id_path)
    logging.debug('Snapshot of staging_area, has succeeded')


def is_activated_branch_same_as_head():

    """return true if branch point to same dir as head in references file."""

    wit_dir_path = get_folder_path('.wit')
    activated_file_path = os.path.join(wit_dir_path, 'activated.txt')
    ref_file_path = os.path.join(wit_dir_path, 'references.txt')

    with open(activated_file_path, 'r') as activated_file:
        activated = activated_file.read()
    
        with open(ref_file_path, 'r') as ref_file:
            content = ref_file.readline().split('=')
            head = content[1].strip()
            return head == activated


def write_to_activated_file(activated_branch: str) -> None:

    wit_dir_path = get_folder_path('.wit')
    activated_file_path = os.path.join(wit_dir_path, 'activated.txt')
    with open(activated_file_path, 'w') as activated_file:
        activated_file.write(activated_branch)


def is_activated(wit_dir_path, branch_name):

    activated_file_path = os.path.join(wit_dir_path, 'activated.txt')
    with open(activated_file_path, 'r') as activated_file:
        activated_name = activated_file.read()

    return branch_name == activated_name





def get_former_commit_id(wit_dir_path: str) -> str:

    ref_path = os.path.join(wit_dir_path, 'references.txt')

    try:
        with open(ref_path, 'r') as ref_file:
            content = ref_file.readline()

    except FileNotFoundError:
        logging.info('File references is not exist yet.')
        return None

    else:
        former_commit_id = content.split('=')[1].strip()
        return former_commit_id


def update_activated_branch_in_ref_file(new_commit_id):

    """Update the value of the activated branch in references file. according to head."""

    activated_branch = get_activated_branch_name()
    wit_dir_path = get_folder_path('.wit')
    ref_file_path = os.path.join(wit_dir_path, 'references.txt')
    with open(ref_file_path, 'r') as ref_file:

        content = ref_file.readlines()
        i = 0
        while i < len(content):
            content[i] = content[i].split('=')
            i += 1

        dict_content = dict(content)
        if activated_branch != '':
            dict_content[activated_branch] = new_commit_id

    content =''
    for k, v in dict_content.items():

        content += k + '=' + v

    with open(ref_file_path, 'w') as ref_file:

        ref_file.write(content)


def create_new_ref_file(file_path, new_commit_id):

    content = 'HEAD=' + new_commit_id + '\n' + 'master=' + new_commit_id + '\n'

    with open(file_path, 'w') as ref_file:

        ref_file.write(content)


def write_to_references_file(wit_dir_path: str, new_commit_id: str):

    file_path = wit_dir_path + '\\references.txt'

    try:
        with open(file_path, 'r')as ref_file:
            content = ref_file.readlines()

    except FileNotFoundError:
        create_new_ref_file(file_path, new_commit_id)

    else:
        former_master_commit_id = content[1].strip().split('=')[1]
        head = 'HEAD=' + new_commit_id + '\n'
        master = 'master='

        if is_activated(wit_dir_path, 'master'):
            master += new_commit_id + '\n'

        else:
            master += former_master_commit_id + '\n'
            update_activated_branch_in_ref_file(new_commit_id)

        with open(file_path, 'r') as references_file:
            content = references_file.readlines()
            branches = ''
            if len(content) > 2:
                branches = content[2:]
                branches = '/n'.join(branches)
                
            content = head + master + branches
            with open(file_path, 'w') as references_file:
                references_file.write(content)


def commit(message: str):
    """Creates a saving point to get back to"""

    if is_father_dir_exist('.wit'):
        logging.debug('.wit dir was found!')

    else:
        logging.error('.wit dir was not found. exit program..')
        return

    wit_dir_path = get_folder_path('.wit')

    commit_id = create_commit_id_dir(wit_dir_path)

    create_metadata_file(commit_id, message, wit_dir_path)

    copy_from_staging_area(wit_dir_path, commit_id)

    write_to_references_file(wit_dir_path, commit_id)