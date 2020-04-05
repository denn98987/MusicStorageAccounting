from bson import DBRef
from db.Author import Author
from db.db import DataBase


class Song:
    __is_changed: bool = False
    __new_author = None
    __new_name_song = None
    __id = None

    def __init__(self,  name_song: str, author: Author):
        self.__author = author
        self.__name_song = name_song

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value: Author):
        self.__is_changed = True
        self.__new_author = value

    @property
    def name_song(self):
        return self.__name_song

    @name_song.setter
    def name_song(self, value: str):
        self.__is_changed = True
        self.__new_name_song = value

    @property
    def id(self):
        if self.__id is None:
            raise Exception("Song didn't add to database yet. Please commit it.")
        return self.__id

    def commit(self, db: DataBase):
        if db.find_obj(self) is None:
            self.__id = db.save_get_id(self)
        elif self.__is_changed:
            new_name_song = self.__new_name_song if self.__new_name_song is not None else self.name_song
            new_author = self.__new_author if self.__new_author is not None else self.author
            db.update(self, Song(new_name_song, new_author))
            self.name_song = new_name_song
            self.author = new_author
            self.__is_changed = False
        else:
            self.__id = db.get_id_obj(self)

    def __dict__(self):
        return {
            "name_song": self.name_song,
            "author": DBRef(collection=DataBase.get_type_collection(self.author), id=self.author.id)
        }

