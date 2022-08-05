from PyPDF2 import PdfMerger

from conf import WORK_PATH


def merge_pdf(files: tuple | list, destination: str):

    """
    :param files:       /home/*/code/beeline//temp/name.pdf
    :param destination: /home/*/code/beeline/result/name.pdf
    :return:
    """

    merger = PdfMerger()
    for pdf in list(files):
        merger.append(pdf)
    merger.write(destination)
    merger.close()
