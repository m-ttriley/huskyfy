__author__ = 'Nick Flanders'

from tkinter import *
from tkinter.ttk import *
import admin.tabs
import admin.song_view
from admin.song import *
from pymongo import MongoClient

class Application:
    """
    Wrapper to coordinate the execution of the admin application
    """

    def __init__(self, db):
        """
        Initializes this Application
        :param db:  the database connection to use for populating this application
        """
        self.db = db
        self.building_collection = db["buildings"]
        self.song_collection = db["songs"]

        # initialize all GUI components visible at startup
        self.root = Tk()
        self.root.geometry("800x600")
        self.root.title("Huskyfy Admin Manager")

        # initialize a dictionary mapping building types to lists of buildings from the db
        self._get_buildings()

        # initialize all tabs to the initial building type
        self.building_type = "academic"
        self._init_tabs()

        # initialize the search box and the search button
        self.search_value = StringVar()
        self.search_box = Entry(self.root, width=51, font=("Arial", 12), textvariable=self.search_value)
        self.search_button = Button(self.root, text="Search", width=10)

        # initialize the drop down menu for selecting the type of building
        self._init_optionmenu()

        self.render()
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
            pass # tabs doesn't exist yet

        self.tabs = admin.tabs.Tabs(
            [result["display_name"] for result in self.buildings[self.building_type]],
            parent=self.root)
        for page, building in enumerate(self.buildings[self.building_type]):
            song_response = self.song_collection.find(
                {"building_id": self.building_collection.find_one(
                    {"display_name": building["display_name"]})["_id"]})
            self.tabs.add_songs(page, [Song.from_dict(record) for record in song_response])

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
        self._init_tabs()
        self.render()

    def render(self):
        """
        Renders the GUI
        """
        self.tabs.grid(row=0, column=0, pady=10, columnspan=2, rowspan=10)
        self.search_box.grid(row=10, column=0)
        self.search_button.grid(row=10, column=1)
        self.menu_label.grid(row=3, column=2)
        self.menu.grid(row=4, column=2)
