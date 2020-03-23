from os import listdir
from bs4 import BeautifulSoup
import requests
import time

filenames = ["frwiki_merged/" + f for f in listdir('frwiki_merged')]
output = open('frwiki_list_merged.txt', 'w')


total = len(filenames)
for name in filenames:
    with open(name, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'lxml')
        # The files that do not have a 'div' element with id equals to
        # 'homonymie' they are not homonymie pages
        if not soup.find(id="homonymie"):
            continue
        total_senses = 0
        try:
            content = soup.find(id="mw-content-text")
            for pos in content.find_all('h2'):
                total_senses += 1
            if total_senses > 0:
                output.write(name.split(
                    "/")[-1][:-5] + "," + str(total_senses) + "\n")
        except Exception:
            continue
output.close()
