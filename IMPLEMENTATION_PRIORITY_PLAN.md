# Implementation Priority Plan

Source of truth: `LECTURE_ALIGNMENT_PLAN.md`.
Deadline: **17:00 on 2026-04-24** — under ~24 working hours remaining. Plan is calibrated for that reality.

---

## 1. Required fixes before submission

Non-negotiable. If any of these are skipped, the submission either fails a spec checkbox or contains a visible inconsistency.

1. **Fix the `data` field in `Transaction`** — spec §5.1 requires `data = amount + SHA-256(amount)`. Currently only the amount is stored. Add a `data_hash` field; include it in the signable payload and in `to_dict()`. Backed by Lecture 02. *(≈15 min)*
2. **Fill in Group 12 member names and IDs** — `PROJECT_README.md` has a blank "Members:" line. Required by both the README rubric and the report. *(≈5 min, needs the group)*
3. **Populate the report's "work distribution" table** — explicit course requirement. Cannot be skipped. *(group task)*
4. **Verify `test_phase1.py` and `test_phase2.py` still run cleanly after fix #1** — regenerate the expected-output block in the README so stdout matches what the grader will see. *(≈10 min)*
5. **Record external references** — `cryptography` library, any code or text borrowed from lectures/tutorials/Stack Overflow. Course explicitly penalises missing citations. *(≈15 min)*

---

## 2. Recommended bonus features if time allows

Ordered strictly by *(grading value) / (implementation cost)*. Stop at any line where time runs out — each item is independently valuable.

| # | Feature | Lecture backing | Est. time | Why it's worth doing |
|---|---|---|---|---|
| B1 | **Coinbase / block-reward transaction** on every mined block | Lec 05, 06 | 30 min | Visible in demo output, one short report paragraph, shows incentive understanding. |
| B2 | **`get_balance(address)` — walk the chain to compute balance** | Lec 06 | 30 min | Turns the chain from a log into a ledger. Pairs naturally with B1 for a believable demo. |
| B3 | **Dynamic difficulty adjustment** (every N blocks, based on average mining time) with a plotted graph | Lec 05, 07 | 60–90 min | Produces a real figure for the report; report section 5 ("Testing & Results") becomes substantive instead of a screenshot dump. |
| B4 | **Merkle proof generation + verification** (`generate_merkle_proof(tx)`, `verify_merkle_proof(...)`) | Lec 04 | 45 min | Demonstrates SPV understanding; one small function plus a demo print. |
| B5 | **Transaction nonce (replay-attack prevention)** on each account | Lec 06 | 20 min | One field, one check, one report sentence. |

**Recommendation:** attempt B1 + B2 + B3. Skip B4, B5 unless all other deliverables are already done. Do **not** start any bonus until §1 is complete and §3/§4 are drafted.

---

## 3. Report points to emphasize

The report is worth 20 % and the code is already "competent-but-thin." The report is where the grade is actually won.

- **Position MiniChain as "Bitcoin-style, simplified"** — permissionless, PoW, SISO, longest-chain rule. One labelled diagram comparing MiniChain vs. Bitcoin vs. Ethereum vs. Fabric along 4 axes (permission model, account model, consensus, programmability). Lectures 05–09.
- **Justify every design choice with a lecture citation** — ECC/ECDSA (Lec 02, 04), SHA-256 (Lec 02, 04), Hashcash PoW (Lec 05), Merkle tree (Lec 04), difficulty = 4 with probability 1/2^4 (Lec 05).
- **Tamper-detection narrative** — one figure with four attack vectors (tx amount, block header, previous-hash link, genesis) and the exact mechanism that catches each. Directly cites Lec 05's "modifying any transaction modifies the block header."
- **If B3 is implemented, include the mining-time graph** — X-axis difficulty 1…6, Y-axis seconds. This single graph lifts the report from "screenshots only" to "analysis."
- **Limitations / Future Work section** — explicitly list what was *deliberately* not built: no P2P networking (Lec 03), no smart contracts (Lec 08), no permissioned consensus (Lec 09), no state channels / DeFi (Lec 10). Frame these as *out-of-scope by design*, not missing features.
- **Work distribution table** — per member, per file/phase. Mandatory.

---

## 4. Explicit non-goals

Do NOT implement, discuss as if implemented, or imply in the README:

- Smart contracts, Solidity, EVM, bytecode, gas (Lec 08).
- Hyperledger Fabric, channels, MSP, endorsement policies, Kafka/SBFT (Lec 09).
- Lightning Network, payment channels, HTLC, DeFi, DIDs, IoT integration (Lec 10).
- P2P networking, node discovery, gossip protocol, mempool, orphan blocks.
- Full UTXO set (SISO is the deliberate simplification).
- Merkle Patricia Trie, state trie, receipts trie (Lec 07).
- Persistence to disk / database (not required; adding it also means adding testing for it).
- CLI, GUI, web frontend.
- Unit-test framework migration (pytest) — the printed demo scripts already satisfy the spec.

Each of these belongs in the report's "Future Work" paragraph, one sentence each, maximum.

---

## 5. Final recommended order of work

Sequential. Do not parallelise ahead of the list — each step depends on the previous.

1. **§1.1 code fix** (`data` field) → re-run both test scripts → regenerate expected-output in README. *(≈30 min)*
2. **§1.2–§1.5 admin fixes** — members, references, regenerated outputs. *(≈30 min, group)*
3. **Write the REQUIRED docs** in this order: `README.md` (from `PROJECT_README.md`), `docs/USAGE.md`, `docs/REPRODUCIBILITY.md`, `docs/CONTRIBUTORS.md`, `docs/COURSE_SPEC.md` (renamed `readme.md`). *(≈2 hr)*
4. **Draft the report skeleton** — section headings, figure placeholders, work-distribution table, lecture-citation placeholders per §3. Do this BEFORE writing any bonus code so the report drives which bonuses matter. *(≈1 hr)*
5. **Bonus B1 (coinbase) + B2 (balance query)** as a pair — they share a demo. *(≈1 hr combined)*
6. **Bonus B3 (difficulty adjustment + graph)** — only if steps 1–5 are complete and > 6 hr remains. *(≈1.5 hr)*
7. **Write the richer docs**: `docs/ARCHITECTURE.md`, `docs/DESIGN.md`, `docs/TESTING.md`. Each with lecture citations. *(≈2 hr)*
8. **Fill in the report body** using the drafted skeleton + the figures produced by B3 (if done). *(≈3–4 hr, group)*
9. **Record the 5-minute presentation video**. Only AFTER the report is frozen. *(≈1 hr shooting, 1 hr editing)*
10. **Final pass** — run both test scripts on a clean clone, verify the README install steps on a teammate's machine, zip and submit. Leave a 2-hour buffer before 17:00 on 2026-04-24. *(≈1 hr)*

**Hard stops:**
- If at T-minus-12 hr the report skeleton isn't done, abandon all remaining bonuses and flip to report + docs only.
- If at T-minus-6 hr the video isn't recorded, abandon all remaining writing and record it.
- Submit early. The Moodle cutoff does not forgive uploads at 16:59.
