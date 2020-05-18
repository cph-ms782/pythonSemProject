import camelot

tables = camelot.read_pdf('test.pdf')

tables.export('foo.csv', f='csv', compress=True) # json, excel, html, sqlite

print(tables[0].parsing_report)

tables[0].to_csv('foo.csv') # to_json, to_excel, to_html, to_sqlite
tables[0].df # get a pandas DataFrame!