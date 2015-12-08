__author__ = 'Nick Flanders'

import sys
from pymongo import MongoClient
import datetime

# confirm that the user want to overwrite all the data in the db before doing so
if input("Are you sure you want to overwrite all data in the database with sample data? (y/n) ") != 'y':
    sys.exit(0)

# determine whether the user wants to output the MongoDB insert commands to a given file
to_file = False
file_path = ""
if len(sys.argv) == 3 and sys.argv[1] == "-f":
    to_file = True
    file_path = sys.argv[2]


MONGO_URL = "mongodb://matt:riley@ds053794.mongolab.com:53794/huskyfy"

client = MongoClient(MONGO_URL)
db = client["huskyfy"]
buildings = db["buildings"]
songs = db["songs"]

# building tuple structure
# (building id, building name, display name, building type, lattitude, longitude)

academic = [
    ("Behrakis Health Science Center", "Behrakis", 42.336901, -71.091703),
    ("Egan Engineering/Science Reseach Center", "Egan", 42.338132, -71.089094),
    ("Ell Hall", "Ell", 42.339695, -71.088012),
    ("Hurtig Hall", "Hurtig", 42.339778, -71.086141),
    ("Kariotis Hall", "Kariotis", 42.338705, -71.090752),
    ("Richards Hall", "Richards", 42.339934, -71.088794),
    ("Ryder Hall", "Ryder", 42.336588, -71.090764),
    ("Shillman Hall", "Shillman", 42.337595, -71.090267),
    ("Snell Library and Engineering Center", "Snell", 42.338479, -71.088040),
    ("International Village", "IV", 42.335086, -71.089382),
    ("West Village F", "WVF", 42.337536, -71.091518),
    ("West Village H", "WVH", 42.338703, -71.092205),
]

residential = [
    ("International Village", "IV", 42.335086, -71.089382),
    ("West Village F", "WVF", 42.337536, -71.091518),
    ("West Village H", "WVH", 42.338703, -71.092205),
    ("Speare Hall", "Speare", 42.340614, -71.089642),
    ("Stetson", "Stetson", 42.341218, -71.090464),
]

other = [
    ("Cabot Physical Education Center", "Cabot", 42.339567, -71.089858),
    ("Marino Recreation Center", "Marino", 42.340350, -71.090349),
    ("Curry Student Center", "Curry", 42.339100, -71.087469),

]

# build up a list of all of the buildings
building_list = []
# track the ids assigned to all of the buildings
ids = dict()
current_id = 0

# add all of the academic buildings
for full, short, lattitude, longitude in academic:
    building_list.append({"_id": current_id, "name": full,
                          "display_name": short, "types": ["academic"],
                          "latitude": lattitude, "longitude": longitude})
    ids[short] = current_id
    current_id += 1

# add all of the residential buildings
for full, short, lattitude, longitude in residential:
    found = False
    for building in building_list:
        if building["name"] == full:
            building["types"].append("residential")
            found = True
    if not found:
        building_list.append({"_id": current_id, "name": full,
                              "display_name": short, "types": ["residential"],
                              "latitude": lattitude, "longitude":longitude})
        ids[short] = current_id
        current_id += 1

# add all of the other buildings
for full, short, lattitude, longitude in other:
    found = False
    for building in building_list:
        if building["name"] == full:
            building["types"].append("other")
            found = True
    if not found:
        building_list.append({"_id": current_id, "name": full,
                              "display_name": short, "types": ["other"],
                              "latitude": lattitude, "longitude":longitude})
        ids[short] = current_id
        current_id += 1




# song tuple structure
#(building id, song title, artist, album, uri, user, date)
song_data = [
    (ids["Marino"], "Instant Crush", "Daft Punk", "Random Access Memories", "2cGxRwrMyEAp8dEbuZaVv6",
    "Nick", datetime.datetime(2015, 12, 4, 12, 20)),
    (ids["IV"], "One More Time", "Daft Punk", "Discovery", "0DiWol3AO6WpXZgp0goxAV",
    "Nick", datetime.datetime(2015, 12, 3, 17, 50)),
    (ids["Behrakis"], "American Money", "Borns", "Dopamine", "4AewKenHXKBt643p473xCk",
    "Nick", datetime.datetime(2015, 12, 2, 11, 23)),
    (ids["IV"], "Migraine", "twenty one pilots", "Vessel", "4rfaoyaZvNa60cj3OKSQV9",
    "Nick", datetime.datetime(2015, 12, 4, 13, 23)),
    (ids["WVF"], "Simple & Sweet", "Jon Bellion", "The Definition", "0wUlGPa8He68F9TmLKdcL4",
     "Nick", datetime.datetime(2015, 11, 30, 13, 10)),
    (ids["WVF"], "Jealous (I Ain't With It)", "Chromeo", "White Women", "3R5FA1Ay1NxgtwbElR78by",
    "Nick", datetime.datetime(2015, 11, 30, 14, 2)),
    (ids["Marino"], "Diane Young", "Vampire Weekend", "Modern Vampires of the City", "104pmtTQOlmW8Zt2BipGKH",
    "Nick", datetime.datetime(2015, 12, 1, 2, 23)),
    (ids["Marino"], "Clearest Blue", "CHVRCHES", "Every Open Eye", "3aUfWeMesfVs2niopKjNxV",
    "Nick", datetime.datetime(2015, 12, 2, 12, 54)),
    (ids["WVF"], "Taxi Cab", "twenty one pilots", "Twenty One Pilots", "4j8gmCSLLy0TSFg2brV01g",
    "Nick", datetime.datetime(2015, 12, 3, 23, 54)),
    (ids["Cabot"], "Goner", "twenty one pilots", "Blurryface", "5P3yUXUC9rZPJPNmYGKEAz",
    "Nick", datetime.datetime(2015, 12, 3, 5, 32)),
    (ids["IV"], "We Sink", "CHVRCHES", "The Bones of What You Believe", "4t7EGF0kXG5KeFrQ7hxdc1",
    "Nick", datetime.datetime(2015, 12, 3, 4, 34)),
    (ids["IV"], "Unbelievers", "Vampire Weekend", "Modern Vampires of the City", "7psPPGwhFzP3pyOcb3ivcT",
    "Nick", datetime.datetime(2015, 12, 3, 4, 35)),
    (ids["IV"], "Divinity", "Porter Robinson", "Worlds", "18cCBvygH6yEFDY0cYN3wT",
    "Nick", datetime.datetime(2015, 12, 3, 1, 23)),
    (ids["IV"], "Lose Yourself to Dance", "Daft Punk", "Random Access Memories", "5CMjjywI0eZMixPeqNd75R",
    "Nick", datetime.datetime(2015, 12, 4, 12, 43)),
    (ids["IV"], "The General", "Dispatch", "Bang Bang", "6n6EXIwLtNwe4u4CFzENYm",
    "Nick", datetime.datetime(2015, 12, 2, 23, 43)),
    (ids["IV"], "Don't Sing", "Data", "Don't Sing", "3Q7Fhds0twd9SAHrcGTwYL",
    "Nick", datetime.datetime(2015, 12, 1, 21, 42)),
    (ids["IV"], "Space Oddity - 2015 Remaster", "David Bowie", "Five Years (1969 - 1973)", "5sUrZEf4qEtjepdgcetith",
    "Nick", datetime.datetime(2015, 12, 3, 12, 43)),
    (ids["IV"], "Superego", "Disclosure", "Caracal", "4vd7KzctkhCVCUnCCyoO0d",
    "Nick", datetime.datetime(2015, 12, 2, 23, 12)),
    (ids["IV"], "Sunrise", "Slaptop", "Sunrise", "0n0p8VGjFfQSXnCKUMPCWU",
    "Nick", datetime.datetime(2015, 11, 30, 1, 32)),
    (ids["IV"], "Paris", "Magic Man", "Before the Waves", "4EaO2XR7gWaHq8DW7nu1iY",
    "Nick", datetime.datetime(2015, 12, 1, 23, 43)),
    (ids["IV"], "Lifted Up (1985)", "Passion Pit", "Kindred", "0WjvB0SzNvgmuM46UjcMr8",
    "Nick", datetime.datetime(2015, 11, 30)),
    (ids["Behrakis"], "Paradise by the Dashboard Light", "Meatloaf", "Bat Out of Hell", "7mzHEzbsl5iOvBRuXwReZU",
    "Nick", datetime.datetime(2015, 12, 3, 3, 43))
]

# create a list of dictionaries to insert as songs into the db
songs_list = [
    {"building_id": building, "title": title, "artist": artist, "album": album,
     "uri": uri, "user": user, "date": date}
    for building, title, artist, album, uri, user, date in song_data
]

print("Equivalent MongoDB insert statements:\n\n")

# remove any buildings that were already in the db
buildings.remove()
print("db.buildings.remove({})")
buildings.insert_many(building_list)
for building in building_list:
    print("db.buildings.insert(" + str(building) + ")\n")

# write the commands to a file if necessary
if to_file:
    with open(file_path, 'w') as doc:
        for building in building_list:
            doc.write("db.buildings.insert(" + str(building) + ")\n")

# remove any songs that were already in the db
songs.remove()
print("db.songs.remove({})")
songs.insert_many(songs_list)
for song in songs_list:
    print("db.songs.insert(" + str(song).replace("datetime.datetime", "ISODate") + ")\n")
print("db.songs.createIndex({building_id: 1})\n\n")

# write the commands to a file if necessary
if to_file:
    with open(file_path, 'a') as doc:
        for song in songs_list:
            doc.write("db.songs.insert(" + str(song).replace("datetime.datetime", "ISODate") + ")\n")
        doc.write("db.songs.createIndex({building_id: 1})\n")
        
print("Database updated with {} songs and {} buildings.".format(len(songs_list), len(building_list)))