from api.api import jsonDB
from notes.api_config import progressCategory, mediaCategory, API_LIST

class notesDB(jsonDB):
    
    def __init__(self):
        '''Notes database, contains notes and external ID for entries.'''
        super().__init__('json/notes.json', "notes")

        # add all external connections
        self.API = API_LIST

    
    def get_external_entry(self, note):
        '''Fetch external information. 

        Parameter: note as dictionary/record
        '''
        parts = note['DB'].split("/")
        external_db = parts[0]
        external_db_id = "/".join(parts[1:])

        entry = self.API[external_db].getByID(external_db_id)
        return entry

    def add_note_entries(self, entry):
        '''Add pandas dataframe as rows at the end of the database.
        Duplicates and index automatically removed and reset.

        No returned value.
        
        Parameter: 
            - new_entries: pandas dataframe
        '''
        self.add_entries(entry)
        self.df = self.df.drop_duplicates()
        self.df = self.df.reset_index(drop=True)

    def to_html_internal(self, note):
        external_db = note['DB'].split("/")[0]
        note_str = f"""
                <table class='gridtable'> <tr><th>Type</th><th>Progress</th><th>DB</th></tr>
                <tr>    <td>{mediaCategory(note['type']).name}</td>
                        <td>{progressCategory(note['progress']).name}</td>
                        <td>{external_db.upper()}</td>
                </tr>
                </table>
                """
        
        if 'notes' in note.keys():
            note_str += f"<p align=left>{note['notes']}</p>"

        return note_str

    def to_html_external(self, note):
        external_db = note['DB'].split("/")[0]
        entry = self.get_external_entry(note)
        return self.API[external_db].to_html(entry)
    
    def to_html(self, note):
        note_str = self.to_html_internal(note)
        external_db_str = self.to_html_external(note)

        return f"<h1>{note['title']}</h1><table> <tr> <td valign=top>{note_str} </td> <td> {external_db_str} </td></tr></table>"

        
    
                




     
