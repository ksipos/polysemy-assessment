from os import listdir
from bs4 import BeautifulSoup
import requests
import time

filenames = ['larousse/'+ f for f in listdir('larousse')]
output = open('larousse_list.txt', 'w')

total = len(filenames)
for name in filenames:
    with open(name, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'lxml')
        total_senses = 0
        try:
            content = soup.find(id="definition")
            for pos in content.find_all("li", {"class": "DivisionDefinition"}):
                total_senses += 1
            # print(name.split("/")[-1][:-5], total_senses)
    #        total_senses -= 1  # ignore for french
            output.write(name.split("/")[-1][:-5] + "," + str(total_senses) + "\n")
        except Exception:
            continue
output.close()
