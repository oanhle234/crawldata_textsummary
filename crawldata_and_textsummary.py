import requests
import re
import bs4 as bs
import nltk
import heapq
from bs4 import BeautifulSoup
from lxml import html
nltk.download('punkt')
nltk.download ('stopwords')
nltk.download ('corpus')


url = 'https://news.ycombinator.com/'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

def title():
    list_title = soup.find_all('a', class_='titlelink')
    for title in list_title:
        print (title.get_text())
    return()

def summary():
    data = bs.BeautifulSoup(x, 'lxml')
    paragraphs = data.find_all('p')

    article_text = " "
    for p in paragraphs:
        article_text += p.text

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values(), default=0)

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    print('SUMMARY:')
    print(summary)
    print('*' * 20)
    return()

list_link = soup.find_all(class_='titlelink')
#for i in list_link:
#    print (i.get('href'))

for link in list_link:
    url_article = link.get('href')
    source = requests.get(url_article)
    x = source.text
    
    summary()
    #if re.search('^http', url_article):
    #    print(url_article)
    #else:
    #    url_of_relative_path = 'https://news.ycombinator.com/' + url_article
    #    print(url_of_relative_path)
