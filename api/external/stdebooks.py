from api.api import Scrapper

import requests
from bs4 import BeautifulSoup

class StdEBooks(Scrapper):

    def __init__(self):
        '''API for parsing Standard Ebook pages'''
        super().__init__("https://standardebooks.org","stdebooks")

    def get_id_from_url(self, url):
        return url.replace(self.url+"/ebooks/", "")
    
    def get_url_from_id(self, id):
        return f"{self.url}/ebooks/{id}"

    def extract_from_page(self, url):
        doc = requests.get(url).text
        soup = BeautifulSoup(doc, 'html.parser')

        temp = [i.text.strip() for i in soup.find("aside", {"id": "reading-ease"}).find_all("p")]

        return {
            "id"    : self.get_id_from_url(url),
            "title" : soup.find_all("header")[1].find("h1", {"property":"schema:name"}).text, 
            "author": soup.find_all("header")[1].find("a", {"property":"schema:author"}).text.strip(),
            "description": soup.find("section", {"id": "description"}).text.strip(),
            "tags"  : soup.find("ul", {"class": "tags"}).text.strip(),
            "length": temp[0],
            "additional-info": ", ".join(temp[1:]),
            "github": soup.find("a", {'class': 'github'}).attrs['href'], 
            "sources": [i.attrs["href"] for i in soup.find("section", {'id': 'sources'}).find_all("a")],
            'cover-image': self.url + soup.find("figure", {"class":"realistic-ebook"}).find('picture').find("img").attrs['src']
        }
    
    def getBlurb(self, entry):
        try:
            return f"[bold]{entry['title']}[/bold] by [bold]{entry['author']}[/bold]\n{entry['description']}"
        except KeyError:
            return entry['warning']
        
    def getEntryAuthors(self, entry):
        return entry['author']
    
    def getEntryID(self, entry):
        return entry['id']
    
    def getEntryTitle(self, entry):
        return entry['title']
    
    def to_html(self, entry):
        res = f"<table><tr><th><img width=250px src='{entry['cover-image']}'></th><th>{entry['title']}</th></tr>"
        for key in entry.keys():
            if key in ['cover-image', 'github', 'sources', 'title']:
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"

        res += f"<tr><td>github</td><td><a href = '{entry['github']}'>{entry['github']}</a></td></tr><tr><td>sources</td><td>"
        for link in entry['sources']:
            res += f"<a href='{link}'>{link}</a>"
        return res + "</td></tr></table>"