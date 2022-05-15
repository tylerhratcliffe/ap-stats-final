import pandas as pd
from requests import head
from openpyxl import Workbook
import os

df = pd.read_excel('All Data - No Outliers.xlsx')

#Sample A
#df = df[['Title','Runtime','Profit or Loss']]

#Sample B
#df = df[['Title','Runtime','IMDB Ranking']]

#Sample C
#df = df[['Title','Runtime','Rating']]

#Sample D
#df = df[['Title','Budget','Profit or Loss']]

#Sample E
#df = df[['Title','Budget','IMDB Ranking']]

#Sample F
#df = df[['Title','Budget','Rating']]

#Sample G
#df = df[['Title','Release Month','Profit or Loss']]

#Sample H
#df = df[['Title','Release Month','IMDB Ranking']]

#Sample I
df = df[['Title','Release Month','Rating']]

#print(df.head)

randomPath = "census statistics\\"
if not os.path.isdir(randomPath):
    os.makedirs(randomPath)

df.to_excel("census statistics\\" + "Census Sample I.xlsx")
