from notes.api_config import progressCategory, mediaCategory
from ui.constants import *
import tarfile

### UI Functionalities ###

def notes_to_html(entry):
    return f"""<table>
        <tr><th colspan='2' style='align:left'> CURRENT DB: {entry['DB'].split('/')[0].upper()}</th></tr>
        <tr><td rowspan='4'>{entry['notes']}</td><td>PROGRESS</td></tr>
        <tr><td>{progressCategory(entry['progress'])}</td></tr>
        <tr><td>TYPE</td></tr>
        <tr><td>{mediaCategory(entry['type'])}</td></tr>
        </table>
    """ 

def api_search(api_selection, title, entry_selection):
    api = api_selection.value
    search = api.searchByTitle(title)
    if len(search) > 0:
        entry_selection.options = search
        entry_selection.value = search[0]
    else:
        entry_selection.options = ['NO RESULTS FOUND']
        entry_selection.value = 'NO RESULTS FOUND'
    
    return api

def api_search_2(api_selection, title, entry_selection, url, output):
    api = api_selection.value
    output.value = ""
    if api in SEARCH_API.values():
        search = api.searchByTitle(title)
        entry_selection.layout.display='block'
        url.layout.display='none'
        if len(search) > 0:
            entry_selection.options = search
            entry_selection.value = search[0]
        else:
            entry_selection.options = ['NO RESULTS FOUND']
            entry_selection.value = 'NO RESULTS FOUND'
    
    elif api in URL_API.values():
        url.layout.display='block'
        entry_selection.layout.display='none'

    
    return api

def save_to_compressed(filename="backup.notes"):
    tar = tarfile.open(filename, "w:gz")
    tar.add("json", arcname="json")
    tar.close()

def load_from_compressed(filename="backup.notes"):
    tar = tarfile.open(filename, "r:gz")
    tar.extractall()
    tar.close()
