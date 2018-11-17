import json
from pprint import pprint  # noqa

from .base import BaseTest
from sebak import keypair
from sebak.transaction import Transaction
from sebak.operation import create_account, payment


class TestTransaction(BaseTest):
    def test_make_transaction(self):
        network_id = b'sebak-test-network'
        seed = 'SAC3GZZ53LSLXBLW5IQTJJE7NWSHXT2SMJCEWN5U3CFBITAYG2WIUOB2'
        kp = keypair.from_seed(seed)

        ops = list()

        kp0 = keypair.random()
        op = create_account(kp0.address().decode('utf-8'), "1000", '')
        ops.append(op)

        kp1 = keypair.random()
        op = payment(kp1.address().decode('utf-8'), "1000")
        ops.append(op)

        tx = Transaction(0, ops)
        tx.source = kp.address().decode('utf-8')

        self.assertTrue(len(tx.hash) > 0)
        sig = tx.get_signature(kp, network_id)
        self.assertTrue(len(sig) > 0)

        tx.sign(kp, network_id)

        d = tx.to_dict()
        self.assertTrue(isinstance(d, dict))
        self.assertTrue(json.dumps(d) is not None)
        self.assertTrue(json.loads(json.dumps(d)) is not None)

    def test_from_json(self):
        network_id = b'sebak-test-network'
        seed = 'SAC3GZZ53LSLXBLW5IQTJJE7NWSHXT2SMJCEWN5U3CFBITAYG2WIUOB2'
        kp = keypair.from_seed(seed)

        ops = list()

        kp0 = keypair.random()
        op = create_account(kp0.address().decode('utf-8'), "1000", '')
        ops.append(op)

        kp1 = keypair.random()
        op = payment(kp1.address().decode('utf-8'), "1000")
        ops.append(op)

        tx = Transaction(0, ops)
        tx.source = kp.address().decode('utf-8')

        self.assertTrue(len(tx.hash) > 0)
        sig = tx.get_signature(kp, network_id)
        self.assertTrue(len(sig) > 0)

        tx.sign(kp, network_id)

        j = json.dumps(tx.to_dict())

        parsed_tx = Transaction.from_json(j)
        self.assertEqual(tx.hash, parsed_tx.hash)
        self.assertEqual(tx.get_signature(kp, network_id), parsed_tx.get_signature(kp, network_id))

    def test_signature_match(self):
        network_id = b'sebak-test-network'
        seed = 'SAC3GZZ53LSLXBLW5IQTJJE7NWSHXT2SMJCEWN5U3CFBITAYG2WIUOB2'
        expected_hash = '7VXGcCbVWKraoYTVN86dqGX1peKNsXkeV5BCcHxPGnxg'

        expected_sig_data, _, tx = self.load_tx(expected_hash)

        self.assertEqual(expected_hash, tx.hash)

        kp = keypair.from_seed(seed)
        self.assertEqual(tx.signature, tx.get_signature(kp, network_id))
