import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

print("hello! Please Choose select a country by a number:")

import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"
print("hello! Please Choose select a country by a number:")

def extract_country(url): #the love... 함수로 빼고싶다..
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  country = soup.find_all("td")

  country_list = []
  currency_list = []
  code_list = []
  number_list = []
  result_list = []

  for i in range(len(country)): #각 요소들 리스트 변환하는 반복문
    if i % 4 == 0:
      country_list += country[i]
    elif i % 4 == 1:
      currency_list += country[i]
    elif i % 4 == 2:
      code_list += country[i]
    elif i % 4 == 3:
      number_list += country[i]

  for x in range(len(country_list)): #No universal currency 솎아내기용 dic
    result_list.append({"Country": country_list[x], "Currency": currency_list[x]})

  code_len = len(code_list)
  for element in range(code_len): #왜 벌써 no universal 3개가 빠져서 len이 3이나 줄었는지 이해못함. 여기까지는 268개가 맞지않나?... 이 반복문에서 265개로 줄어야 하는거 아니냐구 ㅠㅠ
    if result_list[element]["Currency"] == "No universal currency":
      del result_list[element]

  for a in range(code_len):
    result_list[a]["No"] = a
    result_list[a]["Code"] = code_list[a]
  
  for numb in range(code_len):
    print("# {} {}".format(result_list[numb]["No"], result_list[numb]["Country"]))

  check = 1
  while check == 1:
    try: 
      number = int(input("#: "))
      if number > code_len:
        print("Choose a number from the list")
      elif 0 < number <= code_len:
        print("{} currency code is {}".format(result_list[number]["Country"], result_list[number]["Code"]))
        check = 0
    except:
      print("That wasn't a number.")

extract_country(url)

