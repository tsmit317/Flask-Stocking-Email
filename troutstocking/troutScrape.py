import requests
from bs4 import BeautifulSoup

class StockingScrape():

    def __init__(self):
        self.stock_dict = {}

    def scrape_stocking_info(self, troutSoup):
        stocking_dict = {}
        temp_list = []
        for i in troutSoup.findAll('td'):
            temp_list.append(i.get_text(strip=True))

        
        for i in range(0, len(temp_list), 4):
            if temp_list[i] + " County" in stocking_dict:
                stocking_dict[temp_list[i] + " County"].append([temp_list[i+1], temp_list[i+2]])
            else:
                stocking_dict[temp_list[i]  + " County"] = [[temp_list[i+1], temp_list[i+2]]]

        stocking_dict['Date Added'] = troutSoup.find('th', class_='dateHeaderCell').get_text()

        return stocking_dict    

    def update_stocking(self):
        trout_response = requests.get('https://www.ncpaws.org/PAWS/Fish/Stocking/Schedule/OnlineSchedule.aspx')
        troutWP = trout_response.content
        troutSoup = BeautifulSoup(troutWP, 'html.parser')
        
        self.stock_dict = self.scrape_stocking_info(troutSoup)
    

    def get_stocking_dict(self):
        return self.stock_dict


