import requests
from bs4 import BeautifulSoup
from urllib import parse
from datetime import datetime
import time

keyword = input("검색어를 입력하세요.")
page = int(input("가져오고 싶은 페이지 수를 입력하세요."))

base_url = "https://www.coupang.com"
link = '/np/search?q={kerword}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={page}&rocketAll=false&searchIndexingToken=&backgroundColor='

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'    
}

def coupang_info(link):
    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.text)
    items = soup.find_all('li', attrs ={"class":"search-product"})

    for item in items:
        ad = item.find('span', attrs={"class" : "ad-badge-text"})
        if ad is not None:
            if ad.text == "광고":
                print("광고입니다. 건너뜁니다.")
                continue

        title = item.find('div', attrs={"class" : "name"}).text
        title = title.rstrip("\n")
        title = title.replace(",", "")
        print(title)

        link = item.find('a', href=True)['href']
        link = base_url + link
        print(link)

        price = item.find('strong', attrs={"class" : "price-value"}).text
        price = price.rstrip("\n")
        price = price.replace(",", "")
        print(price)

        rating = item.find('em', attrs={"class" : "rating"})
        
        if rating is not None:
            rating = rating.text
            print("별점있다.")
        else:
            print("별점없다.")
            rating = "없음"
        print(rating)

        reviews = item.find("span", attrs={"class" : "rating-total-count"})

        if reviews is not None:
            reviews = reviews.text
            reviews = reviews.replace("(", "")
            reviews = reviews.replace(")", "")            
            print("리뷰있다.")
        else:
            print("리뷰없다.")
            reviews = "없음"
        print(reviews)

        docs = open("./coupang_info.csv", "a", encoding='utf-8-sig',)
        docs.write("{}, {}, {}, {}, {} \n".format(title, link, price, rating, reviews))
        docs.close()

for i in range(1, page):
    link = link.format(keyword = keyword, page = i)
    print(link)
    coupang_info(base_url+link)