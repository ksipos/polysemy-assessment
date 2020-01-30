from os import listdir
from bs4 import BeautifulSoup
import requests
import time

filenames = ['google/'+ f for f in listdir('google')]
output = open('google_list.txt', 'w')
count_zeros = 0
for name in filenames:
    with open(name, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'lxml')
        total_senses = 0
        for pos in soup.find_all("section", {"class":"gramb"}):
            lst = pos.find_all('ul', {'class':'semb'})
            if lst:
                total_senses += len(lst[0].findChildren('li', recursive=False))
            else:
                total_senses += 1
        # print(name.split("/")[-1][:-5], total_senses)
        if total_senses == 0:
            count_zeros += 1
            if name.split("/")[-1][:-5] +".html" in listdir('google_v2'):
                continue
            r = requests.get(url="https://www.lexico.com/en/definition/" + name.split("/")[-1][:-5])
            time.sleep(5)
            soup = BeautifulSoup(r.content, 'lxml')
            try:
                new_name = soup.find_all('ul', {'class': "search-results unpadded"})[0].findChildren('li', recursive=False)[0].text
                r = requests.get(url="https://www.lexico.com/en/definition/" + new_name)
                time.sleep(5)
                with open("google_v2/" + name.split("/")[-1], 'w') as f2:
                    f2.write(str(r.content))
            except Exception:
                print("Exception: ", name)
            continue
        output.write(name.split("/")[-1][:-5] + "," + str(total_senses) + "\n")

total = len(filenames)
filenames = ['google_v2/'+ f for f in listdir('google_v2')]
count_zeros = 0
for name in filenames:
    with open(name, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'lxml')
        total_senses = 0
        for pos in soup.find_all("section", {"class":"gramb"}):
            lst = pos.find_all('ul', {'class':'semb'})
            if lst:
                total_senses += len(lst[0].findChildren('li', recursive=False))
            else:
                total_senses += 1
        # print(name.split("/")[-1][:-5], total_senses)
        if total_senses == 0:
            count_zeros += 1
            print(name)
        output.write(name.split("/")[-1][:-5] + "," + str(total_senses) + "\n")
        
        
print(total, "/", count_zeros)
output.close()