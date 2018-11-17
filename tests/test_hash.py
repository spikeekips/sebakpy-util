import hashlib
import base58
import rlp
from pprint import pprint  # noqa

from .base import BaseTest
from sebak import keypair
from sebak.transaction import Transaction
from sebak.operation import create_account, payment


BASE_FEE = 10000
BASE_RESERVE = 1000000


class TestRLPHash(BaseTest):
    def make_transaction(self, source, sequence_id, ops):
        sops = list()
        for i in ops:
            t, target, amount = i

            op = None
            if t == 'create-account':
                op = create_account(target, amount, '')
            elif t == 'payment':
                op = payment(target, amount)

            if op is None:
                raise 'unknown operation type found: %s' % t

            sops.append(op)

        tx = Transaction(
            sequence_id,
            sops,
        )
        tx.source = source

        return tx

    def test_rlp_encoded_match(self):
        expected_hash = '7VXGcCbVWKraoYTVN86dqGX1peKNsXkeV5BCcHxPGnxg'

        _, expected_rlp_data, tx = self.load_tx(expected_hash)

        encoded = rlp.encode(tx.body)
        self.assertEqual(expected_rlp_data, list(encoded))

        sha256ed = hashlib.sha256(hashlib.sha256(encoded).digest()).digest()

        hsh = base58.b58encode(sha256ed).decode('utf-8')
        self.assertEqual(expected_hash, hsh)

        return

    def test_signature_match(self):
        network_id = b'sebak-test-network'
        seed = 'SAC3GZZ53LSLXBLW5IQTJJE7NWSHXT2SMJCEWN5U3CFBITAYG2WIUOB2'
        expected_hash = '7VXGcCbVWKraoYTVN86dqGX1peKNsXkeV5BCcHxPGnxg'

        expected_sig_data, _, o = self.load_json(expected_hash)

        ops = list()
        for op in o['B']['operations']:
            ops.append((op['H']['type'], op['B']['target'], op['B']['amount']))

        tx = self.make_transaction(
            o['B']['source'],
            o['B']['sequence_id'],
            ops,
        )
        tx.fee = o['B']['fee']

        encoded = rlp.encode(tx.body)
        sha256ed = hashlib.sha256(hashlib.sha256(encoded).digest()).digest()
        hsh = base58.b58encode(sha256ed)

        sig_data = network_id + hsh
        self.assertEqual(expected_sig_data, list(sig_data))

        kp = keypair.from_seed(seed)
        sig = kp.sign(sig_data)

        self.assertEqual(o['H']['signature'], base58.b58encode(sig).decode('utf-8'))
        self.assertEqual(kp.verify(network_id + hsh, sig), None)

        return
