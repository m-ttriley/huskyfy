__author__ = 'Nick Flanders'

from tkinter import *
from tkinter.ttk import *
import admin.tabs
import admin.song_view
import admin.info_view
from admin.song import *


class Application:
    """
    Wrapper to coordinate the execution of the admin application
    """

    # store database as a class field so all components can make queries
    db = None

    # only allow one instance of the application to run at a time
    instance = None

    def __init__(self, db):
        """
        Initializes this Application
        :param db:  the database connection to use for populating this application
        """
        if Application.instance is not None:
            Application.instance.root.focus_force()
            return
        self.db = db
        Application.db = db
        self.building_collection = db["buildings"]
        self.song_collection = db["songs"]

        # initialize all GUI components visible at startup
        self.root = Tk()
        self.root.geometry("1040x520")
        self.root.title("Huskyfy Admin Manager")
        self.root.iconbitmap(r"admin/icon.ico")

        # initialize a dictionary mapping building types to lists of buildings from the db
        self._get_buildings()

        # initialize all tabs to the initial building type
        self.building_type = "academic"
        self._init_tabs()

        # initialize the search box and the search button
        self.search_value = StringVar()
        self.search_box = Entry(self.root, width=90, font=("Arial", 12), textvariable=self.search_value)
        self.search_box.bind("<Return>", self.search)
        self.search_button = Button(self.root, text="Search", width=10, command=self.search)

        # initialize the drop down menu for selecting the type of building
        self._init_optionmenu()

        # initialize the add song button
        self.add_button = Button(self.root, text="Add Song", width=10, command=self.add_song)

        self.render()
        Application.instance = self
        self.root.mainloop()

    def _get_buildings(self):
        """
        Query the database to get all of the buildings of each type and put them in
        the appropriate variable of this Application
        """
        self.buildings = dict()
        building_list = list(self.building_collection.find())
        for building_type in ["academic", "residential", "other"]:
            self.buildings[building_type] = [building for building in building_list if building_type in building["types"]]

    def _init_tabs(self):
        """
        Initializes the tab view of this application
        """
        try:
            self.tabs.destroy()
        except AttributeError:
            # tabs widget doesn't exist yet
            pass

        self.tabs = admin.tabs.Tabs(
            [result["display_name"] for result in self.buildings[self.building_type]],
            parent=self.root)

        self.tabs.bind("<<NotebookTabChanged>>", lambda event: self._set_selected_tab())
        for page, building in enumerate(self.buildings[self.building_type]):
            song_response = self.song_collection.find(
                {"building_id": self.building_collection.find_one(
                    {"display_name": building["display_name"]})["_id"]})
            self.tabs.add_songs(page, [Song.from_dict(record) for record in song_response])
        try:
            self.tabs.select(self.current_tab_index)
        except AttributeError:
            self.current_tab_index = 0

    def _init_optionmenu(self):
        """
        Initialize the Listbox widget containing the types of buildings to display
        """
        self.menu_label = Label(self.root, text="Building Type:")
        self.menu_var = StringVar(self.root)
        b_types = list(self.buildings.keys())
        self.menu = OptionMenu(self.root, self.menu_var, b_types[0],
                               *b_types, command=lambda val: self.set_building_type(val))
        self.menu.config(width=10)

    def set_building_type(self, building_type):
        """
        Sets the building type of this Application
        """
        self.building_type = building_type
        del self.current_tab_index
        self._init_tabs()
        self.render()

    def _set_selected_tab(self):
        """
        Sets the currently selected tab for the Notebook
        """
        self.current_tab_index = self.tabs.index(self.tabs.select())

    def add_song(self):
        """
        Displays a dialogue box for adding a new song
        """
        admin.info_view.InfoView(Song(None, "", "", "", "", building_id=None))

    def search(self, event=None):
        """
        Opens a new window with the result of searching the given string across title, artist, album, and user
        """
        search_string = self.search_value.get()
        results = []
        results += list(self.song_collection.find({"title": {"$regex": ".*" + search_string + ".*", "$options": "i"}}))
        if search_string != "":
            results += list(self.song_collection.find({"artist": {"$regex": ".*" + search_string + ".*", "$options": "i"}}))
            results += list(self.song_collection.find({"album": {"$regex": ".*" + search_string + ".*", "$options": "i"}}))
            results += list(self.song_collection.find({"user": {"$regex": ".*" + search_string + ".*", "$options": "i"}}))

        popup = admin.song_view.SongView(parent=Toplevel(), songs=[Song.from_dict(result) for result in results])
        popup.grid()
        popup.focus_force()
        popup.bind("<Escape>", lambda event: popup.master.destroy())

    def render(self):
        """
        Renders the GUI
        """
        self.tabs.grid(row=0, column=0, pady=10, padx=10, columnspan=2, rowspan=10)
        self.search_box.grid(row=10, column=0, padx=10)
        self.search_button.grid(row=10, column=1)
        self.add_button.grid(row=7, column=2)
        self.menu_label.grid(row=3, column=2)
        self.menu.grid(row=4, column=2)
