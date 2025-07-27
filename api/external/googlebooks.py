from api.api import API
import requests

class GoogleBooks(API):

    def __init__(self):
        super().__init__("https://www.googleapis.com/books/v1/volumes", "googlebooks")

    def searchByTitle(self, title, author="", lang="en"):
        if author == "":
            query = f'intitle:{title}+language:{lang}'
        else:
            query = f'intitle:{title}+inauthor:{author}+language:{lang}'

        params = {"q": query}
        res = requests.get(self.url, params=params).json()
        return res['items'] if 'items' in res.keys() else []
    
    def getByID(self, id):
        return requests.get(f"{self.url}/{id}").json()
    
    def getBlurb(self, entry):
        return entry['volumeInfo']['description'].encode("ascii", 'ignore').decode()

    def getEntryID(self, entry):
        return entry['id']

    def getEntryAuthors(self, entry):
        if 'authors' in entry['volumeInfo']:
            return ", ".join(entry['volumeInfo']['authors'])
        else:
            return ""
    
    def getEntryTitle(self, entry):
        return entry['volumeInfo']['title']
        
    def to_html(self,entry):
        info = {"id" : entry['id']}
        info = info | entry['volumeInfo']
        
        if 'authors' in info.keys():
            info["authors"] = ", ".join(entry['volumeInfo']['authors'])
        if "categories" in info.keys():
            info['categories'] = ", ".join(entry['volumeInfo']['categories'])
        if "description" in info.keys():
            info['description'] = entry['volumeInfo']['description'].encode("ascii", 'ignore').decode(),
            
        title =  entry['volumeInfo']['title']
        info.pop("title", None)
        link = entry['selfLink'],

        if "imageLinks" in info.keys():
            cover = info['imageLinks']['thumbnail']
            info.pop('imageLinks', None)
        else:
            cover = ""

        table = f'<table><tr><td><a href="{link}"><img src="{cover}"></a></td><td>{title}</td></tr>'

        for key in info.keys():
            table += f"<tr><td>{key}</td><td>{info[key]}</td></tr>"
        table += "</table>"

        return table

