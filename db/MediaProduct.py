from bson import DBRef

from db import Recorder
from db.db import DataBase


class MediaProduct:
    __is_changed = False
    __id = None
    __new_name = None
    __new_year = None
    __new_recorder = None

    def __init__(self, name: str, types: [], recorder: Recorder, year: str, songs: []):
        self.__songs = songs
        self.__year = year
        self.__recorder = recorder
        self.__name = name
        self.__types = types
        self.__new_types = types
        self.__new_songs = songs

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__is_changed = True
        self.__new_name = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value: str):
        self.__is_changed = True
        self.__new_year = value

    @property
    def recorder(self):
        return self.__recorder

    @recorder.setter
    def recorder(self, value: str):
        self.__is_changed = True
        self.__new_recorder = value

    @property
    def types(self):
        return self.__types

    def add_type(self, type: str):
        self.__is_changed = True
        self.__new_types.append(type)

    def change_type(self, old_value: str, new_value: str):
        self.__is_changed = True
        self.__new_types[self.types.index(old_value)] = new_value

    def remove_type(self, type: str):
        self.__is_changed = True
        self.__new_types.remove(type)

    @property
    def songs(self):
        return self.__songs

    def add_song(self, song: str):
        self.__is_changed = True
        self.__new_songs.append(song)

    def change_song(self, old_value: str, new_value: str):
        self.__is_changed = True
        self.__new_songs[self.songs.index(old_value)] = new_value

    def remove_song(self, song: str):
        self.__is_changed = True
        self.__new_songs.remove(song)

    @property
    def id(self):
        if self.__id is None:
            raise Exception("MediaProduct didn't add to database yet. Please commit it.")
        return self.__id

    def commit(self, db: DataBase):
        if db.find_obj(self) is None:
            self.__id = db.save_get_id(self)
        elif self.__is_changed:
            new_name = self.__new_name if self.__new_name is not None else self.name
            new_year = self.__new_year if self.__new_year is not None else self.year
            new_recorder = self.__new_recorder if self.__new_recorder is not None else self.recorder
            new_songs = self.songs if self.songs == self.__new_songs else self.__new_songs
            new_types = self.types if self.types == self.__new_types else self.__new_types
            db.update(self, MediaProduct(new_name, new_types, new_recorder, new_year, new_songs))
            self.name = new_name
            self.year = new_year
            self.recorder = new_recorder
            self.__types = new_types
            self.__songs = new_songs
            self.__is_changed = False
        else:
            self.__id = db.get_id_obj(self)

    def __dict__(self):
        return {
            "name": self.name,
            "year": self.year,
            "recorder": DBRef(collection=DataBase.get_type_collection(self.recorder), id=self.recorder.id),
            "types": self.types,
            "songs": [DBRef(collection=DataBase.get_type_collection(song), id=song.id) for song in self.songs]
        }
