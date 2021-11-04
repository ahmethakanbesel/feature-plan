import time
import random

START_TIME = 19231453


def make_id():
    t = int(time.time() / 10) - START_TIME
    u = random.SystemRandom().getrandbits(2)
    _id = (t << 2) | u

    return _id


def reverse_id(_id):
    t = _id >> 8
    return t + START_TIME
