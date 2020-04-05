from db.Author import Author
from db.Recorder import Recorder
from db.Song import Song
from db.db import DataBase
import unittest

#need to refactor
class TestDB(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDB, self).__init__(*args, **kwargs)
        self.db = DataBase("test")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.db.dropDatabase()

    def test_recorder_new(self):
        atlantic = Recorder("Atlantic", "USA")
        atlantic.commit(self.db)
        self.assertEqual({"name": "Atlantic", "country": "USA"}, atlantic.__dict__())
        self.assertEqual({"name": "Atlantic", "country": "USA"},
                         self.db.db.recorder.find({"name": "Atlantic"}, {"_id": False})[0])

    def test_update(self):
        expected = Recorder("boss", "huge")
        expected.commit(self.db)
        self.db.update(Recorder("asa", "sos"), expected)
        actual = self.db.db.recorder.find_one({"name": "boss"}, {"_id": False})
        self.assertEqual(expected.__dict__(), actual)

    def test_author(self):
        itmoment = Author("in this moment", "maria brink", "eduard alal")
        itmoment.commit(self.db)
        expected = itmoment.__dict__()
        actual = self.db.db.author.find_one({"name": "in this moment"}, {"_id": False})
        self.assertEqual(expected, actual)
        itmoment.add_soloist("fag")
        actual = self.db.db.author.find_one({"name": "in this moment"}, {"_id": False})
        expected = itmoment.__dict__()
        self.assertEqual(expected, actual)

    def test_get_id(self):
        a = Recorder("dfv", "dfgfd")
        a.commit(self.db)
        # print(self.db.get_id_obj(a)['_id'])

    def test_song(self):
        linda = Author("linda", "linda")
        linda.commit(self.db)
        vorona = Song("ya vorona", linda)
        vorona.commit(self.db)
        id = self.db.get_id_obj(vorona.author)
        actual = self.db.db.author.find_one({"_id": id})
        vorona.name_song = "i am vorona"
        vorona.commit(self.db)
        # print(actual['name'])

    def test_media(self):
        pass

if __name__ == '__main__':
    unittest.main()
