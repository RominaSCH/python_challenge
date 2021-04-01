import requests
import os

def url_check(URL):
  for url in URL:
    if url[0:4] != "http": #앞에 https://없을경우 붙여주기.
      url = "https://" + url

    try: #예외가 발생할 가능성이 있는 코드
      req_url = requests.get(url)
      stat_url = req_url.status_code
    except: #예외가 발생했을 때 실행할 코드
      print(f"{url} is DOWN")
    else: #예외가 발생하지 않았을 때 실행할 코드
      print(f"{url} is UP")
    #if문의 의 DOWN이 제대로 실행되지 않고 무지하게 긴 오류가 발생해서 try except로 변경

print("Welcome to IsItDown.py")
check = 1 # 전체 동작 루프 변수
while check == 1:
  print("Please write a URL or URLs you want to check. (separated by comma\n")
  URL_f = input("").strip(" ") #공백없애기
  URL = URL_f.replace(' ','') #문자열 중간 공백 제거
  URLs = URL.split(",") # , 기준으로 쪼개기

  url_check(URLs)

  yn = 1
  while yn == 1:
    print("Do you want to restart?")
    answer = input("(y/n)")
    if answer in ["y", "Y"]:
      os.system("clear")
      yn = 0
    elif answer in ["n", "N"]:
      # os.system("clear")
      print("bye")
      check = 0
      yn = 0
    else:
      print("That's not a valid answer.")

