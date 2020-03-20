from os import listdir
from bs4 import BeautifulSoup
import requests
import time

#filenames = ['frwiki_homonymie/'+ f for f in listdir('frwiki_homonymie')]
filenames = ["frwiki_merged/" + f for f in listdir('frwiki_merged')]
output = open('frwiki_list_merged.txt', 'w')
#output = open("frwiki_homonymie.txt", 'w') 

total = len(filenames)
for name in filenames:
    with open(name, 'r') as f:
        html = f.read()
#        if 'homonymie' not in html:
#            continue
#        if "page d’homonymie" not in html.lower():
#            continue
        soup = BeautifulSoup(html, 'lxml')
        if not soup.find(id="homonymie"):
            continue
#        if len([href for href in soup.find_all('a', href=True) if href['href']=="/wiki/Aide:Homonymie"]) < 1:
#            continue
        total_senses = 0
        try:
            content = soup.find(id="mw-content-text")
            for pos in content.find_all('h2'):
                total_senses += 1
            # print(name.split("/")[-1][:-5], total_senses)
    #        total_senses -= 1  # ignore for french
            if total_senses>0:
                output.write(name.split("/")[-1][:-5] + "," + str(total_senses) + "\n")
        except Exception:
            continue
output.close()
