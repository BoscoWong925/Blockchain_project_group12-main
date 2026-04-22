"""
test_bonus.py - Bonus demo for MiniChain

Demonstrates the two optional bonus features, both backed by the lecture
notes:

  * BONUS B1 - Coinbase / block-reward transaction (Lectures 05 & 06)
  * BONUS B2 - get_balance(address) ledger walk       (Lecture 06)

Neither feature is required by the project spec; both are additive and
do not affect the Phase I / Phase II test behaviour.

Usage:
    python test_bonus.py
"""

from src.account import Account
from src.transaction import Transaction
from src.blockchain import Blockchain, BLOCK_REWARD


def separator(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main() -> None:
    print("\n" + "#" * 70)
    print("#" + " " * 20 + "MINICHAIN - BONUS DEMO" + " " * 26 + "#")
    print("#" + " " * 12 + "Coinbase reward + get_balance(address)" + " " * 18 + "#")
    print("#" * 70)

    # --- Accounts ---
    separator("STEP 1: ACCOUNTS")
    alice = Account("Alice")
    bob = Account("Bob")
    charlie = Account("Charlie")
    miner = Account("Miner")
    print(f"  Alice   : {alice.get_address()[:24]}...")
    print(f"  Bob     : {bob.get_address()[:24]}...")
    print(f"  Charlie : {charlie.get_address()[:24]}...")
    print(f"  Miner   : {miner.get_address()[:24]}...")

    # --- Chain with coinbase-rewarded blocks ---
    separator("STEP 2: MINE BLOCKS WITH COINBASE (BONUS B1)")
    bc = Blockchain(difficulty=4)

    # Block 1: one real transaction + coinbase = 2 transactions (power of 2)
    print(f"\n  Adding Block 1 with 1 user tx + coinbase (reward={BLOCK_REWARD})...")
    bc.add_block(
        [Transaction(alice, bob, 10.0)],
        miner=miner,
    )

    # Block 2: three real transactions + coinbase = 4 transactions (power of 2)
    print(f"\n  Adding Block 2 with 3 user txs + coinbase (reward={BLOCK_REWARD})...")
    bc.add_block(
        [
            Transaction(bob, charlie, 4.0),
            Transaction(alice, charlie, 2.0),
            Transaction(charlie, alice, 1.0),
        ],
        miner=miner,
    )

    # --- Clean-chain validation still passes (coinbase bypasses signature check) ---
    separator("STEP 3: CHAIN VALIDATION")
    is_valid, message = bc.is_chain_valid()
    print(f"\n  {message}")
    assert is_valid, "Bonus chain should be valid"
    print("  ✅ Coinbase transactions pass the integrity checks.")

    # --- Balance queries (BONUS B2) ---
    separator("STEP 4: BALANCE QUERIES (BONUS B2)")
    balances = {
        "Alice  ": bc.get_balance(alice.get_address()),
        "Bob    ": bc.get_balance(bob.get_address()),
        "Charlie": bc.get_balance(charlie.get_address()),
        "Miner  ": bc.get_balance(miner.get_address()),
    }
    for name, bal in balances.items():
        print(f"  {name}: {bal:+.2f}")

    # --- Sanity checks ---
    expected_miner = BLOCK_REWARD * 2  # two blocks mined
    expected_alice = -10.0 - 2.0 + 1.0  # sent 10, sent 2, received 1
    expected_bob = 10.0 - 4.0
    expected_charlie = 4.0 + 2.0 - 1.0

    assert abs(balances["Miner  "] - expected_miner) < 1e-9
    assert abs(balances["Alice  "] - expected_alice) < 1e-9
    assert abs(balances["Bob    "] - expected_bob) < 1e-9
    assert abs(balances["Charlie"] - expected_charlie) < 1e-9

    separator("BONUS DEMO — ALL CHECKS PASSED ✅")
    print("  Coinbase reward credited to miner : PASSED")
    print("  get_balance() across chain         : PASSED")
    print("  Chain still validates with coinbase: PASSED")
    print()


if __name__ == "__main__":
    main()
