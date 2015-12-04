"""
huskyfy_admin.py

Provides a GUI for administrative actions for the huskyfy database

Requirements:
 - Python 3.4+

Usage:
    python huskyfy_admin.py
"""

from tkinter import *
from tkinter.ttk import *
import admin.tabs
import admin.song_view
import admin.song
from pymongo import MongoClient


MONGO_URL = "mongodb://matt:riley@ds053794.mongolab.com:53794/huskyfy"

client = MongoClient(MONGO_URL)
db = client.huskyfy

if __name__ == "__main__":
    root = Tk()
    root.grid()
    root.geometry("800x400")
    tabs = admin.tabs.Tabs(["test", "foo", "bar"], parent=root)
    tabs.add_songs(0, [admin.song.Song("test title " + str(i), "test artist", "test album",
                                    "3jb23kj4rb23", user="Nick") for i in range(10)])
    tabs.add_songs(1, [admin.song.Song("test title " + str(i), "test artist", "test album",
                                    "fgnbrn4554y", user="Matt") for i in range(17)])
    tabs.add_songs(2, [admin.song.Song("test title " + str(i), "test artist", "test album",
                                    "qab34b435h5", user="Foo") for i in range(20)])
    tabs.grid(row=0, column=0)
    root.title("Huskyfy Admin Manager")
    root.mainloop()