import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from tqdm import tqdm

movies = []

rawCensus = []
rawCensusMinusIncomplete = []

for i in range(26,30):
    #1, 5
    #6, 11
    #11, 16
    #16, 21
    #21, 26
    url = f"https://www.imdb.com/list/ls074451163/?st_dt=&mode=detail&page={i}&sort=user_rating,desc"
    request = requests.get(url)
    page = request.content

    soup = BeautifulSoup(page, 'lxml')
    pageMovies = soup.find_all('h3', class_='lister-item-header')
    movies.append(pageMovies)

#print(movies[1])

for i in tqdm(range(len(movies))):
    for j in tqdm(range(len(movies[i]))):
        link = movies[i][j].find('a')['href']
        fullLink = "https://www.imdb.com" + link
        #print(fullLink)

        moviePage = requests.get(fullLink)
        moviePage_content = moviePage.content
        pageSoup = BeautifulSoup(moviePage_content, 'lxml')

        try:
            movieTitle = pageSoup.find('h1', attrs={'data-testid': 'hero-title-block__title'}).get_text()
            #print("Title: " + movieTitle)
        except:
            movieTitle = "NA"

        try:
            movieGenre = pageSoup.find('a', class_='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt').get_text()
            #print("Genre: " + movieGenre)
        except:
            movieGenre = "NA"

        try:
            runtime = pageSoup.find('li', attrs={'data-testid': 'title-techspec_runtime'}).get_text()
            runtime = runtime.replace('Runtime', "")
        except:
            runtime = "NA"

        try:
            hours = runtime[:runtime.index(' ')]
            hours = int(hours)
        except:
            hours = 0

        try:
            minutes = runtime[runtime.index(' '):]
            minutes = minutes.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz ¥€'})
            minutes = int(minutes)
        except:
            minutes = 0
        
        totalMinutes = (hours * 60) + minutes
        #print("Runtime: " + str(totalMinutes))

        try:
            budget = pageSoup.find('li', attrs={'data-testid': 'title-boxoffice-budget'}).get_text()
            budget = budget.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz ¥€'})
            budget = int(budget)
            #print("Box office budget: " + str(budget))
        except:
            budget = "NA"

        try:
            worldwideGross = pageSoup.find('li', attrs={'data-testid': 'title-boxoffice-cumulativeworldwidegross'}).get_text()
            worldwideGross = worldwideGross.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz ¥€'})
            worldwideGross = int(worldwideGross)
            #print("Worlwide gross: " + str(worldwideGross))
        except:
            worldwideGross = "NA"

        try:
            profitOrLoss = worldwideGross - budget
            #print("Profit or loss: " + str(profitOrLoss))
        except:
            profitOrLoss = "NA"

        try:
            rating = pageSoup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'}).get_text()
            rating = rating[:rating.index('/')]
            rating = float(rating)
            #print("Rating: " + str(rating))
        except:
            rating = "NA"

        try:
            reviewCount = pageSoup.find('div', attrs={'data-testid': 'reviews-header'}).get_text()
            reviewCount = reviewCount.replace('User reviews', "")
            reviewCount = reviewCount.replace('Review', "")
            #print(reviewCount)

            if 'K' in reviewCount:
                reviewCount = reviewCount.replace('K', "")
                reviewCount = float(reviewCount) * 1000
            else:
                reviewCount = int(reviewCount)
        except:
            reviewCount = "NA"

        try:
            headlineItems = pageSoup.find_all('span', class_='sc-8c396aa2-2 itZqyK')
            certificate = headlineItems[1].get_text()
            #print(certificate)
        except:
            certificate = "NA"

        try:
            openingWeekend = pageSoup.find('li', attrs={'data-testid': 'title-boxoffice-openingweekenddomestic'})
            listItems = openingWeekend.find_all('span', class_='ipc-metadata-list-item__list-content-item')
            rawDate = listItems[1].get_text()
            month = rawDate[:rawDate.index(' ')]
            datetime_object = datetime.strptime(month, "%b")
            month_number = datetime_object.month
            #print(month_number)
        except:
            month = "NA"

        try:
            ranking = pageSoup.find('div', attrs={'data-testid': 'hero-rating-bar__popularity__score'}).get_text()
            ranking = ranking.replace(',', "")
            ranking = int(ranking)
            #print(str(ranking))
        except:
            ranking = "NA"

        try:
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
        except:
            ratingCount = "NA"

        movieItem = [movieTitle, movieGenre, totalMinutes, budget, worldwideGross, profitOrLoss, rating, reviewCount, certificate, month_number, ranking, ratingCount]

        rawCensus.append(movieItem)

        completeRecord = True
        for x in range(len(movieItem)):
            #print(movieItem[x])
            if movieItem[x] == "NA":
                completeRecord = False
        if completeRecord:
            rawCensusMinusIncomplete.append(movieItem)

df = pd.DataFrame(rawCensus)
df.columns = ['Title', 'Genre', 'Runtime', 'Budget', 'Gross', 'Profit or Loss', 'Rating', 'Review Count', 'Certificate', 'Release Month', 'IMDB Ranking', 'Rating Count']
df.to_excel("P6 Raw Census Data.xlsx")

df2 = pd.DataFrame(rawCensusMinusIncomplete)
df2.columns = ['Title', 'Genre', 'Runtime', 'Budget', 'Gross', 'Profit or Loss', 'Rating', 'Review Count', 'Certificate', 'Release Month', 'IMDB Ranking', 'Rating Count']
df2.to_excel("P6 Raw Census Data Minus Incomplete Records.xlsx")

