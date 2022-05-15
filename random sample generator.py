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
sample1 = df.sample(n = 100)
sample2 = df.sample(n = 100)
sample3 = df.sample(n = 100)
sample4 = df.sample(n = 100)
sample5 = df.sample(n = 100)

randomPath = "random samples of 100\\"
if not os.path.isdir(randomPath):
    os.makedirs(randomPath)

with pd.ExcelWriter(randomPath + 'Sample I.xlsx') as writer:
    sample1.to_excel(writer, sheet_name='Trial 1')
    sample2.to_excel(writer, sheet_name='Trial 2')
    sample3.to_excel(writer, sheet_name='Trial 3')
    sample4.to_excel(writer, sheet_name='Trial 4')
    sample5.to_excel(writer, sheet_name='Trial 5')
