from commit_module import get_commit_id
import logging
from graphviz import Digraph
from add import get_folder_path, is_father_dir_exist
import os


def get_parent_commit_id(wit_dir_path, commit_id: str)-> str:

    metadata_path = os.path.join(wit_dir_path, 'images', commit_id) + '.txt'

    with open(metadata_path, 'r') as metadata_file:

        content = metadata_file.readlines()
        parent_commit_id = content[0].split('=')[1].strip()

        return parent_commit_id

def get_master_id(wit_dir_path: str) -> str:

    ref_path = os.path.join(wit_dir_path, 'references.txt')

    try:
        with open(ref_path, 'r') as ref_file:
            content = ref_file.readlines()[1]

    except FileNotFoundError:
        logging.error('references file is not exist yet.')
        raise FileNotFoundError
    
    else:
        master_id = content.split('=')[1].strip()
        return master_id


def draw_graph(cur_commit_id: str, master_id: str, parent_commit_id) -> None:

    g = Digraph('G', filename='commit-graph.gv')

    g.graph_attr['rankdir'] = 'RL'

    g.node('H', 'HEAD')

    g.node('C', cur_commit_id)

    nodes = ['HC']

    if parent_commit_id != 'None':

        g.node('P', parent_commit_id)
        nodes.append('CP')

    if master_id == cur_commit_id:

        g.node('M', 'master')
        nodes.append('MC')

    elif master_id == parent_commit_id:
        g.node('M', 'master')
        nodes.append('MP')

    g.edges(nodes)
    g.view()

def graph():

    if is_father_dir_exist('.wit') is False:
        return


    wit_dir_path = get_folder_path('.wit')

    cur_commit_id = get_commit_id(wit_dir_path)

    master_id = get_master_id(wit_dir_path)

    parent_commit_id = get_parent_commit_id(wit_dir_path, cur_commit_id)

    if cur_commit_id is None:
        logging.info('There was no commit yet.')
        return

    draw_graph(cur_commit_id, master_id, parent_commit_id)