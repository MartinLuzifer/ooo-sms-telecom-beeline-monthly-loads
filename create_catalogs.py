from os import mkdir
from conf import WORK_PATH


def create_temp_catalog():
    try:  # Create ./temp if not exist
        mkdir(folder := f'{WORK_PATH}/temp')
        print(f'create: {folder}')
    except FileExistsError:
        pass


def create_result_catalog_hierarchy(name):
    try:  # Create ./temp if not exist
        mkdir(folder := f'{WORK_PATH}/result/{name}')
        print(f'create: {folder}')
    except FileExistsError:
        pass


def create_result_catalog():
    try:  # Create ./temp if not exist
        mkdir(folder := f'{WORK_PATH}/result')
        print(f'create: {folder}')
    except FileExistsError:
        pass


def create_pdf_catalog(name):
    try:  # Create ./temp if not exist
        mkdir(folder := f'{WORK_PATH}/temp/{name}')
        print(f'create: {folder}')
    except FileExistsError:
        pass
