import requests
from bs4 import BeautifulSoup
import json
import os
from collections import OrderedDict
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
## python파일의 위치

def parse_wine21():
    # driver = webdriver.Chrome('/Users/RyuIlHan/Projects/python-project/websaver/websaver/chromedriver')
    # driver.get('https://google.com')

    # file_data = OrderedDict()
    # file_data["wine_name"] = "Computer"
    # file_data["language"] = "kor"
    # file_data["words"] = {'ram': '램', 'procces' : '프로세스'}

    # data = json.dumps(file_data, ensure_ascii=False, indent="\t") 

    # print(data)
    
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # resent id 164786
    id = 137197 #와인 시작 아이디
    foodCnt = 30 #음식 기본 추천수

    for i in range(130000,164786):    
        req = requests.get('http://www.wine21.com/13_search/wine_view.html?Idx='+str(i))
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        wineNameKor = soup.select('div.cnt > h4')
        wineNameEng = soup.select('div.cnt > div.name_en')
        wineId = id
        wineCountry = soup.select('span > img')
        wineColor = soup.select('div.price > em')
        wineAlcohol = soup.select('div.wine_info > dl > dd:nth-child(12)')
        winePrice = soup.select('dd > strong:nth-child(1)')
        wineVintage = soup.select('dd > strong:nth-child(2)') #trim 필요 (2011, 750ml)
        shopWhich = soup.select('ul>li>span:nth-child(2)')
        shopPhone = soup.select('ul>li>span:nth-child(3)')
        shopName = soup.select('ul>li>span>a')
        
        print(wineNameKor)
        print(str(i))



# "wine_image" : String,
# "wine_avgGrade" : Number,
# "wine_curationGrade" : number,
# "food" : [{"food_name": String, "food_cnt" : Number}],
# "size" : String,
# "user_rating" : [{"user_id" : String, "rating_start" : Number, }],
# "user_rating_cnt" : Number,
# "taste-rating" : {"sweetness" : Number},
# "date" : Date



    data = {}

    # for title in my_titles:
    #     data[title.text] = title.get('href')

parse_wine21()