__author__ = 'Nick Flanders'

import sys
from pymongo import MongoClient
import datetime

# confirm that the user want to overwrite all the data in the db before doing so
if input("Are you sure you want to overwrite all data in the database with sample data? (y/n)") != 'y':
    sys.exit(0)


MONGO_URL = "mongodb://matt:riley@ds053794.mongolab.com:53794/huskyfy"

client = MongoClient(MONGO_URL)
db = client["huskyfy"]
buildings = db["buildings"]
songs = db["songs"]

# building tuple structure
# (building id, building name, display name, building type)
names = ["Behrakis", "Blackman", "Cabot", "Cargill", "Churchill", "Curry", "Dodge",
         "Ell Hall", "Matthews", "Marino", "Meserve", "Mugar", "Richards", "Robinson",
         "Ryder", "Shillman", "Snell", "International Village"]
academic = [
    ("Behrakis Health Science Center", "Behrakis"),
    ("Blackman Auditorium", "Blackman"),
    ("Cargill Hall", "Cargill"),
    ("Churchill Hall", "Churchill"),
    ("Dodge Hall", "Dodge"),
    ("Egan Engineering/Science Reseach Center", "Egan"),
    ("Ell Hall", "Ell"),
    ("Hurtig Hall", "Hurtig"),
    ("Kariotis Hall", "Kariotis"),
    ("Richards Hall", "Richards"),
    ("Shillman Hall", "Shillman"),
    ("Snell Library and Engineering Center", "Snell"),
    ("International Village", "IV"),
    ("West Village F", "WVF"),
    ("West Village H", "WVH"),
    ("West Village G", "WVG")
]

residential = [
    ("International Village", "IV"),
    ("West Village F", "WVF"),
    ("West Village H", "WVH"),
    ("West Village G", "WVG"),
    ("Davenport Commons", "Davenport"),
    ("Kennedy Hall", "Kennedy"),
    ("Kerr Hall", "Kerr"),
    ("Smith Hall", "Smith"),
    ("Speare Hall", "Speare"),
    ("Stetson", "Stetson"),
    ("Willis Hall", "Willis")
]

other = [
    ("Cabot Physical Education Center", "Cabot"),
    ("Marino Recreation Center", "Marino"),
    ("Curry Student Center", "Curry"),

]



# build up a list of all of the buildings
building_list = []
# track the ids assigned to all of the buildings
ids = dict()
current_id = 0

# add all of the academic buildings
for full, short in academic:
    building_list.append({"_id": current_id, "name": full,
                          "display_name": short, "types": ["academic"]})
    ids[short] = current_id
    current_id += 1

# add all of the residential buildings
for full, short in residential:
    found = False
    for building in building_list:
        if building["name"] == full:
            building["types"].append("residential")
            found = True
    if not found:
        building_list.append({"_id": current_id, "name": full,
                              "display_name": short, "types": ["residential"]})
        ids[short] = current_id
        current_id += 1

# add all of the other buildings
for full, short in other:
    found = False
    for building in building_list:
        if building["name"] == full:
            building["types"].append("other")
            found = True
    if not found:
        building_list.append({"_id": current_id, "name": full,
                              "display_name": short, "types": ["other"]})
        ids[short] = current_id
        current_id += 1




# song tuple structure
#(building id, song title, artist, album, uri, user, date)
song_data = [
    (ids["Marino"], "Instant Crush", "Daft Punk", "Random Access Memories", "spotify:track:2cGxRwrMyEAp8dEbuZaVv6",
    "Nick", datetime.datetime(2015, 12, 4, 12, 20)),
    (ids["IV"], "One More Time", "Daft Punk", "Discovery", "spotify:track:0DiWol3AO6WpXZgp0goxAV",
    "Nick", datetime.datetime(2015, 12, 3, 17, 50)),
    (ids["WVF"], "American Money", "Borns", "Dopamine", "spotify:track:4AewKenHXKBt643p473xCk",
    "Nick", datetime.datetime(2015, 12, 2, 11, 23)),
    (ids["Cabot"], "Migraine", "twenty one pilots", "Vessel", "spotify:track:4rfaoyaZvNa60cj3OKSQV9",
    "Nick", datetime.datetime(2015, 12, 4, 13, 23))
]

# create a list of dictionaries to insert as songs into the db
songs_list = [
    {"building_id": building, "title": title, "artist": artist, "album": album,
     "uri": uri, "user": user, "date": date}
    for building, title, artist, album, uri, user, date in song_data
]

# remove any buildings that were already in the db
buildings.remove()
buildings.insert_many(building_list)

# remove any songs that were already in the db
songs.remove()
songs.insert_many(songs_list)