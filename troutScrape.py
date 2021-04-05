import requests
from bs4 import BeautifulSoup


def get_stocking():
    trout_response = requests.get('https://www.ncpaws.org/PAWS/Fish/Stocking/Schedule/OnlineSchedule.aspx')
    troutWP = trout_response.content
    troutSoup = BeautifulSoup(troutWP, 'html.parser')

    

    ndict = {}
    nlist = []
    for i in troutSoup.findAll('td'):
        nlist.append(i.get_text(strip=True))

    for i in range(0, len(nlist), 4):
        if nlist[i] in ndict:
            ndict[nlist[i]].append([nlist[i+1], nlist[i+2]])
        else:
            ndict[ nlist[i]] = [[nlist[i+1], nlist[i+2]]]

    ndict['Date Added'] = troutSoup.find('th', class_='dateHeaderCell').get_text()

    return ndict


