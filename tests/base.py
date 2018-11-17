import unittest
import os
import json
from pprint import pprint  # noqa

from sebak.transaction import Transaction


BASE_FEE = 10000
BASE_RESERVE = 1000000


class BaseTest(unittest.TestCase):
    files = None

    def setUp(self):
        self.files = os.path.join(os.path.dirname(os.path.abspath(__file__)), './files')

    def load_file(self, hsh):
        sig_data = None
        rlp_data = None

        fd = open(os.path.join(self.files, hsh + '.json'))
        strs = list()
        for i, f in enumerate(fd.readlines()):
            if i == 0:
                sig_data = list(map(int, f.split()))
                continue
            elif i == 1:
                rlp_data = list(map(int, f.split()))
                continue

            strs.append(f)

        fd.close()
        return sig_data, rlp_data, '\n'.join(strs)

    def load_json(self, hsh):
        sig_data, rlp_data, s = self.load_file(hsh)

        return sig_data, rlp_data, json.loads(s)

    def load_tx(self, hsh):
        sig_data, rlp_data, s = self.load_file(hsh)

        return sig_data, rlp_data, Transaction.from_json(s)
