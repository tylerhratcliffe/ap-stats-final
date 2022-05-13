import requests
from bs4 import BeautifulSoup
import pandas as pd

movies = []
results = []

for i in range(1,2):
    url = f"https://www.imdb.com/list/ls074451163/?st_dt=&mode=detail&page={i}&sort=user_rating,desc"
    request = requests.get(url)
    page = request.content

    soup = BeautifulSoup(page, 'lxml')
    pageMovies = soup.find_all('h3', class_='lister-item-header')
    movies.append(pageMovies)

#print(movies[1])

for i in range(len(movies)):
    for j in range(len(movies[i])):
        #title = movies[i][j].get_text()
        #print(title)

        link = movies[i][j].find('a')['href']
        fullLink = "https://www.imdb.com" + link
        print(fullLink)

        moviePage = requests.get(fullLink)
        moviePage_content = moviePage.content
        pageSoup = BeautifulSoup(moviePage_content, 'lxml')

        movieTitle = pageSoup.find('h1', attrs={'data-testid': 'hero-title-block__title'}).get_text()
        #print("Title: " + movieTitle)

        movieGenre = pageSoup.find('a', class_='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt').get_text()
        #print("Genre: " + movieGenre)

        runtime = pageSoup.find('li', attrs={'data-testid': 'title-techspec_runtime'}).get_text()
        runtime = runtime.replace('Runtime', "")
        if "hours" in runtime:
            split = runtime.split(' hours ')
        else:
            split = runtime.split(' hour ')
        hours = int(split[0])
        
        if "minutes" in split[1]:
            minutes = int(split[1].replace(' minutes', ""))
        else:
            minutes = int(split[1].replace(' minute', ""))
        totalMinutes = (hours * 60) + minutes
        #print("Runtime: " + str(totalMinutes))

        budget = pageSoup.find('li', attrs={'data-testid': 'title-boxoffice-budget'}).get_text()
        budget = budget.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz ¥€'})
        budget = int(budget)
        #print("Box office budget: " + str(budget))

        worldwideGross = pageSoup.find('li', attrs={'data-testid': 'title-boxoffice-cumulativeworldwidegross'}).get_text()
        worldwideGross = worldwideGross.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ$,()abcdefghijklmnopqrstuvwxyz ¥€'})
        worldwideGross = int(worldwideGross)
        #print("Worlwide gross: " + str(worldwideGross))

        profitOrLoss = worldwideGross - budget
        #print("Profit or loss: " + str(profitOrLoss))

        rating = pageSoup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'}).get_text()
        rating = rating[:rating.index('/')]
        rating = float(rating)
        #print("Rating: " + str(rating))

        reviewCount = pageSoup.find('div', attrs={'data-testid': 'reviews-header'}).get_text()
        reviewCount = reviewCount.replace('User reviews', "")
        reviewCount = reviewCount.replace('Review', "")
        #print(reviewCount)

        headlineItems = pageSoup.find_all('span', class_='sc-8c396aa2-2 itZqyK')
        certificate = headlineItems[1].get_text()
        #print(certificate)

        movieItem = [movieTitle, movieGenre, totalMinutes, budget, worldwideGross, profitOrLoss, rating, reviewCount, certificate]
        results.append(movieItem)

df = pd.DataFrame(results)
df.columns = ['Title', 'Genre', 'Runtime', 'Budget', 'Gross', 'Profit or Loss', 'Rating', 'Review Count', 'Certificate']
df.to_excel("Raw.xlsx")

