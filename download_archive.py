import re

import requests
import urllib3
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

from conf import SSL_VERIFY, EXE_FILE_NAME, STORAGE_URL, HEADERS


def get_binary_archive(url: str, login: str, password: str):

    """
    :param url:
    :param login:
    :param password:
    :param headers:
    :param verify: True default, Set False if urllib3.exceptions::InsecureRequestWarning
    :return:

    """

    if SSL_VERIFY is False:
        urllib3.disable_warnings(InsecureRequestWarning)
        print('<<<WARNING>>> InsecureRequestWarning: Unverified HTTPS request is being made to host')

    with requests.session() as session:

        session.auth = HTTPBasicAuth(username=login, password=password)
        session.verify = SSL_VERIFY
        session.stream = True
        session.headers.update(HEADERS)
        response_text = session.get(url)

        return session.get(
            f'https://agent.beeline.ru/abh/{re.search(f"storage/(.*?)/{EXE_FILE_NAME}", response_text.text).group(0)}'
        )


def write_archive(filename, login, password):

    try:  # write file if not exists
        open(filename, 'r')

    except FileNotFoundError:  # write, because not exists
        binary = get_binary_archive(url=STORAGE_URL, login=login, password=password)
        with open(filename, 'wb') as handle:
            for block in binary.iter_content(1024):
                handle.write(block)

    else:  # not write, because file already exists
        print(f'<<<WARNING>>> File {filename} already exists: SKIP')


if __name__ == '__main__':
    pass
