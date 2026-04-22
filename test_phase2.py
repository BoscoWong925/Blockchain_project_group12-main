"""
test_phase2.py - Phase II Test Script for MiniChain

Demonstrates all Phase II functionality:
  1. Blockchain Construction  - Genesis block + 3 mined blocks
  2. Proof-of-Work Mining     - Each block satisfies difficulty target "0000"
  3. Integrity Verification   - is_chain_valid() on a clean and a tampered chain

Usage:
    python test_phase2.py
"""

from src.account import Account
from src.transaction import Transaction
from src.blockchain import Blockchain


def separator(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Helper: create N accounts
# ---------------------------------------------------------------------------
def make_accounts(*names) -> list:
    return [Account(n) for n in names]


# ---------------------------------------------------------------------------
# Helper: create a list of transactions (must be power of 2)
# ---------------------------------------------------------------------------
def make_transactions(accounts: list, pairs: list) -> list:
    txs = []
    for sender_name, receiver_name, amount in pairs:
        sender   = next(a for a in accounts if a.name == sender_name)
        receiver = next(a for a in accounts if a.name == receiver_name)
        txs.append(Transaction(sender, receiver, amount))
    return txs


# ---------------------------------------------------------------------------
# STEP 1 - Build the blockchain (Genesis + 3 blocks)
# ---------------------------------------------------------------------------
def test_blockchain_construction() -> Blockchain:
    separator("STEP 1: BLOCKCHAIN CONSTRUCTION")

    accounts = make_accounts("Alice", "Bob", "Charlie", "David")

    print("\n  Creating Blockchain (difficulty = 4 leading zeros)...")
    bc = Blockchain(difficulty=4)

    # --- Block 1: 2 transactions ---
    print("\n  Adding Block 1 (2 transactions)...")
    txs1 = make_transactions(accounts, [
        ("Alice",   "Bob",     10.0),
        ("Bob",     "Charlie",  5.0),
    ])
    bc.add_block(txs1)

    # --- Block 2: 4 transactions ---
    print("\n  Adding Block 2 (4 transactions)...")
    txs2 = make_transactions(accounts, [
        ("Charlie", "David",    3.0),
        ("David",   "Alice",    7.5),
        ("Alice",   "Charlie",  2.0),
        ("Bob",     "David",    1.5),
    ])
    bc.add_block(txs2)

    # --- Block 3: 2 transactions ---
    print("\n  Adding Block 3 (2 transactions)...")
    txs3 = make_transactions(accounts, [
        ("David",   "Bob",      4.0),
        ("Charlie", "Alice",    6.0),
    ])
    bc.add_block(txs3)

    # Print the full chain
    bc.print_chain()

    print(f"  ✅ Blockchain built successfully with {len(bc.chain)} blocks.")
    return bc


# ---------------------------------------------------------------------------
# STEP 2 - Verify a clean chain
# ---------------------------------------------------------------------------
def test_valid_chain(bc: Blockchain) -> None:
    separator("STEP 2: INTEGRITY VERIFICATION — Clean Chain")

    is_valid, message = bc.is_chain_valid()
    print(f"\n  Result: {message}")

    assert is_valid, "Clean chain should be valid!"
    print("  ✅ Clean chain passed verification.")


# ---------------------------------------------------------------------------
# STEP 3 - Tamper with a transaction amount in Block 1
# ---------------------------------------------------------------------------
def test_tamper_transaction(bc: Blockchain) -> None:
    separator("STEP 3: TAMPERING SIMULATION — Modify Transaction Amount in Block 1")

    target_block = bc.chain[1]          # Block 1
    target_tx    = target_block.transactions[0]

    original_amount = target_tx.amount
    print(f"\n  Target : Block {target_block.index}, TX {target_tx.tx_id[:16]}...")
    print(f"  Attack : Changing amount {original_amount} → 9999.0")
    target_tx.amount = 9999.0           # Tamper!

    is_valid, message = bc.is_chain_valid()
    print(f"\n  Result: {message}")

    assert not is_valid, "Tampered chain should be detected as invalid!"
    print("  ✅ Tampering detected correctly! (invalid transaction signature)")

    # Restore
    target_tx.amount = original_amount
    is_valid, _ = bc.is_chain_valid()
    assert is_valid
    print("  ✅ Chain restored and valid again.")


# ---------------------------------------------------------------------------
# STEP 4 - Tamper with a block's data field directly
# ---------------------------------------------------------------------------
def test_tamper_block_data(bc: Blockchain) -> None:
    separator("STEP 4: TAMPERING SIMULATION — Modify Block Header Data in Block 2")

    target_block = bc.chain[2]          # Block 2
    original_root = target_block.merkle_root

    print(f"\n  Target : Block {target_block.index}")
    print(f"  Attack : Overwriting merkle_root with zeros")
    target_block.merkle_root = "0" * 64  # Tamper merkle root directly

    is_valid, message = bc.is_chain_valid()
    print(f"\n  Result: {message}")

    assert not is_valid, "Block with modified header should be detected!"
    print("  ✅ Tampering detected correctly! (block hash no longer matches)")

    # Restore
    target_block.merkle_root = original_root
    is_valid, _ = bc.is_chain_valid()
    assert is_valid
    print("  ✅ Chain restored and valid again.")


# ---------------------------------------------------------------------------
# STEP 5 - Tamper with the previous_hash link between blocks
# ---------------------------------------------------------------------------
def test_tamper_previous_hash(bc: Blockchain) -> None:
    separator("STEP 5: TAMPERING SIMULATION — Break the Hash Link Between Blocks")

    target_block = bc.chain[2]          # Block 2
    original_prev = target_block.previous_hash

    print(f"\n  Target : Block {target_block.index}.previous_hash")
    print(f"  Attack : Replacing previous_hash with zeros")
    target_block.previous_hash = "0" * 64  # Tamper hash link

    is_valid, message = bc.is_chain_valid()
    print(f"\n  Result: {message}")

    assert not is_valid, "Broken hash link should be detected!"
    print("  ✅ Broken hash link detected correctly!")

    # Restore
    target_block.previous_hash = original_prev
    is_valid, _ = bc.is_chain_valid()
    assert is_valid
    print("  ✅ Chain restored and valid again.")


# ---------------------------------------------------------------------------
# STEP 6 - Tamper with the Genesis Block
# ---------------------------------------------------------------------------
def test_tamper_genesis(bc: Blockchain) -> None:
    separator("STEP 6: TAMPERING SIMULATION — Tamper with the Genesis Block")

    genesis = bc.chain[0]
    original_hash = genesis.hash

    print(f"\n  Target : Genesis Block hash")
    print(f"  Attack : Overwriting genesis hash with zeros")
    genesis.hash = "0" * 64            # Tamper genesis hash directly

    is_valid, message = bc.is_chain_valid()
    print(f"\n  Result: {message}")

    assert not is_valid, "Tampered Genesis Block should be detected!"
    print("  ✅ Genesis Block tampering detected correctly!")

    # Restore
    genesis.hash = original_hash
    is_valid, _ = bc.is_chain_valid()
    assert is_valid
    print("  ✅ Chain restored and valid again.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("\n" + "#" * 70)
    print("#" + " " * 18 + "MINICHAIN - PHASE II TEST" + " " * 25 + "#")
    print("#" + " " * 10 + "Blockchain, Proof-of-Work & Integrity Verification" + " " * 8 + "#")
    print("#" * 70)

    bc = test_blockchain_construction()
    test_valid_chain(bc)
    test_tamper_transaction(bc)
    test_tamper_block_data(bc)
    test_tamper_previous_hash(bc)
    test_tamper_genesis(bc)

    separator("PHASE II — ALL TESTS COMPLETE ✅")
    print("  Blockchain construction  : PASSED")
    print("  Proof-of-Work mining     : PASSED")
    print("  Clean chain verification : PASSED")
    print("  Tamper tx amount         : DETECTED ✅")
    print("  Tamper block header      : DETECTED ✅")
    print("  Tamper hash link         : DETECTED ✅")
    print("  Tamper Genesis Block     : DETECTED ✅")
    print()


if __name__ == "__main__":
    main()
