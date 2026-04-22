# MiniChain

**Course:** COMP4137 / COMP7200 — Programming Project
**Group No.:** 12
**Members:** `TODO:` names and student IDs — see [docs/CONTRIBUTORS.md](docs/CONTRIBUTORS.md)

A simplified Bitcoin-style blockchain written in Python. Implements all five required tasks of the project spec: ECC accounts, SISO transactions with ECDSA signatures, a verifiable Merkle tree, a linked block chain with a Genesis block, Proof-of-Work mining (difficulty = 4), and integrity verification with tamper detection.

---

## Quick start

```bash
# 1. (optional) virtual env
python -m venv venv
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 2. dependencies
pip install -r requirements.txt

# 3. run the two demo / test scripts
python test_phase1.py   # Phase I: accounts, transactions, Merkle tree
python test_phase2.py   # Phase II: chain, PoW mining, tamper detection
python test_bonus.py    # (optional) coinbase reward + get_balance()
```

> **Windows note:** if the console fails on emoji output (`UnicodeEncodeError: cp950`), run with `PYTHONIOENCODING=utf-8 python test_phase1.py`.

Estimated runtime: **10 – 60 s**, dominated by PoW mining at difficulty 4.

---

## Project layout

```
.
├── README.md                       ← this file
├── requirements.txt
├── src/
│   ├── account.py                  ECC (SECP256K1) key-pair accounts
│   ├── transaction.py              SISO transaction + ECDSA signature
│   ├── merkle_tree.py              SHA-256 bottom-up Merkle tree
│   ├── block.py                    Block structure + PoW mining + Genesis
│   └── blockchain.py               Chain class + is_chain_valid()
├── test_phase1.py                  Phase I demo (Tasks 1 & 2)
├── test_phase2.py                  Phase II demo (Tasks 3, 4, 5)
├── test_bonus.py                   Bonus demo (coinbase + get_balance)
└── docs/
    ├── USAGE.md                    detailed run guide + expected output
    ├── REPRODUCIBILITY.md          hardware / software / experiment matrix
    ├── ARCHITECTURE.md             component map + data flow
    ├── DESIGN.md                   algorithm choices + lecture citations
    ├── TESTING.md                  test inventory + tamper-detection notes
    ├── CONTRIBUTORS.md             group members + work distribution
    └── COURSE_SPEC.md              instructor's original assignment brief
```

Planning artefacts used to build this project live in [`PLAN/`](PLAN/) and are kept for transparency; they are not part of the deliverable.

---

## Requirements

- Python **3.9** or higher
- `cryptography >= 42.0.0` (installed via `requirements.txt`)
- No external dataset — accounts and transactions are generated at runtime by the test scripts.

---

## Reading order

| If you are… | Start with |
|---|---|
| A grader checking reproducibility | [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) |
| A grader running the demos | [docs/USAGE.md](docs/USAGE.md) |
| A reader of the report / video | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) then [docs/DESIGN.md](docs/DESIGN.md) |
| A reader verifying integrity claims | [docs/TESTING.md](docs/TESTING.md) |
| Looking for the assignment brief | [docs/COURSE_SPEC.md](docs/COURSE_SPEC.md) |

---

## License / academic integrity

This code is an academic submission for COMP4137 / COMP7200 at HKBU. External libraries and borrowed material are listed in [docs/CONTRIBUTORS.md](docs/CONTRIBUTORS.md#references).
