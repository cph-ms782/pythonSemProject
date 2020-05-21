from utils.file_utils import pdf2pandas, data_fetcher
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import os
from os import listdir
from os.path import isfile, join
import glob
import re
import operator


def multi_download(url_list, verbose=False):
    """
    downloader filer fra liste, og returnerer liste af
    filename:pandas keypairs for downloadede pdf filer
    i ./data/download folderen 
    """

    workers = 4
    with ThreadPoolExecutor(workers) as ex:
        urls = [url_list[x] for x in range(len(url_list))]

        filenames = []

        for url in url_list:
            filename = url.split("/")[-1]
            fullpath = "./data/download/" + filename + ".pdf"
            if not os.path.exists(fullpath) and filename[0:5].lower() == "antal":
                filenames.append(fullpath)

        # multithreaded download af pdf filer
        ex.map(data_fetcher, urls, filenames)

    return filenames

def generator(value):
    """returnerer en generator så en bool eller streng kan blive til iterable"""
    while True:
        yield value

def find_date(list_files):
    """ returnerer en liste af datoer. Der matcher med listen af filer"""
    # Find dato
    regex_dato = re.compile(
        r'kommune-(\d{2})(\d{2})(\d{4})-')

    list_dates = []
    for _file in list_files:
        matches_dato = re.search(regex_dato, _file)
        # check for dato
        if matches_dato is not None:
            _day=matches_dato.group(1)
            _month=matches_dato.group(2)
            _year=matches_dato.group(3)
            list_dates.append(_year+_month+_day)
        else:
            list_dates.append("")

    return list_dates

def multi_pdf2pandas(scanner="pdfplumber",  verbose=False, data_folder="./data/download/"):
    """
    returnerer dictionary med filename og pandas dataframe som værdier for downloadede
    pdf filer i ./data/download folderen 
    """

    workers = multiprocessing.cpu_count()

    # laver en liste af pdf filer i pågældende folder
    listof_pdf_files_in_download_folder = glob.glob(data_folder + "*.pdf")

    # laver liste en datoer der matcher med filer i download folder
    list_dates = find_date(listof_pdf_files_in_download_folder)
    
    # multicore behandling af pdf filer
    # with Pool(workers) as ex:
    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(pdf2pandas, listof_pdf_files_in_download_folder, iter(generator(scanner)), iter(generator(verbose)))

    # behandling af resultatet (som er en dict med pandas dataframes liste blandet sammen med filnavne liste )
    filename_pandas = zip([filename for filename in listof_pdf_files_in_download_folder], [
        pd for pd in list(res)], [dato for dato in list_dates])

    result = [dict(zip(('file', 'dataframe', 'date'), file_dataframe))
              for file_dataframe in filename_pandas]

    # sorterer liste efter dato
    result.sort(key=operator.itemgetter('date'))

    return result


def single_pdf2pandas(scanner="pdfplumber", verbose=False, data_folder="./data/download/"):
    """
    returnerer dictionary med filename og pandas dataframe som værdier for downloadede
    pdf filer i ./data/download folderen 
    """

    # laver en liste af pdf filer i pågældende folder
    listof_pdf_files_in_download_folder = glob.glob(data_folder + "*.pdf")

    # laver liste en datoer der matcher med filer i download folder
    list_dates = find_date(listof_pdf_files_in_download_folder)

    res = []
    for pdf_file in listof_pdf_files_in_download_folder:
        res.append(pdf2pandas(pdf_file, scanner, verbose))

    # behandling af resultatet (som er en dict med pandas dataframes liste blandet sammen med filnavne liste )
    filename_pandas = zip([filename for filename in listof_pdf_files_in_download_folder], [
        pd for pd in list(res)], [dato for dato in list_dates])

    result = [dict(zip(('file', 'dataframe', 'date'), file_dataframe))
              for file_dataframe in filename_pandas]

    # sorterer liste efter dato
    result.sort(key=operator.itemgetter('date'))

    return result
