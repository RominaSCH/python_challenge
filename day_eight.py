import os
import csv
import requests
from bs4 import BeautifulSoup
import re

os.system("clear")
alba_url = "http://www.alba.co.kr"

first_page_info = []
loc_list = []
title_list = []
work_time_list = []
pay_list = []
regist_list = []
jobs = []

def fisrt_page_job():
  result = requests.get(alba_url)
  soup = BeautifulSoup(result.text, "html.parser")
  title = soup.find_all("span",{"class":"company"})
  impact = soup.find_all("li",{"class":"impact"})
  for element in impact:
    title = element.find("span",{"class":"company"}).get_text()
    link = element.find("a",{"class":"goodsBox-info"})["href"]
    first_page_info.append(["{}".format(title), "{}".format(link)])

def save_to_file(jobs, st):
  name = first_page_info[st][0]
  file = open(f"{name}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["location", "title", "work_time", "pay", "regist_Date"])
  for i in jobs:
    writer.writerow(i)
  return 

def scrapper_jobs():
  for i in range(len(first_page_info)): #각 링크마다 직업정보 얻기
    result = requests.get(first_page_info[i][1])
    soup = BeautifulSoup(result.text, "html.parser")
    body = soup.find("tbody").find_all("td")
    
    #location list
    location = soup.find_all("td",{"class":"local first"})
    for place in location:
      loc = place.get_text()
      loc = re.sub('\xa0', " ", loc)
      loc_list.append(loc)

    for element in body:
      try: #title list
        title = element.find("span",{"class":"company"}).get_text(strip=True)
        title_list.append(title)
      except:
        pass
      
      try: #work time list
        work_time = element.find("span", {"class":["consult", "time"]}).get_text()
        work_time_list.append(work_time)
      except:
        pass

      try: #pay list
        pay_hour = element.find("span",{"class":"payIcon"}).get_text()
        pay_money = element.find("span", {"class":"number"}).get_text()
        pay_list.append("{} {}".format(pay_hour, pay_money))
      except:
        pass

      try: # regist list(미완, 하루이상 지난 목록 못불러옴)
        if element.find("td", {"class":"regDate"}) == None:
          regist_date = element.find("strong").get_text()
          regist_list.append(regist_date)
        elif element.find("td", {"class":"regDate"}) != None:
          regist_date = element.find("td",{"class":"regDate"}).string
          regist_list.append(regist_date)
      except:
        pass

    try: #jobs list 만듬.
      for ele in range(len(title_list)):
        jobs.append([f"{loc_list[ele]}",f"{title_list[ele]}",f"{work_time_list[ele]}",f"{pay_list[ele]}",f"{regist_list[ele]}"])
    except:
      pass
    
    save_to_file(jobs, i) #save csv file 
    del jobs[:] #다음 링크 작업을 위한 초기화
    del loc_list[:]
    del title_list[:]
    del work_time_list[:]
    del pay_list[:]
    del regist_list[:]

def init():
  fisrt_page_job()
  scrapper_jobs()
  save_to_file(jobs, 0)

init()