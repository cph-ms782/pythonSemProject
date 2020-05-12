import re

def regex(array):
    """find patterns i text og returner match object"""

    # REGEX
    # gruppe 1: (\d+) = alle tal
    # gruppe 2: ([a-zæøåA-ZÆØÅ]+) = alle bogstaver inkl æøå men ikke . og tal
    # gruppe 3: ((\d+)(?:\.(\d{1,3}))?) = alle tal og hvis der er et . kommer det også med inkl 3 tal derefter
    regex_city = re.compile('^(\d+)([a-zæøåA-ZÆØÅ-]+)((\d+)(?:\.(\d{1,3}))?)$')

    regex_linie_med_dato = re.compile(
        '^(\d+)AntalCOVID19tilfældeogtestedeperkommune,opgjortden(.+kl\.\d{2}\.\d{2})(\d+)([a-zæøåA-ZÆØÅ-]+)((\d+)(?:\.(\d{1,3}))?)$')

    regex_sidste_linie_med_text = re.compile('^(\d+)Note.+$')


    # print("\npart 1a", array)
    counter = 0
    list_len = len(array)
    while counter<list_len:

        matches_city = re.search(regex_city, array[counter])
        matches_linie_med_dato = re.search(regex_linie_med_dato, array[counter])
        matches_sidste_linie_med_text = re.search(regex_sidste_linie_med_text, array[counter])

        if matches_city is not None:
            # print("matches_city, inde i loop 1. trin. Fjerner: ", array[counter])
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
            # print("matches_linie_med_dato, inde i loop 1. trin. Fjerner: ", array[counter])
            array.pop(counter)
            smittede_fra_sidste_by= matches_linie_med_dato.group(1)
            array.insert(counter+0, smittede_fra_sidste_by)  # 46

            # få dato ind i variabel til senere brug
            opgjort_dato = matches_linie_med_dato.group(2) # 1.maj2020kl.08.00
            # print("\nData opgjort d.: ", opgjort_dato)

            id=matches_linie_med_dato.group(3)      # 430
            array.insert(counter+1, id)                     

            bynavn = matches_linie_med_dato.group(4)
            array.insert(counter+2, bynavn)         # Faaborg-Midtfyn

            testede = matches_linie_med_dato.group(5)
            array.insert(counter+3, testede)         # 1.680

            counter+=4
            matches_linie_med_dato= None

        elif matches_sidste_linie_med_text is not None:
            # print("matches_sidste_linie_med_text, inde i loop 1. trin. Fjerner: ", array[counter])
            array.pop(counter)
            smittede_fra_sidste_by= matches_sidste_linie_med_text.group(1)
            array.insert(counter+0, smittede_fra_sidste_by)  # 46

            counter+=1
            matches_sidste_linie_med_text=None

        else:
            counter+=1

        list_len = len(array)
        # print("counter, list_len", counter, list_len)

    while("" in array) : 
        array.remove("") 

    return array