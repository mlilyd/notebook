from api.external import mangaupdates, mangadex, anilist
from api.external import neodb, ao3, libby, vndb
from api.external import omdb, openlibrary,tmdb, gutendex
from api.external import googlebooks, itchio, stdebooks
from _secret_.key import key
### CONSTANTS ###




SEARCH_API = {
    "Manga Updates" : mangaupdates.MangaUpdates(),
    "AniList"       : anilist.AniList(),
    "MangaDex"      : mangadex.MangaDex(),
    "OMDB"          : omdb.OMDB(),
    "Open Library"  : openlibrary.OpenLibrary(),
    "Google Books"  : googlebooks.GoogleBooks(),
    "TMDB-Movie"    : tmdb.TMDB(key),
    "TMDB-TV"       : tmdb.TMDB(key, type="tv"),
    "VNDB"          : vndb.VNDB(),
    "Project Gutenberg": gutendex.Gutendex()
    }

URL_API = {
    "neoDB":neodb.neoDB(),
    "AO3": ao3.Ao3(),
    "Libby": libby.Libby(),
    "itch.io": itchio.itchIO(),
    "Standard eBooks": stdebooks.StdEBooks()
}

URL_API_DESCRIPT = {
    "neoDB": "Enter neoDB supported URL (IMDB, Goodreads, IGDB, podcast RSS, Steam)",
    "AO3": "Enter Archive of Our Own URL ...",
    "Libby": "Enter Libby share URL ...",
    "itch.io": "Enter itch.io URL ...",
    "Standard eBooks": "Enter Standard eBooks URL"
}

API_TYPE = {
    "AniList": 1,
    "Manga Updates": 1, "MangaDex": 1,
    "OMDB": 3, "Open Library": 0,
    "Google Books": 0, "neoDB": 0,
    "TMDB-Movie": 3, "TMDB-TV": 3,
    "VNDB": 4, "Project Gutenberg": 0
}

NEODB_TYPE = {
    'book':0, 'podcast': 2,
    'movie': 3, 'game':4, 'tv': 3
}

TACHI_API = {'AniList': anilist.AniList(),'Manga Updates':mangaupdates.MangaUpdates(),
             'MangaDex': mangadex.MangaDex(), }