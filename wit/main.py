#upload 175
from init import init
from add import add
from commit import commit
from status import status
from checkout import checkout
from graph import graph
from branch import branch
from merge import merge

import logging
from logging import DEBUG
import os
import sys




logging.basicConfig(level=DEBUG)


def main():
    args = sys.argv[1:]

    if len(args) < 1:
        logging.warning('Usage: python <filename> <function> <parameters..>')

    elif args[0] == 'init':
        init()

    elif args[0] == 'add':

        data_to_copy_path = args[1]
        add(data_to_copy_path)

    elif args[0] == 'commit':
        message = args[1]
        commit(message)

    elif args[0] == 'status':
        status()

    elif args[0] == 'checkout':
        commit_id = args[1]
        checkout(commit_id)

    elif args[0] == 'graph':
        graph()

    elif args[0] == 'branch':
        branch_name = args[1]
        branch(branch_name)

    elif args[0] == 'merge':
       branch_name = args[1]
       merge()

# if __name__ == '__main__':

#     main()


os.chdir(r"C:\Users\Hagai\Desktop\week1\week1")
# init()
# add(r'C:\Users\Hagai\Desktop\week1\week1\hagai\hello.py.txt')
commit('hey')
# status()
# checkout('koko')
# graph()
# branch('koko')
