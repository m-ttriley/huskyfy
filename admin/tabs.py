__author__ = 'Nick Flanders'

from tkinter import *
from tkinter.ttk import *
import admin.song_view

class Tabs(Notebook):
    """
    Represents a tabbed view for displaying information about the songs
    in each building
    """
    def __init__(self, titles, parent=None):
        """
        Initializes a new tabbed view with the given list of titles as the headers
        :param titles: list of header titles
        :param parent: the parent widget of this tabbed view
        :return: an initialized tabbed view
        """
        super(Tabs, self).__init__(master=parent)
        self.titles = titles
        self.frames = [Frame(self) for _ in titles]
        self.song_views = []
        for index, frame in enumerate(self.frames):
            self.add(frame, text="  " + self.titles[index] + "  ")

    def add_songs(self, page: int, songs: list):
        """
        Add the given songs to the given page of this tabs view
        :param songs: the list of Songs to add
        """
        if len(self.frames) > page:
            song_list = admin.song_view.SongView(parent=self.frames[page], songs=songs)
            self.song_views.append(song_list)
            song_list.pack()

