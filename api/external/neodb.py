from api.api import API
import requests

class neoDB(API):

    def __init__(self):
        super().__init__("https://eggplant.place", "neodb")
        self.category_author_map = {
            'book':'author',
            'podcast': 'host',
            'movie': 'director',
            'game':'developer',
            'tv': 'director'
        }

    def searchByTitle(self, title):
        params = { "query": title}
        return requests.get(self.url+"/api/catalog/search", params=params).json()['data']
    
    def getEntryID(self, entry):
        return "/".join(entry['id'].split('/')[-2:])
    
    def getEntryFromURL(self, url):
        '''Get API entry from a URL
        
        Parameter: URL as string
        '''
        params = {'url': url}
        return requests.get(self.url+'/api/catalog/fetch', params=params).json()

    def getByID(self, id):
        return requests.get(self.url+'/api/'+id).json()
    
    def getEntryTitle(self, entry):
        return entry['title']
    
    def getEntryAuthors(self, entry):
        author = entry[self.category_author_map[entry['category']]]
        if type(author) == list:
            if len(author) == 0:
                return "" 
            else:
                return author[0]
        else:
            return author

    def getBlurb(self, entry):
        try:
            return f"{entry['title']}\n\n {entry['category']}\n\n {entry['description']}"
        except KeyError:
            return "This isn't a URL supported by NeoDB!"
        
    def to_html(self, entry):
        res = f'<table> <tr> <td rowspan="2"><img width="175px" src="{entry["cover_image_url"]}"></td> <td>{entry['title']}</td></tr><tr><td>{entry['brief']}</td></tr>'
        for key in entry.keys():
            if key in ['cover_image_url',"title", 'brief']:
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"