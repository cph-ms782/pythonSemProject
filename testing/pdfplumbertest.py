import pdfplumber
import pandas as pd

file = "./testing/test.pdf"

with pdfplumber.open(file) as pdf:
    pages= pdf.pages
    
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split("\n"):
            print(line)