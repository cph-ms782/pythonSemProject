import requests

import csv
import re
import pandas as pd
import tabula
import sys


def data_fetcher(url, savefile_name):
    """
    Henter filer fra nettet. Input url og fil navn der skal gemmes til
    TODO Try except så der kan sendes true/false tilbage om download lykkedes
    """

    response = requests.get(url, savefile_name)

    # get the filename
    # fname = response.headers['Content-Disposition'].split('=')[1]

    # write content to file
    if response.ok:  # status_code == 200:
        with open(savefile_name, 'wb') as f:
            f.write(response.content)
    else:
        print('Kunne ikke downloade filen: ', savefile_name)
    print('-----------------')
    print('Downloaded and saved to file {}'.format(savefile_name))

    return savefile_name


def pdf2pandas(file_path="./data/download/Antal COVID19 tilfaelde per kommune-27042020-ml09.pdf"):
    """
    Tager adressen til en PDF fil som input og sender en pandas dataframe tilbage.
    Hvis den ikke kan læse PDF filen korrekt, kommer en fejl tekst return
    """

    # brug tabula til at lave en csv fil der er let at rette i
    # try:
    #     tabula.convert_into(file_path, file_path+".csv", all=True, pages='all')
    # except Exception as exc:
    #     print('Exception: %s' % (exc))
    #     return "Fejl i konvertering fra pdf til csv fil"
        

    # init af header og række lister
    rows = []

    # REGEX
    # gruppe 1: ([a-zæøåA-ZÆØÅ]+-{0,1}[a-zæøåA-ZÆØÅ]+) = alle bogstaver inkl æøå men ikke . og tal. Kan indeholde et - i midten
    # gruppe 2: ((\d+)(?:\.(\d{1,3}))?) = alle tal og hvis der er et . kommer det også med inkl 3 tal derefter
    # Der kan forekomme mellemrum, så de bliver fjernet ved \s{0,3} og at de ikke kommer med i en gruppe
    # Og det skal lige nævnes efter timers søgen at i ‐{0,1} er det ikke et chr(45) minus tegn,
    # men et chr(8208) minus tegn .... argh :-)
    regex_city = re.compile(
        r'([a-zA-ZæøåÆØÅ]+‐{0,1}[a-zA-ZæøåÆØÅ]+)\s{0,3}(\d+.+)')

    # læser csv fil
    with open(file_path+".csv", 'r') as csvfile:
        print("Tester: ", file_path+".csv")

        # laver et csv reader objekt
        try:
            csvreader = csv.reader(csvfile)
            original_fields = next(csvreader)
        except Exception as exc:
            print('Exception: %s' % (exc))
            return "Fejl i læsning af csv fil"

        # hiver første linie ud. Den kan indeholde kolonne navne

        # hiver linie for linie ud af csv reader objektet
        for row in csvreader:
            try:
                for index, row_val in enumerate(row):
                    row[index] = row[index].replace("<10 tilfælde", "<10tilfælde")
                    row[index] = row[index].replace('"', '')

                # hvis tabula ikke finder de rigtige kolonner, kommer der et mellemrum i mellem værdier
                # så nedenstående splitter på mellemrum (for at undgå <10 tilfælde ikke bliuver splittet)
                # fjernes mellemrum først
                if len(row)==2:
                    new_list = row[0].split(" ")
                    new_list.append(row[1])
                    row = new_list
                if len(row)==3:
                    new_list = row[0].split(" ")
                    new_list.append(row[1])
                    new_list.append(row[2])
                    row = new_list

                # i starten af pandemien var der ikke tal for antal smittede
                # ved at indsætte en ny værdi er der det rigtige antal kolonner
                if len(row)==5:
                    row.insert( 2, "0")
                
                # tabula læser forkert en gang imellem. Hvis der er syv
                # kolonner er det som regel fordi den har splittet københavns og frederiksbergs
                # indbyggerantal op i to værdier, men det kan skifte, så nedenstående linier er 
                # kommenteret ud. 
                # if len(row)==7:
                #     row[4 : 6] = [''.join(row[4 : 6])] 

                # første kolonne skal være tal. Hvis der ikke står et tal
                # opstår en fejl og hele linien kommer ikke med i den endelige csv fil
                # den bliver konverteret tilbage igen for at gøre det lettere at fjerne mellemrum nedenunder
                row[0] = str(int(row[0]))

                # anden kolonne kan have fejl i sig
                # 430,Faaborg‐Midtfyn1.680,3 1,51.809,60
                # 440,Kerteminde808,1 3,23.773,55
                # Fejlen er Faaborg‐Midtfyn1.680 eller Kerteminde808
                # så regex (som blev lavet længere oppe) separerer denne i to
                matches_city = re.search(regex_city, row[1])

                # check for at se om der er kommet en fejl og at regex'en har opfanget den
                if matches_city is not None:
                    # midlertidig liste til at holde styr på genopbygninbg af en række i csv filen
                    temp = []

                    # løber igennem en enkelt række i csv filen. Ved anden værdig index==1
                    # bliver de nu separerede værdier lagt ind en efter hinanden
                    for index, row_val in enumerate(row):
                        if index == 1:
                            temp.append(matches_city.group(1).replace(" ", ""))
                            temp.append(matches_city.group(2).replace(" ", ""))
                        else:
                            temp.append(row_val.replace(" ", ""))

                    # den opbyggede liste lægges ind rows
                    rows.append(temp)
                    matches_city = None
                else:
                    # der er ikke fundet en fejl og rækken lægges ind i listen som den er
                    # dog fjernes mellemrum, der kan snige sig ind i tallene
                    for index, row_val in enumerate(row):
                        row[index] = row_val.replace(" ", "")

                    rows.append(row)
            except:
                print("Forkert type data fjernet fra dataset: ", row)

        # totale antal rækker før oprensning
        print("Totalt antal rækker før oprens: %d" % (csvreader.line_num))

        # opret ny liste til brug til csv fil og pandas
        final_list = []

        headers = ['KOMKODE', 'KOMNAVN', 'Antal testede',
                   'Antal COVID‐19 tilfælde', 'Befolkning', 'Kumulativ']
        if original_fields[0] != 'KOMKODE':
            final_list.append(headers)
            try:
                original_fields[0] = int(original_fields[0])
                final_list.append(original_fields)
            except:
                print(
                    "original header indeholder ikke data, så den kommer ikke med i listen: ", original_fields)
        else:
            final_list.append(headers)

        final_list += rows

        print("Totalt antal rækker efter oprens: %d" % (len(final_list)))

    with open(file_path + "_cleaned.csv", 'w') as csvfile:
        # skaber csv writer object
        csvwriter = csv.writer(csvfile)

        # skriver data til csv fil
        csvwriter.writerows(final_list)

    # opretter pandas dataframe fra nylig lavet liste
    try:
        df = pd.DataFrame(final_list[1:], columns=headers)
    except ValueError as err:
        df = "ValueError: {0}".format(err)

    return df
