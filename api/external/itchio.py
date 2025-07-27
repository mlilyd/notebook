from api.api import Scrapper
from bs4 import BeautifulSoup
import requests

class itchIO(Scrapper):
    
    def __init__(self):
        '''API for reading data from itch.io pages'''
        super().__init__("itch.io", "itchio")

    def get_id_from_url(self,url):
        return f"{url.split("/")[-2].split('.')[0]}:{url.split("/")[-1]}"
    
    def get_url_from_id(self,id):
        return f"https://{id.split(":")[0]}.{self.url}/{id.split(":")[1]}"

    def extract_from_page(self, url):
        doc = requests.get(url).text
        soup = BeautifulSoup(doc, 'html.parser')

        table = [i.text for i in soup.find("table").find_all("td")]
        keys = [table[i] for i in range(0, len(table), 2)]
        values = [table[i] for i in range(1, len(table), 2)]
        meta = dict(zip(keys,values))

        return {
            "id": self.get_id_from_url(url),
            "title": soup.find("title").text.strip(" by ")[0],
            "cover-image": soup.find_all("img")[0].attrs['src'],
            "description": soup.find("div", {'class':"formatted_description"}).text,
        } | meta
    
    
    def getBlurb(self, entry):
        try:
            return f"[bold]{entry['title']}[/bold] by [bold]{self.getEntryAuthors(entry)}[/bold]\n{entry['description']}"
        except KeyError:
            return entry['warning']
        
    def getEntryAuthors(self, entry):
        if "Author" in entry.keys():
            return entry['Author']
        else:
            return entry['Authors']
    
    def getEntryID(self, entry):
        return entry['id']
    
    def getEntryTitle(self, entry):
        return entry['title']
    
    def to_html(self, entry):
        res = f'<img width=250px src="{entry['cover-image']}">'
        res += "<table>"
        for key in entry.keys():
            if key == 'cover-image':
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"