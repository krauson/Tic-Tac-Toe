from commit_module import get_commit_id 
import logging
from add import get_folder_path, is_father_dir_exist
import os
from logging import DEBUG


logging.basicConfig(level=DEBUG)


def add_name_to_ref_file(wit_dir_path: str, branch_name: str) -> None:

    ref_file_path = os.path.join(wit_dir_path, 'references.txt')
    cur_commit_id = get_commit_id(wit_dir_path)
    content = branch_name + '=' + cur_commit_id + '\n'

    with open(ref_file_path, 'a') as ref_file:
        ref_file.write(content)
        logging.info('%s was added to references file.', branch_name)

def branch(branch_name: str):

    if is_father_dir_exist('.wit') is False:
        return

    wit_dir_path = get_folder_path('.wit')

    add_name_to_ref_file(wit_dir_path, branch_name)


os.chdir(r"C:\Users\Hagai\Desktop\week1\week1")
branch('Gadi')