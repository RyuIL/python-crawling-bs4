import requests
from bs4 import BeautifulSoup
import json
import os
from collections import OrderedDict
import time
import re
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
## python파일의 위치

def parse_wine21():
    # driver = webdriver.Chrome('/Users/RyuIlHan/Projects/python-project/websaver/websaver/chromedriver')
    # driver.get('https://google.com')

    file_data = OrderedDict()
    shop_data = OrderedDict()
    # file_data["wine_name"] = "Computer"
    # file_data["language"] = "kor"
    # file_data["words"] = {'ram': '램', 'procces' : '프로세스'}

    # data = json.dumps(file_data, ensure_ascii=False, indent="\t") 

    # print(data)
    
    #BASE_DIR = os.path.dirname(os.path.abspath(__file__))


    #frmMain > article > div.column_block_1.board_list.wine_view_wrap > div.column_detail2 > div.wine_info > dl > dt:nth-child(1)
    #frmMain > article > div.column_block_1.board_list.wine_view_wrap > div.column_detail2 > div.wine_info > dl > dd:nth-child(12)
#frmMain > article > div.column_block_1.board_list.wine_view_wrap > div.column_detail2 > div.wine_info > dl > dt:nth-child(11)
    # resent id 164786
    start = 137197 #와인 시작 아이디
    end = 164786
    foodCnt = 30 #음식 기본 추천수
    
    myid = 0
    #137813
    text = open("text.txt", "a", encoding="utf-8")
    for i in range(163857+1,end):    
        req = requests.get('http://www.wine21.com/13_search/wine_view.html?Idx='+str(i))
        html = req.text
        if html.find("와인정보가 검색되지 않았습니다.")!=-1:
            print("continue not find")
            continue
        print(i)
        soup = BeautifulSoup(html, 'html.parser')

        wineNameKor = soup.select('div.cnt > h4')
        wineNameEng = soup.select('div.cnt > div.name_en')
        wine21Id = i
        wineCountry = soup.select('span > img')
        wineColor = soup.select('div.price > em')

        wineAlcoholSelecter = soup.select('div.wine_info > dl > dt')
        wineAlcoholIsEmpty = True
        for idx in range(1,len(wineAlcoholSelecter)):
            if ("알코올도수"==wineAlcoholSelecter[idx].text.replace(" ", "")):
                alIndex = idx+1
                wineAlcohol = soup.select('div.wine_info > dl > dd:nth-child('+str(alIndex*2)+")")
                wineAlcoholIsEmpty = False
                break
            else : wineAlcoholIsEmpty=True
        if not wineAlcoholIsEmpty:
            if wineAlcohol[0].text.find("~")!=-1:
                print("continue")
                continue
        
        winePrice = soup.select('dd > strong:nth-child(1)')
        wineVintage = soup.select('dd > strong:nth-child(2)') #trim 필요 (2011, 750ml)
        shopWhich = soup.select('ul>li>span:nth-child(2)')
        shopPhone = soup.select('ul>li>span:nth-child(3)')
        shopName = soup.select('ul>li>span>a')
        
        # print(wineNameKor)
        # print(str(i))
        
        if wineNameKor:
            wineNameEngData = wineNameEng[0].text
            wineNameKorData = wineNameKor[0].text
            wineCountryData = wineCountry[0].get('alt')
            wineColorData = wineColor[0].text

            if not wineAlcoholIsEmpty : 
                wineAlcoholData = float(wineAlcohol[0].text[:-1])
            else : wineAlcoholData = -1
            winePriceData = winePrice[0].text
            myid = myid+1
            vintageSize = cleanText(wineVintage[0].text)
            wineVintageData = "정보없음"
            if len(vintageSize)==1:
                wineSizeData = vintageSize[0]
            else : 
                wineVintageData = vintageSize[0]
                wineSizeData = vintageSize[1]
            
            shopIsEmpty = True
            if shopName:
                shopDataArr = ""
                shopIsEmpty = False
                for idx in range(len(shopName)):
                    shopNameWhich = cleanShop(shopWhich[idx].text)
                    shopWhichData = shopNameWhich[0]
                    shopNameData = shopNameWhich[1]
                    shopPhoneData = shopPhone[idx].text
                    
                    shop_data["shop_witch"] = shopWhichData
                    shop_data["shop_name"] = shopNameData
                    shop_data["shop_phone"] = shopPhoneData

                    shopData = json.dumps(shop_data, ensure_ascii=False, indent="\t")
                    
                    
                    if idx!=len(shopName)-1:
                        shopDataArr = shopDataArr + shopData+","
                    else : 
                        shopDataArr = shopDataArr + shopData
                
                shopDataArr = "\"shop\" : ["+shopDataArr+"]"
                            
            file_data["wine_name_kor"] = wineNameKorData
            file_data["wine_name_eng"] = wineNameEngData
            file_data["wine_id"] = wine21Id
            file_data["wine_color"] = wineColorData
            file_data["wine_country"] = wineCountryData
            file_data["Alcohol"] = wineAlcoholData
            file_data["wine_size"] = wineSizeData
            file_data["price"] = winePriceData
            file_data["wine_vintage"] = wineVintageData
            file_data["id"]  = myid
            # file_data["shop"] = shopDataArr

            data = json.dumps(file_data, ensure_ascii=False, indent="\t")

            
            if not shopIsEmpty : 
                result = data[:-1]+","+shopDataArr+"},"
            else :
                result = data+","

            text.write(result+"\n")
            
            
            #print(data[:-1]+","+shopDataArr+"},")
    
    text.close()

def cleanText(readData):
    text = re.sub('[\(\)]', '', readData)
    vintageSize = text.split(', ')
    return vintageSize

def cleanShop(readData):
    text = re.sub('[\[]', '', readData)
    shopNameWhich = text.split('] ')
    return shopNameWhich

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