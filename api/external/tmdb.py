from api.api import API
import requests

class TMDB(API):

    def __init__(self, authorization, type="movie"):
        super().__init__("https://api.themoviedb.org/3/", f"tmdb-{type}")
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {authorization}"
        }
        self.type = type
        self.img_url = "https://image.tmdb.org/t/p/w500"

    def searchByTitle(self, title):
        params = {
            "query": title
        }
        response = requests.get(f"{self.url}search/{self.type}?", headers=self.headers, params=params)
        return response.json()['results']
    
    def searchByTitle(self, title, language="en", release_year=0):
        params = {
            "query": title,
            "language": language,
            "primary_release_year": release_year
        }
        response = requests.get(f"{self.url}search/{self.type}?", headers=self.headers, params=params)
        return response.json()['results']
    
    def getByID(self, id):
        return requests.get(f"{self.url}{self.type}/{id}", headers=self.headers).json()
    
    def getEntryID(self, entry):
        return entry['id']
    
    def getEntryTitle(self, entry):
        temp = self.getByID(entry['id'])
        if self.type == "tv":
            return temp['name']
        else:
            return temp['title']
    
    def getEntryAuthors(self, entry):
        temp = self.getByID(entry['id'])
        if len(temp['production_companies']) > 0:
            return temp['production_companies'][0]['name']
        else:
            return ""
    
    def getBlurb(self, entry):
        return entry['overview']
    
    def to_html(self, entry):
        res = f"<table><tr><td rowspan='2'><img height=150px src='{self.img_url+entry['poster_path']}'></td>"
        if 'title' in entry.keys():
            res += f"<td>{entry['title']}</td></tr><tr><td>{entry['overview']}</td></tr>"
        else: 
            res += f"<td>{entry['name']}</td></tr><tr><td>{entry['overview']}</td></tr>"
        for key in entry.keys():
            if key in ['title', 'name', 'overview']:
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"