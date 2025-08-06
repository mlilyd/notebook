from api.api import Scrapper
from bs4 import BeautifulSoup
import requests

class Ao3(Scrapper):

    def __init__(self):
        '''API for reading data from AO3 pages'''
        super().__init__("https://archiveofourown.org/", "ao3")

    def extract_from_page(self, url):
        
        doc = requests.get(url).text
        soup = BeautifulSoup(doc, 'html.parser')
        return {
            "id"    : self.get_id_from_url(url),
            "title" : soup.body.find("h2", {"class": "title heading"}).text.replace("\\n","").strip(),
            "author" : soup.body.find("h3", {'class':'byline heading'}).text.replace("\\n","").strip(),
            "date_published" : soup.body.find("dd", {'class':'stats'}).find("dd", {"class":"published"}).text,
            "fandom" : [i.text for i in soup.body.find("dd", {'class':'fandom tags'}).find_all("a")],
            "summary" : soup.body.find("div", {'class': 'summary'}).find("blockquote").text.replace("\\n","").strip(),
            "language" : soup.body.find("dd", {'class':'language'}).text.replace("\\n","").strip(),
            "age_rating" : soup.body.find("dd", {'class':'rating tags'}).text.replace("\\n","").strip(),
            "warning_tags" : [i.text for i in soup.body.find("dd", {'class':'warning tags'}).find_all("a")],
            "category_tag" : [i.text for i in soup.body.find("dd", {'class':'category tags'}).find_all("a")],
            "characters" : [i.text for i in soup.body.find("dd", {'class':'character tags'}).find_all("a")],
            "other_tags" : [i.text for i in soup.body.find("dd", {'class':'freeform tags'}).find_all("a")],
            "last_update" : soup.body.find("dd", {'class':'stats'}).find("dd", {"class":"status"}).text,
            "word_count" : soup.body.find("dd", {'class':'stats'}).find("dd", {"class":"words"}).text,
            "chapters_count" : soup.body.find("dd", {'class':'stats'}).find("dd", {"class":"chapters"}).text,
            "comment_count" : soup.body.find("dd", {'class':'stats'}).find("dd", {"class":"comments"}).text,
            "kudos" : soup.body.find("dd", {'class':'stats'}).find("dd", {"class":"kudos"}).text,
            "bookmarks" : soup.body.find("dd", {'class':'stats'}).find("dd", {"class":"bookmarks"}).text,
            "hits" : soup.body.find("dd", {'class':'stats'}).find("dd", {"class":"hits"}).text
        }

    def get_id_from_url(self, url):
        return url.replace(f"{self.url}works/","").split("/")[0]

    def get_url_from_id(self, id):
        return f"{self.url}works/{id}"

    def getBlurb(self, entry):
        try:
            tags = ", ".join(entry['other_tags'])
            characters = ", ".join(entry['characters'])
            res =  f"{entry['title']} by {entry['author']}\n\nFandom: {entry['fandom']}\n\nCharacters: {characters}\n\n{entry['summary']}\n\n{tags}"
        except KeyError:
            res = entry['warning']
        return res
            
    def getEntryID(self, entry):
        return entry['id']
    
    def getEntryAuthors(self, entry):
        return entry['author']
    
    def getEntryTitle(self, entry):
        return entry['title']
    
    def to_html(self, entry):
        res = "<table class='gridtable'>"
        for key in entry.keys():
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"