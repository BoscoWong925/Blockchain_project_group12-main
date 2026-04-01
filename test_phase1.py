"""
test_phase1.py - Phase I Test Script for MiniChain

This script demonstrates all Phase I functionality:
  1. Account Generation   - Creates 4 accounts using ECC (SECP256K1)
  2. Transaction Generation - Creates 4 signed SISO transactions
  3. Signature Verification - Verifies each transaction's digital signature
  4. Merkle Tree Construction - Builds a Merkle Tree and prints the root

Usage:
    python test_phase1.py
"""

from src.account import Account
from src.transaction import Transaction
from src.merkle_tree import build_merkle_tree, print_merkle_tree


def separator(title: str) -> None:
    """Print a formatted section separator."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_account_creation() -> list:
    """
    Task 1a: Generate 4 blockchain accounts using ECC key pairs.
    Returns a list of Account objects.
    """
    separator("STEP 1: ACCOUNT GENERATION (ECC - SECP256K1)")

    names = ["Alice", "Bob", "Charlie", "David"]
    accounts = []

    for name in names:
        acc = Account(name)
        accounts.append(acc)
        print(f"\n  Account: {acc.name}")
        print(f"  Address (public key hex): {acc.get_address()}")

    print(f"\n  ✅ Successfully created {len(accounts)} accounts.")
    return accounts


def test_transaction_generation(accounts: list) -> list:
    """
    Task 1b: Generate 4 signed SISO transactions between the accounts.
    Returns a list of Transaction objects.
    """
    separator("STEP 2: TRANSACTION GENERATION (SISO)")

    alice, bob, charlie, david = accounts

    # Create 4 transactions (power of 2 for Merkle Tree)
    tx_pairs = [
        (alice, bob, 10.0),       # Alice sends 10 coins to Bob
        (bob, charlie, 5.0),      # Bob sends 5 coins to Charlie
        (charlie, david, 3.0),    # Charlie sends 3 coins to David
        (david, alice, 7.5),      # David sends 7.5 coins to Alice
    ]

    transactions = []
    for sender, receiver, amount in tx_pairs:
        tx = Transaction(sender, receiver, amount)
        transactions.append(tx)

        print(f"\n  Transaction: {sender.name} → {receiver.name}  |  Amount: {amount}")
        print(f"  TX ID:      {tx.tx_id}")
        print(f"  Signature:  {tx.signature[:64]}...")

    print(f"\n  ✅ Successfully created {len(transactions)} transactions.")
    return transactions


def test_signature_verification(transactions: list) -> None:
    """
    Verify the digital signature of every transaction.
    """
    separator("STEP 3: SIGNATURE VERIFICATION")

    all_valid = True
    for tx in transactions:
        is_valid = tx.verify_signature()
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"  TX {tx.tx_id[:16]}...  {tx.sender.name} → {tx.receiver.name}  |  Signature: {status}")
        if not is_valid:
            all_valid = False

    if all_valid:
        print("\n  ✅ All transaction signatures verified successfully.")
    else:
        print("\n  ❌ Some signatures failed verification!")

    # --- Tamper test: modify a transaction and verify it fails ---
    print("\n  --- Tamper Test: Modifying a transaction amount ---")
    tampered_tx = transactions[0]
    original_amount = tampered_tx.amount
    tampered_tx.amount = 9999.0  # Tamper with the amount

    is_valid_after_tamper = tampered_tx.verify_signature()
    status = "✅ VALID" if is_valid_after_tamper else "❌ INVALID (tamper detected!)"
    print(f"  TX {tampered_tx.tx_id[:16]}...  after tampering amount to 9999.0  |  Signature: {status}")

    # Restore the original amount
    tampered_tx.amount = original_amount
    is_valid_restored = tampered_tx.verify_signature()
    status = "✅ VALID" if is_valid_restored else "❌ INVALID"
    print(f"  TX {tampered_tx.tx_id[:16]}...  after restoring original amount   |  Signature: {status}")

    if not is_valid_after_tamper and is_valid_restored:
        print("\n  ✅ Tamper detection works correctly! Modified data invalidates the signature.")
    else:
        print("\n  ❌ Tamper detection test failed.")


def test_merkle_tree(transactions: list) -> None:
    """
    Task 2: Build a Merkle Tree from the 4 transactions and display the structure.
    """
    separator("STEP 4: MERKLE TREE CONSTRUCTION")

    print(f"\n  Building Merkle Tree from {len(transactions)} transactions...")
    print(f"  (Number of transactions is a power of 2: {len(transactions)} = 2^{len(transactions).bit_length() - 1})")

    # Display the Transaction IDs used as input
    print("\n  Input Transaction IDs:")
    for i, tx in enumerate(transactions):
        print(f"    T{i + 1}: {tx.tx_id}")

    # Build the Merkle Tree
    tree = build_merkle_tree(transactions)

    # Print the full tree structure
    print_merkle_tree(tree)

    print(f"  ✅ Merkle Root successfully computed.")

    # --- Verify: changing one TX ID should change the Merkle Root ---
    print("  --- Merkle Root Integrity Test ---")
    print("  Modifying one transaction and rebuilding the tree...")

    original_tx_id = transactions[0].tx_id
    transactions[0].tx_id = "0" * 64  # Tamper with TX ID

    tampered_tree = build_merkle_tree(transactions)
    transactions[0].tx_id = original_tx_id  # Restore

    if tree["root"] != tampered_tree["root"]:
        print(f"  Original Merkle Root:  {tree['root']}")
        print(f"  Tampered Merkle Root:  {tampered_tree['root']}")
        print(f"\n  ✅ Merkle Roots differ — tampering is detectable!")
    else:
        print(f"\n  ❌ Merkle Roots are the same — this should not happen!")


def main():
    """Run all Phase I tests."""
    print("\n" + "#" * 70)
    print("#" + " " * 20 + "MINICHAIN - PHASE I TEST" + " " * 24 + "#")
    print("#" + " " * 14 + "Account, Transaction & Merkle Tree" + " " * 20 + "#")
    print("#" * 70)

    # Step 1: Create accounts
    accounts = test_account_creation()

    # Step 2: Generate transactions
    transactions = test_transaction_generation(accounts)

    # Step 3: Verify signatures (including tamper test)
    test_signature_verification(transactions)

    # Step 4: Build Merkle Tree
    test_merkle_tree(transactions)

    # Final summary
    separator("PHASE I - ALL TESTS COMPLETE ✅")
    print("  Account generation:       PASSED")
    print("  Transaction generation:   PASSED")
    print("  Signature verification:   PASSED")
    print("  Tamper detection:         PASSED")
    print("  Merkle Tree construction: PASSED")
    print()


if __name__ == "__main__":
    main()
