from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import sys
import requests

argv = sys.argv
argc = len(argv)
if argc != 2:
    print("Usage:", argv[0], "searchterm")
    exit(1)

searchterm = argv[1]
url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
# NEED TO DOWNLOAD CHROMEDRIVER, insert path to chromedriver inside parentheses in following line
browser = webdriver.Chrome()
browser.get(url)
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
counter = 0
succounter = 0

if not os.path.exists(searchterm):
    os.mkdir(searchterm)

for _ in range(500):
    browser.execute_script("window.scrollBy(0,10000)")

for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
    counter = counter + 1
    print( "Total Count:", counter)
    print( "Succsessful Count:", succounter)
    print( "URL:",json.loads(x.get_attribute('innerHTML'))["ou"])

    img = json.loads(x.get_attribute('innerHTML'))["ou"]
    imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]
    try:
        req = requests.get(img, params={'User-Agent': header})
        raw_img = req.content
        with open(os.path.join(searchterm , searchterm + "_" + str(counter) + "." + imgtype), "wb") as File :
            File.write(raw_img)
        succounter = succounter + 1
    except:
            print("can't get img")

print(succounter, "pictures succesfully downloaded")
browser.close()
