from utils.file_utils import pdf2pandas, data_fetcher
from utils.start_utils import multi_download, multi_pdf2pandas, single_pdf2pandas
from choropleth_builder2 import build as choro
# import choro_web
from webScraping import webScraping
import os.path
import sys
import getopt


def usage():
    return """
    Options :
    –h or --help --name: denne hjælpe tekst
    -m or --multi: Benyt multi-core til at konvertere. OBS! Virker ikke på Windows. Standard er single
    -t or --tabula: Benyt tabula-py til at skanne pdf filer med. Standard er pdfplumber
    -v or --verbose: Alt bliver printet ud (også pandas)
    -p or --pandas: Print pandas i en terminal. Standard output er choropleth kort i browseren
    --no-cache: Download alt igen. OBS! Ikke implementeret. Slet i stedet manuelt alt i folderen ./data/download

    Eksempel:
    python start.py         # singlecore. Viser choropleth map i browser
    python start.py -m      # multicore. Viser choropleth map i browser
    python start.py -v      # viser al tekst
    python start.py -v -m   # argumenterne kan kombineres
    """


def run(arguments):
    try:
        opts, args = getopt.getopt(
            arguments, "hmtvp", ["help", "multi", "tabula", "no-cache", "pandas"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    verbose = False
    scanner = "pdfplumber"
    process = "single"
    no_cache = False
    output = "choro"

    for option, argument in opts:
        if option in ("-v", "--verbose"):
            print(option)
            verbose = True
        elif option in ("-h", "--help"):
            print(usage())
            sys.exit(2)
        elif option in ("-m", "--multi"):
            process = "multi"
        elif option in ("-t", "--tabula"):
            scanner = "tabula"
        elif option in ("-p", "--pandas"):
            output = "pandas"
        elif option in ("--no-cache"):
            no_cache = True

        else:
            assert False, "kan ikke genkende option"

    # hent URL'er med PDF
    url_liste = webScraping.webscraping()

    # download PDF'er fra URL'er og lægger dem i data/download folderen
    print("verbose:", verbose)
    multi_download(url_liste, verbose)

    if process == "multi":
        # konverter til pandas multiprocessing
        pandas_liste = multi_pdf2pandas(scanner, verbose)
    else:
        # konverter til pandas single process
        pandas_liste = single_pdf2pandas(scanner, verbose)

    # for at vise fil navn sammen med pandas
    if output == "pandas" or verbose:
        for pandas in pandas_liste:
            print(pandas)

    if output == "choro":
        # byg choropleth map
        index = len(pandas_liste)-1
        print("Checker liste fra neden og op (nyeste dato først), for at se om den er i det rigtige format")
        while index > 0:
            if isinstance(pandas_liste[index]["dataframe"], str):
                if verbose:
                    print("Streng fundet i data for: ", pandas_liste[index]['file'], ". Tager næste i listen")
                index -= 1
            # pandas er fundet men den kan være forkert størrelse
            elif pandas_liste[index]["dataframe"].size < 311:
                if verbose:
                    print("Forkert formet panda dataframe fundet i data for filen: ", pandas_liste[index]['file'], ". Tager næste i listen")
                index -= 1
            # hvis fundne værdi ikke er en streng og den er en pandas med størrelse 311 så kan den bruges
            else:
                shape = pandas_liste[index]["dataframe"].shape
                if verbose:
                    print("shape", shape)
                if shape[0]==311 and shape[1]==7:
                    print("Sender data fra d. ", pandas_liste[index]["date"], " (år/måned/dag) til choropleth map")
                    index == 0
                    choro(pandas_liste[index]["dataframe"])
                    print("Færdig")
                    sys.exit(0)
                else:
                    if verbose:
                        print("Form af dataframe: ", shape)
                    print("Forkert formet panda dataframe fundet i data for filen: ", pandas_liste[index]['file'], ". Tager næste i listen")
                    index -= 1


if __name__ == "__main__":
    run(sys.argv[1:])
