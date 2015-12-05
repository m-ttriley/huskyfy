__author__ = 'Nick Flanders'

from tkinter import *
from tkinter.ttk import *
from time import strptime, mktime
from datetime import datetime
import admin.application

class InfoView(Frame):
    """
    Represents a view of an individual song that provides the ability to view
    and update detailed information about a given song
    """

    # only allow one concurrent instance per song
    instances = []

    def __init__(self, song, parent=None):
        """
        Initializes this InfoView
        """
        # only have one instance per song open at any given time
        for instance in InfoView.instances:
            if instance.song == song:
                instance.parent.focus_force()
                return
        self.song = song
        self.song_collection = admin.application.Application.db["songs"]
        if parent is None:
            parent = Toplevel()
            parent.title(self.song.title + " Info")
        self.parent = parent
        super(Frame, self).__init__(self.parent, None)

        # initialize labels
        self.song_label = Label(master=self.parent, text="Song:")
        self.artist_label = Label(master=self.parent, text="Artist:")
        self.album_label = Label(master=self.parent, text="Album:")
        self.building_label = Label(master=self.parent, text="Building ID:")
        self.user_label = Label(master=self.parent, text="User:")
        self.date_label = Label(master=self.parent, text="Date:")
        self.uri_label = Label(master=self.parent, text="Spotify URI:")

        #initialize entry boxes
        self.song_var = StringVar(master=self.parent, value=song.title)
        self.song_box = Entry(master=self.parent, text=self.song_var, width=40)
        self.artist_var = StringVar(master=self.parent, value=song.artist)
        self.artist_box = Entry(master=self.parent, text=self.artist_var, width=40)
        self.album_var = StringVar(master=self.parent, value=song.album)
        self.album_box = Entry(master=self.parent, text=self.album_var, width=40)
        self.building_var = StringVar(master=self.parent, value=song.building_id)
        self.building_box = Entry(master=self.parent, text=self.building_var, width=40)
        self.user_var = StringVar(master=self.parent, value=song.user)
        self.user_box = Entry(master=self.parent, text=self.user_var, width=40)
        self.date_var = StringVar(master=self.parent, value=song.date)
        self.date_box = Entry(master=self.parent, text=self.date_var, width=40)
        self.uri_var = StringVar(master=self.parent, value=song.uri)
        self.uri_box = Entry(master=self.parent, text=self.uri_var, width=40)

        # initialize update button
        self.update_button = Button(self.parent, text="Update", command=self.update_db)
        self.delete_button = Button(self.parent, text="Delete", command=self.delete_song)

        self.render()
        InfoView.instances.append(self)
        self.parent.protocol("WM_DELETE_WINDOW", lambda: InfoView.instances.remove(self) or self.parent.destroy())

    def update_db(self):
        """
        Updates the information in the database to the current values
        """
        date_string = self.date_var.get()
        date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        fields = {"title": self.song_var.get(), "artist": self.artist_var.get(), "album": self.album_var.get(),
                  "uri": self.uri_var.get(), "user": self.user_var.get(), "date": date,
                  "building_id": int(self.building_var.get())}
        if self.song.id is not None:
            self.song_collection.update({"_id": self.song.id}, fields)
        else:
            self.song_collection.insert(fields)
        self.parent.destroy()
        admin.application.Application.instance._init_tabs()
        admin.application.Application.instance.render()

    def delete_song(self):
        """
        Removes the song associates with this InfoView from the database
        """
        self.song_collection.remove({"_id": self.song.id})
        self.parent.destroy()
        admin.application.Application.instance._init_tabs()
        admin.application.Application.instance.render()

    def render(self):
        """
        Renders this InfoView object
        """
        self.song_label.grid(row=0, column=0, padx=5, pady=7)
        self.artist_label.grid(row=1, column=0, padx=5, pady=7)
        self.album_label.grid(row=2, column=0, padx=5, pady=7)
        self.building_label.grid(row=3, column=0, padx=5, pady=7)
        self.user_label.grid(row=4, column=0, padx=5, pady=7)
        self.date_label.grid(row=5, column=0, padx=5, pady=7)
        self.uri_label.grid(row=6, column=0, padx=5, pady=7)

        self.song_box.grid(row=0, column=1, padx=5, pady=7, columnspan=2)
        self.artist_box.grid(row=1, column=1, padx=5, pady=7, columnspan=2)
        self.album_box.grid(row=2, column=1, padx=5, pady=7, columnspan=2)
        self.building_box.grid(row=3, column=1, padx=5, pady=7, columnspan=2)
        self.user_box.grid(row=4, column=1, padx=5, pady=7, columnspan=2)
        self.date_box.grid(row=5, column=1, padx=5, pady=7, columnspan=2)
        self.uri_box.grid(row=6, column=1, padx=5, pady=7, columnspan=2)

        self.update_button.grid(row=7, column=1, padx=5, pady=7)
        self.delete_button.grid(row=7, column=2, padx=5, pady=7)