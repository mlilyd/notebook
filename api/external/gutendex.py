from api.api import API
import requests

class Gutendex (API):

    def __init__(self):
        super().__init__("https://gutendex.com", "gutendex")

    def searchByTitle(self, title):
        params = {
            "search": title
        }
        return requests.get(self.url+"/books", params=params).json()['results']

    def getByID(self, id):
        params = {
            "ids": id
        }
        return requests.get(self.url+"/books", params=params).json()['results'][0]

    def getBlurb(self, entry):
        return entry['summaries']
    
    def getEntryAuthors(self, entry):
        return entry['authors'][0]['name']
    
    def getEntryID(self, entry):
        return entry['id']
    
    def getEntryTitle(self, entry):
        return entry['title']
    
    def to_html(self, entry):
        res = "<table class='gridtable'>"
        for key in entry.keys():
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"