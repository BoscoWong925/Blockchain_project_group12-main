# Lecture → Project Alignment Plan

Purpose: Before writing any new code or docs, map the 10 course lectures onto the 5 project requirements so that the final submission uses course vocabulary, shows the group understood the material, and justifies each design choice with a citation back to a lecture. This is a planning document — no code or docs are written yet.

---

## 0. How to read this document

For each lecture we answer four questions:

1. **What does the lecture cover?** (one line)
2. **Which ideas are directly relevant to the 5 required tasks?**
3. **Which ideas are partially relevant — good as bonus features, discussion material, or report framing?**
4. **Which ideas are irrelevant — acknowledged as background only, must not leak into code or scope?**

Then a synthesis section rolls everything up into (a) per-task influence on the code, (b) a bonus-feature priority list, and (c) vocabulary conventions.

**Key:** 🟢 directly relevant • 🟡 partially relevant • 🔴 irrelevant / out of scope

---

## 1. Per-lecture mapping

### Lecture 01 — Introduction to Blockchain
*Distributed-ledger overview; history, structure, consensus families, applications.*

🟢 **Directly relevant**
- **Block structure with previous-hash chaining** → Task 3. Confirms header fields `previous_hash`, `timestamp`, `nonce`, `merkle_root`.
- **Genesis block concept** → Task 3. The current `create_genesis_block()` matches this.
- **Immutability through hash chaining** → Task 5. Directly justifies `is_chain_valid()`.
- **Consensus families (PoW / PoS / PoET / PoA)** → Task 4. PoW is the right choice for the project; others are context only.

🟡 **Partially relevant**
- **Account vs. UTXO model** — we use SISO (simplified UTXO). Worth naming this explicitly in the report.
- **Decentralization / P2P networks** — MiniChain runs single-process; mention as scope limit, not a feature.
- **NFTs, tokenization, application use-cases** — good for the report introduction's context paragraph.

🔴 **Irrelevant**
- Specific altcoins (Zcash, Litecoin), staking economies, IoT/medical use cases — scope creep.

---

### Lecture 02 — Cryptographic Primitives
*Symmetric vs. asymmetric crypto, hash functions, digital signatures, collision resistance.*

🟢 **Directly relevant**
- **One-way hash + collision resistance** → Tasks 1, 2, 3. Justifies SHA-256 everywhere.
- **Public-key cryptography (ECC, RSA)** → Task 1. Justifies the ECC choice.
- **Digital signature = sign with private key, verify with public key, over hash of message** → Task 1. Exactly what `Transaction._sign_transaction` does.
- **Chained hash (simpler precursor of Merkle tree)** → Task 2. Worth mentioning as the conceptual stepping stone in the report.

🟡 **Partially relevant**
- **Symmetric encryption (AES/DES)** — not used in MiniChain; mention in a "why we chose ECDSA" paragraph.
- **Key-distribution problem** — motivates why public-key crypto solves trustless identity; 1–2 report sentences.
- **MACs, Diffie–Hellman** — pure background.

🔴 **Irrelevant**
- Historical ciphers (Enigma, DES cracking), RC4/MD5 weaknesses, deep modular-arithmetic derivations.

---

### Lecture 03 — Distributed Systems & Consensus
*Distributed-systems primer, CAP, Byzantine Generals, Paxos/BFT/PoW.*

🟢 **Directly relevant**
- **Byzantine Generals Problem** → Task 4/5 framing. The *reason* PoW exists; cite this in the report.
- **State Machine Replication / total-order broadcast** → Task 3. Each block is an SMR step — good conceptual model.
- **Distributed consensus definition** → Task 4. Frames what mining is solving.

🟡 **Partially relevant**
- **CAP theorem** — one-line note that MiniChain prefers Consistency + Partition-tolerance.
- **Paxos / Raft** — explicit contrast with PoW in the report.
- **P2P network model** — scope limit: MiniChain is single-process.

🔴 **Irrelevant**
- Specific DHT protocols (Chord, Gnutella), Two Generals paradox formalism, Hyperledger Fabric (covered in Lec 09).

---

### Lecture 04 — Bitcoin 1 (Merkle Tree & ECDSA)
*SHA-256, Merkle-tree construction and proofs, ECDSA on secp256k1.*

🟢 **Directly relevant — the most important lecture for Phase I**
- **SHA-256 as the Bitcoin hash function** → Tasks 1–5.
- **Merkle tree construction (binary, bottom-up)** → Task 2. Current implementation matches.
- **Power-of-two leaves / duplicate-last-leaf padding rule** → Task 2. Spec asks for power of 2; duplication handles the general case (bonus).
- **ECDSA on secp256k1** → Task 1. Already implemented correctly.
- **Trapdoor function intuition** → Task 1 report framing.
- **Merkle tree stored in block header → tamper detection** → Tasks 3 and 5. Exactly how our tamper tests work.

🟡 **Partially relevant**
- **Merkle proof / authentication path** — bonus: add `generate_merkle_proof(tx)` and `verify_merkle_proof(...)` to support SPV-style light-client verification. High ROI, small code.
- **O(n) vs. O(log n) verification cost** — good figure for the report.
- **Batch signature verification via single root signature** — mention in the report.

🔴 **Irrelevant**
- Bitcoin-specific address encoding (Base58Check, version bytes), certificate authorities, PKI revocation.

---

### Lecture 05 — Bitcoin 2 (Blocks, PoW, UTXO, Scripts)
*Bitcoin block format (80-byte header), UTXO model, Hashcash-style PoW, difficulty adjustment, Bitcoin Script.*

🟢 **Directly relevant — the most important lecture for Phase II**
- **80-byte block header (prev_hash, merkle_root, timestamp, nBits/difficulty, nonce)** → Task 3. Our header fields mirror this.
- **Hashcash PoW: find nonce s.t. H(header) has k leading zeros** → Task 4. This is our mining loop exactly.
- **Probability of success = 1/2^k** → Task 4. Worth putting in the report as the difficulty-calibration formula.
- **Longest-chain rule** → Task 5 framing. Our single-chain model implicitly follows this.
- **Double-spending prevention** → Task 5. Even though we don't have a UTXO set, we should mention the principle.
- **Mining difficulty target** → Task 4. Justifies `DIFFICULTY = 4`.

🟡 **Partially relevant (high ROI bonus features)**
- **Coinbase transaction / block reward** — bonus: add a miner-reward transaction to each block. Small code, substantial report weight.
- **Transaction fees** — bonus: `fee = sum(inputs) − sum(outputs)`; low ROI under SISO.
- **UTXO set** — spec picks SISO to sidestep this; mention UTXO as "the full version we simplified."
- **Difficulty adjustment** — bonus: adjust target every N blocks based on average mining time; excellent report content (produces a graph).
- **SPV / light clients** — ties into the Merkle-proof bonus from Lec 04.
- **Mempool / orphan blocks** — mention as "out of scope for single-node MiniChain."

🔴 **Irrelevant**
- Bitcoin Script opcodes (we use raw ECDSA), SegWit, Taproot, Lightning, Bitcoin variants (BCH/BSV/BTG).

---

### Lecture 06 — Permissionless Blockchain 1 (Ethereum Fundamentals)
*Account-based model, EOAs, gas, Solidity basics.*

🟢 **Directly relevant**
- **EOA controlled by ECDSA key pair** → Task 1. Validates our `Account` class design.
- **Account-based model as an alternative to UTXO** → Task 1 report framing. We can now explicitly position MiniChain as "SISO (UTXO-like), not account-based."

🟡 **Partially relevant**
- **Transaction nonce (replay prevention)** — bonus: add a per-account nonce field. Cheap, demonstrates we know about replay attacks.
- **Block reward / mining incentive** — same as Lec 05 note.
- **Gas mechanism** — conceptual only; MiniChain has no executable code.

🔴 **Irrelevant**
- EVM, Solidity, tokens (ERC-20), DApps, Merkle Patricia Trie internals (summary mention only).

---

### Lecture 07 — Permissionless Blockchain 2 (Ethereum Advanced)
*Patricia Trie, GHOST/LMD-GHOST, uncle blocks, Ethash, PoS transition, difficulty adjustment.*

🟢 **Directly relevant**
- **Difficulty-adjustment formula** → Task 4. Concrete algorithm we can simplify for a bonus feature.
- **Chain-selection rule (longest-chain vs. GHOST)** → Task 5. We should explicitly state in the report that MiniChain uses the longest-chain rule.

🟡 **Partially relevant**
- **Patricia Trie** — mention as "what we would use for a state trie in a richer design."
- **Uncle / ommer blocks** — scope limit: single-chain MiniChain has no uncles.
- **Ethash memory-hardness** — one-line contrast with our plain-SHA-256 PoW.
- **PoS transition** — future-work paragraph in the report.

🔴 **Irrelevant**
- Ethereum 2.0 Beacon chain, LMD-GHOST specifics, EVM bytecode, specific parameter tuning (12-s block target etc.), IPFS/Swarm off-chain storage.

---

### Lecture 08 — Smart Contracts / Solidity
*EVM opcodes, gas, contract deployment, Bitcoin-vs-Ethereum comparison.*

🟢 **Directly relevant**
- **Bitcoin vs. Ethereum comparison table** → report positioning. Places MiniChain clearly in the "Bitcoin-style, simplified" quadrant.
- **Authorization pattern (msg.sender == owner)** → Task 1/5. Conceptual parallel to our "signature must match sender's public key" check.

🟡 **Partially relevant**
- **Event/log emission** — bonus: emit log events per block for readability in the demo output. Cosmetic.
- **Finite execution via gas limit** — one-line mention that MiniChain transactions are trivially finite.

🔴 **Irrelevant — this entire lecture is largely out of scope**
- Solidity syntax, EVM stack machine, storage/memory distinction, contract security (reentrancy, overflow), bytecode compilation, contract accounts.
- **Scope rule:** the project spec does NOT require smart contracts. Do not implement any of this. One paragraph in the report: "smart contracts are an extension axis we did not pursue."

---

### Lecture 09 — Permissioned Blockchain (Hyperledger Fabric)
*Permissioned vs. permissionless, Fabric architecture, chaincode, MSP, channels, deterministic consensus.*

🟢 **Directly relevant**
- **Permissioned vs. permissionless distinction** → report framing. State explicitly: "MiniChain is permissionless." One sentence.

🟡 **Partially relevant**
- **Deterministic vs. probabilistic consensus** — good report contrast; MiniChain's PoW is probabilistic (longest-chain rule).
- **Ledger = world state + transaction history** — conceptual model that matches our Block list.

🔴 **Irrelevant — this entire lecture is mostly out of scope**
- Hyperledger Fabric components (orderer, peers, MSP, chaincode), endorsement policies, channels, private data collections, Kafka/SBFT consensus, enterprise PKI.
- **Scope rule:** no Fabric-style access control, no membership service, no channels. Report should spend ≤½ page on this comparison.

---

### Lecture 10 — Advanced Topics (DeFi, Payment Channels, DIDs, IoT, MCS)
*DeFi, Lightning Network, state channels, HTLC, DIDs, blockchain + IoT, mobile crowdsensing.*

🟢 **Directly relevant**
- *(essentially none for the required 5 tasks)*

🟡 **Partially relevant**
- **Scalability numbers (Bitcoin 7 tx/s, Ethereum 15, Visa 24 000)** — useful report context.
- **Merkle proofs for light-client validation** — reinforces the Lec 04 bonus.

🔴 **Irrelevant — this lecture is entirely out of scope for implementation**
- DeFi protocols (DEX, lending, DAO), stablecoins, Lightning Network, payment channels, HTLC, DIDs, IoT integration, mobile crowdsensing incentives.
- **Scope rule:** at most a "future work" paragraph in the report. Do not build any of this.

---

## 2. Rolled-up influence on the project

### 2.1 Per-task design influence (the essentials)

| Task | Lectures that justify it | What this changes in the project |
|---|---|---|
| **Task 1 — Accounts / Transactions** | Lec 02, 04, 06, 08 | Confirm ECDSA on secp256k1, confirm hash-of-message signing. **Action:** add the missing "SHA-256 of amount" field in `data` (required by spec §5.1 and backed by Lec 02). |
| **Task 2 — Merkle Tree** | Lec 01, 04 | Bottom-up SHA-256, power-of-two leaves. **Action:** optionally add `generate_merkle_proof()` + `verify_merkle_proof()` (Lec 04 bonus). |
| **Task 3 — Block / Chain** | Lec 01, 03, 05, 07 | 80-byte-header equivalent is the minimum bar. Current implementation already meets it. **Action:** none required; just cite Lec 05 in the report. |
| **Task 4 — PoW Mining** | Lec 03, 05, 07 | Hashcash-style nonce search against difficulty target. **Action (bonus):** implement difficulty adjustment based on average block time (Lec 05/07); produces a real graph for the report. |
| **Task 5 — Integrity Verification** | Lec 01, 03, 05 | Chain validation = rehash every block + check `previous_hash` + check tx signatures. Current tamper tests cover the attack surface. **Action:** add longest-chain-rule paragraph to report (Lec 05/07). |

### 2.2 Bonus-feature priority list (directly grounded in the lectures)

Ordered by *(report value × code cost⁻¹)*. All are OPTIONAL.

1. **Fix the §5.1 `data` field** — include SHA-256 hash of amount alongside amount. Backed by Lec 02. ~10 min.
2. **Difficulty-adjustment algorithm** — Lec 05 formula, simplified. Produces a mining-time graph for the report. ~1 hr.
3. **Coinbase / block-reward transaction** — Lec 05 & 06. Each mined block emits a reward to the miner's address. ~30 min.
4. **Merkle proof + verification** — Lec 04. Adds 2 functions plus a demo. ~45 min.
5. **Transaction nonce (replay prevention)** — Lec 06. One field, one check. ~20 min.
6. **Balance query `get_balance(address)`** — walks the chain; shows the chain is a ledger. Not tied to a specific lecture but fits the account-model discussion in Lec 06. ~30 min.

Items 1–3 are strongly recommended; 4–6 are polish.

### 2.3 Vocabulary & naming conventions (adopt from lectures)

To match lecture terminology exactly:

- `merkle_root` (not `tx_root`) — Lec 01, 04, 05.
- `previous_hash` / `prev_block_hash` — Lec 01, 05.
- `difficulty_target` (or `nBits` only if Bitcoin-specific) — Lec 05.
- `nonce` for PoW counter; keep it separate from any tx-level nonce (Lec 06).
- `digital signature` and `ECDSA` — Lec 02, 04.
- `sender_address` / `receiver_address` for public-key identifiers — Lec 06.
- `genesis block` (two words) — Lec 01.
- `longest chain rule` — Lec 05, 07.
- `coinbase transaction` if we implement block rewards — Lec 05.
- `tamper detection` — Lec 01, 05.

### 2.4 Out-of-scope guardrails (what NOT to do)

From lectures 07–10 especially, avoid the following even if tempting:

- No smart-contract engine, no Solidity, no EVM emulation (Lec 08).
- No Hyperledger / Fabric / permissioned consensus (Lec 09).
- No Lightning / payment channels / HTLC / DeFi / DIDs (Lec 10).
- No Patricia Trie — stick with the simple balanced Merkle tree (Lec 07).
- No P2P networking layer — single-process is explicitly in scope.

Each of these should appear in the report's "Limitations / Future Work" section as *deliberate* non-goals, not oversights.

---

## 3. How this plan should drive the documentation structure

This lecture mapping feeds the earlier `DOC_STRUCTURE_PLAN.md` as follows:

- **`docs/DESIGN.md`** — each design decision should cite the lecture that backs it (e.g. "SECP256K1 — Lecture 04").
- **`docs/ARCHITECTURE.md`** — use lecture vocabulary from §2.3 consistently.
- **Report (separate deliverable)** — sections map 1:1 onto lectures:
  - *Cryptographic foundations* → Lec 02, 04
  - *Distributed-systems framing* → Lec 03
  - *Protocol design* (block / chain / PoW) → Lec 05
  - *Positioning vs. Ethereum and Fabric* → Lec 06, 07, 08, 09
  - *Future work* → Lec 07, 10
- **`docs/TESTING.md`** — tamper detection should be explained in the language of Lec 05 (merkle-root change invalidates block hash, broken previous-hash link breaks chain, etc.).

---

## 4. Risks and assumptions

- **Assumption:** the 10 lectures supplied are the complete course material. If additional slides exist (tutorials, supplementary readings), this mapping may be incomplete.
- **Assumption:** the spec's "data = amount + hash-of-amount" (§5.1) aligns with Lec 02's digital-signature discussion. We are interpreting "crypto-hash of amount" as a literal SHA-256 of the amount string, not a signature.
- **Assumption:** PoW with fixed difficulty = 4 is acceptable. Difficulty adjustment (bonus #2) is a polish item, not required.
- **Unclear:** how strictly the grader expects *every* bonus feature to be cited back to a lecture. The safe default: cite when adding extras, skip citation for required-task implementations already present in the code.
- **Unclear:** whether the report allows explicit "we chose not to implement X from Lecture Y because it is out of scope" statements. Assumed yes — this demonstrates we understood the lecture.

---

## 5. Next step (not yet — awaiting approval)

Once this plan is approved:

1. Update `DOC_STRUCTURE_PLAN.md` to cross-reference this file (one line in the Risks section).
2. Use this document as the source-of-truth for citations in `docs/DESIGN.md` when we eventually write it.
3. Use §2.2 to decide which bonus features (if any) to implement before the 2026-04-24 deadline.

Stop here. No code or new docs yet.
