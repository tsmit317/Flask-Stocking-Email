import requests
from bs4 import BeautifulSoup


def get_stocking():
    trout_response = requests.get('https://www.ncpaws.org/PAWS/Fish/Stocking/Schedule/OnlineSchedule.aspx')
    troutWP = trout_response.content
    troutSoup = BeautifulSoup(troutWP, 'html.parser')

    
    stocking_dict = {}
    temp_list = []
    for i in troutSoup.findAll('td'):
        temp_list.append(i.get_text(strip=True))

    
    for i in range(0, len(nlist), 4):
        if temp_list[i] + " County" in stocking_dict:
            stocking_dict[temp_list[i] + " County"].append([temp_list[i+1], temp_list[i+2]])
        else:
            stocking_dict[temp_list[i]  + " County"] = [[temp_list[i+1], temp_list[i+2]]]

    stocking_dict['Date Added'] = troutSoup.find('th', class_='dateHeaderCell').get_text()

    return stocking_dict


