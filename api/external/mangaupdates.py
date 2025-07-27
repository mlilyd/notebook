from api.api import API
import requests

class MangaUpdates(API):

    def __init__(self):
        super().__init__("https://api.mangaupdates.com/v1/series", "mangaupdates")

    def searchByTitle(self, title):
        search = requests.post(f'{self.url}/search', data={'search': title}).json()['results'][:5]
        return [entry['record'] for entry in search]
        
    def getByID(self, id):
        return requests.get(f"{self.url}/{id}").json()
    
    def getBlurb(self, entry):
        return f"{entry['title']}\n{entry['description']}"
    
    def getEntryID(self, entry):
        return entry['series_id']
    
    def getEntryAuthors(self, entry):
        temp = self.getByID(self.getEntryID(entry))
        authors = ", ".join(i['name'] for i in temp['authors'] if i['type']=="Author")
        artists = ", ".join(i['name'] for i in temp['authors'] if i['type']=="Artist")
        return f"{authors}, {artists}"
    
    def getEntryTitle(self, entry):
        return entry['title']
    
    def to_html(self, entry):
        altTitleStr = "</br>".join(i['title'] for i in entry['associated'])
        genre = ", ".join(i['genre'] for i in entry['genres'])
        category = ", ".join(i['category'] for i in entry['categories'])
        authors = ", ".join(i['name'] for i in entry['authors'] if i['type']=="Author")
        artists = ", ".join(i['name'] for i in entry['authors'] if i['type']=="Artist")
        publishers = "</br> ".join(i['publisher_name'] for i in entry['publishers'])
        related_series = ""
        for i in entry['related_series']:
            related_series += f"<tr><td>{i['relation_type']}</td><td>{i['related_series_name']}</td></tr>"

        return f'''<table>
                <tr> <td><img width=250px src="{entry['image']['url']['original']}"></td><td>{entry["description"]}</td> </tr>
                <tr> <td>ID: {entry['series_id']}</td> <td>Alternate Titles: {altTitleStr}</td> </tr> 
                
                <tr> <td>Author(s)</td> <td>{authors}</td></tr>
                <tr> <td>Artist(s)</td> <td>{artists}</td></tr>

                <tr> <td>Genre</td> <td>{genre}</td></tr>
                <tr> <td>Categories</td> <td>{category}</td></tr>
                <tr> <td>Type</td> <td>{entry['type']}</td> </tr> 
                <tr> <td>Year of Publication</td> <td>{entry['year']}</td> </tr>
                <tr> <td>Publication Status</td> <td>{entry['status']}, {entry['latest_chapter']} is the last chapter</td> </tr>
                <tr> <td>Licensed in English</td> <td>{entry['licensed']}</td> </tr>
                <tr> <td>Publisher(s)</td> <td>{publishers}</td></tr>
                <tr> <td><td><b>Related Series</b></td></tr>
                {related_series}
                </table>'''