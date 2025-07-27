from api.external import mangaupdates, mangadex
from api.external import neodb, ao3, libby, vndb
from api.external import omdb, openlibrary,tmdb, gutendex
from api.external import googlebooks, itchio, stdebooks

### CONSTANTS ###

SEARCH_API = {
    "Manga Updates": mangaupdates.MangaUpdates(),
    "MangaDex": mangadex.MangaDex(),
    "OMDB": omdb.OMDB(),
    "Open Library": openlibrary.OpenLibrary(),
    "Google Books": googlebooks.GoogleBooks(),
    "TMDB-Movie": tmdb.TMDB(),
    "TMDB-TV": tmdb.TMDB(type="tv"),
    "VNDB": vndb.VNDB(),
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

TACHI_API = {'MangaDex': mangadex.MangaDex(), 'Manga Updates':mangaupdates.MangaUpdates()}