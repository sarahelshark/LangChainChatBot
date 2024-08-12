import datetime
import json


googleApplicationCredentials = "GOOGLE_APPLICATION_CREDENTIALS"
alpeniteVertexai = "alpenite-vertexai.json"

main = "__main__"
embedding = "embedding"
endProgram = "End of the program"
folderPDF =  "files"
foldeXLSX = "files"
folderDOCX = "files"
descTqdm = "Generating data"
default_language = "DEFAULT"
ingnore_columns = ['ID', 'CODE','CATALOGUES ASSIGNED','COLOR FILTER','CARE LABEL','TAXCODE','SIZE GUIDE','FIT DESCRIPTION','FIT FILTER','COMPOSITION FILTER']
languages = ['EN', 'IT', 'FR', 'ES', 'DE', 'CN']
columns = ['SKU','EN','IT','FR','ES','DE','CN']
tqdmLanguages = {'EN':'ENGLISH', 'IT':'ITALIAN', 'FR':'FRENCH', 'ES':'SPANISH', 'DE':'GERMAN', 'CN':'CHINESE'}
geminiResponse = "You are a helpful AI assistant, you reply in the same language as the user."
encoding = "utf-8"

# calculate the timestamp
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
fileNameXLSX = f"output_{timestamp}.xlsx"

# Constants for the XLSX file reading - scripts/readXLS.pyå
inputPath = "input_*.xlsx"
noDataFound = "Nessun dato trovato nei file XLSX nella sotto-cartella."
nofilesFound = "Nessun file trovato."
record = "records"
knfd = "NFKD"

# # Constants for the DOCX file reading - scripts/readfileDOCXToString.py
# fixedPart = "You are a digital assistant that helps creating short description about products. The user will provide you with some data and you will have to generate a marketing description of the product. The description must consider this briefing :"
# guidelinesDoesNotExist = "The file 'guidelines.docx' does not exist in the 'files' folder."
# guideLines = "guidelines.docx"

# # Constants for the PDF file reading - scripts/readFilePDF.py
project = "alpenite-vertexai"
bucket = "alpenite-canali-bucket"
successEmbedding = "Embeddings indexed successfully."
# pdf= ".pdf"
# txt = ".txt"
pathOutputEmbeddings = "testum/embeddings/result.json"
embedding = "embedding"
textEmbedding = "textembedding-gecko@001"
region = "europe-west3"
# mineType = "application/pdf"
# processorId = "41802978c1f66082"