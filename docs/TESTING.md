# Testing & Tamper Detection

Supports report §4 ("Testing & Results"). Inventories every test script and documents the exact classes of tamper the current validator catches — and the classes it does not.

---

## 1. Test inventory

| Script | Covers | What it demonstrates |
|---|---|---|
| [test_phase1.py](../test_phase1.py) | Tasks 1 & 2 | Account creation; signed SISO transactions; signature-verification tamper test; Merkle tree construction; Merkle-root tamper test |
| [test_phase2.py](../test_phase2.py) | Tasks 3, 4, 5 | Chain construction with Genesis + 3 mined blocks; PoW at difficulty 4; clean-chain validation; four independent tamper scenarios |
| [test_bonus.py](../test_bonus.py) | Bonuses B1, B2 | Coinbase transaction, `get_balance()` walk, chain still validates with coinbase present |
| [test_adversarial.py](../test_adversarial.py) | Validator soundness | Five mutation scenarios that earlier versions of `is_chain_valid()` missed; each must now be rejected |

Every script is self-contained, prints every result, and uses `assert` to fail loudly on regressions. No external test framework is required.

---

## 2. What the validator actually checks

`Blockchain.is_chain_valid()` applies six layers, in order, to every non-Genesis block (plus a Genesis self-consistency check):

| # | Layer | Mechanism |
|---|---|---|
| 1 | **Block-hash self-consistency + PoW** | Recomputes the block hash from header fields (`index, previous_hash, timestamp, merkle_root, nonce`) and compares it to `block.hash`; also checks the leading-zero target. |
| 2 | **Previous-hash linkage** | `block.previous_hash == chain[block.index - 1].hash`. |
| 3 | **Coinbase structural rules** | At most one transaction whose `input_address == COINBASE_ADDRESS`; if present, it must be at position 0. |
| 4 | **Per-transaction field consistency** | For every tx: `amount_hash == SHA-256(str(amount))`; `tx_id` recomputed from current contents equals the stored `tx_id`. |
| 5 | **Signature verification** | Non-coinbase transactions must pass ECDSA verify; coinbase-like transactions must carry an empty signature. |
| 6 | **Merkle-root recomputation** | For non-empty blocks, rebuild the tree from current transactions and compare the root to `block.merkle_root`. |

Finally, the Genesis block's stored hash must equal its freshly recomputed hash.

---

## 3. Phase I tamper tests (`test_phase1.py`)

### 3.1 Transaction amount tamper (signature invalidation)
- **Attack:** overwrite `transaction.amount` with a different value after signing.
- **Detection:** `verify_signature()` reserialises `input ‖ output ‖ amount ‖ amount_hash` from current attribute values and runs ECDSA verify. The original signature was produced over the original bytes, so the tampered payload fails verification.
- **Security primitive:** ECDSA unforgeability (Lectures 02, 04).

### 3.2 Merkle root tamper (tree-rebuild mismatch)
- **Attack:** change one `tx_id` and rebuild the Merkle tree.
- **Detection:** the rebuilt root differs because SHA-256 is collision-resistant — any leaf change propagates to the root.
- **Security primitive:** SHA-256 collision resistance (Lecture 02).

---

## 4. Phase II tamper tests (`test_phase2.py`)

All four attacks target `is_chain_valid()` at difficulty 4. Each attack is followed by a restore + re-validate pair, demonstrating the check is specific, not blanket.

| # | Attack | Caught by layer |
|---|---|---|
| A | `chain[1].transactions[0].amount` → `9999.0` | 5 (ECDSA verify fails; also 4, 6) |
| B | `chain[2].merkle_root` → `0…0` | 1 (block-hash recomputation diverges) |
| C | `chain[2].previous_hash` → `0…0` | 2 (linkage) |
| D | `chain[0].hash` → `0…0` (Genesis) | 2 (downstream linkage); Genesis self-check is the second layer |

---

## 5. Bonus-path tests (`test_bonus.py`)

- **Clean chain with coinbase:** mined blocks may carry one coinbase at position 0; `is_chain_valid()` returns `True`.
- **Balance arithmetic:** `get_balance(addr)` matches hand-computed totals for all four accounts.

---

## 6. Adversarial regression tests (`test_adversarial.py`)

These scenarios exposed false negatives in earlier validator drafts. Each one must now be rejected.

| # | Attack | Caught by layer |
|---|---|---|
| A | Mutate `tx_id` only on a mined normal transaction | 4 (tx_id recomputation); 6 (Merkle mismatch) |
| B | Mutate `amount_hash` only on a mined normal transaction | 4 (amount_hash consistency) |
| C | Mutate coinbase `amount` after mining (coinbase has no signature) | 4 (amount_hash no longer matches; tx_id no longer matches); 6 (Merkle mismatch) |
| D | Inject a second `CoinbaseTransaction` into a mined block | 3 (at-most-one-coinbase rule) |
| E | Move the coinbase out of position 0 | 3 (coinbase-position rule) |

All five scenarios are asserted to fail validation in the script; a regression fails the script loudly.

---

## 7. What the validator does NOT check

Out of scope by design — see [DESIGN.md §8](DESIGN.md#8-explicitly-rejected-extensions):

- **Network-level attacks** — double-spend via fork, 51 % attack, eclipse. MiniChain runs in a single process with no networking.
- **Replay of valid transactions** — no per-account nonce in the required spec; a correctly signed transaction can be re-included.
- **Reward-value policy** — the validator accepts any coinbase `amount` as long as it is internally consistent with its `amount_hash`, `tx_id`, and the Merkle root. Enforcing `amount == BLOCK_REWARD` (or a halving schedule) was intentionally not added; the spec does not require an incentive policy.
- **Economic invariants** — no non-negative-balance check, no sum-of-inputs vs sum-of-outputs invariant (SISO model does not use change outputs).
- **Persistence corruption** — no on-disk state.
- **Concurrent mining / race conditions** — single-process execution.

These are all acknowledged as Future Work in the report.

---

## 8. Reproducing test output

```bash
PYTHONIOENCODING=utf-8 python test_phase1.py
PYTHONIOENCODING=utf-8 python test_phase2.py
PYTHONIOENCODING=utf-8 python test_bonus.py
PYTHONIOENCODING=utf-8 python test_adversarial.py
```

Hash values vary per run (ECC keys and timestamps are fresh each execution); the pass/fail conclusions do not.
