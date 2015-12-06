__author__ = 'Nick Flanders'

from tkinter import *
from tkinter.ttk import *
from admin.info_view import *


class SongView(Treeview):
    """
    Represents a list view for displaying lists of songs
    """
    _columns = ("Song", "Artist", "Album", "URI", "User", "Date")
    _col_widths = (150, 150, 150, 180, 120, 150)

    def __init__(self, parent=None, songs=None):
        """
        Initializes a TreeView widget to display information pertaining to songs
        :param parent:  the parent widget of this TreeView
        :return:        an initialized SongList (TreeView)
        """
        super(SongView, self).__init__(master=parent, height=20)
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
        self.bind("<Double-1>", self._on_double_click)

    def add_songs(self, new_songs: list):
        """
        Add the given songs to this SongView
        :param songs: the list of Songs to add
        """
        for song in new_songs:
            self.insert('', 'end', values=(song.title, song.artist, song.album, song.uri, song.user, song.date))
        self.songs += new_songs

    def _on_double_click(self, event):
        """
        Handle a double click action on a specific item in this SongView
        """
        index = self.index(self.identify_row(event.y))
        InfoView(self.songs[index])
