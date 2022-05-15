import pandas as pd
from requests import head
from openpyxl import Workbook
import os

df = pd.read_excel('All Data - No Outliers.xlsx')

sample1 = df[df['Genre'] == "Drama"].sample(n=100)
print(sample1)

sample2 = df[df['Genre'] == "Action"].sample(n=100)
print(sample2)

sample3 = df[df['Genre'] == "Comedy"].sample(n=100)
print(sample3)

sample4 = df[df['Genre'] == "Adventure"].sample(n=100)
print(sample4)

sample5 = df[df['Genre'] == "Crime"].sample(n=100)
print(sample5)

randomPath = "genres\\"
if not os.path.isdir(randomPath):
    os.makedirs(randomPath)

with pd.ExcelWriter(randomPath + 'Genres.xlsx') as writer:
    sample1.to_excel(writer, sheet_name='Drama')
    sample2.to_excel(writer, sheet_name='Action')
    sample3.to_excel(writer, sheet_name='Comedy')
    sample4.to_excel(writer, sheet_name='Adventure')
    sample5.to_excel(writer, sheet_name='Crime')
