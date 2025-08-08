import ui.components as uic
import pandas as pd
import notes.tachbk as tachbk

from IPython.display import display

def entry_display(notes):
    '''Screen switching note entry's external DB.

    Parameter: notesDB object.
    '''

    entry_id = uic.entry_id()
    entry_id.layout = {'width': "90%"}

    api_dropdown = uic.widgets.Dropdown(options = uic.SEARCH_API | uic.URL_API, layout = {'width': '200px'},
                                        style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})

    dropdowns = uic.dropdowns(horizontal=False)
    note_input = uic.notes_input(description="Notes:", width="90%", height="300px")
    currentDB = uic.widgets.HTML(value = "<b>CURRENT DB:</b> ")
    currentDB_output = uic.show_notes_entry(notes.getByID(entry_id.value), notes, 
                                            dropdowns, note_input, currentDB)
    newDB_output = uic.widgets.HTML(layout={'width': '90%', 'height': '350px'})
    entryHeader = uic.widgets.HTML(value=f"<h2>{notes.getByID(entry_id.value)['title']} by {notes.getByID(entry_id.value)['authors']}  </h2>")
    entry_selection = uic.widgets.Select(layout = {'width': '300px', 'height': '150px'},
                                         style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'} )
    url = uic.widgets.Text(placeholder="Enter supported URL (IMDB, Goodreads) ...",
                        layout = {'width':'100%','align': 'right', 'display':'None'})

    ##########################

    def on_id_change(change):
        entry = notes.getByID(entry_id.value)
        oldAPI = notes.API[entry['DB'].split("/")[0]]
        extern = notes.get_external_entry(entry)

        note_input.value = entry['notes']
        entryHeader.value = f"<h2>{entry['title']} by {entry['authors']}</h2>"
        dropdowns.children[0].value = entry['progress']
        dropdowns.children[1].value = entry['type']
        currentDB.value = f"<b>CURRENT DB:</b> {entry['DB'].split("/")[0].upper()}"
        currentDB_output.value= oldAPI.to_html(extern)
        uic.api_search_2(api_dropdown, entry['title'], entry_selection, url, newDB_output)

    def on_notes_change(change):
        notes.df.at[entry_id.value, 'notes'] = note_input.value

    def on_progress_change(change):
        notes.df.at[entry_id.value, 'progress'] = dropdowns.children[0].value

    def on_type_change(change):
        notes.df.at[entry_id.value, 'type'] = dropdowns.children[1].value

    def on_selection_change(change):
        api = api_dropdown.value
        if entry_selection.value != "NO RESULTS FOUND" and api in uic.SEARCH_API.values():
            selection = api.getByID(api.getEntryID(entry_selection.value))
            newDB_output.value = api.to_html(selection)
        else:
            newDB_output.value = "NO RESULTS FOUND"

    def on_url_change(change):
        api = api_dropdown.value
        if api in uic.URL_API.values():
            selection = api.getEntryFromURL(url.value)
            if 'warning' in selection.keys():
                newDB_output.value = selection['warning']
            else:
                newDB_output.value = api.to_html(selection)

    def on_api_change(change):
        entry = notes.getByID(entry_id.value)
        api = uic.api_search_2(api_dropdown, entry['title'], entry_selection, url, newDB_output)
        if entry_selection.value != "NO RESULTS FOUND":
            selection = api.getByID(api.getEntryID(entry_selection.value))
            newDB_output.value = api.to_html(selection)
        else:
            newDB_output.value = "NO RESULTS FOUND"

    url.observe(on_url_change, names='value')
    entry_id.observe(on_id_change, names='value')
    note_input.observe(on_notes_change, names='value')
    dropdowns.children[0].observe(on_progress_change, names='value')
    dropdowns.children[1].observe(on_type_change, names='value')
    entry_selection.observe(on_selection_change, names='value')
    api_dropdown.observe(on_api_change, names='value')

    ##########################
    def process(b):
        new_api = api_dropdown.value
        if new_api in uic.SEARCH_API.values():
            if entry_selection.value != "NO RESULTS FOUND":
                new_id = new_api.getEntryID(entry_selection.value)
                notes.df.at[entry_id.value, 'DB'] = f"{new_api.name}/{new_id}"
        elif new_api in uic.URL_API.values():
            selection = new_api.getEntryFromURL(url.value)
            new_id = new_api.getEntryID(selection)
            notes.df.at[entry_id.value, 'DB'] = f"{new_api.name}/{new_id}"
            
        # refresh note entry output
        entry = notes.getByID(entry_id.value)
        oldAPI = notes.API[entry['DB'].split("/")[0]]
        extern = notes.get_external_entry(entry)
        currentDB.value = f"<b>CURRENT DB:</b> {entry['DB'].split("/")[0].upper()}"
        currentDB_output.value= oldAPI.to_html(extern)
            
    accept_button = uic.general_accept_button(process, "Switch DB")
    accept_button.layout = {'align': 'left'}
    ##########################

    note_output = uic.widgets.VBox([entry_id, dropdowns, note_input, currentDB])
    DB = uic.widgets.Accordion([currentDB_output], titles=("Entry",""), layout={'width':'65%'}, selected_index=0)
    api_menu = uic.widgets.HBox([api_dropdown, accept_button])
    switch = uic.widgets.VBox([api_menu, url, entry_selection, newDB_output, ])
    switchCollapse = uic.widgets.Accordion([switch], titles=('Switch DB',""))
    left = uic.widgets.VBox([note_output, switchCollapse])

    return uic.widgets.HBox([left, DB])

def search_API(globvar):
    '''Screen for going searching through API that allows for searches via keywords/title.

    globvar = {'notes' : [],'title': None}
        - notes: list of records for created entries.
        - title: title placeholder
    '''

    title = uic.widgets.Text(placeholder="Search title...", layout = {'width':'90%','align': 'right'},
                             style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})
    blurb_html = uic.widgets.HTML(layout={'width': '90%', 'height': '350px'})
    status = uic.widgets.Output()
    
    dropdowns = uic.dropdowns()
    notes_input = uic.notes_input()

    entry_selection = uic.widgets.Select(options = [], layout = {'width': '90%', 'height': '20%'},
                                         style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})
    api_toggle = uic.widgets.ToggleButtons(options = uic.SEARCH_API.keys(),
                                           style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})

    #### uic functionalities
    def on_title_change(change):
        globvar['title'] = title.value
        api = uic.SEARCH_API[api_toggle.value]
        response = api.searchByTitle(title.value)
        entry_selection.options = list((response))
    
    title.observe(on_title_change, names='value')

    def on_api_toggle_change(change):
        api = uic.SEARCH_API[api_toggle.value]
        response = api.searchByTitle(title.value)
        entry_selection.options = list((response))
        dropdowns.children[1].value = uic.API_TYPE[api_toggle.value]

    api_toggle.observe(on_api_toggle_change, names='value')

    def on_selection_change(change):
        blurb_html.value = ""
        api = uic.SEARCH_API[api_toggle.value]
        selection_id = api.getEntryID(entry_selection.value)
        selection = api.getByID(selection_id)
        blurb_html.value = api.to_html(selection)

        if api_toggle.value == "neoDB":
            dropdowns.children[1].value = uic.NEODB_TYPE[selection['category']]

    entry_selection.observe(on_selection_change, names='value')

    ### processing entry when accept button is pressed
    def process(b):
        api = uic.SEARCH_API[api_toggle.value]
        selection = entry_selection.value

        entry = {}
        entry['title'] = api.getEntryTitle(selection)
        entry['authors'] = api.getEntryAuthors(selection)
        entry['type'] = dropdowns.children[1].value
        entry['DB'] = f"{api.name}/{api.getEntryID(selection)}"
        entry['progress'] = dropdowns.children[0].value
        entry['notes'] = notes_input.value

        globvar['notes'].append(entry)

        with status: 
            uic.rprint(f"New note for [bold]{entry['title']}[/bold] has been created!")
    
    accept_button = uic.general_accept_button(process)
    
    ### layout ###
    api_box = uic.widgets.VBox([api_toggle, entry_selection, blurb_html], layout = {'width': '100%'})
    note_box = uic.widgets.VBox([notes_input, accept_button, status], layout = {'width': '100%'})
    return uic.widgets.VBox([title, api_box, dropdowns, note_box])

def add_tachi(globvar, tachiDB):

    '''Screen for going through tachi entries and searching them up on mangaupdates and mangadex

    tachidf - pandas dataframe of tachi entries
    internTachiBK - internal db of tachi entries

    globvar = {'notes' : []}
        - notes: list of records for created entries.

    '''

    fileUpload = uic.widgets.FileUpload(accept='.tachibk')
    category = uic.widgets.Dropdown(description='Category', options=[None], value=None)
    progress = uic.progress_input()
    indexSelector = uic.widgets.IntRangeSlider(
        min=0,max=0, step=1, description='Index', orientation='horizontal', readoutNone=True)
    entry_list = uic.widgets.Select(layout={'width':'10%','height':'500px'})
    notes_input = uic.notes_input(width='85%')
    blurb_html = uic.widgets.HTML(layout={'width': '90%', 'height': '350px'})
    title_html = uic.widgets.HTML(value="<b>Searching for ...</b>")
    status = uic.widgets.Output()
    api_toggle = uic.widgets.ToggleButtons(options = uic.TACHI_API.keys())

    entry_selection = uic.widgets.Select(options=['None'],value='None',
        layout={'width': '85%', 'height': '100px'})

    ##########################
    def on_file_upload(change):
        from_backup = tachbk.from_tachibk_upload(fileUpload)
        df = pd.DataFrame(from_backup)
        entry_list.options = dict(zip(list(df['title']), from_backup))
        category.options = list(set(df['category']))
        category.value = 0

    def on_category_change(change):
        from_backup = tachbk.from_tachibk_upload(fileUpload)
        df = pd.DataFrame(from_backup)
        df = df.loc[df['category']== category.value]
        selEntries = list(df.to_dict(orient='index').values())
        entry_list.options = dict(zip(list(df['title']), selEntries))
        indexSelector.max = df.shape[0]
        indexSelector.value = [0, df.shape[0]]

    def on_range_change(change):
        from_backup = tachbk.from_tachibk_upload(fileUpload)
        df = pd.DataFrame(from_backup)
        df = df.loc[df['category']== category.value][indexSelector.value[0]:indexSelector.value[1]]
        selEntries = list(df.to_dict(orient='index').values())
        entry_list.options = dict(zip(list(df['title']), selEntries))
 
    def on_list_change(change):
        title = entry_list.value['title']
        blurb_html.value = ""
        title_html.value = f"<b>Searching for {title}</b>"
        api = uic.TACHI_API[api_toggle.value]
        response = api.searchByTitle(title)
        entry_selection.options = ['Use tachi entry'] + list((response))
        notes_input.value = entry_list.value['notes']
        
    def on_api_toggle_change(change):
        api = uic.TACHI_API[api_toggle.value]
        response = api.searchByTitle(entry_list.value['title'])
        entry_selection.options = ['Use tachi entry'] + list((response))

    def on_selection_change(change):
        selection = entry_selection.value
        if selection != 'Use tachi entry':
            api = uic.TACHI_API[api_toggle.value]
            selection_id = api.getEntryID(entry_selection.value)
            selection = api.getByID(selection_id)
            blurb_html.value = api.to_html(selection)
        else:
            blurb_html.value = tachiDB.to_html(entry_list.value)

    def process(b):
        tachi_entry = entry_list.value
        api = uic.TACHI_API[api_toggle.value]
        entry = {}
        entry['title'] = tachi_entry["title"]
        entry['authors'] = ",". join(set(tachi_entry["author"].split(",") + tachi_entry['artist'].split(",")))
        entry['progress'] = progress.value
        entry['type'] = 1
        entry['notes'] = notes_input.value

        selection = entry_selection.value
        if selection != 'Use tachi entry':
            ext_id = api.getEntryID(selection)
            entry['DB'] = f"{api.name}/{ext_id}"
        
        else:
            df = pd.DataFrame(tachi_entry, index=range(1)).drop(['category'], axis=1)
            new_id = tachiDB.add_entry(df) #take new intern ID
            entry['DB'] = f"tachibk/{new_id}"
        
        globvar['notes'].append(entry)

        with status:
            uic.rprint(f"New note for {entry['title']} has been created!")

    entry_list.observe(on_list_change, names='value')
    fileUpload.observe(on_file_upload, names='value')
    category.observe(on_category_change, names='value')
    indexSelector.observe(on_range_change, names='value')
    api_toggle.observe(on_api_toggle_change, names='value')
    entry_selection.observe(on_selection_change, names='value')
 
    accept_button = uic.general_accept_button(process)
    file_handling =  uic.widgets.HBox([fileUpload, category, indexSelector])
    api_selection = uic.widgets.VBox([title_html, api_toggle, entry_selection, blurb_html], layout={'width':'80%'})
    middle = uic.widgets.HBox([entry_list, api_selection])
    input_buttons = uic.widgets.VBox([progress,accept_button])
    notes_handling = uic.widgets.HBox([notes_input, input_buttons])

    return uic.widgets.VBox([file_handling, middle, notes_handling, status])
    
def add_libby(globvar):
    '''Screen for going through Libby json export entries

    libby_file: path to wear libby export is
    isComic: boolean, True if list is populated by graphic novels,
        False otherwise. False, by default.
    globvar = {'notes' : []}
        - notes: list of records for created entries.
    '''

    fileUpload = uic.widgets.FileUpload(accept=".json", multiple=False, tooltip="Upload Libby JSON export.",layout={'width':'150px'})
    isComic = uic.widgets.Checkbox(value=False, description="Entry is a graphic novel", indent=False)
    notes_input = uic.notes_input(width='150px', height='500px')
    libby_entries = uic.widgets.Select(layout = {'height': '500px', 'width': '150px'}, enable=False)
    status = uic.widgets.Output()
    entry_html = uic.widgets.HTML(layout={'height': '30%', 'width': '400px'})

    def on_file_upload(change):
        contents = uic.codecs.decode(fileUpload.value[0]['content'])
        libby_entries.options = uic.json.loads(contents)['titles']
        libby_entries.enable=True

    def on_selection_change(change):
        entry = libby_entries.value
        entry_html.value = f"<table><tr><td rowspan='2'><img height=250px src='{entry['cover']['url']}'></th><th>{entry['title']['text']}</th></tr>><tr><td>by {entry['author']}</td></tr></table>"
    
    def process(b):
        libby_entry = libby_entries.value
        entry = {}
        entry['title'] = libby_entry['title']['text']
        entry['authors'] = libby_entry['author']
        entry['progress'] = 0
        if libby_entry['cover']['format'] == 'ebook':
            entry['type'] = 1 if isComic.value else 0
        else:
            entry['type'] = 2

        link = libby_entry['title']['url'].split('/')[-1]
        entry['DB'] = f"libby/{link}"
        entry['notes'] = notes_input.value
        
        globvar['notes'].append(entry)

        with status:
            uic.rprint(f"New note for {entry['title']} has been created!")

    fileUpload.observe(on_file_upload, names='value')
    libby_entries.observe(on_selection_change, names='value') 
    load_libby = uic.widgets.VBox([fileUpload,libby_entries], layout={'width':'25%'})      
    notes_handling = uic.widgets.VBox([isComic, notes_input], layout={'width':'25%'}) 
    accept_button = uic.general_accept_button(process)

    entry_handling = uic.widgets.HBox([load_libby, entry_html, notes_handling])
    return uic.widgets.VBox([entry_handling,accept_button, status])

def add_from_url(globvar):
    ''' Screen for adding entries from external entries via URL. Currently supports:
        - Goodreads, IMDB, IGDB, Steam, podcast RSS (via NeoDB)
        - Archive of Our Own
        - Libby share URL
        
    globvar = {"notes": []}
        - notes: list to be filled with created note entries
    '''
    notes_input = uic.notes_input()
    dropdowns = uic.dropdowns()
    api_toggle = uic.widgets.ToggleButtons(options = uic.URL_API.keys())
    blurb_html = uic.widgets.HTML(layout={'width': '90%'})
    status = uic.widgets.Output()
    url = uic.widgets.Text(placeholder="Enter supported URL (IMDB, Goodreads) ...",
                        layout = {'width':'90%','align': 'right'},
                        style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})

    #########################
    def on_api_change(change):
        url.placeholder = uic.URL_API_DESCRIPT[api_toggle.value]
        if str(url.value) != "" or url.value is not None:
            api = uic.URL_API[api_toggle.value]
            selection = api.getEntryFromURL(url.value)
            if "warning" not in selection.keys():
                blurb_html.value = api.to_html(selection)
            else:
                blurb_html.value = selection['warning']

    api_toggle.observe(on_api_change, names='value')

    def on_url_change(change):
        api = uic.URL_API[api_toggle.value]
        selection = api.getEntryFromURL(url.value)
        if "warning" not in selection.keys():
                blurb_html.value = api.to_html(selection)
        else:
            blurb_html.value = selection['warning']

    url.observe(on_url_change, names='value')
    ###############################
    def process(b):
        api = uic.URL_API[api_toggle.value]
        selection = api.getEntryFromURL(url.value)

        entry = {}
        entry['title'] = api.getEntryTitle(selection)
        entry['authors'] = api.getEntryAuthors(selection)
        entry['type'] = dropdowns.children[1].value
        entry['DB'] = f"{api.name}/{api.getEntryID(selection)}"
        entry['progress'] = dropdowns.children[0].value
        entry['notes'] = notes_input.value
        globvar['notes'].append(entry)

        with status:
            uic.rprint(f"New note for {entry['title']} has been created!")

    accept_button = uic.general_accept_button(process)
    note_box = uic.widgets.VBox([notes_input, accept_button, status], layout = {'width': '100%'})
    return uic.widgets.VBox([api_toggle, url, blurb_html, dropdowns, note_box])

def add_manual(globvar):
    ''' Screen for adding manual entries

    globvar = {"notes": [], "entries": [], "lastID": 0}:
        - notes: list to be filled with created note entries
        - entries: lis tto be filled with details of entries
        - lastID: last ID in internal DB
    '''

    notes_input = uic.notes_input()
    dropdowns = uic.dropdowns()

    title = uic.widgets.Text(placeholder="Title...", layout = {'width':'90%'}, style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})
    authors = uic.widgets.Text(placeholder = "Authors...", layout = {'width':'90%'}, style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})
    url = uic.widgets.Text(placeholder = "URL to media", layout = {'width':'45%'}, style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})
    img_url = uic.widgets.Text(placeholder = "URL to image cover/banner", layout = {'width':'45%'}, style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})
    descript_input = uic.widgets.Textarea(placeholder='Description...', layout={'width': '90%', 'height':'150px'},
                                          style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})
    
    date_published = uic.widgets.DatePicker(description='Published', layout={'width':'45%'})
    language = uic.widgets.Text(placeholder="Language...", layout={'width':'45%'}, style = {'background':'transparent', 'text_color': 'var(--vscode-editor-foreground)'})
    
    status = uic.widgets.Output()

    ##########################
    def process(b):

        # set note fields
        entry_notes = {}
        entry_notes['DB'] = f"internal/{globvar['lastID']}"
        entry_notes['title'] = title.value
        entry_notes['authors'] = authors.value
        entry_notes['type'] = dropdowns.children[1].value
        entry_notes['progress'] = dropdowns.children[0].value
        entry_notes['notes'] = notes_input.value

        # set entry fields
        entry = {}
        entry['title'] = title.value
        entry['authors'] = authors.value
        entry['url'] = url.value
        entry['published'] = date_published.value.strftime("%Y-%m-%d")
        entry['language'] = language.value
        entry['image'] = img_url.value
        entry['description'] = descript_input.value

        globvar['notes'].append(entry_notes)
        globvar['entries'].append(entry)
        globvar['lastID'] += 1

        with status:
            uic.rprint(f"New note for {entry_notes['title']} has been created!")
    
    ########################## 

    accept_button = uic.general_accept_button(process)
    links = uic.widgets.HBox([url, img_url])
    lang_date = uic.widgets.HBox([date_published, language])
    return uic.widgets.VBox([title, authors, links, lang_date, dropdowns, descript_input, notes_input, accept_button, status])

def review_new_notes(search, manual, from_url, from_libby, from_tachi, notes, interndb):
    '''Screen for reviewing and adding new notes

    Parameters:
        - search = {'notes': [], 'title': None}
        - manual = {'notes': [], 'entries': [], 'lastID': 0}
        - from_url =   {'notes': []}
        - from_tachi = {'notes': []}
        - from_libby = {'notes': []}
        - notes
        - interndb
    '''
    
    dropdown = uic.widgets.Dropdown(layout={'width': '90%'}, options={'Notes':{
    "From URL":from_url['notes'], "From Libby": from_libby['notes'], "From Tachi": from_tachi['notes'],
    "From Searches": search['notes'], "Manual Notes": manual['notes']}, 'Entries': {"Manual Entries": manual['entries']}})

    note_list = uic.widgets.SelectMultiple(layout={'width':'90%','height':'500px'}, options=dropdown.value)
    preview = uic.widgets.Output(layout={'width':'85%', 'height': '10px'}, style={'border':'2px solid gray'})

    def on_dropdown_change(change):
        note_list.options = dropdown.value

    def on_selection_change(change):
        preview.clear_output()
        selected = []
        for i in note_list.value:
            selected+=i
        with preview:
            display(pd.DataFrame(selected))

    dropdown.observe(on_dropdown_change, names='value')
    note_list.observe(on_selection_change, names='value')
    def process(b):
        selected = []
        for i in note_list.value:
            selected+=i
        dropdown_keys = list(dropdown.options.keys())
        dropdown_val = list(dropdown.options.values())
        
        if dropdown_keys[dropdown_val.index(note_list.options)] == "Notes":
            notes.add_note_entries(pd.DataFrame(selected))
        else:
            interndb.add_intern_entries(pd.DataFrame(selected))
 
    confirm_button = uic.general_accept_button(process, text="Save Entries to DB")
    sel_list = uic.widgets.VBox([dropdown, note_list], layout={'width':'15%'})
    main = uic.widgets.HBox([sel_list, preview])
    return uic.widgets.VBox([main, confirm_button])

def add_entries(search, manual, from_url, from_libby, from_tachi, tachidb, notes, interndb):
    ''' Screen for adding entries

    Parameters:
        - search = {'notes': [], 'title': None}
        - manual = {'notes': [], 'entries': [], 'lastID': 0}
        - from_url =   {'notes': []}
        - from_tachi = {'notes': []}
        - from_libby = {'notes': []}
        - tachidb
        - notes
        - interndb
    '''

    pages = [search_API(search), add_from_url(from_url), add_libby(from_libby), 
             add_tachi(from_tachi, tachidb),add_manual(manual), 
           review_new_notes(search, manual, from_url, 
                            from_libby, from_tachi, notes, interndb)]

    tab_titles = ["Search API", "Add From URL", "Add From Libby", 
                  "Add From Tachi", "Manual Entry", "Review"]
    return uic.widgets.Tab(children = pages, titles = tab_titles,
                           layout={'height': '500px'})