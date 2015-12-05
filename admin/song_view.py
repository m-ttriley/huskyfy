__author__ = 'Nick Flanders'

from tkinter import *
from tkinter.ttk import *


class SongView(Treeview):
    """
    Represents a list view for displaying lists of songs
    """
    _columns = ("Song", "Artist", "Album", "URI", "User", "Date")
    _col_widths = (150, 120, 120, 80, 80, 80)

    def __init__(self, parent=None, songs=None):
        """
        Initializes a TreeView widget to display information pertaining to songs
        :param parent:  the parent widget of this TreeView
        :return:        an initialized SongList (TreeView)
        """
        super(SongView, self).__init__(master=parent)
        if len(songs) == 0:
            self.songs = []
        else:
            self.songs = songs
        self["columns"] = SongView._columns
        for index, name in enumerate(SongView._columns):
            self.heading(name, text=name)
            self.column(name, width=SongView._col_widths[index])
        self.add_songs(songs)
        self["show"] = "headings"

    def add_songs(self, new_songs: list):
        """
        Add the given songs to this SongView
        :param songs: the list of Songs to add
        """
        for song in new_songs:
            self.insert('', 'end', values=(song.title, song.artist, song.album, song.uri, song.user, song.date))
        self.songs += new_songs
