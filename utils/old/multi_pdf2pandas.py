if __name__ == '__main__':

    from concurrent.futures import ProcessPoolExecutor
    import multiprocessing
    from multiprocessing import Pool
    from utils.file_utils import pdf2pandas
    import glob

    """
    returnerer dictionary med filename og pandas dataframe som værdier for downloadede
    pdf filer i ./data/download folderen 
    """
    # Call me from the CLI for example with:
    # python your_script.py arg_1 [arg_2 ...]
    # run(sys.argv[1:])

    data_folder="./data/download/"
    workers = multiprocessing.cpu_count()

    # laver en liste af pdf filer i pågældende folder
    listof_pdf_files_in_download_folder = glob.glob(data_folder + "*.pdf")

    # multicore behandling af pdf filer
    # with Pool(workers) as ex:
    # with ProcessPoolExecutor(workers) as ex:
    with Pool(workers) as ex:
        res = ex.map(pdf2pandas, listof_pdf_files_in_download_folder)

    # behandling af resultatet (som er en dict med pandas dataframes liste blandet sammen med filnavne liste )
    filename_pandas = zip([filename for filename in listof_pdf_files_in_download_folder], [
                    pd for pd in list(res)])

    # result = dict(zip('file', 'dataframe'), filename_pandas)
    result = [dict(zip(('file', 'dataframe'), file_dataframe)) for file_dataframe in filename_pandas]
    # result = dict(zip([filename for filename in listof_pdf_files_in_download_folder], [
    #               pd for pd in list(res)]))

    return result