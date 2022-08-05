import requests
import json
import re
import datetime
import subprocess
from time import sleep
from requests.auth import HTTPBasicAuth
from os import mkdir, path, listdir, remove

from PyPDF2 import PdfFileWriter, PdfFileReader
from os.path import isfile, join

# Load credentials for LK beeline
import create_catalogs

print(f'Try load credentials from ./account.json')
try:
    with open('./account.json', 'r') as file:
        accounts = json.loads(str(file.read()))
except FileNotFoundError:
    print('Отсутствует файл account.json \n')
    accounts = []

# Create catalog hierarchy
for folder in ['./output', './output2']:
    try:
        mkdir(folder)
    except FileExistsError:
        print(f'catalog {folder} already exists')

# Get current datetime
now = datetime.datetime.now()
year = now.year
month = now.month
if month == 1:
    year -= 1
    month = 12
else:
    month -= 1

# Get filename for archives
exeFileName = str(year) + '-'
if month < 10:
    exeFileName += '0'
exeFileName += str(month) + '.exe'





print("Processing " + str(year) + " year and " + str(month) + " month")

# scrapping files from beeline backoffice
for oneAccount in accounts:

    print("processing " + oneAccount["account"])
    try:
        mkdir('output/' + oneAccount["account"])
    except FileExistsError:
        print(f"WARNING: Директория уже существует")

    print("request page " + oneAccount["account"])
    ret = requests.get(
        url='https://agent.beeline.ru/abh/?section=storage',
        auth=HTTPBasicAuth(
            oneAccount["login"],
            oneAccount["password"]
        ),
        verify=False
    )

    try:
        m = re.search('storage/(.*?)/' + exeFileName, ret.text)
        print('request file https://agent.beeline.ru/abh/' + m.group(0))

        r = requests.get(
            url=f'https://agent.beeline.ru/abh/{m.group(0)}',
            stream=True,
            auth=HTTPBasicAuth(
                oneAccount["login"],
                oneAccount["password"]
            ),
            verify=False
        )

        print(f'saving file {oneAccount["account"]} \n \n')

        try:  # записать файл, если он Отсутствует
            open(file=f'./output/{oneAccount["account"]}/{exeFileName}').name
        except FileNotFoundError:
            with open(f'./output/{oneAccount["account"]}/{exeFileName}', 'wb') as handle:
                for block in r.iter_content(1024):
                    handle.write(block)
        else:
            print(f'ERROR: File already exists \n')

    except AttributeError:
        print('ERROR: Выгружать нечего \n \n')

# extracting archives
workPath = path.dirname(path.realpath(__file__))

for oneAccount in accounts:
    try:
        print(f'output/{oneAccount["account"]}/{exeFileName}')
        p = subprocess.Popen(
            f'output/{oneAccount["account"]}/{exeFileName} /s',
            cwd=f'output/{oneAccount["account"]}'
        )
        p.wait()
    except FileNotFoundError:
        print(f'File ./output/{oneAccount["account"]}/{exeFileName} Not Found')

#    try:
#        remove(f'./output/{oneAccount["account"]}/{exeFileName}')
#    except FileNotFoundError:
#        print(f'./output/{oneAccount["account"]}/{exeFileName} не существует')


def append_pdf(input, output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


# merging files
for oneAccount in accounts:
    print("Merging files for account " + oneAccount["account"])
    onlyfiles = [f for f in listdir('./output/' + oneAccount["account"]) if
                 isfile(join('./output/' + oneAccount["account"], f)) and f[-3:].lower() == 'pdf']

    accountFiles = {}

    for oneFile in onlyfiles:
        prefixPos = oneFile.find('_')
        if prefixPos > 0:
            prefix = oneFile[1:prefixPos]
            if prefix not in accountFiles:
                accountFiles[prefix] = {}

            if "_счет-авн" in oneFile.lower():
                accountFiles[prefix]['1'] = oneFile
            elif "_счет-фактура" in oneFile.lower():
                accountFiles[prefix]['2'] = oneFile
            elif "_акт" in oneFile.lower():
                accountFiles[prefix]['3'] = oneFile
            elif "_детализация" in oneFile.lower():
                accountFiles[prefix]['4'] = oneFile

    for oneMerge in accountFiles:
        if len(accountFiles[oneMerge]) == 4:
            print('Preparing ' + oneMerge + '_' + str(year) + '_' + str(month) + '.pdf')

            output = PdfFileWriter()

            append_pdf(PdfFileReader(
                open('./output/' + oneAccount["account"] + '/' + accountFiles[oneMerge]['1'], "rb")), output)
            append_pdf(PdfFileReader(
                open('./output/' + oneAccount["account"] + '/' + accountFiles[oneMerge]['2'], "rb")), output)
            append_pdf(PdfFileReader(
                open('./output/' + oneAccount["account"] + '/' + accountFiles[oneMerge]['3'], "rb")), output)
            append_pdf(PdfFileReader(
                open('./output/' + oneAccount["account"] + '/' + accountFiles[oneMerge]['4'], "rb")), output)

            output.write(open('./output2/' + oneMerge + '_' + str(year) + '_' + str(month) + '.pdf', "wb"))

sleep(10)
