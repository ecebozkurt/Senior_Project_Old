import requests
import urllib.request
import time
from bs4 import BeautifulSoup


# TODO Edit To Actually Get User Input
def get_keywords_from_user():
    return "chopin", "etudes"


def construct_url(composer_last_name, piece):
    user_keywords = "best recording" + composer_last_name + "+" + piece
    user_keywords.replace(" ", "+")
    return "https://www.google.com/search?q=" + user_keywords


# TODO Gracefully Exit instead of the string written
def http_requests(url):
    http_response = requests.get(url)
    if http_response.status_code == 200:
        return http_response
    else:
        return "Try a different URL"


def parse_google_search(http_response):
    soup = BeautifulSoup(http_response.text, 'html.parser')
    # parse the html code that the http request returns by first finding all a tags
    a_tags = soup.findAll('a')

    # put all of the actual URL results in an array
    search_results = []
    for value in a_tags:
        url_string = value.get("href")
        if "url" in url_string:
            # get rid of the first 7 characters of the string
            search_results.append(url_string[7:])

    return search_results


def parse_website(http_response, composer, piece):
    soup = BeautifulSoup(http_response.text, 'html.parser')
    h2_p_tags = soup.findAll(['h2', 'p'])
    # for tag in h2_p_tags:
    #     tag_str = str(tag).lower()
    #     if piece in tag_str:
    #
    #         return tag_str
    return h2_p_tags


if __name__ == '__main__':
    # construct the google search url by getting the keywords from the user
    composer_name, piece_name = get_keywords_from_user()
    google_search_url = construct_url(composer_name, piece_name)
    response = http_requests(google_search_url)
    # parse the google search results and return a list of urls in the order in which they are displayed
    url_results = parse_google_search(response)

    # get response from the first google search result url
    first_search_response = http_requests(url_results[0])
    best_recording = parse_website(first_search_response, composer_name, piece_name)
    print(best_recording)






