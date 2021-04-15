import requests
from bs4 import BeautifulSoup
from datetime import date


class StockingScrape():

    def __init__(self):
        self.stock_dict = {}

    def scrape_stocking_info(self, troutSoup):
        stocking_dict = {}
        temp_list = []

        today =  date.today()
        t = today.strftime("%A - %B %d, %Y")
        dayofweek = today.strftime("%A")
      
        div_for_today = troutSoup.find('div', id= dayofweek.lower() + 'Container')
        if  div_for_today is not None:

            for i in div_for_today.findAll('td'):
                temp_list.append(i.get_text(strip=True))

            
            for i in range(0, len(temp_list), 4):
                if temp_list[i] + " County" in stocking_dict:
                    stocking_dict[temp_list[i] + " County"].append([temp_list[i+1], temp_list[i+2]])
                else:
                    stocking_dict[temp_list[i]  + " County"] = [[temp_list[i+1], temp_list[i+2]]]

            stocking_dict['Date Added'] = div_for_today.find('th', class_='dateHeaderCell').get_text()
       
        return stocking_dict    

    def update_stocking(self):
        trout_response = requests.get('https://www.ncpaws.org/PAWS/Fish/Stocking/Schedule/OnlineSchedule.aspx')
        troutWP = trout_response.content
        troutSoup = BeautifulSoup(troutWP, 'html.parser')
        
        self.stock_dict = self.scrape_stocking_info(troutSoup)
    
    def update_and_get_stocking_dict(self):
        self.update_stocking()
        return self.stock_dict

    def get_stocking_dict(self):
        return self.stock_dict

    def test_new(self):
        self.stock_dict = {'Caldwell County': [['WILSON CREEK', 'Delayed Harvest']],  'Date Added': 'Monday - August 12, 2021'}


