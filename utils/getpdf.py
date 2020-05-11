from PDFutils import read_pdf
from ssi_clean import clean
from df_clean import df_clean
from ssi_regex import regex
import pandas as pd
import tabula

# hent pdf fil fra nettet
# fetched = data_fetcher(
#     'https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-01052020-prst', file_path)

# indtil videre sendes True med når der hentes. Dette skal automatiseres
# if fetched:
#     print("det lykkedes at hente data")

file_path= './data/ssi_test.pdf'
# file_path= './data/Antal-covid19-tilfaelde-per-kommune-05052020-s0l0.pdf'
# file_path= './data/Antal-covid19-tilfaelde-per-kommune-27032020-fg23.pdf'
# file_path= './data/Antal COVID19 tilfaelde per kommune-27042020-ml09.pdf'



df = tabula.read_pdf(file_path, pages='all') 
# print(df)

if df.size<70:
    print("Størrelse på dataset: ", df.size)
    print("Der mangler nogle data. Prøver med regex")
    data = read_pdf(file_path)
    # print("part 1 --", data)

    data = clean(data)
    array = data.split("---")
    # print("\nArray", array)

    array = regex(array)

    final_list =[]
    temp_list=[]
    counter = 0
    for string in array:
        temp_list.append(string)
        counter +=1
        if counter==6:
            final_list.append(temp_list)
            temp_list =[]
            counter =0

    # print("\npart 1b", array)

    # konverter oprenset data til pandas
    headers =  ['KOMKODE', 'KOMNAVN','Antal testede','Antal COVID‐19 tilfælde','Befolkning','Kumulativ']
    df = pd.DataFrame(final_list, columns = headers)
    # df.dropna(inplace=True)
    # df = df[df["KOMKODE"].str.isdigit()]

else:
    # rens CSV fil
    df = df_clean(df)

print("df", df)
# print("df", df[23:67])













# konverter til pandas
# df=pd.DataFrame(columns['KOMKODE', 'KOMNAVN','Antal testede','Antal COVID‐19 tilfælde','Befolkning','Kumulativ'])

    
# df = pd.concat([df, df2], ignore_index=False)
# print(df)
# tabula.convert_into(file_path, file_path+".csv", all = True, pages='all') 

# df2=pd.read_csv(file_path+".csv", headers=['KOMKODE', 'KOMNAVN','Antal testede','Antal COVID‐19 tilfælde','Befolkning','Kumulativ'])


# df2.columns = ['KOMKODE', 'KOMNAVN','Antal testede','Antal COVID‐19 tilfælde','Befolkning','Kumulativ']
# print("df2", df2)
