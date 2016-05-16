import unittest

from app.security import secure_token
import random


class SecurityTest(unittest.TestCase):

    def test_tokens(self):
        random.seed(1001)
        token = secure_token()
        self.assertEqual(len(token), 64)
        e = "3e70ac6dab84ef33d5570b541a4d376772c091e504fdb220b033cfa5f265d0fd"
        self.assertEqual(token, e)


if __name__ == '__main__':
    unittest.main()
