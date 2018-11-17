import hashlib
import json
import base58
import rlp
from pprint import pprint  # noqa
from rlp.sedes import (
    text,
    big_endian_int,
    List,
)

from ..constant import BASE_FEE
from ..common import iso8601now
from ..operation import Operation
from .. import keypair


class Transaction:
    source = None
    sequence_id = None
    ops = None
    fee = None
    signature = None

    def __init__(self, sequence_id, ops):
        self.sequence_id = sequence_id

        if ops is None:
            ops = list()
        else:
            for op in ops:
                assert isinstance(op, Operation)

        self.ops = ops

    @property
    def body(self):
        if self.fee is None:
            fee = str(BASE_FEE * len(self.ops))
        else:
            fee = self.fee

        return Body(
            Source=self.source,
            Fee=fee,
            SequenceID=self.sequence_id,
            Operations=self.ops,
        )

    @property
    def hash(self):
        encoded = rlp.encode(self.body)
        sha256ed = hashlib.sha256(hashlib.sha256(encoded).digest()).digest()
        return base58.b58encode(sha256ed).decode('utf-8')

    def get_signature(self, kp, network_id):
        assert isinstance(kp, keypair)
        assert isinstance(network_id, bytes)

        sig_data = network_id + self.hash.encode('utf-8')

        return base58.b58encode(kp.sign(sig_data)).decode('utf-8')

    def sign(self, kp, network_id):
        self.source = self.source
        self.signature = self.get_signature(kp, network_id)

        return

    def to_dict(self, strict=True):
        if strict:
            assert len(self.signature) > 0
            assert len(self.hash) > 0

        ops = list()
        for op in self.ops:
            ops.append(op.to_dict())

        if self.fee is None:
            fee = BASE_FEE * len(self.ops)
        else:
            fee = int(self.fee)

        return dict(
            H=dict(
                version="1",
                created=iso8601now(),
                signature=self.signature,
            ),
            B=dict(
                source=self.source,
                fee=str(fee),
                sequence_id=self.sequence_id,
                operations=ops,
            ),
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, b):
        return cls.from_dict(json.loads(b))

    @classmethod
    def from_dict(cls, o):
        tx = cls(o['B']['sequence_id'], list())
        tx.source = o['B']['source']
        tx.fee = o['B']['fee']
        tx.signature = o['H']['signature']

        for op in o['B']['operations']:
            tx.ops.append(Operation.from_dict(op))

        return tx


class Body(rlp.Serializable):
    fields = (
        ('Source', text),
        ('Fee', text),
        ('SequenceID', big_endian_int),
        ('Operations', List((Operation,), False)),
    )

    def serialize(self):
        cl = list()
        for i in self.as_dict()['Operations']:
            cl.append(i.__class__)

        class t(rlp.Serializable):
            fields = (
                ('Source', text),
                ('Fee', text),
                ('SequenceID', big_endian_int),
                ('Operations', List(tuple(cl), False)),
            )

        d = self.as_dict()
        tt = t(
            Source=d['Source'],
            Fee=d['Fee'],
            SequenceID=d['SequenceID'],
            Operations=d['Operations'],
        )

        return tt.serialize(tt)
