import requests
import os, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import urllib.request
import pandas as pd

# launch chrome browser
driver = webdriver.Chrome()

urls = ["http://***********/tango/level1/meishi.html"
       ,"http://***********/tango/level1/doushi.html"
       ,"http://***********/tango/level1/keiyoushi.html"
        
       ,"http://***********/tango/level2/meishi.html"
       ,"http://***********/tango/level2/doushi.html"
       ,"http://***********/tango/level2/keiyoushi.html"
        
       ,"http://***********/tango/level3/meishi.html"
       ,"http://***********/tango/level3/doushi.html"
       ,"http://***********/tango/level3/keiyoushi.html"]

tango = []
tango_pinyin = []
tango_meaning = []
reibun = []
reibun_pinyin = []
reibun_meaning = []

for url in urls:
    driver.get(url)
    current_url = driver.current_url
    html = requests.get(current_url)

    bs = BeautifulSoup(html.content, 'lxml')

    tango_elems = bs.select('[class="divBunruiC"]')
    tango_pinyin_elems = bs.select('[class="divBunruiP"]')
    tango_meaning_elems = bs.select('[class="divBunruiN"]')
    reibun_elems = bs.select('[class="divBunruiExC"]')
    reibun_pinyin_elems = bs.select('[class="divBunruiExP"]')
    reibun_meaning_elems = bs.select('[class="divBunruiExN"]')

    for (tango_elem,tango_pinyin_elem,tango_meaning_elem,reibun_elem,reibun_pinyin_elem,reibun_meaning_elem) in zip(tango_elems,tango_pinyin_elems,tango_meaning_elems,reibun_elems,reibun_pinyin_elems,reibun_meaning_elems):
        tango.append(tango_elem.text)
        tango_pinyin.append(tango_pinyin_elem.text)
        tango_meaning.append(tango_meaning_elem.text)
        reibun.append(reibun_elem.text)
        reibun_pinyin.append(reibun_pinyin_elem.text)
        reibun_meaning.append(reibun_meaning_elem.text)

#単語データフレーム
df_tango = pd.DataFrame(
    {'単語':tango,
     '拼音':tango_pinyin,
     '意味':tango_meaning})

#例文データフレーム
df_reibun = pd.DataFrame(
    {'例文':reibun,
     '拼音':reibun_pinyin,
     '意味':reibun_meaning})


df_tango.to_excel("単語.xlsx")
df_reibun.to_excel("例文.xlsx")

driver.quit()

