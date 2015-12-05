"""
huskyfy_admin.py

Provides a GUI for administrative actions for the huskyfy database

Requirements:
 - Python 3.4+

Usage:
    python huskyfy_admin.py
"""

from admin.application import Application
from pymongo import MongoClient


MONGO_URL = "mongodb://matt:riley@ds053794.mongolab.com:53794/huskyfy"

client = MongoClient(MONGO_URL)
db = client.huskyfy

buildings = db["buildings"]
songs = db["songs"]



if __name__ == "__main__":
    app = Application(db)
    """
    root = Tk()
    root.grid()
    root.geometry("800x400")

    building_list = [result["display_name"] for result in buildings.find()]

    tabs = admin.tabs.Tabs(building_list, parent=root)
    song_results = songs.find({"building_id": buildings.find_one({"display_name": "WVF"})["_id"]})
    tabs.add_songs(0, [Song.from_dict(record) for record in song_results])
    tabs.grid(row=0, column=0, pady=10, columnspan=2)

    search_value = StringVar()
    search_box = Entry(root, width=51, font=("Arial", 12), textvariable=search_value)
    search_box.grid(row=1, column=0)

    search_button = Button(root, text="Search", width=10)
    search_button.grid(row=1, column=1)
    root.title("Huskyfy Admin Manager")
    root.mainloop()"""