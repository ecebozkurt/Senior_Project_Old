import requests
from bs4 import BeautifulSoup
import re
import unidecode


# TODO Description
def clean_html_text(http_response):
    soup = BeautifulSoup(http_response.text, 'html.parser')
    # get rid of Javascript and CSS elements
    [script.extract() for script in soup(['script', 'style'])]
    text = soup.get_text()
    # get rid of special accents for easier search
    normal = unidecode.unidecode(text)
    return normal


# TODO Description
def get_data(url, type_list):
    http_response = requests.get(url)
    list_str = clean_html_text(http_response)
    head, sep, list_str = list_str.partition("Most Popular " + type_list)
    head, sep, list_str = list_str.partition("Most Popular " + type_list)
    list_str, sep, tail = list_str.partition("ArkivMusic")

    # get rid of the values inside parantheses
    list_str = re.sub(r'\(.+\)', '', list_str)

    # get their last names only for easier search, if they are people
    if type_list != "Labels" or type_list != "Ensembles":
        list_str_last = re.sub(r',.+\n', '', list_str)
        list_str += list_str_last

    list_str = list_str.strip()
    return list_str


# TODO Description
def make_lists():
    conductor_str = get_data("https://www.arkivmusic.com/classical/NameList?featured=1&role_wanted=3", "Conductors")
    label_str = get_data("https://www.arkivmusic.com/classical/MusicList?featured=1&role_wanted=6", "Labels")
    performer_str = get_data("https://www.arkivmusic.com/classical/NameList?featured=1&role_wanted=2", "Performers")
    ensemble_str = get_data("https://www.arkivmusic.com/classical/NameList?featured=1&role_wanted=4", "Ensembles")
    return





