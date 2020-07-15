import sys
import random
from datetime import datetime


def block_tv_automatic():
    if sys.argv:
        print(sys.argv)
        arg = float(sys.argv[0])
        return random.choices([True, False], [arg, arg - 1.0], k=1)[0]
