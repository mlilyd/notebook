'''
Module for auto-import without any manual input
'''
from api.external import mangaupdates, mangadex
from api.internal import TachiBk
import codecs
import json

internTachiBK = TachiBk()

def fromTachibk(tachbkdf, db):
    '''Auto-import from tachi-based backup files.

    Returns a list of records

    Parameters:
        - tachbkdf: tachi backup as pandas dataframe
        - db: internal tachi database  
    '''    
    API = [mangadex.MangaDex(), mangaupdates.MangaUpdates()]
    notes = []

    for _,tachi_entry in tachbkdf.iterrows():
        
        entry = {}
        entry['title'] = tachi_entry.title
        entry['authors'] = ",". join(set(tachi_entry.author.split(",") + tachi_entry.artist.split(",")))
        entry['progress'] = 0
        entry['type'] = 1
        entry['notes'] = ""

        #create internal copy with new id, append to intern DB
        new_id = db.add_entry(tachi_entry.drop('category').to_frame().T) #take new intern ID
        entry['DB'] = f"tachibk/{new_id}"

        notes.append(entry)
            
    return notes

def fromLibby(libby_file, isComic=False):
    '''Auto-import from libby list json export

    Returns a list of records

    Parameters:
        - libby_file: libby json file
        - isComic: boolean, True if list is populated by graphic novels,
        False otherwise. False, by default.
    ''' 
    
    libby_entries = json.load(codecs.open(libby_file))['titles']
    notes = []
    for libby_entry in libby_entries:
        entry = {}
        entry['title'] = libby_entry['title']['text']
        entry['authors'] = libby_entry['author']
        entry['progress'] = 0
        if libby_entry['cover']['format'] == 'ebook':
            entry['type'] = 1 if isComic else 0
        else:
            entry['type'] = 2

        link = libby_entry['title']['url'].split('/')[-1]
        entry['DB'] = f"libby/{link}"
        
        notes.append(entry)
    
    return notes