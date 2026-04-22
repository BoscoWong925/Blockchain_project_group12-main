# Reproducibility

Written to satisfy §7 of the project spec ("Evaluation of Reproducibility Artifacts").

---

## 1. Artifact identification

- **Title:** MiniChain — Implementation of a Mini Blockchain
- **Course:** COMP4137 / COMP7200 (HKBU)
- **Group:** 12
- **Members:** see [CONTRIBUTORS.md](CONTRIBUTORS.md)
- **Abstract:** MiniChain is a self-contained Python implementation of a simplified Bitcoin-style blockchain. It covers account creation via Elliptic Curve Cryptography (SECP256K1), single-input-single-output (SISO) transactions signed with ECDSA, a SHA-256 Merkle tree, a linked chain of blocks secured by Hashcash-style Proof-of-Work (difficulty = 4), and a verifier that detects four classes of tampering. The artifact reproduces every experiment discussed in the report by running two scripts.

---

## 2. Dependencies and requirements

### Hardware
- Any modern x86-64 or ARM CPU
- ≥ 4 GB RAM
- No GPU, no network access required

### Operating system
- Any of: macOS 12+, Ubuntu 20.04+, Windows 10+
- Verified on Windows 11 (Python 3.11)

### Software
| Software | Version |
|---|---|
| Python | 3.9 or newer |
| `cryptography` | ≥ 42.0.0 (see `requirements.txt`) |

### Input data
- None. Accounts, key pairs, and transactions are generated at runtime.

---

## 3. Installation and deployment

Estimated total time: **< 2 minutes** on a clean machine with Python already installed.

```bash
# 1. (optional) isolated environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 2. install dependencies
pip install -r requirements.txt
```

---

## 4. Experiment workflow

Estimated total execution time: **10 – 60 s** (dominated by PoW mining at difficulty 4; wall-clock varies with CPU).

| # | Command | What it produces | Matches report section |
|---|---|---|---|
| 1 | `python test_phase1.py` | Account addresses, 4 signed transactions, tamper-detect output, Merkle root, tampered-vs-original root comparison | Phase I results (Tasks 1 & 2) |
| 2 | `python test_phase2.py` | Genesis + 3 mined blocks, clean-chain validation, 4 tamper scenarios each detected | Phase II results (Tasks 3, 4, 5) |

On Windows, prepend `PYTHONIOENCODING=utf-8` if the console rejects emoji output.

---

## 5. Experiment-to-result mapping

| Experiment | Script | Expected result |
|---|---|---|
| ECC account generation | `test_phase1.py` | 4 unique compressed-public-key hex addresses |
| SISO transaction creation | `test_phase1.py` | 4 transactions each with `tx_id`, `input`, `output`, `amount`, `amount_hash`, `signature` |
| ECDSA signature verification | `test_phase1.py` | All 4 signatures `VALID` |
| Signature tamper detection | `test_phase1.py` | Modified amount → signature `INVALID`; restored → `VALID` |
| Merkle root construction | `test_phase1.py` | Single 64-hex-char root; tampered tx → different root |
| Genesis block creation | `test_phase2.py` | Block index 0, hash starts with `0000` |
| PoW mining at difficulty 4 | `test_phase2.py` | Every block's hash starts with `0000` |
| Clean-chain validation | `test_phase2.py` | `is_chain_valid()` returns `True` |
| Tamper tx amount | `test_phase2.py` | Detected via invalid ECDSA signature |
| Tamper block header (`merkle_root`) | `test_phase2.py` | Detected via block hash mismatch |
| Break previous-hash link | `test_phase2.py` | Detected via broken chain link |
| Tamper Genesis block (`hash`) | `test_phase2.py` | Detected via downstream link mismatch |

All expected outputs are printed in human-readable form to stdout.

---

## 6. Determinism and run-to-run variance

- **Non-deterministic** across runs: account public keys, transaction IDs, Merkle roots, block timestamps, mining nonces, block hashes. These depend on freshly generated ECC keys and current time.
- **Deterministic** across runs: the *shapes* of all outputs, the pass/fail conclusions, the count of mined blocks, the four detected tamper scenarios.
- The Genesis block uses a fixed `timestamp = 0.0` so its structure (but not its hash across ECDSA-independent fields) is reproducible.

---

## 7. Known limitations (affecting reproducibility)

- Mining time at difficulty 4 has high variance (seconds to tens of seconds) because the nonce search is random.
- No persistence layer. Closing the Python process discards the chain. This is intentional: the demo scripts are self-contained.
- `PYTHONIOENCODING=utf-8` may be required on legacy Windows consoles.
