import unittest
import tempfile

from model import Base, Employee, LunchOrder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, column, func, text


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

        session = DBSession()
        s = select([text('sum(employee.id) + 1')]).select_from(Employee)
        result = session.execute(s)




if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    unittest.main()

