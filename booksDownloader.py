import requests
import time
from bs4 import BeautifulSoup

url= "https://link.springer.com/search/page/1?facet-content-type=%22Book%22&package=mat-covid19_textbooks#038;showAll=true&#038;facet-language=%22En%22&#038;sortOrder=newestFirst"

r = requests.get(url)
bs = BeautifulSoup(r.text, 'html.parser')

numOfPages = int(bs.find('span', class_='number-of-pages').get_text())

page = 1

while (page < numOfPages + 1):
    bookList = []
    bookCode = []
    
    booksInPage = bs.find_all('a', class_='title' , href=True)

    for i in range(len(booksInPage)):
        bookList.append( booksInPage[i].get_text() )

    for a in bs.find_all('a', class_='title', href=True):
        bookCode.append( a['href'].split("/")[3])
       
    for i in range(len(bs.find_all('a', class_='title', href=True))):
        urlDown = "https://link.springer.com/content/pdf/10.1007/" + bookCode[i]  + ".pdf"

        download = requests.get(urlDown)

        with open('C:/Users/Rafael/Documents/Livros/'+ bookList[i]  +'.pdf', 'wb') as pdf:
            pdf.write(download.content)
            print("Book: " + bookList[i] + "- Downloaded")

        time.sleep(3)

    page += 1

    url= "https://link.springer.com/search/page/" + str(page) + "?facet-content-type=%22Book%22&package=mat-covid19_textbooks#038;showAll=true&#038;facet-language=%22En%22&#038;sortOrder=newestFirst"
    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'html.parser')
