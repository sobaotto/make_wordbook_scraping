from selenium.webdriver.chrome.options import Options

options = Options()

options.add_argument("--headless")

import requests
import os, time, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import urllib.request
import pandas as pd
import numpy as np

routers = [
    "/meishi.html"
    ,"/doushi.html"
    ,"/keiyoushi.html"
]

for i,router in enumerate(routers,1):
    # launch chrome browser
    driver = webdriver.Chrome(options = options)
    #driver = webdriver.Chrome()
    # google image search
    driver.get("http://***********/tango/level" + str(-(-i//3)) +router)
    current_url = driver.current_url
    html = requests.get(current_url)

    bs = BeautifulSoup(html.content, 'lxml')

    elems = bs.select('source')
    
    #番号取得
    elems_number = bs.select('[class="divBunruiLeft"]')
    numbers = []
    for number in elems_number:
        numbers.append(number.text)
    
    #単語の日本語訳取得
    elems_tango_mean = bs.select('[class="divBunruiN"]')
    tango_means = []
    #例文の日本語訳取得
    elems_reibun_mean = bs.select('[class="divBunruiExN"]')
    reibun_means = []
    for (tango_mean,reibun_mean) in zip(elems_tango_mean,elems_reibun_mean):
        tango_means.append(tango_mean.text)
        reibun_means.append(reibun_mean.text)
    
    #単語の拼音取得
    tango_pinyin_elems = bs.select('[class="divBunruiP"]')
    tango_pinyin = []
    #例文の拼音を取得
    reibun_pinyin_elems = bs.select('[class="divBunruiExP"]')
    reibun_pinyin = []
    for (tango_pinyin_elem,reibun_pinyin_elem) in zip(tango_pinyin_elems,reibun_pinyin_elems):
        tango_pinyin.append(tango_pinyin_elem.text)
        reibun_pinyin.append(reibun_pinyin_elem.text)
    
    #例文を取得
    elems_example = bs.select('[class="divBunruiExC"]')
    ex_sentences = []
    for elem_example in elems_example:
        ex_sentences.append(elem_example.text.replace("。",""))
    #ex_sentences 
    
    #単語を取得
    elems_tango = bs.select('[class="divBunruiC"]')
    tangos = []
    for tango in elems_tango:
        tangos.append(tango.text)

    #URLの取得
    url_list = []   
    for elem in elems:  
        tango_reibun_urls = elem.attrs['src']
        encode_pre_url = urllib.parse.quote(tango_reibun_urls) 
        encode_url = encode_pre_url.replace("..","http://***********/tango") 
        url_list.append(encode_url)
        #ファイル名の取得
    
    #urlを単語と例文に分ける
    tango_urls = []
    reibun_urls = []
    for j,url in enumerate(url_list):
        if j%2==0:
            tango_urls.append(url)
        else:
            reibun_urls.append(url)    
            
    def make_file_name(cns,jps,pinyins):
        file_names = []
        for (number,cn,jp,pinyin) in zip(numbers,cns,jps,pinyins):  
            file_name = number
            file_names.append(file_name)
        return file_names
    
        #例文の頭に単語を載せる関数
    def reibun_top(file_names):
        reibun_file_names = []
        for reibun_file_name in file_names:
            reibun_file_names.append(reibun_file_name.replace("_","_【"+tango+"】"))
        return reibun_file_names 
    
    file_names = make_file_name(tangos,tango_means,tango_pinyin)
    #reibun_file_names = reibun_top(file_names)
    
    
    save_dir = "レベル" + str(-(-i//3))
    print("\n",i,"番目")
    if save_dir not in os.listdir("./"):
        os.mkdir(save_dir)
        print("保存先フォルダを、作成しました。\n")
    else:
        print("保存先フォルダは、作成済みです。\n")
    
    #実際の取得作業（URLとファイル名が必要）
    for (url, name) in zip(tango_urls, file_names):
        done = False
        count = 0
        while done == False:
            #print("{}.mp3".format(name))
            try:
                file_name = "{}.mp3".format(name)
                urllib.request.urlretrieve(url,os.path.join(save_dir, file_name))
                #time.sleep(1)
                done = True
            except:
                if count<10:
                    count+=1
                else:
                    print("ダメだった。")
                    break
        if count != 0:
            print(file_name,">"*5,count)

    driver.quit()

driver.quit()
