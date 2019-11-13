import requests
from bs4 import BeautifulSoup
import nltk


# TODO Edit To Actually Get User Input
# TODO Description
def get_keywords_from_user():
    return "chopin", "etudes"


# TODO Description
def construct_url(composer_last_name, piece):
    user_keywords = "best recording " + composer_last_name + "+" + piece
    user_keywords = user_keywords.replace(" ", "+")
    return "https://www.google.com/search?q=" + user_keywords


# TODO Gracefully Exit instead of the string written
# TODO Description
def http_requests(url):
    http_response = requests.get(url)
    if http_response.status_code == 200:
        return http_response
    else:
        return "Try a different URL"


# TODO Description
def parse_google_search(http_response):
    soup = BeautifulSoup(http_response.text, 'html.parser')

    # parse the html code that the http request returns by first finding all a tags
    a_tags = soup.findAll('a')

    # put all of the actual URL results in an array
    search_results = []
    for value in a_tags:
        url_string = value.get("href")
        if "url" in url_string:
            # get rid of the first 7 characters of the string and get rid of any unnecessary search queries after "&"
            url_string_clean = url_string[7:]
            index = url_string_clean.index("&")
            url_string_clean = url_string_clean[:index]

            # make sure the search result does not include a youtube link or a google sign up
            if "youtube" not in url_string_clean and "google" not in url_string_clean:
                search_results.append(url_string_clean)

    return search_results


# TODO Description
def clean_html_text(http_response):
    soup = BeautifulSoup(http_response.text, 'html.parser')
    # get rid of Javascript and CSS elements
    [script.extract() for script in soup(['script', 'style'])]
    # find the main article
    body_text = soup.findAll('article')
    if body_text:
        # get rid of the html tags
        text = body_text[0].get_text()
    else:
        text = soup.get_text()

    return text


# TODO Description
def do_nlp(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    tokens = [nltk.tokenize.word_tokenize(sentence) for sentence in sentences]
    pos_tagged_tokens = [nltk.pos_tag(token) for token in tokens]
    ne_chunks = nltk.ne_chunk_sents(pos_tagged_tokens)
    print(list(ne_chunks)[0].pprint())
    return ne_chunks


# TODO Description
def write_to_file(composer, piece, results):
    file_name = composer + piece + ".txt"
    f = open(file_name, "a")
    f.write(results)
    f.close()
    return f


if __name__ == '__main__':
    # construct the google search url by getting the keywords from the user
    composer_name, piece_name = get_keywords_from_user()
    google_search_url = construct_url(composer_name, piece_name)
    response = http_requests(google_search_url)
    # parse the google search results and return a list of urls in the order in which they are displayed
    url_results = parse_google_search(response)
    # get response from the first google search result url
    first_search_response = http_requests(url_results[0])
    clean_text = clean_html_text(first_search_response)

    print(first_search_response.text)
    #write_to_file(composer_name, piece_name, str(clean_text))

    #do_nlp(clean_text)

