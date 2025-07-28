from api.api import API
import requests

class AniList(API):

    def __init__(self, url="https://graphql.anilist.co", name="anilist"):
        super().__init__(url, name)
        self.fields = '''
        {
            id
            title {
            romaji
            english
            native
            }
            staff {
                nodes {
                name {
                    full
                }
                primaryOccupations
                }
            }
            startDate {
            day
            month
            year
            }
            endDate {
            day
            month
            year
            }
            description
            countryOfOrigin
            isAdult
            status
            chapters
            volumes
            genres
            tags {
            name
            }
            source
            averageScore
            popularity
            meanScore
            externalLinks {
            url
                }
                coverImage {
                    medium
                }
                }
            }
            }
        '''
        self.variables = {'page':1, 'perPage':5}
        self.exclude_profes = ['Letterer', 'Translator', '']

    def searchByTitle(self, title):
        query = '''query ($page: Int, $perPage: Int, $search: String){
        Page (page: $page, perPage: $perPage) {
            pageInfo {
            currentPage
            hasNextPage
            perPage
            }
            media (search: $search, type: MANGA)'''+self.fields
        variables = {"search": title} | self.variables
        response = requests.post(self.url, json={'query':query, 'variables':variables}).json()
        return response['data']['Page']['media']
    
    def getByID(self, id):
        query = '''query ($id: Int, $page: Int, $perPage: Int){
        Page (page: $page, perPage: $perPage) {
            pageInfo {
            currentPage
            hasNextPage
            perPage
            }
            media (id: $id, type: MANGA)'''+self.fields
        variables = {"id": id} | self.variables
        response = requests.post(self.url, json={'query':query, 'variables':variables}).json()
        return response['data']['Page']['media'][0]
    
    def getBlurb(self, entry):
        return f"{entry['title']['english']} by {self.getEntryAuthors(entry)}\n\n{entry['description']}"
    
    def check_profes(self,node_staff):
        
        if len(node_staff['primaryOccupations']) == 0:
            return False
        for profes in node_staff['primaryOccupations']:
            if profes in self.exclude_profes:
                return False
        return True

    def getEntryAuthorsList(self, entry):
        return[(i['name']['full'],i['primaryOccupations']) for i in entry['staff']['nodes'] if self.check_profes(i)]
    
    def getEntryAuthors(self, entry):
        list = self.getEntryAuthorsList(entry)
        return ", ".join([i[0] for i in list])
    
    def getEntryID(self, entry):
        return entry['id']
    
    def getEntryTitle(self, entry):
        return entry['title']['english']
    
    def to_html(self, entry):
        res = f"<table><tr><td rowspan='2'><img height=150px src='{entry['coverImage']['medium']}'></td> <td>{entry['title']}</td></tr><tr><td>{entry['description']}</td></tr>"
        for key in entry.keys():
            if key in ['title', 'coverImage', 'description']:
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"
    