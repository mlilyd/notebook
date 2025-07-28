'''UI Components '''
import ipywidgets as widgets 
from ui.actions import *


### Input Fields ###
def notes_input(description="", width="90%", height='100px'):
    return widgets.Textarea(
        value='',
        placeholder='Enter new notes',
        description=description,
        layout={'width': width, 'height':height},
        style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'}
    )

class notesInput(widgets.Textarea):
    def __init__(self, descript="", width="90%", height='100px'):
        super().__init__(
        value='',
        placeholder='Enter new notes',
        description=descript,
        layout={'width': width, 'height':height},
        style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'}            
        )

def entry_id():
    return widgets.IntText(
        value=0,
        description='ID:',
        disabled=False,
        layout = {'width': '20%'},
        style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'}
    )

### Dropdown Menu ###

def progress_input(width='90%'):
    return widgets.Dropdown(
    options = [('Completed', 0), ('On-going', 1),
                ('Wishlist', 2), ('Dropped', 3)],
    description = 'Progress: ',
    layout = {'width': width},
    style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'}
)

def type_input(width='90%'):
    return widgets.Dropdown(
    options = [('Novel, Article, Fanfic', 0),
                ('Comic, Manga, Webtoon', 1),
                ('Audiobook, Podcast', 2),
                ('Movies, Series, Anime, Video', 3),
                ('Video games, Multimedia', 4)],
    description = 'Type: ',
    layout = {'width': width},
    style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'}
)

def dropdowns(horizontal=True):
    if horizontal:
        return widgets.HBox([progress_input('35%'), type_input('35%')])
    else: 
        return widgets.VBox([progress_input(), type_input()])
    
### HTML Outputs ###

def show_notes_entry(entry, notes, dropdowns, notes_input, currentDB):
    api = notes.API[entry['DB'].split("/")[0]]
    extern = notes.get_external_entry(entry)
    
    notes_input.value = entry['notes']
    dropdowns.children[0].value = entry['progress']
    dropdowns.children[1].value = entry['type']
    currentDB.value = f"CURRENT DB: {entry['DB'].split("/")[0].upper()}"

    extern_output = widgets.HTML(value= api.to_html(extern))
    return extern_output

#### Button ###
def general_save_button(notes):
    button = widgets.Button(
        icon = "check",
        tooltip = "Save notes",
        layout = {'width': '40px', 'height': '150px'},
        style = {'button_color':'lightgreen'}
    )

    def save(b):
        notes.save()
        print("Notes saved!")

    button.on_click(save)
    return button

def general_accept_button(process_function, text="Create New Note", width="90%"):
    accept_button = widgets.Button(
        description = text,
        tooltip = text,
        layout = {'width':width,'align': 'right'},
        style = {'button_color': 'lightblue'}
    )
    accept_button.on_click(process_function)
    return accept_button


class SaveButton(widgets.Button):

    def __init__(self, notes, interndb, tachidb, **kwargs):
        super().__init__(**kwargs)
        self.notes = notes
        self.interndb = interndb
        self.tachidb = tachidb

    def __on_click(self, b):
        self.notes.save()
        self.interndb.save()
        self.tachidb.save()

