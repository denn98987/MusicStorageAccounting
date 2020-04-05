from db.db import DataBase


class Recorder:
    __is_changed = False
    __new_name = None
    __new_country = None
    __id = None

    def __init__(self, name: str, country: str):
        self.__name = name
        self.__country = country

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__new_name = value
        self.__is_changed = True

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, value):
        self.__new_country = value
        self.__is_changed = True

    def __dict__(self):
        return {
            "name": self.name,
            "country": self.country
        }

    def remove(self, db: DataBase):
        db.remove(self)

    def commit(self, db: DataBase):
        if db.find_obj(self) is None:
            self.__id = db.save_get_id(self)
        elif self.__is_changed:
            new_name = self.name if self.__new_name is None else self.__new_name
            new_country = self.country if self.__new_country is None else self.__new_country
            db.update(self, Recorder(new_name, new_country))
            self.name, self.country = new_name, new_country
            self.__is_changed = False
        else:
            self.__id = db.get_id_obj(self)
