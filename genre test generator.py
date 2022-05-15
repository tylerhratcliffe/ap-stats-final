import pandas as pd
from requests import head
from openpyxl import Workbook
import os

df = pd.read_excel('All Data - No Outliers.xlsx')

sample1 = df[df['Genre'] == "Drama"]
sample1 = sample1[['Title','Genre','Rating']]
#print(sample1)

sample2 = df[df['Genre'] == "Action"]
sample2 = sample2[['Title','Genre','Rating']]
#print(sample2)

sample3 = df[df['Genre'] == "Comedy"]
sample3 = sample3[['Title','Genre','Rating']]
#print(sample3)

#sample4 = df[df['Genre'] == "Adventure"].sample(n=100)
#sample4 = sample4[['Title','Genre','Rating']]
#print(sample4)

#sample5 = df[df['Genre'] == "Crime"].sample(n=100)
#sample5 = sample5[['Title','Genre','Rating']]
#print(sample5)

randomPath = "genres\\"
if not os.path.isdir(randomPath):
    os.makedirs(randomPath)

with pd.ExcelWriter(randomPath + 'All Drama, Action, Comedy.xlsx') as writer:
    sample1.to_excel(writer, sheet_name='Drama')
    sample2.to_excel(writer, sheet_name='Action')
    sample3.to_excel(writer, sheet_name='Comedy')
    #sample4.to_excel(writer, sheet_name='Adventure')
    #sample5.to_excel(writer, sheet_name='Crime')
