from utils.file_utils import pdf2pandas, data_fetcher
from start_utils import multi_download, multi_pdf2pandas, single_pdf2pandas
from webScraping import webScraping
import os.path
import sys
import sys
import getopt

def usage():
    return """
    Usage :
    –h or --help --name: denne hjælpe tekst
    -m or --multi: Benyt multi-core til at konvertere. Virker ikke på Windows. Standard er single
    -t or --tabula: Benyt tabula-py til at skanne pdf filer med. Standard er pdfplumber
    -v or --verbose: Alt bliver printet ud
    """


def run(arguments):
    try:
        opts, args = getopt.getopt(arguments, "hmtv", ["help", "multi", "tabula"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    verbose = False
    scanner="pdfplumber"
    process="single"

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

        else:
            assert False, "kan ikke genkende option"

    
    # hent URL'er med PDF
    url_liste = webScraping.webscraping()

    # download PDF'er fra URL'er og lægger dem i data/download folderen
    print("verbose:", verbose)
    multi_download(url_liste, verbose)

    if process=="multi":
        # konverter til pandas multiprocessing
        pandas_liste = multi_pdf2pandas(scanner, verbose)
    else:
        # konverter til pandas single process
        pandas_liste = single_pdf2pandas(scanner, verbose)

    # for at vise fil navn sammen med pandas
    for pandas in pandas_liste:
        print(pandas)


if __name__ == "__main__" :
    run(sys.argv[1:])

