from utils.file_utils import pdf2pandas, data_fetcher
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import os
from os import listdir
from os.path import isfile, join


def multi_download(url_list):
    """
    downloader filer fra liste, og returnerer liste af
    filename:pandas keypairs for downloadede pdf filer
    i ./data/urls folderen 
    """

    workers = 4
    with ThreadPoolExecutor(workers) as ex:
        urls = [url_list[x] for x in range(len(url_list))]
        filenames = []
        # filenames = [str(y)+".txt" for y in range(len(url_list))]
        for url in url_list:
            filename = url.split("/")[-1]
            fullpath = "./data/urls/" + filename + ".pdf"
            if not os.path.exists(fullpath):
                filenames.append(fullpath)

        # multithreaded download af pdf filer
        ex.map(data_fetcher, urls, filenames)

    return filenames


def multi_pdf2pandas():
    """
    returnerer liste af filename:pandas keypairs for downloadede
    pdf filer i ./data/urls folderen 
    """

    workers = multiprocessing.cpu_count()
    data_folder = "./data/urls"

    listof_pdf_files_in_urls_folder = ["./data/urls/" + f for f in listdir(
        data_folder) if isfile(join(data_folder, f))]

    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(pdf2pandas, listof_pdf_files_in_urls_folder)
    result = dict(zip([filename for filename in listof_pdf_files_in_urls_folder], [
                  avg for avg in list(res)]))
    return result
