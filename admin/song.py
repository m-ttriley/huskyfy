__author__ = 'Nick Flanders'

class Song:
    """
    Wrapper object containing song information
    """
    def __init__(self, title, artist, album, uri, building_id, user=None, date=None):
        """
        Initialize the song with the given information
        :param title: title of the song as a string
        :param artist: song artist as a string
        :param album: song album as a string
        :param uri: the Spotify URI used for playing the song as a string
        :param user: the username of the person who added the song as a string
        :return:
        """
        self.title = title
        self.artist = artist
        self.album = album
        self.uri = uri
        self.building_id = building_id
        if user is None:
            self.user = ""
        else:
            self.user = user
        self.date = date

    @classmethod
    def from_dict(cls, json):
        """
        Initialize a song based on responses from the db
        :param json: the dictionary containing the json response from the db
        """
        title = json["title"]
        artist = json["artist"]
        album = json["album"]
        uri = json["uri"]
        user = json["user"]
        building_id = json["building_id"]
        date = json["date"]
        return cls(title, artist, album, uri, building_id, user, date)

