'''
Somehow very scuffed, I don't understand the inconsistencies of this API. Ja
'''

from api.api import API
import requests

class OpenLibrary(API):

    def __init__(self):
        super().__init__("https://openlibrary.org/", "openlibrary")

    def searchByTitle(self, title):
        params = {
            'fields': 'key,title,author_name, first_publish_year, first_sentence',
            'title': title
        }

        return requests.get(self.url+"search.json/", params=params).json()['docs']       
    
    def getByID(self, id):
        return requests.get(self.url+"/works/"+id+".json").json()

    def splitID(self, id):
        return id.split("/")[2]

    def getEntryID(self, entry):
        key = entry['key']
        return self.splitID(key)
    
    def getEntryTitle(self, entry):
        return entry['title']

    def getEntryAuthors(self, entry):
        return entry['author_name'][0]

    def getBlurb(self, entry):
        text =  f"{entry['title']} by {entry['author_name'][0]}, first published {entry['first_publish_year']}\n"
        if "first_sentence" in entry.keys():
            text += entry['first_sentence'][0]
        return text
    
    def getEdition(self, entry):
        '''Get edition of an entry'''
        res = requests.get(self.url+f"/works/{self.getEntryID(entry)}/editions.json")
        return res.json()['entries'][0]
    
    def getAuthorName(self, authorID):
        '''Get author's name given an authorID'''
        res = requests.get(f"https://openlibrary.org/authors/{authorID}.json").json()
        if 'personal_name' in res.keys():
            return res['personal_name']
        else: 
            return res['name']

    def to_html(self, entry):
        edition = self.getEdition(entry)
        cover = f"https://covers.openlibrary.org/b/olid/{self.getEntryID(entry)}-L.jpg"
        res = f'<table> <tr> <td><img width="175px" src="{cover}"></td> <td></td></tr> <tr><td>ID: {self.getEntryID(entry)}</td><td></td></tr>'
       
        # show description

        if 'description' in entry.keys():
            description = entry['description']
        elif 'first_sentence' in entry.keys():
            description = entry['first_sentence']['value']
        else:
            description = ""
        
        res += f'<tr><td> Description/First Sentence </td> <td>{description}</td> </tr>'
        
        # show authors

        authors = list(set([self.getAuthorName(self.splitID(author['author']['key'])) for author in entry['authors']]))
            
        res += f'<tr><td> Authors </td> <td>{", ".join(authors)}</td> </tr>'
        # show publishing date/year

        if "first_publish_year" in entry.keys():
            publish_date = entry['first_publish_year']
        elif "publish_date" in edition.keys():
            publish_date = edition['publish_date']
        else:
            publish_date = ""

        res += f'<tr><td> Date/Year</td> <td>{publish_date}</td> </tr>'


        for key in entry.keys():
            if key not in ['title', "key", "cover_i", 'type', 'last_modified', 'created', 'authors', 'description']:
                if type(entry[key]) == list:
                    continue
                    #res += "<td>" + ", ".join(entry[key]) + "</td></tr>"
                else:
                    res += f"<tr><td>{key}</td>"
                    res += f"<td>{entry[key]}</td></tr>"
       

        
        return res + "</table>"