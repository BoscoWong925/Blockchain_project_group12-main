# Final Submission Materials

Source of truth: final submission readiness brief provided in chat.

## 1. Missing Human Input

- README.md line 5: add member names, or replace the current placeholder with a short reference line pointing to docs/CONTRIBUTORS.md.
- docs/CONTRIBUTORS.md section 1: fill 3 to 5 rows of member name and student ID.
- docs/CONTRIBUTORS.md section 2: fill per-member work distribution mapped to files and phases.
- docs/CONTRIBUTORS.md section 3: fill any extra external sources actually used beyond the baseline already listed there.
- docs/CONTRIBUTORS.md section 4: optional acknowledgements only; leave empty if not needed.
- No other human-input placeholders remain in the documented submission set.

## 2. Report Writing Outline

- Section 1. Introduction
  - State project scope and course context.
  - State the five required tasks delivered.
  - State the simplified Bitcoin-style positioning.
  - Add one short contributor paragraph from CONTRIBUTORS.md section 2.
  - Source: README.md, docs/DESIGN.md, docs/CONTRIBUTORS.md.

- Section 2. System Architecture
  - Present the component and data-flow diagram.
  - Describe Account -> Transaction -> Merkle Tree -> Block -> Blockchain.
  - Summarize module responsibilities.
  - Source: docs/ARCHITECTURE.md.
  - Required new item: redraw the architecture diagram as a proper report figure.

- Section 3. Design and Implementation
  - ECC on SECP256K1 for accounts and signatures.
  - SHA-256 uses across transaction, Merkle, and block logic.
  - SISO transaction model.
  - Transaction data field: amount plus amount hash.
  - tx_id derivation.
  - Merkle tree construction.
  - Block header and Genesis block.
  - Proof-of-Work at difficulty 4.
  - Six validator layers.
  - Source: docs/DESIGN.md.
  - Required new items: one pseudocode block for mine() and one pseudocode block for is_chain_valid().

- Section 4. Testing and Results
  - Summarize Phase I results.
  - Summarize Phase II results.
  - Summarize bonus results.
  - Summarize adversarial results.
  - Include the catch-matrix table.
  - Explain every screenshot and figure in the text.
  - Source: docs/TESTING.md, docs/USAGE.md, test_phase1.py, test_phase2.py, test_bonus.py, test_adversarial.py.

- Section 5. Limitations and Future Work
  - List only documented non-goals and limitations.
  - Use: no reward-value policy, no replay prevention, no fork choice, no P2P, no persistence, no UTXO, no smart contracts.
  - Keep this section short.
  - Source: docs/DESIGN.md and docs/TESTING.md.

- Section 6. Conclusion
  - One short closing paragraph.
  - State what was implemented.
  - State what was demonstrated.
  - State what remains deliberately out of scope.

- Section 7. References
  - List lecture 01 to 10.
  - List every actual external source from docs/CONTRIBUTORS.md section 3.
  - Format to course citation style.

- Wording flag
  - Do not write: "detects all tampering".
  - Do not write: "any single-bit tamper anywhere in the chain is caught".
  - Do not write: "every single-field tamper reduces to a cryptographic check".
  - Safe wording: the six validation layers catch the audited tamper classes listed in docs/TESTING.md; attacks outside that scope are acknowledged limitations.

## 3. Video Recording Checklist

- 0:00 to 0:20
  - Show title card with project title, course, group number, and member names.
  - Voiceover: team introduction.

- 0:20 to 1:00
  - Show architecture diagram.
  - Voiceover: Account -> Transaction -> Merkle Tree -> Block -> Blockchain, plus SISO, PoW, and permissionless single-process scope.

- 1:00 to 1:40
  - Run python test_phase1.py.
  - Voiceover: ECC account creation, four signed SISO transactions, Merkle root creation, and amount tamper causing signature invalidation.

- 1:40 to 2:40
  - Run python test_phase2.py.
  - Voiceover: Genesis plus three mined blocks, hashes with 0000 prefix, clean-chain validation, and four tamper cases detected with specific errors.

- 2:40 to 3:20
  - Run python test_bonus.py.
  - Voiceover: coinbase transaction and get_balance totals.

- 3:20 to 4:10
  - Run python test_adversarial.py.
  - Highlight Scenario C and Scenario D.
  - Voiceover: the six validator layers catch the audited attack set.

- 4:10 to 4:40
  - Show one limitations slide.
  - Visible text must include at least three non-goals from the documented limitation set.

- 4:40 to 5:00
  - Show closing card.
  - Summarize five required tasks, two bonuses, and audited adversarial coverage.

- Recording constraints
  - Final export: MP4, 16:9, 720p, 500 MB or less.
  - Record terminal at higher resolution first, then down-sample.
  - Speed mining sections instead of cutting them out.
  - Use one narrator.

- Wording flag
  - Do not say the system catches all tampering.
  - Say it catches the audited tamper classes.

## 4. Capture Checklist

### Screenshots

- S1: test_phase1.py output showing Merkle root computed, tree levels, and the "Merkle Roots differ" block.
- S2: test_phase1.py output showing the amount tamper block with VALID -> INVALID -> VALID.
- S3: test_phase2.py final summary from blockchain construction passed through Genesis tamper detected.
- S4: test_phase2.py Step 3 raw error line for the ECDSA-caught tamper.
- S5: test_phase2.py Step 4 raw line showing invalid hash or broken PoW.
- S6: test_bonus.py balance block showing Alice, Bob, Charlie, and Miner totals.
- S7: test_adversarial.py final summary block with all adversarial cases detected.
- S8: test_adversarial.py Scenario C raw line showing coinbase amount rejection through stale amount_hash.

### Figures To Redraw

- F1: component and data-flow diagram from docs/ARCHITECTURE.md.
- F2: six-layer validator flowchart from docs/DESIGN.md.
- F3: catch-matrix table from docs/TESTING.md.
- F4: positioning table comparing MiniChain with Bitcoin, Ethereum, and Fabric from docs/ARCHITECTURE.md.

### Stored Text Outputs

- Save full stdout from test_phase1.py.
- Save full stdout from test_phase2.py.
- Save full stdout from test_bonus.py.
- Save full stdout from test_adversarial.py.
- Store them in an outputs folder inside the final submission package.

## 5. Final Submission Package

- README.md
- requirements.txt
- src/account.py
- src/transaction.py
- src/merkle_tree.py
- src/block.py
- src/blockchain.py
- test_phase1.py
- test_phase2.py
- test_bonus.py
- test_adversarial.py
- docs/ARCHITECTURE.md
- docs/CONTRIBUTORS.md
- docs/COURSE_SPEC.md
- docs/DESIGN.md
- docs/REPRODUCIBILITY.md
- docs/TESTING.md
- docs/USAGE.md
- PLAN/DOC_STRUCTURE_PLAN.md
- PLAN/LECTURE_ALIGNMENT_PLAN.md
- outputs/ with full stdout captures for the four scripts
- final report PDF
- final MP4 video

## 6. Final Verification Steps

1. Fill docs/CONTRIBUTORS.md sections 1 to 3 and update README.md line 5.
2. Run test_phase1.py, test_phase2.py, test_bonus.py, and test_adversarial.py from the final submission state.
3. Save full stdout from all four runs into outputs/.
4. Capture S1 to S8 from those final runs.
5. Redraw F1 to F4.
6. Check the report PDF against course rules: English only, own words, no large pasted code blocks, pseudocode only where needed, every figure explained, references formatted.
7. Check report wording against the documented limitation set in docs/TESTING.md and docs/DESIGN.md.
8. Check the video against the shot list, runtime, aspect ratio, resolution, and file-size limits.
9. Run one final wording pass on report captions, conclusion, and video narration.
10. Remove any overclaiming phrases before submission.

## Wording Risk To Flag In Final Pass

- Do not use: "detects all tampering".
- Do not use: "any single-bit tamper anywhere in the chain is caught".
- Do not use: "every single-field tamper reduces to a cryptographic check".
- Use instead: the six validation layers catch the audited tamper classes; attacks outside that scope remain acknowledged limitations.