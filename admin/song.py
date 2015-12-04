__author__ = 'Nick Flanders'

class Song:
    """
    Wrapper object containing song information
    """
    def __init__(self, title, artist, album, uri, user=None):
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
        if user == None:
            self.user = ""
        else:
            self.user = user

