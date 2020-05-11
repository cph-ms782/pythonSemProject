
# importing required modules
# conda install tabula-py PyPDF2 requests panda
import PyPDF2
import requests
import pandas as pd
# import tabula
import re


def data_fetcher(url, savefile_name):
    """
    fetches data from external site
    TODO Try catch så der kan sendes true/false tilbage om download lykkedes
    """

    response = requests.get(url, savefile_name)

    # get the filename
    # fname = response.headers['Content-Disposition'].split('=')[1]

    # write content to file
    if response.ok:  # status_code == 200:
        with open(savefile_name, 'wb') as f:
            f.write(response.content)
    print('-----------------')
    print('Downloaded and saved to file {}'.format(savefile_name))

    return True


def read_pdf(address):
    """
    convert data into text
    TODO lav open with ressources så den lukker ressourcen selv
    Done- merge to pageObjects til een med mergePage, https://pythonhosted.org/PyPDF2/PageObject.html#PyPDF2.pdf.PageObject
    """

    # creating a pdf file object
    pdfFileObj = open(address, "rb")

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    if pdfReader==-1:
        print("Couldn't find file")
        return False

    # printing number of pages in pdf file
    print("pdfReader.numPages", pdfReader.numPages)

    # lav een eller flere page objects
    counter=2
    if  pdfReader.numPages==1:
        pageObj = pdfReader.getPage(0)
    else:
        pageObj = pdfReader.getPage(0)
        while counter <=  pdfReader.numPages:
            pageObjTemp = pdfReader.getPage(counter-1)
            pageObj.mergePage(pageObjTemp)
            counter+=1

    # extracting text from page
    data = pageObj.extractText()

    # closing the pdf file object
    pdfFileObj.close()

    return data

def regex(text):
    """find patterns i text og returner match object"""

# hent pdf fil fra nettet
# file_path= './data/ssi_test.pdf'
file_path= './data/Antal-covid19-tilfaelde-per-kommune-05052020-s0l0.pdf'
# fetched = data_fetcher(
#     'https://files.ssi.dk/Antal-covid19-tilfaelde-per-kommune-01052020-prst', file_path)

# indtil videre sendes True med når der hentes. Dette skal automatiseres
# if fetched:
#     print("det lykkedes at hente data")

# konverter til pandas
# tabula kan bruges men den henter ikke 100% korrekt
# df = tabula.read_pdf(file_path, pages='all') 

data = read_pdf(file_path)
print("part 1 --", data)

data=data.replace('\n\n', '---')
data=data.replace('\n', '---')
data=data.replace('Kommune(id)Kommune---(navn)Antal---testedeAntalCOVID19tilfældeBefolkningKumulativincidens(per100.000indbyggere)', '')
data=data.replace('Frederiksber---g', 'Frederiksberg')
data=data.replace('Fredensbor---g', 'Fredensborg')
data=data.replace('Lyngby---Taarbæk', 'Lyngby-Taarbæk')
data=data.replace('Helsingø---r', 'Helsingør')
data=data.replace('Høje---Taastrup', 'Høje-Taastrup')
data=data.replace('Brøndersle---v', 'Brønderslev')
data=data.replace('Hadersle---v', 'Haderslev')
data=data.replace('Faaborg---Midtfyn', 'Faaborg-Midtfyn')
data=data.replace('<10tilfælde', '---<10tilfælde---')   # der er to tilfælde af <10tilfælde, hvor der er data på hver sin side
data=data.replace('------', '---')                      # dette pga ovenstående hack. Så kommer der steder med seks streger i stedet for tre
array = data.split("---")
print("\nArray", array)


# REGEX
# gruppe 1: (\d+) = alle tal
# gruppe 2: ([a-zæøåA-ZÆØÅ]+) = alle bogstaver inkl æøå men ikke . og tal
# gruppe 3: ((\d+)(?:\.(\d{1,3}))?) = alle tal og hvis der er et . kommer det også med inkl 3 tal derefter
regex_city = re.compile('^(\d+)([a-zæøåA-ZÆØÅ-]+)((\d+)(?:\.(\d{1,3}))?)$')

regex_linie_med_dato = re.compile(
    '^(\d+)AntalCOVID19tilfældeogtestedeperkommune,opgjortden(.+kl\.\d{2}\.\d{2})(\d+)([a-zæøåA-ZÆØÅ-]+)((\d+)(?:\.(\d{1,3}))?)$')

regex_sidste_linie_med_text = re.compile('^(\d+)Note.+$')


print("\npart 1a", array)
counter = 0
list_len = len(array)
while counter<list_len:

    matches_city = re.search(regex_city, array[counter])
    matches_linie_med_dato = re.search(regex_linie_med_dato, array[counter])
    matches_sidste_linie_med_text = re.search(regex_sidste_linie_med_text, array[counter])

    if matches_city is not None:
        print("matches_city, inde i loop 1. trin. Fjerner: ", array[counter])
        array.pop(counter)
        # i tilfælde af at der er under 100 tusind indbyggere vil tallet der splittes hernedenunder
        # kun være på fem cifre (i modsætning til de normale seks).
        # Eksempelvis 96420Assens1.320. 96420. De 96 kommer fra Vordingborg
        if len(str(matches_city.group(1)))==5:
            array.insert(counter+0, matches_city.group(1)[0:2])
            array.insert(counter+1, matches_city.group(1)[2:])
        else:
            array.insert(counter+0, matches_city.group(1)[0:3])
            array.insert(counter+1, matches_city.group(1)[3:])
        array.insert(counter+2, matches_city.group(2))
        array.insert(counter+3, matches_city.group(3))
        counter+=4
        matches_city=None
    # fjern dato og læg det i variabel til senere brug
    # '46AntalCOVID19tilfældeogtestedeperkommune,opgjortden1.maj2020kl.08.00430Faaborg-Midtfyn1.680'
    elif matches_linie_med_dato is not None:
        print("matches_linie_med_dato, inde i loop 1. trin. Fjerner: ", array[counter])
        array.pop(counter)
        smittede_fra_sidste_by= matches_linie_med_dato.group(1)
        array.insert(counter+0, smittede_fra_sidste_by)  # 46

        # få dato ind i variabel til senere brug
        opgjort_dato = matches_linie_med_dato.group(2) # 1.maj2020kl.08.00
        print("\nData opgjort d.: ", opgjort_dato)

        id=matches_linie_med_dato.group(3)      # 430
        array.insert(counter+1, id)                     

        bynavn = matches_linie_med_dato.group(4)
        array.insert(counter+2, bynavn)         # Faaborg-Midtfyn

        testede = matches_linie_med_dato.group(5)
        array.insert(counter+3, testede)         # 1.680

        counter+=4
        matches_linie_med_dato= None

    elif matches_sidste_linie_med_text is not None:
        print("matches_sidste_linie_med_text, inde i loop 1. trin. Fjerner: ", array[counter])
        array.pop(counter)
        smittede_fra_sidste_by= matches_sidste_linie_med_text.group(1)
        array.insert(counter+0, smittede_fra_sidste_by)  # 46

        counter+=1
        matches_sidste_linie_med_text=None

    else:
        counter+=1

    list_len = len(array)
    print("counter, list_len", counter, list_len)

while("" in array) : 
    array.remove("") 


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

print(pand[0:34])

# conda install -c plotly plotly=4.6.0

# from urllib.request import urlopen
# import json
# with open('kommuner.geojson', 'r') as data:
#     kommuner = json.load(data)

# # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
# #                    dtype={"fips": str})

# import plotly.express as px

# fig = px.choropleth(pand, geojson=kommuner, locations='KOMNAVN', color='Kumulativ',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 12),
#                            scope="europe",
                           
#                            labels={'Kumulativ':'Kumulativ incidens (per 100.000 indbyggere)'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()