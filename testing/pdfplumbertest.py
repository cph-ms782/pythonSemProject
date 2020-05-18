import pdfplumber
import pandas as pd
import csv

file_path = "./testing/antal.pdf"
verbose = True

# opret fil med tekst
text_lines = []
with pdfplumber.open(file_path) as pdf:
    pages= pdf.pages
    
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split("\n"):
            print(line)
            line = line.replace("\xa0", "").split(" ")
            text_lines.append(line)


# skriv til fil
with open(file_path + ".csv", 'w', encoding='utf-8') as csvfile:
        # skaber csv writer object
        csvwriter = csv.writer(csvfile)

        # skriver data til csv fil
        try:
            csvwriter.writerows(text_lines)
        except Exception as exc:
            if verbose:
                print('Exception - Fejl i skriving af csv fil: %s' % (exc))
