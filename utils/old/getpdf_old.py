from PDFutils import read_pdf
from ssi_clean import clean
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

# konverter til pandas
# tabula kan bruges men den henter ikke 100% korrekt
# df = tabula.read_pdf(file_path, pages='all') 
# tabula.convert_into(file_path, file_path+".csv", all = True, pages='all') 
# print("df", df)

data = read_pdf(file_path)
print("part 1 --", data)

data = clean(data)
array = data.split("---")
print("\nArray", array)

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

print("\npart 1b", array)

# konverter oprenset data til pandas
headers =  ['KOMKODE', 'KOMNAVN','Antal testede','Antal COVID‐19 tilfælde','Befolkning','Kumulativ']
pand = pd.DataFrame(final_list, columns = headers)

print(pand)