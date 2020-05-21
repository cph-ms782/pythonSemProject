import requests
import pandas as pd
import os
from os import listdir
from os.path import isfile, join


def data_factory(url, savefile_name):
    """fetches data from external site and return panda data"""

    response = requests.get(url, savefile_name)

    # get the filename
    fname = response.headers['Content-Disposition'].split('=')[1]

    # write content to file
    if response.ok:  # status_code == 200:
        with open(savefile_name, 'wb') as f:
            f.write(response.content)
        print('-----------------')
        print('Downloaded and saved to file {}'.format(savefile_name))
        return True
    else:
        print("Fejl i download. Prøver gemt fil")
        return False


def kommunealder(verbose=True): 
    url = 'https://api.statbank.dk/v1/data/FOLK1A/CSV?valuePresentation=CodeAndValue&delimiter=Semicolon&OMR%C3%85DE=*&ALDER=*&Tid=2020K2'
    savefile="./data/kommunedata.csv"
    
    downloaded=False
    if not os.path.exists(savefile):
        downloaded = data_factory(url, savefile)

    if verbose:
        if downloaded:
            print("Data hentet fra Dansk Statistik")
        else:
            print("Data hentes ikke fra Dansk Statistik. Forsøger med tidligere gemt fil")

    try:
        data = pd.read_csv(savefile, delimiter=";")
    except Exception as exc:
        if verbose:
            print('Exception - Fejl i læsning af kommunedata. Kunne ikke hente fil og ingen på disk i download folder: %s' % (exc))
        return "Fejl i læsning af kommunedata. Kunne ikke hente fil og ingen på disk i download folder"


    #oprensning af data
    data = data[~data.OMRÅDE.str.contains('000')]
    data = data[~data.OMRÅDE.str.contains('081')]
    data = data[~data.OMRÅDE.str.contains('082')]
    data = data[~data.OMRÅDE.str.contains('083')]
    data = data[~data.OMRÅDE.str.contains('084')]
    data = data[~data.OMRÅDE.str.contains('085')]
    data = data[~data.ALDER.str.contains('IALT I alt')]


    data['OMRÅDE'] = data['OMRÅDE'].str.extract(r'(\d+) .+', expand=True)
    data['ALDER'] = data['ALDER'].str.extract(r'(\d+) .+', expand=True)
    data['TID'] = data['TID'].str.extract(r'(.+) .+', expand=True)

    data['ALDER'] = pd.to_numeric(data['ALDER'], errors='coerce')
    data['INDHOLD'] = pd.to_numeric(data['INDHOLD'], errors='coerce')

    bins = [-1, 16, 26, 41, 66, 126]
    labels = ['0-15', '16-25', '26-40', '41-65', '66+']
    data['ALDER'] = pd.cut(data['ALDER'], bins=bins, labels=labels, right=False)

    KOMKODER = data.groupby("OMRÅDE")['OMRÅDE'].max()
    alderliste = []
    for komkode in KOMKODER:
        data3 = data.loc[data['OMRÅDE'] == komkode].groupby('ALDER')['INDHOLD'].sum()
        streng = "0-15: " + str(data3['0-15']) + ", 16-25: " + str(data3['16-25']) + ", 26-40: " + str(
            data3['26-40']) + ", 41-65: " + str(data3['41-65']) + ", 66+: " + str(data3['66+'])
        alderliste.append(streng)

    kommune_alder = zip(["0" + kommune for kommune in KOMKODER], [
        alder for alder in alderliste])

    return [dict(zip(('KOMKODE', 'ALDER'), ALDER)) for ALDER in kommune_alder]

