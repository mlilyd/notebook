'''
For reading comic information from tachi backups

!!Can only load one protobuf schema at a time because they're so similar!!

'''
#from schema import mihon_pb2 as mihon
#from schema import sy_pb2 as sy
from schema import komikku_pb2 as komikku
import gzip

def get_info(raw, sources):
    '''Extract information from entries in tachi-based backup file.
    '''
    new_entry = {}
    new_entry['title'] = raw.title
    if hasattr(raw, 'author'):    
        new_entry['author'] = raw.author
    if hasattr(raw, 'artist'):
        new_entry['artist'] = raw.artist
    if hasattr(raw, 'description'):
        new_entry['description'] = raw.description
    if hasattr(raw, 'genre'):
        new_entry['genre'] = " ".join(raw.genre)
    if hasattr(raw, 'notes'):
        new_entry['notes'] = raw.notes
    else:
        new_entry['notes'] = ""
    new_entry['cover'] = raw.thumbnailUrl
    new_entry['url'] = raw.url
    new_entry['source'] = sources[raw.source]
    if len(raw.categories) > 0:
        new_entry['category'] = raw.categories[0]
    else:
        new_entry['category'] = -1
    return new_entry

def from_tachibk(backupFile):
    '''Read tachi-based backup file.
    
    Returns a list of records.

    Parameter: path to tachi backup file.
    '''
    backup = komikku.Backup()
    with gzip.open(backupFile, "rb") as f: #decompress backup
        backup.ParseFromString(f.read())
    
    sources =  {i.sourceId: i.name for i in backup.backupSources}
    
    return [get_info(i, sources) for i in backup.backupManga if len(i.categories) > 0]

def from_tachibk_upload(upload):
    '''Read uploaded tachi-based backup file
    
    Return sa list of records
    
    Parameter: ipywidgets.widgets.FileUpload object'''

    backup = komikku.Backup()
    content = upload.value[0].content
    decomp = gzip.decompress(content)
    backup.ParseFromString(decomp)
    
    sources =  {i.sourceId: i.name for i in backup.backupSources}
    return [get_info(i, sources) for i in backup.backupManga if len(i.categories) > 0]
