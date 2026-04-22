"""
test_adversarial.py - Focused adversarial checks for MiniChain.

These scenarios exposed false-negatives in earlier versions of
Blockchain.is_chain_valid(). They must all be detected for the current
validator to be considered sound.

Covered:
  A. Mined normal tx: mutate tx_id only                       -> invalid
  B. Mined normal tx: mutate amount_hash only                 -> invalid
  C. Mined bonus chain: mutate coinbase amount after mining   -> invalid
  D. Extra coinbase (2 coinbases in one block)                -> invalid
  E. Coinbase at non-zero position                            -> invalid

Each tampered state is immediately restored so the chain validates cleanly
before the next scenario runs. Assertions fail the script loudly if any
scenario is NOT detected.
"""

from src.account import Account
from src.transaction import (
    COINBASE_ADDRESS,
    CoinbaseTransaction,
    Transaction,
)
from src.blockchain import Blockchain, BLOCK_REWARD


def _expect_invalid(bc: Blockchain, label: str) -> str:
    is_valid, message = bc.is_chain_valid()
    assert not is_valid, (
        f"[{label}] expected tampering to be REJECTED, but validator said "
        f"chain is valid. Message: {message}"
    )
    return message


def _expect_valid(bc: Blockchain, label: str) -> None:
    is_valid, message = bc.is_chain_valid()
    assert is_valid, (
        f"[{label}] expected clean chain to be VALID, validator said invalid. "
        f"Message: {message}"
    )


def main() -> None:
    print("\n" + "#" * 70)
    print("#" + " " * 15 + "MINICHAIN - ADVERSARIAL VALIDATION TEST" + " " * 14 + "#")
    print("#" * 70)

    # --- Build a chain with one normal-tx block and one coinbase-tx block ---
    alice = Account("Alice")
    bob = Account("Bob")
    charlie = Account("Charlie")
    miner = Account("Miner")

    print("\n  Building test chain (Genesis + 2 blocks, difficulty=4)...")
    bc = Blockchain(difficulty=4)

    # Block 1: two normal transactions (no coinbase).
    tx_ab = Transaction(alice, bob, 10.0)
    tx_bc = Transaction(bob, charlie, 4.0)
    bc.add_block([tx_ab, tx_bc])

    # Block 2: one coinbase + one normal tx (total 2 = power of 2).
    tx_ca = Transaction(charlie, alice, 2.0)
    bc.add_block([tx_ca], miner=miner)

    _expect_valid(bc, "setup sanity")
    print("  ✅ Clean chain validates.\n")

    # ------------------------------------------------------------------
    # Scenario A: mutate tx_id only on a mined normal transaction.
    # The signed payload is unchanged (so ECDSA still verifies), and the
    # block hash is still internally consistent with the stored header.
    # Earlier versions missed this; we now catch it via tx_id
    # recomputation AND via Merkle-root recomputation.
    # ------------------------------------------------------------------
    print("  [A] Mutating tx_id of a mined normal transaction...")
    original_tx_id = tx_ab.tx_id
    tx_ab.tx_id = "a" * 64
    msg = _expect_invalid(bc, "A: tx_id mutation")
    print(f"      Rejected: {msg}")
    tx_ab.tx_id = original_tx_id
    _expect_valid(bc, "A: restore")

    # ------------------------------------------------------------------
    # Scenario B: mutate amount_hash only on a mined normal transaction.
    # This leaves the numeric amount intact, and signature/tx_id are still
    # the originals. Must be caught by the amount_hash consistency check.
    # ------------------------------------------------------------------
    print("\n  [B] Mutating amount_hash of a mined normal transaction...")
    original_amount_hash = tx_bc.amount_hash
    tx_bc.amount_hash = "b" * 64
    msg = _expect_invalid(bc, "B: amount_hash mutation")
    print(f"      Rejected: {msg}")
    tx_bc.amount_hash = original_amount_hash
    _expect_valid(bc, "B: restore")

    # ------------------------------------------------------------------
    # Scenario C: mutate coinbase amount after mining.
    # Coinbase has no signature (verify_signature() returns True), so
    # previously this went undetected. Must now be caught by one of:
    # amount_hash mismatch, tx_id mismatch, or Merkle-root mismatch.
    # ------------------------------------------------------------------
    print("\n  [C] Mutating coinbase amount on a mined block...")
    block2 = bc.chain[2]
    coinbase = block2.transactions[0]
    assert coinbase.input_address == COINBASE_ADDRESS, (
        "setup error: expected coinbase at index 0 of block 2"
    )
    original_amount = coinbase.amount
    coinbase.amount = 999999.0
    msg = _expect_invalid(bc, "C: coinbase amount mutation")
    print(f"      Rejected: {msg}")
    coinbase.amount = original_amount
    _expect_valid(bc, "C: restore")

    # ------------------------------------------------------------------
    # Scenario D: inject an extra CoinbaseTransaction into a mined block.
    # Validator must reject purely on structural grounds ("at most one
    # coinbase"). Merkle mismatch would also catch this, but the
    # structural check is more informative and fires first.
    # ------------------------------------------------------------------
    print("\n  [D] Injecting a second coinbase into a mined block...")
    extra_cb = CoinbaseTransaction(miner, BLOCK_REWARD)
    block2.transactions.append(extra_cb)
    msg = _expect_invalid(bc, "D: extra coinbase")
    print(f"      Rejected: {msg}")
    block2.transactions.pop()
    _expect_valid(bc, "D: restore")

    # ------------------------------------------------------------------
    # Scenario E: place a coinbase at non-zero position.
    # Simulate by swapping coinbase with the following transaction in
    # block 2. Validator must reject with the positional rule.
    # ------------------------------------------------------------------
    print("\n  [E] Moving coinbase out of position 0...")
    # block 2 is [coinbase, tx_ca]; swap them so coinbase is at index 1.
    block2.transactions[0], block2.transactions[1] = (
        block2.transactions[1],
        block2.transactions[0],
    )
    msg = _expect_invalid(bc, "E: coinbase out-of-position")
    print(f"      Rejected: {msg}")
    block2.transactions[0], block2.transactions[1] = (
        block2.transactions[1],
        block2.transactions[0],
    )
    _expect_valid(bc, "E: restore")

    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  ADVERSARIAL TEST — ALL 5 SCENARIOS DETECTED ✅")
    print("=" * 70)
    print("  A: stale tx_id (normal tx)              DETECTED")
    print("  B: stale amount_hash (normal tx)        DETECTED")
    print("  C: coinbase amount mutation             DETECTED")
    print("  D: duplicate coinbase in one block      DETECTED")
    print("  E: coinbase at non-zero position        DETECTED")
    print()


if __name__ == "__main__":
    main()
