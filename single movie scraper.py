
from numpy import double, full
import requests
from bs4 import BeautifulSoup
from datetime import datetime

link = f"https://www.imdb.com/title/tt0111161/"
page = requests.get(link)
page_content = page.content
pageSoup = BeautifulSoup(page_content, 'lxml')

movieTitle = pageSoup.find('h1', class_='sc-b73cd867-0 fbOhB').get_text()
print("Title: " + movieTitle)

movieGenre = pageSoup.find('a', class_='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt').get_text()
print("Genre: " + movieGenre)

runtime = pageSoup.find('li', attrs={'data-testid': 'title-techspec_runtime'}).get_text()
runtime = runtime.replace('Runtime', "")

hours = runtime[:runtime.index(' ')]
hours = int(hours)
minutes = runtime[runtime.index(' '):]
minutes = minutes.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz ¥€'})
minutes = int(minutes)

        
totalMinutes = (hours * 60) + minutes
print("Runtime: " + str(totalMinutes))

try:
    budget = pageSoup.find('li', attrs={'data-testid': 'title-boxoffice-budget'}).get_text()
    budget = budget.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz ¥€'})
    budget = int(budget)
    
except:
    budget = 0

print("Box office budget: " + str(budget))

worldwideGross = pageSoup.find('li', attrs={'data-testid': 'title-boxoffice-cumulativeworldwidegross'}).get_text()
worldwideGross = worldwideGross.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz '})
worldwideGross = int(worldwideGross)
print("Worlwide gross: " + str(worldwideGross))

profitOrLoss = worldwideGross - budget
print("Profit or loss: " + str(profitOrLoss))

rating = pageSoup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'}).get_text()
rating = rating[:rating.index('/')]
rating = double(rating)
print("Rating: " + str(rating))

reviewCount = pageSoup.find('div', attrs={'data-testid': 'reviews-header'}).get_text()
reviewCount = reviewCount.replace('User reviews', "")
reviewCount = reviewCount.replace('Review', "")
print(reviewCount)

headlineItems = pageSoup.find_all('span', class_='sc-8c396aa2-2 itZqyK')
certificate = headlineItems[1].get_text()
print(certificate)

try:
    openingWeekend = pageSoup.find('li', attrs={'data-testid': 'title-boxoffice-openingweekenddomestic'})
    listItems = openingWeekend.find_all('span', class_='ipc-metadata-list-item__list-content-item')
    rawDate = listItems[1].get_text()
    month = rawDate[:rawDate.index(' ')]
    datetime_object = datetime.strptime(month, "%b")
    month_number = datetime_object.month
    print(month_number)
except:
    month = "NA"

ranking = pageSoup.find('div', attrs={'data-testid': 'hero-rating-bar__popularity__score'}).get_text()
ranking = int(ranking)
print(str(ranking))

ratingCount = pageSoup.find('div', class_='sc-7ab21ed2-3 dPVcnq').get_text()

if 'K' in ratingCount:
    ratingCount = ratingCount.replace('K', "")
    ratingCount = float(ratingCount) * 1000
elif 'M' in ratingCount:
    ratingCount = ratingCount.replace('M', "")
    ratingCount = float(ratingCount) * 1000000
else:
    ratingCount = ratingCount.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz '})
    ratingCount = int(ratingCount)

print(ratingCount)