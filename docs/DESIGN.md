# Design Decisions

Each key choice is stated, then justified with a lecture citation. Supports report §3 ("Design & Implementation").

---

## 1. Cryptographic primitives

### 1.1 ECC on SECP256K1 for accounts and signatures
- **Decision:** every account is an ECC key pair generated on the SECP256K1 curve; addresses are the compressed-point hex encoding of the public key.
- **Why:** SECP256K1 is the curve used by Bitcoin (Lecture 04). ECC provides 256-bit security with much smaller keys than RSA, which Lecture 02 identifies as the primary benefit of ECC over RSA for signature systems. The curve is implemented by the well-audited `cryptography` library.
- **Trade-off:** we rely on a trusted library rather than implementing ECDSA by hand. The spec explicitly permits this (§5.1 footnote 1).

### 1.2 SHA-256 as the only hash function
- **Decision:** SHA-256 is used for `tx_id`, `amount_hash`, Merkle-tree leaves and interior nodes, and the block header hash.
- **Why:** Lecture 02 explains collision- and pre-image-resistance; Lecture 04 confirms SHA-256 (256-bit output) as the Bitcoin choice. Using one hash function everywhere keeps security analysis simple.

### 1.3 Signable payload includes `amount_hash`
- **Decision:** the signed message is `input ‖ output ‖ amount ‖ amount_hash`.
- **Why:** spec §5.1 mandates that the `data` field contains both the amount and the crypto-hash of the amount. Including both in the ECDSA input means a tamper on either field invalidates the signature.

---

## 2. Transaction model

### 2.1 SISO (Single-Input-Single-Output), not full UTXO
- **Decision:** each transaction transfers `amount` from one address to one address with no change outputs and no chained inputs.
- **Why:** spec §5.1 fixes SISO; Lecture 05 presents full UTXO as the alternative and Lecture 06 contrasts it with Ethereum's account model. SISO keeps the implementation pedagogically clear.
- **Known cost:** no balance invariant is enforced at mining time. `get_balance(address)` (if added as a bonus) would walk the chain to compute balances.

### 2.2 Transaction ID as JSON-of-contents SHA-256
- **Decision:** `tx_id = SHA-256(sort_keys JSON of {input, output, amount, amount_hash, signature})`.
- **Why:** spec §5.1 requires `tx_id` to be the hash of the transaction contents. Sorted JSON gives a deterministic, language-agnostic serialisation.

---

## 3. Merkle tree

### 3.1 Balanced binary tree, power-of-two leaves
- **Decision:** number of transactions per block is a power of two; leaves are `SHA-256(tx_id)`; parent = `SHA-256(left ‖ right)`.
- **Why:** spec §5.2 permits the power-of-two assumption "for simplicity"; Lecture 04 presents exactly this construction. Padding non-power-of-two inputs (duplicate last leaf) is a common extension but not required.

### 3.2 Root stored in block header
- **Decision:** `merkle_root` is a header field alongside `previous_hash`, `timestamp`, `nonce`.
- **Why:** Lectures 01, 04, 05 — this is the mechanism by which any tampered transaction invalidates the block hash.

---

## 4. Block and chain

### 4.1 Header fields
- **Decision:** header is `{index, previous_hash, timestamp, merkle_root, nonce}`, hashed as sorted JSON.
- **Why:** mirrors the Bitcoin 80-byte header described in Lecture 05 (version bytes omitted, since MiniChain has no protocol versioning).

### 4.2 Fixed-timestamp Genesis block
- **Decision:** the Genesis block is created with `timestamp = 0.0` and mined to satisfy the same difficulty target.
- **Why:** a fixed timestamp makes the Genesis block's structure reproducible across runs, which aids reproducibility claims (Lecture 01 flags the Genesis block as a distinguished case).

### 4.3 Chain linking via `previous_hash`
- **Decision:** every non-Genesis block stores the hash of its predecessor and verification walks the chain checking this link.
- **Why:** chain linking is the core immutability primitive (Lecture 01); combined with PoW it gives the "re-mining cost on every subsequent block" property Lecture 05 emphasises.

---

## 5. Proof-of-Work

### 5.1 Hashcash-style nonce search
- **Decision:** `Block.mine(difficulty)` iterates `nonce` from 0, recomputing the header hash each step, until the digest starts with `difficulty` leading hex zeros.
- **Why:** this is the Hashcash protocol formalised in Lecture 05. The expected number of attempts is `16^difficulty = 2^(4·difficulty)`; at difficulty 4 this is ~65 k hashes, finishing in under a second on any modern CPU.

### 5.2 Fixed difficulty = 4
- **Decision:** `DIFFICULTY = 4` hardcoded in `src/block.py`.
- **Why:** the spec's §5.4 example uses four leading zeros. Keeping difficulty fixed keeps the PoW demonstration within an acceptable wall-clock time for grading. Lecture 05 describes dynamic difficulty adjustment as an optional extension.

### 5.3 Longest-chain rule (implicit, single-chain)
- **Decision:** MiniChain maintains exactly one chain; no fork handling.
- **Why:** Lecture 05's longest-chain rule resolves forks; with a single process and no network, there is only ever one candidate chain. This is a deliberate simplification.

---

## 6. Integrity verification

### 6.1 Layered checks in `is_chain_valid()`
- **Decision:** for every non-Genesis block, apply six layers in order (see [TESTING.md §2](TESTING.md#2-what-the-validator-actually-checks)):
  1. Block-hash self-consistency and PoW target.
  2. `previous_hash` linkage to the predecessor block.
  3. Coinbase structural rules — at most one coinbase per block, and if present it must be at position 0, identified by `input_address == COINBASE_ADDRESS`.
  4. Per-transaction field consistency — `tx_id` recomputed from current contents, `amount_hash == SHA-256(str(amount))`, coinbase signature must be empty.
  5. ECDSA signature verification on non-coinbase transactions.
  6. Merkle root recomputed from current transactions must match `block.merkle_root`.
  A final Genesis self-consistency check closes the iteration.
- **Why:** earlier drafts trusted `tx_id` and `amount_hash` as once-set values and bypassed signature checks for coinbase by class type, which left several false negatives (e.g. mutating only `tx_id`, or mutating a coinbase `amount`). The layered check enforces the invariants directly instead of trusting frozen fields.

### 6.2 Tampering is cryptographically, not heuristically, detected
- **Decision:** detection relies on collision resistance of SHA-256 and unforgeability of ECDSA, combined with structural invariants on the coinbase position and count.
- **Why:** Lectures 02 and 04 establish SHA-256 and ECDSA as the security primitives; reusing them for validation is both minimal and sound. The coinbase rules are structural (not cryptographic) and come from Lecture 05's description of coinbase transactions as protocol-trusted, singleton, first-in-block.

### 6.3 Explicit non-goals of the validator
- **No economic policy.** The validator does not enforce `coinbase.amount == BLOCK_REWARD`, non-negative balances, or sum-of-inputs = sum-of-outputs. These would be trivial to add but are outside the project spec.
- **No replay prevention.** A valid transaction can be re-included; there is no per-account nonce.
- **No network-level defences.** Fork choice, double-spend across branches, 51 % attacks, and eclipse attacks are network phenomena that require a multi-node simulator; explicitly out of scope.
See [TESTING.md §7](TESTING.md#7-what-the-validator-does-not-check).

---

## 7. Optional extensions actually implemented

| Extension | Lecture that motivates it | Where it lives |
|---|---|---|
| **Coinbase / block-reward transaction (B1)** | 05, 06 | `CoinbaseTransaction` in [src/transaction.py](../src/transaction.py); optional `miner=` argument on `Blockchain.add_block()` in [src/blockchain.py](../src/blockchain.py); demo in [test_bonus.py](../test_bonus.py). Rewards default to `BLOCK_REWARD = 6.25`. |
| **`get_balance(address)` ledger walk (B2)** | 06 | `Blockchain.get_balance()` in [src/blockchain.py](../src/blockchain.py); demo in [test_bonus.py](../test_bonus.py). |

Both are backwards-compatible: Phase I and Phase II tests run unchanged and produce identical pass results.

---

## 8. Explicitly rejected extensions

Not implemented, deliberately:

| Feature | Lecture that introduces it | Reason for rejection |
|---|---|---|
| Smart contracts / EVM / Solidity | 06, 07, 08 | Out of spec scope. |
| Hyperledger Fabric-style permissioned consensus | 09 | Out of spec scope. |
| Lightning Network, HTLC, payment channels, DeFi, DIDs | 10 | Layer-2 and application-layer. |
| Merkle Patricia Trie | 07 | Simple balanced tree suffices for SISO transactions. |
| P2P networking, mempool, orphan-block handling | 03, 05 | Single-process demo is in scope. |
| Dynamic difficulty adjustment | 05, 07 | Insufficient time before the 2026-04-24 deadline; would produce a nice graph but is not required. |
| Full UTXO model with change outputs | 05 | Spec explicitly selects SISO. |
| Merkle proof / SPV verification | 04 | Not required; no light-client consumer in the demo. |
| Transaction nonce (replay prevention) | 06 | Not required; MiniChain has no mempool. |

Each of these is acknowledged in the report's *Future Work* section.
