# sebakpy-util

`sebakpy-util` will introduce the basic usage of SEBAK for python.

## Installation

`sebakpy-util` requires,

* python3.6 o rlater.
* Windows environment was not tested yet.

```sh
$ python --version
Python 3.6.5

$ git clone https://github.com/spikeekips/sebakpy-util.git
$ python setup.py install
```

## Test

```sh
$ python -m unittest discover -v -s ./ -f
```


## Create new transaction

### Prerequisite
Before creating new transaction, you should check these,

* 'secret seed' of source account
* 'public address' of target account
* 'network id'

You can simply check 'network id' from SEBAK node information. If the address of your sebak node is 'https://testnet-sebak.blockchainos.org',
```sh
$ curl -v https://testnet-sebak.blockchainos.org
...
  "policy": {
    "network-id": "sebak-test-network",
    "initial-balance": "10000000000000000000",
    "base-reserve": "1000000",
...
```

The value of `"network-id"`, `sebak-test-network` is the 'network id'.

### Operation

For the nature of transaction of SEBAK, one `Transction` can have multple `Operation`s. `Operation` is the base unit of operating accounts like creating new account and payment. Currently SEBAK supports various kind of operations, but most of users will use `CreateAccount` and `Payment` operations.

```python
>>> from sebak.operation import create_account, payment

>>> target = 'GB3AOQD2M5AKMNWUP2HFCVQYFQNGTAFTJ24BHZ56ONSGGOXMG3EBO6OE'
>>> amount = '100'
>>> payment_operation = payment(target, amount)

>>> target = 'GD54SAKFHJ2QSBLEHZIQV3UWQ42OD6VQ6HKF6TN6F72US3AUQNDSONEV'
>>> amount = '1000000'
>>> create_account_operation = create_account(target, amount)
```

* `amount` must be `str`.
* the unit of `amount` must be `GON`, `1BOS` is `10000000GON`.
* `target` should be valid address of keypair.

At this time, you can up to `100` operations in one transaction. This number can be adjusted. This limit also can be checked by node information.

### Transaction

```python
>>> from sebak.transaction import Transaction

>>> operations = (payment_operation, create_account_operation)
>>> sequence_id = 1
>>> tx = Transaction(sequence_id, operations)
```

* `sequence_id` is the last state of account. It will be varied when your account state is changed, so you should check the latest `sequence_id` from network. You can get the laetst `sequence_id` from https://bosnet.github.io/sebak/api/#accounts-account-details-get .

#### Sending Transation

You must sign you transaction instance before sengding transaction.
```python
>>> from sebak import keypair

>>> source = 'SDJLIFJ3PMT22C2IZAR4PY2JKTGPTACPX2NMT5NPERC2SWRWUE4HWOEE'
>>> kp = keypair.from_seed(source)
>>> network_id = b'sebak-test-network'
>>> tx.sign(kp, network_id)
>>> tx.hash
'8PqQDCrvewu6JvGqHgyagESwjQ7zAeTKGJHeJmVi2X4n'
>>> tx.signature
'nU46BuF6f1PUUCoHoy3EXMxdibvRC6ZYyzLPsr4aNJYJnDDvSdcn52Qf9CGy5R9UbkMgW6mdKGwrHNvd3oCoRsp'
```

* `kp` must be generated from your `secret-seed`, not `public address'.
* `network_id` must be `bytes`.

If you successfully sign your transaction, you can serialize your transaction instance to 'json', or 'dict',

```python
>>> json_string = tx.to_json()
>>> print(json_string)
{
  "H": {
    "version": "1",
    "created": "2018-11-17 14:21:58-09.00",
    "signature": "nU46BuF6f1PUUCoHoy3EXMxdibvRC6ZYyzLPsr4aNJYJnDDvSdcn52Qf9CGy5R9UbkMgW6mdKGwrHNvd3oCoRsp"
  },
  "B": {
    "source": "GAG5EESGOZIHTKK5N2NBHX25EWRC3S3TWZT7RMCSBX65A3KTJKILQKCF",
    "fee": "20000",
    "sequence_id": 1,
    "operations": [
      {
        "H": {
          "type": "payment"
        },
        "B": {
          "amount": "100",
          "target": "GB3AOQD2M5AKMNWUP2HFCVQYFQNGTAFTJ24BHZ56ONSGGOXMG3EBO6OE"
        }
      },
      {
        "H": {
          "type": "create-account"
        },
        "B": {
          "amount": "1000000",
          "target": "GD54SAKFHJ2QSBLEHZIQV3UWQ42OD6VQ6HKF6TN6F72US3AUQNDSONEV",
          "linked": ""
        }
      }
    ]
  }
}
```

```python
>>> d = tx.to_dict()

from pprint import pprint
>>> pprint(d)
{ 'B': { 'fee': '20000',
         'operations': [ { 'B': { 'amount': '100',
                                  'target': 'GB3AOQD2M5AKMNWUP2HFCVQYFQNGTAFTJ24BHZ56ONSGGOXMG3EBO6OE'},
                           'H': {'type': 'payment'}},
                         { 'B': { 'amount': '1000000',
                                  'linked': '',
                                  'target': 'GD54SAKFHJ2QSBLEHZIQV3UWQ42OD6VQ6HKF6TN6F72US3AUQNDSONEV'},
                           'H': {'type': 'create-account'}}],
         'sequence_id': 1,
         'source': 'GAG5EESGOZIHTKK5N2NBHX25EWRC3S3TWZT7RMCSBX65A3KTJKILQKCF'},
  'H': { 'created': '2018-11-17 14:21:58-09.00',
         'signature': 'nU46BuF6f1PUUCoHoy3EXMxdibvRC6ZYyzLPsr4aNJYJnDDvSdcn52Qf9CGy5R9UbkMgW6mdKGwrHNvd3oCoRsp',
         'version': '1'}}
```

The API of sending transaction, please see https://bosnet.github.io/sebak/api/#trasactions-transactions-post .

## Operations

* In SEBAK, like other cryptocurrencies there is 'fee'. 'fee' is multiplied by the number of operations in one transaction.

### `CreateAccount`

* `target` address must new account, this means, it does not exist in the SEBAK network. You can check the account status thru account API of SEBAK. Please see https://bosnet.github.io/sebak/api/#accounts-account-details-get .
* `amount` for creating account must be bigger than base reserve, you can check the amount from SEBAK node information like 'network-id'

### `Payment`

* `target` address must exist in network.
