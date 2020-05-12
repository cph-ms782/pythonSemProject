import PyPDF2

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