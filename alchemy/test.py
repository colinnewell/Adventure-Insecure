import unittest
import tempfile

from model import Base, Employee, LunchOrder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBTest(unittest.TestCase):

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.engine = create_engine('sqlite:///' + self.folder.name + 'test.db')
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.folder.cleanup()

    def test_simple(self):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        employee = Employee(name='Colin')
        session.add(employee)

        session.commit()



if __name__ == '__main__':
    unittest.main()

