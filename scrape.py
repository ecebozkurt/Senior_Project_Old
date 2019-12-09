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

            # make sure the search result does not include a youtube link or a google sign up/sign in
            if "youtube" not in url_string_clean and "google" not in url_string_clean and \
                    "amazon" not in url_string_clean and "prestomusic" not in url_string_clean:
                search_results.append(url_string_clean)

    return search_results


# TODO Description
def clean_html_text(http_response):
    soup = BeautifulSoup(http_response.text, 'html.parser')
    # get rid of Javascript and CSS elements
    [script.extract() for script in soup(['script', 'style'])]
    text = soup.get_text()
    return text


# TODO Description
def gramophone_clean(text):
    strip_arr = ["Facebook", "Instagram", "Youtube", "YouTube", "Skip to main content", "Subscribe", "Magazine", "Reviews",
                "Podcast", "Apple", "Twitter", "Archive", "Forum", "Music", "Composers", "Artists", "Features", "Blogs",
                 "Contact Us", "Advertise", "House Rules", "Privacy Policy", "Terms & Conditions", "Latest issue",
                 "Read Review", "pf"]

    # for Deutsche Gramophon Remove everything after the Follow us text.
    text, sep, tail = text.partition('Follow us')
    head, sep, text = text.partition('No 1')

    for item in strip_arr:
        text = text.replace(item, "")

    return sep + text


# TODO Description
def talk_classical_clean(text):
    strip_arr = ["View Profile", "View Forum Posts", "View Blog Entries", "Reply With Quote", "Senior Member",
                 "Junior Member", "Banned", "Visit Homepage"]
    # start after the first forum entry
    head, sep, text = text.partition("#1")
    text, sep, tail = text.partition("Jump to page:")

    for item in strip_arr:
        text = text.replace(item, "")

    text_arr = text.split("Join Date")
    new_text_arr = []
    for item in text_arr:
        item = item.replace('\n', '')
        item = item.replace('\t', ' ')
        items = item.split("Likes (Received)")
        for i in items:
            new_text_arr.append(i)

    final_arr = []
    for item in new_text_arr:
        if "Likes (Given)" not in item:
            final_arr.append(item)

    # after we are done with getting rid of the unnecessary values, join the text delimited by \ns
    text = "\n".join(final_arr)
    return text


# TODO Description
def nyt_clean(text):
    strip_arr = ["Share This Page", "Continue reading the main story", "Advertisement", "Credit", "Associated Press",
                 "Photo" "Opt out or contact us anytime"]
    head, sep, text = text.partition("Continue reading the main story")

    # get rid of subscription popup
    head, sep, tail = text.partition("Newsletter")
    head2, sep, tail2 = tail.partition("Opt out or contact us anytime")
    text = head + tail2

    for item in strip_arr:
        text = text.replace(item, "")

    # get rid of the parts that are not the main article
    head, sep, tail = text.partition("Subscribe")
    text = head
    text = text.strip()
    return text


# TODO Description
def wfmt_clean(text):
    head, sep, text = text.partition("Share this Post")
    text, sep, tail = text.partition("Related Posts")
    text = text.strip()
    return text


# TODO Description
def quora_clean(text):
    text_arr = text.split("answer views")
    print(text_arr)
    return text


# TODO Description
def look_for_piece(text, composer, piece):
    if composer in text.lower() and piece in text.lower():
        return True
    else:
        return False


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
    # for each google search result get the response, and clean the text
    count = 1
    for url_result in url_results:
        search_response = http_requests(url_result)
        if type(search_response) != str:
            clean_text = clean_html_text(search_response)

            if "gramophone" in url_result:
                clean_text = gramophone_clean(clean_text)
            elif "talkclassical" in url_result:
                clean_text = talk_classical_clean(clean_text)
            elif "nytimes" in url_result:
                clean_text = nyt_clean(clean_text)
            elif "wfmt" in url_result:
                clean_text = wfmt_clean(clean_text)
            elif "quora" in url_result:
                clean_text = quora_clean(clean_text)
                
            # if the article actually includes the piece that the user is searching for
            if look_for_piece(clean_text, composer_name, piece_name):
                write_to_file(composer_name, piece_name + str(count), str(clean_text))
                # do_nlp(clean_text)
                count += 1


