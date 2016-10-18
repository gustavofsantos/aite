#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import sys
import urllib

url = "http://www.allitebooks.com/"
book_list = {}
download_list = []

def run(command):
    global url
    global book_list
    parts = command.split(' ')
    parts.reverse()
    link = url
    while len(parts) > 0:
        part = parts.pop()
        if part == 'list':
            list_articles(url)
        elif part == 'search':
            s = '+'.join(parts)
            link = url + '?s=' + s
            list_articles(link)
        elif part == 'data':
            view_booklist()
        elif part == 'download':
            parts.reverse()
            book = ' '.join(parts)
            download(book_list[book])
        elif part == 'exit':
            print('~ bye ~')
            sys.exit()

def view_booklist():
    global book_list
    for book in book_list:
        print('\"{}\"\n\t> {}'.format(book, book_list.get(book)))

def list_articles(link):
    global url
    global book_list

    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html5lib")
    articles = soup.find_all('article')
    i = 0
    page_count = 1
    page_total = 0

    # how much pages have?
    try:
        temp = soup.find_all('span', {'class': 'pages'})[0].text.split(' ')
        
        page_count = int(temp[0])
        page_total = int(temp[2])

        print("{} of {}".format(page_count, page_total))

        for article in articles:
                titles = article.find_all('h2')
                for title in titles:
                    names = title.find_all('a')
                    for name in names:
                        book_list[name.text] = name.get('href')
                        print('[{}] {}'.format(i, name.text))
                        i += 1

        while page_count < page_total or page_count > 0:
            com = input('next | prev > ')
            if com == 'next':
                page_count += 1
                new_link = url + '/page/{}/'.format(page_count) + link[len(url):len(link)-1]
                r = requests.get(new_link)
                soup = BeautifulSoup(r.content, "html5lib")
                articles = soup.find_all('article')

                for article in articles:
                    titles = article.find_all('h2')
                    for title in titles:
                        names = title.find_all('a')
                        for name in names:
                            book_list[name.text] = name.get('href')
                            print('[{}] {}'.format(i, name.text))
                            i += 1
            elif com == 'prev':
                i -= 10
                if page_count > 1:
                    page_count += 1
                    new_link = url + '/page/{}/'.format(page_count) + link[len(url):len(link)-1]
                    r = requests.get(new_link)
                    soup = BeautifulSoup(r.content, "html5lib")
                    articles = soup.find_all('article')

                    for article in articles:
                        titles = article.find_all('h2')
                        for title in titles:
                            names = title.find_all('a')
                            for name in names:
                                book_list[name.text] = name.get('href')
                                print('[{}] {}'.format(i, name.text))
                                i += 1
                else:
                    print('[-] Unable do back, is the main page')
            elif com == 'ok':
                break
    except:
        print('[-] Nothing was found')

def download(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html5lib")
    dl_links = soup.find_all('span', {'class': 'download-links'})

    book_link = dl_links[0].find_all('a')[0].get('href')

    book_name = book_link.split('/')[-1]
    
    print('[*] Downloading from {}'.format(book_link))

    with open(book_name, 'wb') as file:
        req = requests.get(book_link)
        file.write(req.content)
        
    print('[+] Saved as {}'.format(book_name))


def main():
    commands = ['list', 'search', 'data', 'download', 'exit']
    while True:
        print(commands)
        prompt = input('> ')
        run(prompt)

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == '--help':
            print('help')
        else:
            print('[-] Error. Run ./aite.py --help for help')
    else:
        main()

