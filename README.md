# MiniChain

This branch is the hand-in version of our blockchain project for COMP4137 / COMP7200.
It keeps only the source code and a short README.

The project implements the main parts of a simple Bitcoin-style blockchain:

- ECC accounts based on SECP256K1
- signed single-input single-output transactions
- a Merkle tree built from transaction IDs
- blocks linked by hashes
- proof-of-work mining
- chain validation and tamper checks

## Files in this branch

```
README.md
src/
    account.py
    transaction.py
    merkle_tree.py
    block.py
    blockchain.py
```

## Running the code

Use Python 3.9 or above.
Install the `cryptography` package before running the project:

```bash
pip install cryptography
```

The code is organized as reusable classes in `src/`.
The hand-in branch does not include the larger development notes or helper test files.

## Notes

The mining difficulty is set in the code.
At higher difficulty values, creating blocks will take longer because proof-of-work is done by repeated hashing.
