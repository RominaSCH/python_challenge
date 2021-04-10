import requests
from bs4 import BeautifulSoup
import os

# 1.page 2.request 3.job extract

def extract_job(res):
    title = res.find("span", {"class": "title"}).get_text()
    company = res.find("span", {"class": "company"}).get_text()
    location = res.find("span", {"class": "region"}).get_text()
    link = res.select_one("li > a")["href"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://weworkremotely.com{link}"
    }

def extract_jobs(word):
  jobs = []
  try:
    URL = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    resul = requests.get(URL)
    soup = BeautifulSoup(resul.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    for res in results:
        job = extract_job(res)
        jobs.append(job)
  except:
    pass
    
  return jobs

def get_jobs(word):
  jobs = extract_jobs(word)
  return jobs