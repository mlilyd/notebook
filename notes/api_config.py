from enum import IntEnum
from _secret_.key import key
from api.internal import oldDB,TachiBk, internDB
from api.external import mangaupdates, mangadex
from api.external import libby, tmdb, ao3, vndb, anilist
from api.external import omdb, neodb, itchio, vndb, gutendex
from api.external import openlibrary, googlebooks, stdebooks

class progressCategory(IntEnum):
    COMPLETED = 0
    ONGOING = 1
    WISHLIST = 2
    DROPPED = 3

class mediaCategory(IntEnum):
    TEXT = 0
    VISUAL = 1
    AUDIO = 2
    VIDEO = 3
    MULTI = 4

API_LIST = {
             "old": oldDB(),
             "tachibk": TachiBk(),
             "internal": internDB(),
             "mangaupdates": mangaupdates.MangaUpdates(),
             "mangadex": mangadex.MangaDex(),
             "anilist": anilist.AniList(),
             "libby": libby.Libby(),
             "omdb": omdb.OMDB(),
             "openlibrary": openlibrary.OpenLibrary(),
             "googlebooks": googlebooks.GoogleBooks(),
             "neodb": neodb.neoDB(),
             "tmdb-movie": tmdb.TMDB(key),
             "tmdb-tv": tmdb.TMDB(key, type="tv"),
             "ao3": ao3.Ao3(),
             "itchio": itchio.itchIO(),
             "vndb": vndb.VNDB(),
             "stdebooks": stdebooks.StdEBooks(),
             "gutendex": gutendex.Gutendex()
        }