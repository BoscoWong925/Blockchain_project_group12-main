"""Merkle tree helpers."""

import hashlib
from typing import List

from src.transaction import Transaction


def sha256_hash(data: str) -> str:
    """Return the SHA-256 hex digest for a string."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def build_merkle_tree(transactions: List[Transaction]) -> dict:
    """Build a Merkle tree from a non-empty power-of-two transaction list."""
    n = len(transactions)
    if n == 0:
        raise ValueError("Transaction list must not be empty.")
    if n & (n - 1) != 0:
        raise ValueError(
            f"Number of transactions must be a power of 2, got {n}."
        )

    current_level = [sha256_hash(tx.tx_id) for tx in transactions]
    all_levels: List[List[str]] = [current_level[:]]

    while len(current_level) > 1:
        next_level: List[str] = []
        for i in range(0, len(current_level), 2):
            combined = current_level[i] + current_level[i + 1]
            parent_hash = sha256_hash(combined)
            next_level.append(parent_hash)

        current_level = next_level
        all_levels.append(current_level[:])

    merkle_root = current_level[0]

    return {"root": merkle_root, "levels": all_levels}


def print_merkle_tree(tree: dict) -> None:
    """Print the tree from root to leaves."""
    levels = tree["levels"]
    total_levels = len(levels)

    print("\n" + "=" * 70)
    print("                    MERKLE TREE STRUCTURE")
    print("=" * 70)

    for idx in range(total_levels - 1, -1, -1):
        if idx == total_levels - 1:
            label = "Root"
        elif idx == 0:
            label = "Leaves (H(tx_id))"
        else:
            label = f"Level {idx}"

        print(f"\n--- {label} ---")
        for j, hash_value in enumerate(levels[idx]):
            print(f"  [{j}] {hash_value}")

    print("\n" + "=" * 70)
    print(f"  Merkle Root: {tree['root']}")
    print("=" * 70 + "\n")
