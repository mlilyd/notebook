from api.api import API
import requests

class OMDB(API):

    def __init__(self):
        super().__init__("http://www.omdbapi.com/", "omdb")
        self.apikey = "ec990a9e"

    def searchByTitle(self, title):
        params = {
            'apikey': self.apikey,
            'plot': "full",
            't':title,
        }

        res = requests.post(self.url, params=params).json()
        return [] if 'Error' in res.keys() else [res]
    
    def getByID(self, id):
        params = {
            'apikey': self.apikey,
            'plot': "full",
            'i': id
        }
        return requests.post(self.url, params=params).json()

    def getEntryID(self, entry):
        return entry['imdbID']
    def getEntryTitle(self, entry):
        return entry['Title']
    def getEntryAuthors(self, entry):
        return entry['Director']
    def getBlurb(self, entry):
        return f"{entry['Title']}\n{entry['Plot']}\nYear: {entry['Year']}"
    
    def to_html(self, entry):
        res = f'<table> <tr> <td rowspan="2"><img width="175px" src="{entry["Poster"]}"></td> <td>{entry['Title']}</td></tr><tr><td>{entry['Plot']}</td></tr>'
        for key in entry.keys():
            if key in ["Poster", 'Title', "Ratings", "Response"]:
                continue
            else:
                res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        ratings = "<tr><td></td><th><b>Ratings</b></th></tr>"
        for i in entry["Ratings"]:
            ratings += f"<tr><td>{i['Source']}</td><td>{i['Value']}</td></tr>" 
        return res + ratings + "</table>"
