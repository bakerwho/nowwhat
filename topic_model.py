import re
from gensim import models, corpora
from nltk import word_tokenize
from nltk.corpus import stopwords

NUM_TOPICS = 10
STOPWORDS = stopwords.words('english')

def clean_text(text):
    tokenized_text = word_tokenize(text.lower())
    cleaned_text = [t for t in tokenized_text if t not in STOPWORDS and re.match('[a-zA-Z\-][a-zA-Z\-]{2,}', t)]
    return cleaned_text

# For gensim we need to tokenize the data and filter out stopwords
tokenized_data = []
for text in data:
    tokenized_data.append(clean_text(text))
