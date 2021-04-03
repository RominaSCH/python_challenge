import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")
"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

url = "https://www.iban.com/currency-codes"
print("hello! Please Choose select a country by a number:")

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

len_list = 265 #len(result_list) 값 사용시 에러가 나서 지정, 해결못했음

for element in range(len_list):
  if result_list[element]["Currency"] == "No universal currency":
    del result_list[element]

for a in range(len_list):
  result_list[a]["No"] = a
  result_list[a]["Code"] = code_list[a]
  
for numb in range(len_list):
  print("# {} {}".format(result_list[numb]["No"], result_list[numb]["Country"]))


def choose_uno():
  print("\nWhere are you from? Choose a country by number.")
  uno = ""
  try:
    num = int(input("#: "))
    if 0 <= num < len_list:
        uno = result_list[num]["Code"]
        print(result_list[num]["Country"])
        choose_dos(uno)
    elif num >= len_list:
        print("Choose a number from the list")
        choose_uno()
  except ValueError:
    print("That wasn't a number.")
    choose_uno()

def choose_dos(uno):
  print("\nYou choose another country.")
  dos = ""
  try:
    num = int(input("#: "))
    if 0 <= num < len_list:
        dos = result_list[num]["Code"]
        print(result_list[num]["Country"])
        exchange_amount(uno, dos)
    elif num >= len_list:
        print("Choose a number from the list")
        choose_dos(uno)
  except ValueError:
    print("That wasn't a number.")
    choose_dos(uno)

def exchange_amount(uno, dos):
  num = 0
  print("\nHow many {} do you want to convert to {}".format(uno, dos))
  try:
    num = int(input("#: "))
    exchange_currency(num, uno, dos)
  except ValueError:
    print("That wasn't a number.")
    exchange_amount(uno, dos)

def exchange_currency(amount, con_uno, con_dos):
  try:
    convert_url = "https://transferwise.com/gb/currency-converter/{}-to-{}-rate?amount={}".format(con_uno, con_dos, amount)
    result = requests.get(convert_url)
    convert_soup = BeautifulSoup(result.text, "html.parser")
    cur = convert_soup.find("div",{"class":"js-Calculator"}).find("input")["value"]
    currency = float(cur)
    converted = amount * currency
    print("\n{} {} is {} {}".format(con_uno, amount, con_dos, converted))
  except:
    print("No country currency both or one.")

choose_uno() #start

# print(format_currency(5000, "KOR", locale="ko_KR"))