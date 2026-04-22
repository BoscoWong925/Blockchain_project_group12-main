# MiniChain — Implementation of a Mini Blockchain

**Course:** COMP4137 / COMP7200  
**Group No:** 12  
**Members:**


## Abstract

MiniChain is a simplified, functional blockchain system implemented in Python.  
It covers all four required components:

1. **Account & Transaction Generation** — ECC (SECP256K1) key pairs for accounts; SISO transactions with unique TX ID, data field (amount + SHA-256 hash of amount), input/output addresses, and ECDSA digital signature.
2. **Verifiable Merkle Tree** — SHA-256 bottom-up Merkle Tree over a power-of-2 set of transactions, producing a single Merkle Root.
3. **Blockchain Construction** — Linked blocks each containing a header (previous hash, timestamp, nonce, Merkle root) and a list of confirmed transactions. A Genesis Block function creates the first block.
4. **Proof-of-Work Mining & Integrity Verification** — PoW mining loop (difficulty = 4 leading zeros); `is_chain_valid()` checks every block's hash, hash-link, and transaction signatures; tamper detection tests confirm that any modification is caught immediately.

---

## Project Structure

```
blockchain/
├── src/
│   ├── __init__.py        # Package initialiser
│   ├── account.py         # ECC account (key pair) generation
│   ├── transaction.py     # SISO transaction creation & signing
│   ├── merkle_tree.py     # Merkle Tree construction & display
│   ├── block.py           # Block structure, Genesis block, PoW mining
│   └── blockchain.py      # Blockchain class & is_chain_valid()
├── test_phase1.py         # Phase I test: accounts, transactions, Merkle Tree
├── test_phase2.py         # Phase II test: blockchain, mining, integrity
├── requirements.txt       # Python dependencies
└── PROJECT_README.md      # This file
```

---

## Artifact Dependencies and Requirements

### Hardware
- Any modern CPU (no GPU required)
- Minimum 4 GB RAM

### Operating System
- macOS 12+, Ubuntu 20.04+, or Windows 10+

### Software / Libraries
- Python **3.9** or higher
- `cryptography >= 42.0.0`

### Input Data
- No external dataset required. All accounts and transactions are generated
  programmatically at runtime by the test scripts.

---

## Installation and Deployment

### Step 1 — Clone the repository
```bash
git clone https://github.com/ks-120/Blockchain_project_group12.git
cd Blockchain_project_group12
```
*Estimated time: < 30 seconds*

### Step 2 — (Optional) Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```
*Estimated time: < 1 minute*

---

## Execution Guide

### Run Phase I Test (Accounts, Transactions, Merkle Tree)
```bash
python3 test_phase1.py
```

### Run Phase II Test (Blockchain, Mining, Integrity Verification)
```bash
python3 test_phase2.py
```

*Estimated total execution time: 10–60 seconds (dominated by PoW mining at difficulty = 4)*

---

## Expected Output

### Phase I (`test_phase1.py`)
```
STEP 1: ACCOUNT GENERATION
  Account: Alice  Address (public key hex): 02a3f...
  ✅ Successfully created 4 accounts.

STEP 2: TRANSACTION GENERATION
  Transaction: Alice → Bob  |  Amount: 10.0
  TX ID:      4f3a1b...
  ✅ Successfully created 4 transactions.

STEP 3: SIGNATURE VERIFICATION
  TX 4f3a1b...  Alice → Bob  |  Signature: ✅ VALID
  ✅ All transaction signatures verified successfully.
  --- Tamper Test ---
  after tampering amount to 9999.0  |  Signature: ❌ INVALID (tamper detected!)
  ✅ Tamper detection works correctly!

STEP 4: MERKLE TREE CONSTRUCTION
  Merkle Root: 8d3f2a...
  ✅ Merkle Root successfully computed.
  ✅ Merkle Roots differ — tampering is detectable!
```

### Phase II (`test_phase2.py`)
```
STEP 1: BLOCKCHAIN CONSTRUCTION
  ⛏️  Mining Genesis Block...  ✅ Hash: 0000xxxx...
  ⛏️  Mining Block 1...        ✅ Nonce=XXXXX, Hash: 0000xxxx...
  ⛏️  Mining Block 2...        ✅ Nonce=XXXXX, Hash: 0000xxxx...
  ⛏️  Mining Block 3...        ✅ Nonce=XXXXX, Hash: 0000xxxx...

STEP 2: CLEAN CHAIN VERIFICATION
  ✅ Blockchain is valid. All blocks and transactions are intact.

STEP 3–6: TAMPER DETECTION
  ✅ Modified transaction amount  — detected (invalid ECDSA signature)
  ✅ Modified block header field  — detected (hash mismatch)
  ✅ Broken previous_hash link    — detected (broken chain link)
  ✅ Modified Genesis Block       — detected (hash recomputation)
```

---

## Reproducibility of Experiments

| Experiment | Script | Expected Result |
|---|---|---|
| Account generation | `test_phase1.py` | 4 unique ECC public key addresses |
| SISO transaction creation | `test_phase1.py` | 4 transactions with TX ID, data, input, output, signature |
| Signature verification | `test_phase1.py` | All valid; tampered amount → invalid |
| Merkle Tree root | `test_phase1.py` | Single SHA-256 root hash; changes if any TX is modified |
| Genesis Block creation | `test_phase2.py` | Block 0, hash starts with `0000` |
| PoW mining (difficulty=4) | `test_phase2.py` | All block hashes start with `0000` |
| Clean chain integrity check | `test_phase2.py` | `is_chain_valid()` returns `True` |
| Tamper TX amount | `test_phase2.py` | Detected via invalid ECDSA signature |
| Tamper block header | `test_phase2.py` | Detected via hash/PoW mismatch |
| Tamper previous_hash link | `test_phase2.py` | Detected via broken hash link |
| Tamper Genesis Block | `test_phase2.py` | Detected via hash recomputation |

All results are printed to stdout in a clearly labelled, human-readable format.
