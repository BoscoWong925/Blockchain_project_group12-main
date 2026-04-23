# MiniChain

MiniChain is a simplified Bitcoin-style blockchain project written in Python for COMP4137 / COMP7200.

The project implements the main parts of a simple Bitcoin-style blockchain:

- ECC accounts based on SECP256K1
- signed single-input single-output transactions
- a Merkle tree built from transaction IDs
- blocks linked by hashes
- proof-of-work mining
- chain validation and tamper checks

## Project files

```
README.md
requirements.txt
src/
    account.py
    transaction.py
    merkle_tree.py
    block.py
    blockchain.py
test_phase1.py
test_phase2.py
test_bonus.py
test_adversarial.py
```

## Getting started

Use Python 3.9 or above.

Create a virtual environment if you want to keep the dependencies isolated:

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Install the dependency:

```bash
pip install -r requirements.txt
```

## Running the tests

The project includes four test scripts:

- `test_phase1.py` for accounts, transactions, signatures, and the Merkle tree
- `test_phase2.py` for blockchain construction, proof-of-work, and chain validation
- `test_bonus.py` for coinbase reward and balance checking
- `test_adversarial.py` for extra tampering checks

Run them from the project root:

```bash
python test_phase1.py
python test_phase2.py
python test_bonus.py
python test_adversarial.py
```

## Notes

The mining difficulty is set in the code.
At higher difficulty values, creating blocks will take longer because proof-of-work is done by repeated hashing.
