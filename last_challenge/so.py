import requests
from bs4 import BeautifulSoup

# URL = f"https://stackoverflow.com/jobs?q=python"

# 1.page 2.request 3.job extract

# def get_last_page(url):
#     result = requests.get(url)
#     soup = BeautifulSoup(result.text, "html.parser")
#     pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
#     last_page = pages[-2].get_text(strip=True)
#     return int(last_page)

def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find("h3", {
        "class": "fc-black-700"
    }).find_all("span",
                recursive=False)  #recursive=False 는 첫 번째의 span 만 가져올 수 있다.
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html["data-jobid"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}/"
    }

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        # print(f"Scrapping Stack Overflow Page : {page+1}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for res in results:
            job = extract_job(res)
            jobs.append(job)
    return jobs

def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}"
  # last_page = get_last_page(url)
  jobs = extract_jobs(5, url)
  return jobs
