import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

url = "https://remoteok.io/remote-dev+python-jobs"

def extract_job(html):
  try:
    location = html.find("div",{"class":"location"}).get_text()
    company = html.find("h3",{"itemprop":"name"}).get_text()
    title = html.find("h2",{"itemprop":"title"}).get_text()
    job_id = html["data-id"]
  except:
    pass
  return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://remoteok.io/remote-jobs/{job_id}"
    }

def extract_jobs(word):
  try:
    url = f"https://remoteok.io/remote-{word}-jobs"
    jobs = []
    resul = requests.get(url, headers=headers)
    soup = BeautifulSoup(resul.text, "html.parser")
    results = soup.find_all("tr",{"class":"job"})
    for res in results:
      job = extract_job(res)
      jobs.append(job)
  except:
    pass
  return jobs
  
def get_jobs(word):
  jobs = extract_jobs(word)
  return jobs