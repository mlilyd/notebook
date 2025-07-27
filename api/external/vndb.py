from api.api import API
import requests

class VNDB(API):

    def __init__(self):
        '''API for fethcing information from VNDB'''
        super().__init__("https://api.vndb.org/kana", "vndb")
        self.header = {'content-type': 'application/json'}
        self.fields = "id, title, image.url, alttitle, aliases, olang, description, length_minutes, length, average, rating, relations.relation, tags.name, editions.name, developers.name, extlinks.url, extlinks.label, devstatus, released"

    def searchByTitle(self, title):
        json_data = {
            "filters": ["search", "=", title],
            "fields" : self.fields
        }
        search = requests.post(self.url+"/vn", json= json_data, headers=self.header).json()
        return search['results']
    
    def getByID(self, id):
        json_data = {
            "filters": ["id", "=", id],
            "fields" : self.fields
        }
        search = requests.post(self.url+"/vn", json= json_data, headers=self.header).json()
        return search['results'][0]
    
    def getEntryID(self, entry):
        return entry['id']
    
    def getEntryTitle(self, entry):
        return entry['title']
    
    def getEntryAuthors(self, entry):
        return entry['developers'][0]['name']
    
    def getBlurb(self, entry):
        return f"[bold]{entry['title']}[/bold]\n\n{entry['description']}"
    
    def to_html(self, entry):
        res = f"<table><tr><td rowspan='2'><img width=250px src='{entry['image']['url']}'></th><th>{entry['title']}</th></tr>><tr><td>{entry['description']}</td></tr>"
        for key in entry.keys():
            if key in ['image', 'title', 'description']:
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"
    