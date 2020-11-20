import logging
import os


def get_commit_id(wit_dir_path: str):

    original_path = os.getcwd()
    references_file = wit_dir_path + '\\references.txt'

    try:
        with open(references_file, 'r') as ref_file:
            content = ref_file.readline()

    except FileNotFoundError:
        logging.warning('references file does not exist.')
        return None

    else:
        content = content.split('=')
        content[1] = content[1].strip()
        commit_id = content[1]
        return commit_id

    finally:
        os.chdir(original_path)