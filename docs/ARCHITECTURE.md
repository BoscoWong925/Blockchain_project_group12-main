# Architecture

One-page structural view of MiniChain. Supports report §2 ("System Architecture").

---

## 1. Component map

```
                        ┌──────────────────────────────┐
                        │         Blockchain           │
                        │    src/blockchain.py         │
                        │                              │
                        │  • chain: List[Block]        │
                        │  • add_block(txs)            │
                        │  • is_chain_valid()          │
                        └──────────────┬───────────────┘
                                       │ contains
                                       ▼
                        ┌──────────────────────────────┐
                        │            Block             │
                        │        src/block.py          │
                        │                              │
                        │  header: previous_hash,      │
                        │          timestamp,          │
                        │          merkle_root,        │
                        │          nonce               │
                        │  body  : List[Transaction]   │
                        │  mine(difficulty)            │
                        │  compute_hash()              │
                        └─────┬──────────────────┬─────┘
                              │                  │
                    builds    │                  │ contains
                              ▼                  ▼
                ┌──────────────────┐    ┌──────────────────┐
                │   Merkle Tree    │    │   Transaction    │
                │ src/merkle_tree  │    │ src/transaction  │
                │                  │    │                  │
                │ sha256 bottom-up │    │ tx_id, input,    │
                │ → root 256 bits  │    │ output, amount,  │
                └────────┬─────────┘    │ amount_hash,     │
                         │              │ signature        │
                         │ hashes of    └─────────┬────────┘
                         │ tx_ids                 │ signed by
                         │                        ▼
                         │              ┌──────────────────┐
                         │              │     Account      │
                         │              │  src/account.py  │
                         │              │                  │
                         │              │ ECC SECP256K1    │
                         │              │ private_key, pk  │
                         │              └──────────────────┘
                         ▼
                  (merkle_root stored in Block header)
```

---

## 2. Module responsibility table

| Module | Responsibility | Key symbols |
|---|---|---|
| [src/account.py](../src/account.py) | ECC key-pair creation; address = compressed public key hex | `Account(name)`, `get_address()` |
| [src/transaction.py](../src/transaction.py) | SISO transaction build + ECDSA signing + `tx_id` computation | `Transaction(sender, receiver, amount)`, `verify_signature()` |
| [src/merkle_tree.py](../src/merkle_tree.py) | Bottom-up SHA-256 Merkle tree over transaction IDs | `build_merkle_tree(txs)` → `{root, levels}` |
| [src/block.py](../src/block.py) | Block header + body + PoW mining + Genesis block factory | `Block`, `Block.mine()`, `create_genesis_block()`, `DIFFICULTY = 4` |
| [src/blockchain.py](../src/blockchain.py) | Chain container + tamper-detection logic | `Blockchain`, `add_block(txs)`, `is_chain_valid()` |

---

## 3. End-to-end data flow

**A. Creating a signed transaction**
1. Sender's `Account` holds an ECC private key.
2. `Transaction.__init__` gathers `(input_address, output_address, amount)`, computes `amount_hash = SHA-256(amount)` (spec §5.1), signs `input ‖ output ‖ amount ‖ amount_hash` with the sender's private key, then computes `tx_id = SHA-256(JSON contents)`.

**B. Mining a block**
1. `Blockchain.add_block(txs)` creates a `Block` with `previous_hash = last_block.hash`.
2. The block builds a Merkle tree from its transaction list; the root is written into the header.
3. `Block.mine(difficulty)` iterates `nonce` from 0, recomputing the SHA-256 of the header dict until the hex digest starts with `difficulty` zeros (Hashcash rule, Lecture 05).
4. The mined block is appended to `chain`.

**C. Validating the chain (`is_chain_valid`)**
For each block from last to first:
1. Recompute the block hash and confirm it matches the stored hash **and** satisfies the PoW target.
2. Confirm `previous_hash` equals the predecessor block's stored hash.
3. Verify every transaction's ECDSA signature.
Finally, confirm the Genesis block's stored hash still equals its recomputed hash.

The six validation layers together are: (1) per-transaction `tx_id` recomputation, (2) per-transaction `amount_hash` consistency, (3) ECDSA signature verification on non-coinbase transactions, (4) Merkle root recomputation from the current transactions, (5) block header hash + PoW target, (6) `previous_hash` linkage, plus a Genesis self-consistency check. A single mutation to any field covered by these layers is detected; see [TESTING.md](TESTING.md) for the catch-matrix and the attack classes that are explicitly out of scope.

---

## 4. Placement in the blockchain design space

MiniChain is deliberately a *Bitcoin-style simplification*:

| Axis | MiniChain | Bitcoin | Ethereum | Hyperledger Fabric |
|---|---|---|---|---|
| Permission model | permissionless | permissionless | permissionless | permissioned |
| Transaction model | SISO (UTXO-like) | UTXO | account-based | account-based |
| Consensus | PoW (fixed diff = 4) | PoW (dynamic) | PoS (2022+) | endorsement + ordering |
| Programmability | none (fixed tx format) | limited Script | Turing-complete (EVM) | chaincode |
| Networking | single process | global P2P | global P2P | consortium P2P |

Positioning rationale: matches Lectures 05–09, keeps the implementation within the scope defined by the project spec.
