# sebakpy-util

`sebakpy-util` will introduce the basic usage of SEBAK for python.

## Installation

`sebakpy-util` requires,

* python3.6 o rlater.
* Windows environment was not tested yet.

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
from sebak.operation import create_account, payment

target = 'GB3AOQD2M5AKMNWUP2HFCVQYFQNGTAFTJ24BHZ56ONSGGOXMG3EBO6OE'
amount = '100'
payment_operation = payment(target, amount)

target = 'GD54SAKFHJ2QSBLEHZIQV3UWQ42OD6VQ6HKF6TN6F72US3AUQNDSONEV'
amount = '1000000'
create_account_operation = create_account(target, amount)
```

* `amount` must be `str`.
* the unit of `amount` must be `GON`, `1BOS` is `10000000GON`.
* `target` should be valid address of keypair.

At this time, you can up to `100` operations in one transaction. This number can be adjusted. This limit also can be checked by node information.

### Transaction

```python
from sebak.transaction import Transaction

source = 'SDJLIFJ3PMT22C2IZAR4PY2JKTGPTACPX2NMT5NPERC2SWRWUE4HWOEE'
operations = (payment_operation, create_account_operation)
sequence_id = 1
tx = Transaction(sequence_id, operations)
```

* `sequence_id` is the last state of account. It will be varied when your account state is changed, so you should check the latest `sequence_id` from network. You can get the laetst `sequence_id` from https://bosnet.github.io/sebak/api/#accounts-account-details-get .

#### Sending Transation

You must sign you transaction instance before sengding transaction.
```python
network_id = b'sebak-test-network'
tx.sign(kp, network_id)
```

* `kp` must be generated from your `secret-seed`, not `public address'.
* `network_id` must be `bytes`.

The API of sending transaction, please see https://bosnet.github.io/sebak/api/#trasactions-transactions-post .

## Operations

* In SEBAK, like other cryptocurrencies there is 'fee'. 'fee' is multiplied by the number of operations in one transaction.

### `CreateAccount`

* `target` address must new account, this means, it does not exist in the SEBAK network. You can check the account status thru account API of SEBAK. Please see https://bosnet.github.io/sebak/api/#accounts-account-details-get .
* `amount` for creating account must be bigger than base reserve, you can check the amount from SEBAK node information like 'network-id'

### `Payment`

* `target` address must exist in network.
