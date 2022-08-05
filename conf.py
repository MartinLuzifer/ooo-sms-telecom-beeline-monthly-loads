from os import path

NEED_YEAR = '2022'
NEED_MONTH = '07'  # 01, 02 ... 11, 12

# directory
WORK_PATH = (path.dirname(path.realpath(__file__)))
EXE_FILE_NAME = f'{NEED_YEAR}-{NEED_MONTH}.exe'
MERGE_PDF = f'{WORK_PATH}/result/'

# network
STORAGE_URL = 'https://agent.beeline.ru/abh/?section=storage'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'}
SSL_VERIFY = False
