import pdfplumber
from pandas import pd

file = "test.pdf"

with pdfplumber.open(file) as pdf:
    pages= pdf.pages
    
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split("\n"):
            print(line)