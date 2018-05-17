import sys
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import os

website_code = ""

if not os.path.isdir("images"):
    os.mkdir('images')


def download_image(disease_image_url, diseases_pest_name):
    urllib.request.urlretrieve(disease_image_url, os.path.join(
        'images', diseases_pest_name + ".jpg"))


def get_correct_url(url):
    parsed_url = urlparse(url)
    if bool(parsed_url.scheme):
        return url
    else:
        return "http://www.agriculture.gov.au" + url


try:
    page = requests.get("http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases")
except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

soup = BeautifulSoup(page.content, 'html.parser')

list_of_diseases_names = []
list_of_disease_image_url = []
list_of_origins = []
list_of_identity = []
list_of_legal = []
list_of_secure = []
list_of_columns_name = ["Disease Name", "Image link", "Origin", "See if you can identify the pest",
                        "Check what can legally come into Australia", "Secure any suspect specimens"]

list_of_diseases = list(soup.find("ul", class_="flex-container").children)
for disease_li in list_of_diseases:
    anchor = disease_li.find("a", href=True)
    diseases_pest_name = str.strip(anchor.getText())
    website_code = website_code + "<h1>" + diseases_pest_name + "</h1><br>"
    disease_image_url = get_correct_url((anchor.find("img", src=True)["src"]))
    website_code = website_code + "<img src = '" + disease_image_url + "'/>" + "<br>"
    try:
        download_image(disease_image_url, diseases_pest_name)
    except:
        disease_image_url = os.path.join('images', 'blank.jpg')

    disease_image_url = os.path.join(os.getcwd(), 'images', diseases_pest_name + '.jpg')
    disease_image_url = "=HYPERLINK(\"file:\\\\" + disease_image_url + "\",\"Click here to see " + diseases_pest_name + "\")"
    pest_info_url = get_correct_url(str.strip(anchor["href"]))
    list_of_diseases_names.append(diseases_pest_name)
    list_of_disease_image_url.append(disease_image_url)
    try:
        disease_page = requests.get(pest_info_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    pest_soup = BeautifulSoup(disease_page.content, 'html.parser')
    all_info = str(pest_soup.find("div", class_="pest-header-content"))
    o = all_info.split("<strong>")
    origin = ''
    titles = []
    for i in o:
        if 'origin' in i.lower():
            origin = i.split('strong>')[1].split('<br')[0]
            break;
        else:
            origin = ' '
    try:
        collapsefaq = list(pest_soup.find('div', id='collapsefaq').find_all('div', class_='hide'))
    except:
        identify = " "
        legal = " "
        secure = " "
        list_of_identity.append(identify)
        list_of_legal.append(legal)
        list_of_secure.append(secure)
        list_of_origins.append(origin)
        website_code = website_code + "<h4>Origin </h4>" + origin + "<br>"
        website_code = website_code + "<h4>See if you can identify the pest </h4>" + identify + "<br>"
        website_code = website_code + "<h4>Check what can legally come into Australia </h4>" + legal + "<br>"
        website_code = website_code + "<h4> Secure any suspect specimens </h4>" + secure + "<br>"
        website_code = website_code + "<br><br><hr><br><br>"
        continue
    identify = str(collapsefaq[0].get_text()).strip()
    legal = str(collapsefaq[1].get_text()).strip()
    secure = str(collapsefaq[2].get_text()).strip()
    list_of_origins.append(origin)
    list_of_identity.append(identify)
    list_of_legal.append(legal)
    list_of_secure.append(secure)
    website_code = website_code + "<h4>Origin </h4>" + origin + "<br>"
    website_code = website_code + "<h4>See if you can identify the pest </h4>" + identify + "<br>"
    website_code = website_code + "<h4>Check what can legally come into Australia </h4>" + legal + "<br>"
    website_code = website_code + "<h4> Secure any suspect specimens </h4>" + secure + "<br>"
    website_code = website_code + "<br><br><hr><br><br>"

master_list = [list_of_diseases_names, list_of_disease_image_url, list_of_origins, list_of_identity, list_of_legal,
               list_of_secure]
zipped = list(zip(list_of_columns_name, master_list))
data = dict(zipped)
df = pd.DataFrame(data)
df.to_excel("Result.xlsx")

with open("index.html", "w+", encoding='utf-8') as web_page:
    web_page.write(website_code)

print("DONE")
