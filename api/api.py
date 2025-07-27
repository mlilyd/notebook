from rich import print as rprint
from IPython.display import HTML
from abc import ABC, abstractmethod
import pandas as pd
import codecs

class API(ABC):
    ''' Abstract interface class to connect various database to notes
    '''

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def name(self):
        return self.name

    @abstractmethod
    def searchByTitle(self,title):
        ''' Search API by an media title.
        
        Returns a list of records from the query.

        Parameter: title as string.
        '''
        pass

    @abstractmethod
    def getByID(self,id):
        ''' Get API entry by its ID.
        
        Returns a record/dictionary of API entry.

        Parameter: API ID
        '''
        pass
    
    @abstractmethod
    def getBlurb(self, entry):
        ''' Get a short summary/info/overview of an entry. To be used during searches.
        
        Returns a string

        Parameter: entry as record/dictionary.
        '''
        pass
    
    @abstractmethod
    def getEntryID(self, entry):
        ''' Get ID of an entry.
        
        Returns ID

        Parameter: entry as record/dictionary.
        '''
        pass

    @abstractmethod
    def getEntryTitle(self, entry):
        ''' Get title of an entry.
        
        Returns title

        Parameter: entry as record/dictionary.
        '''
        pass

    @abstractmethod
    def getEntryAuthors(self, entry):
        ''' Get authors of an entry.
        
        Returns authors

        Parameter: entry as record/dictionary.
        '''
        pass

    @abstractmethod
    def to_html(self, entry):
        ''' Create HTML table of entry.
        
        Returns a string

        Parameter: entry as record/dictionary.
        '''
        pass

class jsonDB(API): 

    def __init__(self, jsonFile, name): 
        ''' abstract class for internal json databases
            
            Parameter:
                jsonFile: path to json file (string)
                name: name of database (string)
        '''
        super().__init__(jsonFile, name)
        self.df = pd.read_json(codecs.open(self.url, 'r', 'utf-8'), orient='index')
    

    def getBlurb(self, entry, columnName):
        '''Get a summary from an entry by fetching a specific column name.
            Column name to be defined in subclass
        '''
        return entry['columnName']
    
    def getEntryID(self, entry):
        return entry['id']

    def getEntryAuthors(self, entry):
        return f"{entry['author']}, {entry['artist']}"
    
    def getEntryTitle(self, entry):
        return entry['title']

    def getByID(self, id):
        id = int(id)
        entry = self.df.loc[[id]].to_dict(orient='index')[id]
        entry['id'] = id
        return entry

    def searchByTitle(self, title):
        search = self.df.loc[self.df['title'].str.contains(title)]
        search = search.to_dict(orient='index')
        res = []
        for key in search.keys():
            rec =  search[key]
            rec['id'] = key
            res.append(rec)
        return res
    
    def searchByColumn(self, column, query):
        ''' Search database by column
            
        Returns a list of records that matches the keyword query.
        
        Parameter:
            column - string, column to filter by
            query - string to query by.
        '''
        search = self.df.loc[self.df[column].str.contains(query)]
        search = search.to_dict(orient='index')
        res = []
        for key in search.keys():
            rec =  search[key]
            rec['id'] = key
            res.append(rec)
        return res
    
    def save(self):
        '''Save database changes to JSON file.
        
        No parameters, no values returned.
        '''
        self.df.to_json(codecs.open(self.url, 'w', 'utf-8'), orient='index')

    def add_entries(self,new_entries):
        '''Add pandas dataframe as rows at the end of the database.
        
        No returned value.
        
        Parameter: 
            - new_entries: pandas dataframe
        '''
        self.df = pd.concat([self.df, new_entries], ignore_index=True)
    

class Scrapper(API):
    '''Abstract API class for external databases with no open API (web-scrapping)
    '''

    def __init__(self, url, name):
        super().__init__(url, name)
    
    def searchByTitle(self, title):
        print("This API doesn't support search")
        return []
    
    @abstractmethod
    def get_id_from_url(self,url):
        '''Convert URL to ID'''
        pass   

    @abstractmethod 
    def get_url_from_id(self,id):
        '''Convert ID to  URL'''
        pass

    @abstractmethod
    def extract_from_page(self, url):
        '''Extract information from page with beautiful soup
        
        Parameter: API supported URL'''
        pass

    def getEntryFromURL(self, url):
        if self.url not in url:
            return {"warning":f"This isn't a {self.name} URL."}
        return self.extract_from_page(url)

    def getByID(self, id):
        url = self.get_url_from_id(id)
        return self.extract_from_page(url)
    
####### API Tests #######


def check_API(api):

    entry_by_title = api.searchByTitle("fish")[0]
    id = api.getEntryID(entry_by_title)
    entry_by_id = api.getByID(id)

    if api.getEntryID(entry_by_title) == api.getEntryID(entry_by_id):
        rprint("[green]Search and fetching by ID working![/green]")
    else:
        rprint("[red]Search and fetching by ID not working![/red]")

    rprint (f"[bold]Title[/bold]: {api.getEntryTitle(entry_by_title)} [bold]Author[/bold]: {api.getEntryAuthors(entry_by_title)}\n[bold]Blurb[/bold]:\n{api.getBlurb(entry_by_title)}\n")
    
    return HTML(api.to_html(entry_by_id))

def check_Scrapper(api, url):
    if api.get_url_from_id(api.get_id_from_url(url)) == url:
        rprint("[green]ID and URL conversions working![/green]")
    else:
        rprint("[red]ID and URL conversions not working![/red]")

    entry = api.getEntryFromURL(url)

    rprint (f"[bold]Title[/bold]: {api.getEntryTitle(entry)} [bold]Author[/bold]: {api.getEntryAuthors(entry)}\n[bold]Blurb[/bold]:\n{api.getBlurb(entry)}\n")
    
    return HTML(api.to_html(api.getEntryFromURL(url)))
