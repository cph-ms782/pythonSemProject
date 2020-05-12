def clean(data):
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

    return data