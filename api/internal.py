from api.api import jsonDB
from codecs import open
import pandas as pd


class oldDB(jsonDB):

    def __init__(self):
        '''Database for old entries from when I was using some other app to keep track of things I've read.'''
        super().__init__("json/old.json", "old")

    def getBlurb(self, entry):
        '''Get blurb from old entries'''
        return super().getBlurb(entry, "description")
       
    def to_html(self, entry):
        res = "<table>"
        res += f'<tr> <td><img height=150px src="{entry['cover']}"></td><td>{entry['title']}</td> </tr>'
        for key in entry.keys():
            if key in ['cover', 'title']:
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"


class TachiBk(jsonDB):
    
    def __init__(self):
        '''Database for entries from tachi-based backups.'''
        super().__init__("json/tachibk.json", "tachibk")

    def getBlurb(self, entry):
        '''Get blurb from tachi-based entries'''
        return super().getBlurb(entry, "description")

    def to_html(self, entry):
        res = "<table>"
        res += f'<tr> <td><img height=150px src="{entry['cover']}"></td><td>{entry['title']}</td> </tr>'
        for key in entry.keys():
            if key in ['cover', 'title']:
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"
    
    def add_entry(self, entry):
        '''Add pandas dataframe as rows at the end of the database.
        Duplicates and index automatically removed and reset.

        Returns the last index.
        
        Parameter: 
            - new_entries: pandas dataframe
        '''
        self.add_entries(entry)
        return self.df.shape[0]-1

class internDB(jsonDB):

    def __init__(self):
        '''Database for manual entries'''
        super().__init__("json/internal.json", "internal")
        
    def getBlurb(self, entry):
        '''Get blurb from old entries'''
        return super().getBlurb(entry, "description")
    
    def to_html(self, entry):
        res = "<table>"
        res += f'<tr> <td><img height=150px src="{entry['image']}"></td><td>{entry['title']}</td> </tr>'
        for key in entry.keys():
            if key in ['image', 'title']:
                continue
            res += f"<tr><td>{key}</td><td>{entry[key]}</td></tr>"
        
        return res + "</table>"
    
    def getLastID(self):
        '''Return the last ID in manualDB'''
        return self.df.shape[0]-1
    
    def add_intern_entries(self, entry):
        '''Add pandas dataframe as rows at the end of the database.
        Duplicates and index automatically removed and reset.

        Returns the last index.
        
        Parameter: 
            - new_entries: pandas dataframe
        '''
        self.add_entries(entry)
        return self.df.shape[0]-1
    
