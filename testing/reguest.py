import requests
import pandas as pd

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

    data = pd.read_csv(savefile_name, delimiter=";")
    return data
  
#  2008: (428864/5475791)*100 = 7.8%
  
#  2020: (544588/5822763)*100 = 9,3%

# Change (544588-428864)*100/544588 = 21%

url = 'https://api.statbank.dk/v1/data/FOLK1A/CSV?valuePresentation=CodeAndValue&delimiter=Semicolon&OMR%C3%85DE=*&ALDER=*&Tid=2020K2'

data = data_factory(url, "testersen.csv")
data = data.drop(labels=range(0,2)) # sletter første to linier data
data = data[~data.OMRÅDE.str.contains('Region')] # fjerner linier med region
data = data.sort_values(by='INDHOLD', ascending=False)
data[0:5]