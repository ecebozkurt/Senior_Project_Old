import nltk
import make_database
import scrape
import os


# TODO Edit To Actually Get User Input
# TODO Description
def get_keywords_from_user():
    return "chopin etudes"


# TODO Description
def do_nlp(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    tokens = [nltk.tokenize.word_tokenize(sentence) for sentence in sentences]
    pos_tagged_tokens = [nltk.pos_tag(token) for token in tokens]
    ne_chunks = nltk.ne_chunk_sents(pos_tagged_tokens)
    print(list(ne_chunks)[0].pprint())
    return ne_chunks


if __name__ == '__main__':
    conductor_list, conductor_last_list, performer_list, performer_last_list, \
    label_list, ensemble_list = make_database.get_strings()

    piece = get_keywords_from_user()
    dir_name = piece.replace(' ', "_")
    # scrape data, add it inside directory as text files
    scrape.scrape_main(piece)

    os.chdir(dir_name)
    # open each file into a string and start processing
    for filename in os.listdir(os.getcwd()):
        with open(filename, 'r') as file:
            data = file.read()
            sentences = nltk.tokenize.sent_tokenize(data)

    # move back up to the parent directory
    os.chdir("..")



