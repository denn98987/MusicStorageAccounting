from db import Author
from db.db import DataBase

class Playlist:
    __is_changed = False
    __new_name = ""
    __new_songs = [[Author, str]]

    def __init__(self, name: str, songs: [[Author, str]]):
        self.__name = name
        self.__songs = songs
        self.__new_songs = songs

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__is_changed = True
        self.__new_name = value

    @property
    def songs(self):
        return self.__songs

    @songs.setter
    def songs(self, value):
        self.__is_changed = True
        self.__songs = value

    def add_song(self, author: Author, song: str):
        self.__is_changed = True
        self.__new_songs.append([Author, song])
