from api.api import API
import requests

class MangaDex(API):

    def __init__(self):
        super().__init__("https://api.mangadex.dev/", 'mangadex')

    def searchByTitle(self, title):
        params = {
            "title": title,
            "limit": 5 
        }

        return requests.get(self.url+"/manga", params=params).json()['data']
    
    def getByID(self, id):
        return requests.get(f"{self.url}/manga/{id}").json()['data']
    
    def getBlurb(self, entry):
        attr = entry['attributes']
        if 'en' in attr['description'].keys():
            descript = attr['description']['en']
        else:
            descript = ""
        return f"{attr['title']}\n{descript}"
    
    def getEntryID(self, entry):
        return entry['id']
    
    def getCoverURL(self, entry):
        '''Get cover URL given an entry.

        Parameter: entry as dictionary.
        '''
        cover_id = [i['id'] for i in entry['relationships'] if i['type'] == "cover_art"][0]
        filename = requests.get(f"{self.url}/cover/{cover_id}").json()['data']['attributes']['fileName']
        return f"https://mangadex.org/covers/{entry['id']}/{filename}"
    
    def getCoverURLbyID(self, id):
        '''Get cover URL given an entry's ID.

        Parameter: entry ID as string
        '''

        entry = self.getByID(id)
        return self.getCoverURL(entry)
    
    def getArtists(self, entry):
        '''Get a list of artists' names given a MangaDex entry.'''
        artists_id = [i['id'] for i in entry['relationships'] if i['type'] == "artist"]
        names = []
        for id in artists_id:
            names.append(requests.get(f"https://api.mangadex.dev/author/{id}").json()['data']['attributes']['name'])
        return names

    def getAuthors(self, entry):
        '''Get a list of authors' names given a MangaDex entry.'''
        artists_id = [i['id'] for i in entry['relationships'] if i['type'] == "author"]
        names = []
        for id in artists_id:
            names.append(requests.get(f"https://api.mangadex.dev/author/{id}").json()['data']['attributes']['name'])
        return names
    
    def getEntryAuthors(self, entry):
        return f"{self.getAuthors(entry)}, {self.getArtists(entry)}"
    
    def getEntryTitle(self, entry):
        return entry['attributes']['title']['en']

    def to_html(self, entry):
        cover_url = self.getCoverURL(entry)
        authors = self.getAuthors(entry)
        artists = self.getArtists(entry)

        attr = entry['attributes']
        links = [ i for i in attr['links'].values() if "http" in i]
        tags = ", ".join([i['attributes']['name']['en'] for i in attr['tags']])
        altTitleStr = "<b>Alternate Titles:</b></br>"
        for altTitle in attr['altTitles']:
            for lang, title in altTitle.items():
                altTitleStr += f"{title} ({lang}) </br> "

        description = attr['description']['en'] if 'en' in attr['description'].keys() else attr['description']

        res = f"""<table>
                <tr> <td><img height=150px src="{cover_url}"></td><td>{altTitleStr}</td> </tr>
                <tr> <td>ID</td> <td>{entry['id']}</td> </tr> 
                <tr> <td>Author(s)</td> <td>{'</br>'.join(authors)}</td></tr>
                <tr> <td>Artist(s)</td> <td>{'</br>'.join(artists)}</td></tr>
                <tr> <td>Original Language</td> <td>{attr['originalLanguage']}</td> </tr> 
                <tr> <td>Year of Publication</td> <td>{attr['year']}</td> </tr>
                <tr> <td>Publication Status</td> <td>{attr['status']}</td> </tr> 
                <tr> <td>Description</td> <td>{description}</td> </tr>
                <tr> <td>Tags</td> <td>{tags}</td></tr>
                <tr> <td>Links</td> <td>{'</br>'.join(links)}</td></tr>
                </table>
                """
        return res