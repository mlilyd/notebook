from api.api import Scrapper
import requests
from bs4 import BeautifulSoup # type: ignore

class Libby(Scrapper):

    def __init__(self):
        '''API for extract data from Libby share pages'''
        super().__init__("https://share.libbyapp.com/title/", 'libby')

    def get_id_from_url(self, url):
        return url.split("/")[-1]
    
    def get_url_from_id(self, id):
        return f"{self.url}{id}"

    def extract_from_page(self, url):
 
        doc = requests.get(url).text
        soup = BeautifulSoup(doc, 'html.parser')
        table = soup.table.tbody.find_all("td")
        
        res = {
            "id"   : self.get_id_from_url(url),
            "title": soup.h1.text,
            "media_type": soup.h2.text,
            "authors" : table[0].text,
            "date_published" : table[1].text.replace("\\xe2\\x80\\x93", "-"),
            "audience" : table[2].text,
            "publisher" : table[3].text,
            "genre" : table[4].text,
            "blurb" : soup.article.text
        }
        return res
         
    def getBlurb(self, entry):
        try:
            return f"[bold]{entry['title']}[/bold] by [bold]{entry['authors']}[/bold]\n{entry['blurb']}"
        except KeyError:
            return entry['warning']
        
    def getEntryID(self, entry):
        return entry['id']

    def getEntryTitle(self, entry):
        return entry['title']
    
    def getEntryAuthors(self, entry):
        return entry['authors']
    
    def to_html(self, entry):
        res = "<table class='gridtable'>"
        for key in entry.keys():
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"
    


