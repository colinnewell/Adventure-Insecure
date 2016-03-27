import os
os.environ['APP_SETTINGS'] = 'config.TestingConfig'
from app import app, db
import unittest
import tempfile
import re


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_filename = tempfile.mkstemp()
        # FIXME: this isn't actually working.
        app.config['DATABASE_URI'] = 'sqlite:///' + self.db_filename
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_filename)

    def test_base(self):
        rv = self.app.get('/')
        assert 'Lunch Ordering' in rv.data.decode('utf-8')

    def get_csrf_token(self, rv):
        m = re.search('.*name="csrf_token".*?value="([^"]+)".*',
                      rv.data.decode('utf-8'))
        csrf = m.group(1)
        return csrf

    def login(self, user, password):
        rv = self.app.get('/auth/login')
        csrf = self.get_csrf_token(rv)
        return self.app.post('/auth/login', data=dict(
            email=user,
            password=password,
            csrf_token=csrf,
        ), follow_redirects=True)

    def test_login_fail(self):
        rv = self.login('bogus', 'test')
        assert 'Invalid email' in rv.data.decode('utf-8')
        rv = self.login('bogus@example.org', 'test')
        assert 'Incorrect email or password' in rv.data.decode('utf-8')


if __name__ == '__main__':
    unittest.main()
