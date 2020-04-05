import pymongo


class DataBase:
    def __init__(self, name: str):
        client = pymongo.MongoClient()
        self.db = client[name]

    def save_get_id(self, inserting_obj):
        coll = self.db[self.get_type_collection(inserting_obj)]
        insert_dict = inserting_obj.__dict__()
        return coll.insert_one(insert_dict).inserted_id["_id"]

    def update(self, updating_obj, new_obj):
        self.db[self.get_type_collection(updating_obj)].replace_one(updating_obj.__dict__(), new_obj.__dict__())

    def remove(self, removing_obj):
        self.db[self.get_type_collection(removing_obj)].delete_one(removing_obj.__dict__())

    def find_obj(self, obj):
        return self.db[self.get_type_collection(obj)].find_one(obj.__dict__(), {"id": False})

    def get_id_obj(self, obj):
        result = self.db[self.get_type_collection(obj)].find_one(obj.__dict__(), {"_id": 1})
        return result["_id"] if result is not None else None

    @staticmethod
    def get_type_collection(obj: object) -> str:
        return type(obj).__name__.lower()
