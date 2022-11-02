import string
import sys
import requests
import os

from bs4 import BeautifulSoup

saved_articles = []
global article_type, i


def get_content(url):
    r = requests.get(url)
    if r.status_code != 200:
        print(f"The URL returned {r.status_code}!")
        sys.exit()
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        r.close()
        return soup


def get_news_articles(url):
    soup = get_content(url)
    articles = soup.find_all('article')
    create_folder()
    global article_type
    for article in articles:
        if article.find('span', {'data-test': 'article.type'}).text == f'\n{article_type}\n':
            write_in_the_file(article.find('a').get('href'), article.find('a').text)


def get_body(url):
    soup = get_content(url)
    body = soup.find('div', class_='c-article-body main-content').text
    return body


def write_in_the_file(url, name):
    url = 'https://www.nature.com' + url
    for c in string.punctuation:
        name = name.replace(c, "")
    name = name.replace(" ", "_")
    body = get_body(url)
    global i
    file = open(f'Page_{i+1}/{name}.txt', 'wb')
    file.write(body.encode('utf-8'))
    file.close()
    saved_articles.append(f'Page_{i+1}/' + name + '.txt')


def create_folder():
    global i
    os.mkdir(f'Page_{i + 1}')


def switching_pages(num):
    global i
    for i in range(num):
        website = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={i+1}'
        get_news_articles(website)


def main():
    num_page = int(input())
    global article_type
    article_type = input()
    switching_pages(num_page)
    print('Saved articles:\n' + str(saved_articles))


if __name__ == '__main__':
    main()
