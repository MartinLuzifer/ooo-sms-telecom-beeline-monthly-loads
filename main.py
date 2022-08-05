import os
from os import listdir
from os.path import isfile, join
from subprocess import Popen
from time import sleep

from create_catalogs import *
from download_archive import write_archive
from accounts import ACCOUNTS
from conf import WORK_PATH, NEED_YEAR, NEED_MONTH
from merge_pdf import merge_pdf


if __name__ == '__main__':
    create_temp_catalog()
    create_result_catalog()
    for one_account in ACCOUNTS:
        create_result_catalog_hierarchy(one_account['account'])
        create_pdf_catalog(one_account['account'])

    for one_account in ACCOUNTS:

        # VAR
        account, login, password = (one_account['account'], one_account['login'], one_account['password'])

        # ===>>> /home/*/*/code/beeline/temp/PV022-07-2022.exe
        archive_name = f'{WORK_PATH}/temp/{account}-{NEED_YEAR}-{NEED_MONTH}.exe'

        # ===>>> /home/*/*/code/beeline/temp/PV022/
        pdf_dir = f'{WORK_PATH}/temp/{account}/'

        # ===>>> /home/*/*/code/beeline/temp
        temp_dir = f'{WORK_PATH}/temp/'

        # ===>>> /home/*/*/code/beeline/result/
        result_dir = f'{WORK_PATH}/result/'

        # DOWNLOAD ARCHIVE
        print(f'<<<DOWNLOAD>>> {archive_name}')
        write_archive(archive_name, login, password)

        # EXTRACT FILES FROM ARCHIVE
        print(f'<<<EXTRACT>>> unzip files from {archive_name}')
        Popen(args=(f'{archive_name}', '/s'), cwd=pdf_dir).wait()

        # MERGING PDF FROM ARCHIVE
        all_files = [f for f in listdir(pdf_dir) if isfile(join(pdf_dir, f)) and f[-3:].lower() == 'pdf']
        while all_files:
            file_list = []
            prefix = all_files[0][0:all_files[0].find('_')]

            for one in list(all_files):  # Без list() не будет работать
                if prefix in one:
                    print(f"Добавление {one}")
                    file_list.append(f"{pdf_dir}{one}")
                    all_files.remove(one)
                    sleep(0.2)

            merge_pdf(file_list, f'{result_dir}{account}/{account}-{prefix}.pdf')
            print(f'Файлы Склеены в {result_dir}{account}-{prefix}.pdf')

            for remove_file in file_list:
                print(f"удаление: {remove_file}")
                os.remove(remove_file)
                sleep(0.2)
            
            print()
            sleep(2)

        try:
            os.rmdir(pdf_dir)
        except FileExistsError:
            pass

        # END
    print('<<<DOWNLOAD>>> end\n')
