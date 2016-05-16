import random
import hashlib


def secure_token():
    random_values = ''.join(["%.4x" % random.getrandbits(32) for _ in range(10)])
    return hashlib.sha256(random_values.encode('utf-8')).hexdigest()
