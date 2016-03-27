import unittest

from app.security import secure_token
import random


class SecurityTest(unittest.TestCase):

    def test_tokens(self):
        random.seed(1001)
        token = secure_token()
        self.assertEqual(len(token), 64)
        e = "78858341de6318734209c4c993a330fe29b4feccdbd17a2ec2f22e12f0179026"
        self.assertEqual(token, e)


if __name__ == '__main__':
    unittest.main()
