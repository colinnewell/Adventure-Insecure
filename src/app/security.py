import random
import hashlib
import logging


def secure_token():
    random_values = ''.join(["%.4x" % random.getrandbits(32) for _ in range(10)])
    logger = logging.getLogger('securetoken')
    logger.warning('Secure token generated: %s', random_values)

    return hashlib.sha256(random_values.encode('utf-8')).hexdigest()
