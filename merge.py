import os
from branch import branch
from add import get_folder_path, is_father_dir_exist
from commit_module import get_commit_id


wit_dir_path = get_folder_path('.wit')

def get_branch_commit_id(branch_name: str) -> str:
    
    ref_file_path = os.path.join(wit_dir_path, 'references.txt')

    with open(ref_file_path, 'r') as ref_file:

        content = ref_file.readlines()
        i = 0
        while i < len(content):
            content[i] = content[i].split('=')
            i += 1

        dict_content = dict(content)

        try:
            branch_commit_id = dict_content[branch_name].strip()

        except KeyError:
            print('%s does not exist in the references file.', branch_name)
            raise KeyError

        else:
            return branch_commit_id


def get_parent_commit_id(commit_id: str) -> str:
    pass


def get_common_base(branch_name: str) -> str:

    head_commit_id = get_commit_id(wit_dir_path)
    branch_commit_id = get_branch_commit_id(branch_name)

    head_index = head_commit_id
    branch_index = branch_commit_id

    while branch_index != None:

        if head_index == branch_index:
            return head_index

        else:



def merge(branch_name: str) -> None:



    if is_father_dir_exist('.wit') is False:
        return

    common_base = get_common_base(branch_name)