import re
import io
import string
import emoji
import datefinder
import spacy
import en_core_web_sm
from spacy import displacy
from collections import Counter
import numpy as np
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

spacy_nlp = en_core_web_sm.load()


def remove_emojies(word):
    return emoji.demojize(word)


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


def remove_apostrophe(word):
    return decontracted(word)


def substitute_company_names(phrase):
    phrase = re.sub(r"\$[A-Za-z]+", "ORG", phrase)
    phrase = re.sub("Netflix", "ORG", phrase)
    phrase = re.sub("Disney", "ORG", phrase)
    phrase = re.sub("Apple", "ORG", phrase)
    phrase = re.sub("Alphabet", "ORG", phrase)
    phrase = re.sub("Tesla", "ORG", phrase)
    phrase = re.sub("Facebook", "ORG", phrase)
    phrase = re.sub("netflix", "ORG", phrase)
    phrase = re.sub("disney", "ORG", phrase)
    phrase = re.sub("baba", "ORG", phrase)
    phrase = re.sub("apple", "ORG", phrase)
    phrase = re.sub("alphabet", "ORG", phrase)
    phrase = re.sub("tesla", "ORG", phrase)
    phrase = re.sub("facebook", "ORG", phrase)
    phrase = re.sub("SPY", "ORG", phrase)
    phrase = re.sub("spy", "ORG", phrase)
    phrase = re.sub("spy500", "ORG", phrase)
    phrase = re.sub("S&P", "ORG", phrase)
    phrase = re.sub("S&P500", "ORG", phrase)
    phrase = re.sub("s&p500", "ORG", phrase)
    return phrase


def substitute_date(phrase):
    matches = datefinder.find_dates(phrase, source=True, index=True)
    indices = []
    number_dates = 0
    number_dates2 = 0
    y = 0
    try:
        for match in matches:
            indices.append(match[2])
        for i in indices:
            if number_dates == 0:
                phrase = phrase[:i[0]] + "  Date  " + phrase[i[1]:]
            else:
                phrase = phrase[:i[0] - number_dates2 + len("  Date  ") * y] + "  Date  " + phrase[
                                                                                            i[1] - number_dates2 + len(
                                                                                                "  Date  ") * y:]
            number_dates = +i[1] - i[0]
            number_dates2 = number_dates + number_dates2
            y += 1
    finally:
        return phrase


def substitute_prices(word):
    return re.sub(r"\$[0-9]+", "price", word)


def substitute_entities(phrase):
    doc = spacy_nlp(phrase)
    newString = phrase
    for e in reversed(doc.ents):
        start = e.start_char
        end = start + len(e.text)
        newString = newString[:start] + e.label_ + newString[end:]
    return newString


def remove_entities(words):
    entities = ['cardinal', 'date', 'event', 'price', 'org', 'fac', 'gpe', 'language', 'law', 'loc', 'money', 'norp',
                'ordinal', 'percent', 'person', 'product', 'quantity', 'time', 'work_of_art']
    return [i for i in words if i not in entities]


def remove_single_letters(words):
    return [i for i in words if len(i) > 1]


def remove_hyperlink(word):
    return re.sub(r"http\S+", "", word)


def to_lower(word):
    result = word.lower()
    return result


def remove_number(word):
    result = re.sub(r'\d+', '', word)
    return result


def remove_punctuation(word):
    # result = word.translate(str.maketrans(dict.fromkeys(string.punctuation)))
    return re.sub(r'[^A-Za-z]', ' ', word)


def remove_whitespace(word):
    result = word.strip()
    return result


def replace_newline(word):
    return word.replace('\n', '')


def remove_stop_words(words):
    result = [i for i in words if i not in ENGLISH_STOP_WORDS]
    return result


def filtering_pipeline(sentence):
    cleaning_utils = [substitute_date,
                      to_lower,
                      substitute_company_names,
                      substitute_prices,
                      remove_hyperlink,
                      remove_number,
                      remove_emojies,
                      remove_apostrophe,
                      remove_punctuation,
                      substitute_entities,
                      to_lower,  # Run to lower again since sometimes entities are with uppercase
                      replace_newline,
                      remove_whitespace]
    cleaning_tokens = [remove_stop_words,
                       remove_single_letters]
    for o in cleaning_utils:
        sentence = o(sentence)
    sentence = spacy_nlp(sentence)
    sentence = [sent.lemma_.strip() for sent in sentence]
    for i in cleaning_tokens:
        sentence = i(sentence)
    return sentence


def sentiment_analysis_pipeline(tokens):
    return remove_entities(tokens)


def convert_array(blob):
    """
    Using BytesIO to convert the binary version of the array back into a numpy array.

    :param BLOG blob: BLOB containing a NumPy array
    :return: One steaming hot NumPy array
    :rtype: numpy.array
    """
    out = io.BytesIO(blob)
    out.seek(0)

    return np.load(out)
