import random
import hashlib


def secure_token():
    random_values = ''.join(["%.2x" % random.randint(0, 255) for _ in range(10)])
    return hashlib.sha256(random_values.encode('utf-8')).hexdigest()
