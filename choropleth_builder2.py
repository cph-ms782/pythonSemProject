from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import os
import copy 


def getGeo():
    with urlopen('https://raw.githubusercontent.com/ok-dk/dagi/master/geojson/kommuner.geojson') as response:
        counties = json.load(response)

    ##Sorts the list of features by the property KOMNAVN
    counties['features'] = sorted(counties['features'],key= lambda i: i['properties']['KOMNAVN'])
    
    ##Adding id to the properties of the geojson
    count = 0

    for feature in counties['features']:
        feature['properties']['ID'] = str(count)
        count = count +1
    
    counties2 = copy.deepcopy(counties)
    return counties2

def build(df):
    counties = getGeo()
    # os.chdir(os.getcwd() + '/data/download')

    # df = pd.read_csv('./data/download/Antal-covid19-tilfaelde-per-kommune-03042020-2-ru34.pdf_cleaned.csv')
    df.sort_values(by='KOMNAVN',inplace=True)
    df.insert(0,'ID', range(0, len(df)))
    # print(type(df))
    df2 = copy.deepcopy(df)
    print("Bygger chorppleth kort i browser. Vent venligst......kan tage lidt tid")
    fig = px.choropleth_mapbox(df2,geojson=counties,locations='ID',
                            color='Antal COVID‐19 tilfælde',
                            mapbox_style="stamen-toner",
                            featureidkey='properties.ID',
                            color_continuous_scale="rainbow",
                            hover_name='KOMNAVN',
                            hover_data={},
                            center = {"lat": 55.9396761,"lon":9.5155848},
                            zoom=6)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig.show()
