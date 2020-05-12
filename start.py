from utils.file_utils import pdf2pandas, data_fetcher
import os.path

def henteURL():
    """
    manuelt hentede URL'er. Skal udskiftes med automatik
    """

    return [
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-27032020-fg23",
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-03042020-2-ru34",
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-10042020-2-ud79",
        "https://files.ssi.dk/antal-covid19-tilfaelde-per-kommune-17042020-ph56",
        "https://files.ssi.dk/Antal%20COVID19%20tilfaelde%20per%20kommune-20042020-dd09",
        "https://files.ssi.dk/antal-covid19-tilfaelde-per-kommune-21042020-gt78",
        "https://files.ssi.dk/antal-covid19-tilfaelde-per-kommune-22042020-po90",
        "https://files.ssi.dk/antal-covid19-tilfaelde-per-kommune-23042020-bnl4",
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-24042020-wr59",
        "https://files.ssi.dk/Antal%20COVID19%20tilfaelde%20per%20kommune-27042020-ml09",
        "https://files.ssi.dk/antal-covid19-tilfaelde-per-kommune-28042020-gg64",
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-29042020-ut65",
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-30042020-vf49",
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-01052020-prst",
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-04052020-sl67",
        "https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-05052020-s0l0"
    ]

# hent URL'er med PDF
url_liste = henteURL()

# download PDF'er fra URL'er
# pandas_liste = []
# for url in url_liste:
#     filename = url.split("/")[-1]
#     fullpath = "./data/"+ filename + ".pdf"
#     if not os.path.exists(fullpath):
#         data_fetcher(url, fullpath)
    
#     # konverter til pandas
#     result = pdf2pandas(fullpath)
#     # if not isinstance(result, str):
#     pandas_liste.append(result)

# for url, pandas in zip(url_liste, pandas_liste):
#     print(url)
#     print(pandas)

result = pdf2pandas("./data/antal-covid19-tilfaelde-per-kommune-17042020-ph56.pdf")
print(result)




# problem skanninger i filer
"""
https://files.ssi.dk/antal-covid19-tilfaelde-per-kommune-17042020-ph56
ValueError: 6 columns passed, passed data had 7 columns

https://files.ssi.dk/antal-covid19-tilfaelde-per-kommune-21042020-gt78
ValueError: 6 columns passed, passed data had 7 columns

https://files.ssi.dk/antal-covid19-tilfaelde-per-kommune-28042020-gg64
ValueError: 6 columns passed, passed data had 7 columns

https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-30042020-vf49
ValueError: 6 columns passed, passed data had 7 columns

"""