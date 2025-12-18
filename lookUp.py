import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

def remove_fluff(sentence:str):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return set([word for word in tokens if word not in stop_words])