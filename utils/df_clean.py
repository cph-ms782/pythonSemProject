import numpy as np
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import pandas as pd


def df_clean(data):
    """
    Clean pandas dataframe
    """
    print("Dataframe cleaning")

    columns = ['KOMKODE', 'KOMNAVN', 'Antal testede',
               'Antal COVID‐19 tilfælde', 'Befolkning', 'Kumulativ']
    print(data)

    # I tilfælde af at data i første række har lagt sig som kolonne navne ved et fejl i konvertering fra 
    # PDF til dataframe, så skal kolonne navnene lægges tilbage som første række
    if data.columns[0].isdigit():
        # Opret en ny dataframe som skal indeholde data fra kolonne navne
        print("data.columns[0].isdigit()")
        df = pd.DataFrame(columns=columns)
        new_row = pd.Series(data.columns)
        new_df = pd.DataFrame([new_row])
        # Giv den nye dataframe de rigtige kolonne navne
        new_df.columns = columns

        # giv det originale dataframe de samme kolonne navne
        data.columns = columns

        # læg de to dataframes sammen, og opret en ny række-index
        data2 = pd.concat([new_df, data], ignore_index=True)

    # Hvis alt er kommet over normalt, skal der bare lægges rigtige kolonne navne på
    else:
        # læg header på dataframe
        data.columns = columns
        data2=data
        # print(data.head())

    # removing null values to avoid errors
    print(data2)
    data2.dropna(inplace=True)
    # data2 = data2[data2["KOMKODE"] != 'NaN']
    print(data2)

    # Fjern rækker hvor felter i kolonne KOMKODE ikke er et tal
    data2 = data2[data2["KOMKODE"].str.isdigit()]
    print(data2)

    # display
    # print(data)

    return data2
