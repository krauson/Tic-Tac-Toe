import logging
import os


def init():

    original_location = os.getcwd()
    subdir_names = ('images', 'staging_area')
    try:
         os.mkdir('.wit')
         os.chdir('.wit')
         with open('activated.txt', 'w') as activated_file:
            activated_file.write('master')
         for name in subdir_names:
             os.mkdir(name)


    except FileExistsError:
        logging.warning('.wit folder was already exist.')

    else:
        os.chdir(original_location)

        logging.info("\'.wit\' folder and its subfolders have been created successfully.")


class FolderNotFound(Exception):
    pass