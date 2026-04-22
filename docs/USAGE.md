# Usage Guide

Detailed run instructions and the full expected stdout for both demo scripts.

---

## 1. Environment setup

| Step | Command | Notes |
|---|---|---|
| Clone / extract | — | Ensure the folder structure matches the layout in [README.md](../README.md). |
| (Optional) virtual env | `python -m venv venv` + activate | Keeps `cryptography` isolated. |
| Install deps | `pip install -r requirements.txt` | Installs `cryptography >= 42.0.0`. |

Python 3.9+ is required. Tested on Python 3.11.

---

## 2. Running the Phase I demo

```bash
python test_phase1.py
```

Covers the required tasks:
- Task 1 — account generation (ECC SECP256K1) and SISO transaction generation
- Task 2 — SHA-256 Merkle tree construction and tamper test

**What it does, step by step:**

1. Creates 4 accounts (Alice, Bob, Charlie, David).
2. Generates 4 signed SISO transactions between them.
3. Verifies each transaction's ECDSA signature.
4. Tampers with one transaction's amount and reverifies → signature should become invalid.
5. Restores the amount and reverifies → valid again.
6. Builds the Merkle tree from the 4 transaction IDs and prints the levels.
7. Tampers with one `tx_id` and rebuilds the tree → root differs from the original.

**Abridged expected output** (hash values differ per run because ECC keys are random):

```
######################################################################
#                    MINICHAIN - PHASE I TEST                        #
######################################################################

=== STEP 1: ACCOUNT GENERATION (ECC - SECP256K1) ===
  Account: Alice   Address (public key hex): 02a3f1...
  ...
  ✅ Successfully created 4 accounts.

=== STEP 2: TRANSACTION GENERATION (SISO) ===
  Transaction: Alice → Bob  |  Amount: 10.0
  TX ID:      4f3a1b...
  Signature:  30440220...
  ...
  ✅ Successfully created 4 transactions.

=== STEP 3: SIGNATURE VERIFICATION ===
  TX 4f3a1b...  Alice → Bob  |  Signature: ✅ VALID
  ...
  --- Tamper Test ---
  after tampering amount to 9999.0  |  Signature: ❌ INVALID (tamper detected!)
  after restoring original amount   |  Signature: ✅ VALID
  ✅ Tamper detection works correctly!

=== STEP 4: MERKLE TREE CONSTRUCTION ===
  Building Merkle Tree from 4 transactions...
  --- Root ---
    [0] 525ba6...
  --- Level 1 ---
    [0] d1648d...
    [1] 9a9269...
  --- Leaves (H(tx_id)) ---
    [0] 75fc30...
    [1] d11e2f...
    [2] e7ca5c...
    [3] daadcb...
  ✅ Merkle Root successfully computed.
  --- Merkle Root Integrity Test ---
  Original Merkle Root:  525ba6...
  Tampered Merkle Root:  8ca8e4...
  ✅ Merkle Roots differ — tampering is detectable!
```

Expected final line: `PHASE I - ALL TESTS COMPLETE ✅` with all five sub-tests `PASSED`.

---

## 3. Running the Phase II demo

```bash
python test_phase2.py
```

Covers the required tasks:
- Task 3 — block construction, Genesis block, chain linking
- Task 4 — Proof-of-Work mining with difficulty 4
- Task 5 — `is_chain_valid()` and four distinct tamper attacks

**What it does:**

1. Creates four accounts.
2. Builds a `Blockchain` with a mined Genesis block.
3. Mines three additional blocks (2, 4, and 2 transactions).
4. Prints the full chain.
5. Runs `is_chain_valid()` on the clean chain → must return `True`.
6. Simulates four tamper attacks and confirms each is detected:
   - **Tx amount tamper** on Block 1 → invalid ECDSA signature.
   - **Block header tamper** (overwrite `merkle_root`) on Block 2 → block hash mismatch.
   - **Previous-hash link tamper** on Block 2 → broken chain link.
   - **Genesis block tamper** (overwrite `hash`) → detected via downstream link check.
7. Each tamper is reverted and the chain is re-validated.

**Abridged expected output:**

```
######################################################################
#                    MINICHAIN - PHASE II TEST                       #
######################################################################

=== STEP 1: BLOCKCHAIN CONSTRUCTION ===
  ⛏️  Mining Genesis Block...  ✅ Hash: 0000xxxx...
  ⛏️  Mining Block 1 (difficulty=4)...  ✅ Nonce=XXXXX, Hash=0000xxxx...
  ⛏️  Mining Block 2 (difficulty=4)...  ✅ Nonce=XXXXX, Hash=0000xxxx...
  ⛏️  Mining Block 3 (difficulty=4)...  ✅ Nonce=XXXXX, Hash=0000xxxx...

=== STEP 2: INTEGRITY VERIFICATION — Clean Chain ===
  ✅ Blockchain is valid. All blocks and transactions are intact.

=== STEP 3: TAMPER TX AMOUNT  →  DETECTED (invalid signature)
=== STEP 4: TAMPER BLOCK HEADER →  DETECTED (block hash mismatch)
=== STEP 5: BREAK HASH LINK    →  DETECTED (broken link)
=== STEP 6: TAMPER GENESIS     →  DETECTED (broken link)
```

Expected final summary: all seven checks marked `PASSED` / `DETECTED ✅`.

---

## 4. Adversarial validator check (`test_adversarial.py`)

```bash
python test_adversarial.py
```

Runs five narrow scenarios that earlier validator drafts missed (and the current validator must reject):

- **A:** mutate a mined normal transaction's `tx_id` only → rejected (tx_id recomputation, Merkle mismatch).
- **B:** mutate a mined normal transaction's `amount_hash` only → rejected (amount_hash consistency).
- **C:** mutate a mined coinbase `amount` after mining → rejected (amount_hash + tx_id + Merkle mismatch).
- **D:** inject a second `CoinbaseTransaction` into a block → rejected (at-most-one-coinbase rule).
- **E:** move a coinbase out of position 0 → rejected (coinbase-position rule).

Each tampered state is restored after being rejected; the clean chain must re-validate before the next scenario runs.

---

## 5. (Optional) Bonus demo

```bash
python test_bonus.py
```

Demonstrates two optional features (backed by Lectures 05 & 06):

- **Coinbase transaction:** each mined block includes a coinbase tx that pays `BLOCK_REWARD = 6.25` coins to the miner's address. Coinbases have no ECDSA signature and are trusted by protocol.
- **`get_balance(address)`:** walks the entire chain and returns `received − sent` for an address. Coinbase txs only credit (never debit).

Final balances printed should match:

```
  Alice  : -11.00        (sent 10, sent 2, received 1)
  Bob    : +6.00         (received 10, sent 4)
  Charlie: +5.00         (received 4, received 2, sent 1)
  Miner  : +12.50        (2 coinbase rewards × 6.25)
```

All three integrity checks (chain still validates, coinbase credited, balances correct) must print `PASSED`.

---

## 6. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `UnicodeEncodeError: 'cp950' codec can't encode character '✅'` | Windows console defaulting to CP950. Run with `PYTHONIOENCODING=utf-8 python test_phase1.py`. |
| Mining hangs | Difficulty = 4 normally finishes in seconds. On very slow machines, reduce `DIFFICULTY` in [src/block.py](../src/block.py). |
| `ModuleNotFoundError: No module named 'src'` | Run from the project root, not from inside `src/`. |
| `ModuleNotFoundError: No module named 'cryptography'` | `pip install -r requirements.txt` was not run. |

---

## 7. What to screenshot for the report

For the report's *Testing & Results* section, capture:
1. Final summary block of `test_phase1.py` (step 4 "Merkle Roots differ").
2. Final summary block of `test_phase2.py` (all six steps).
3. One tamper-detection output (step 3 or 4 of `test_phase2.py`) showing the failure message.
