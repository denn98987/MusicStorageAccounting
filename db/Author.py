from db.db import DataBase


class Author:
    __is_changed = False
    __new_name = None
    __new_soloists = None
    __id = None

    def __init__(self, name: str, *soloists):
        self.__name = name
        self.__soloists = list(soloists)
        self.__new_soloists = list(soloists)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__is_changed = True
        self.__new_name = value

    @property
    def soloists(self):
        return self.__soloists

    @soloists.setter
    def soloists(self, value: []):
        self.__soloists = value

    def add_soloist(self, soloist: str):
        self.__is_changed = True
        self.__new_soloists.append(soloist)

    def change_soloist(self, old_value: str, new_value: str):
        self.__is_changed = True
        self.__new_soloists[self.soloists.index(old_value)] = new_value

    def remove_soloist(self, soloist: str):
        self.__is_changed = True
        self.__new_soloists.remove(soloist)

    @property
    def id(self):
        if self.__id is None:
            raise Exception("This author didn't add in database yet. Please commit it.")
        return self.__id

    def commit(self, db: DataBase):
        if db.find_obj(self) is None:
            self.__id = db.save_get_id(self)
        elif self.__is_changed:
            new_name = self.name if self.__new_name is None else self.__new_name
            new_soloists = self.soloists if self.soloists == self.__new_soloists else self.__new_soloists
            db.update(self, Author(new_name, new_soloists))
            self.name, self.soloists = new_name, new_soloists
            self.__is_changed = False
        else:
            self.__id = db.get_id_obj(self)
        self.__new_soloists = []

    def __dict__(self):
        return {
            "name": self.name,
            "soloists": self.soloists
        }
