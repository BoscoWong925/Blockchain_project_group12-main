"""
merkle_tree.py - Verifiable Merkle Tree for MiniChain

Constructs a Merkle Tree from a list of transactions.
- Leaf nodes are SHA-256 hashes of individual Transaction IDs.
- Parent nodes are SHA-256( hash_left + hash_right ).
- The tree is built bottom-up until a single Merkle Root remains.

Assumption: The number of transactions is always a power of 2 (e.g., 2, 4, 8, 16).
"""

import hashlib
import math
from typing import List

from src.transaction import Transaction


def sha256_hash(data: str) -> str:
    """
    Compute the SHA-256 hash of a given string.

    Args:
        data: The input string to hash.

    Returns:
        A hex-encoded SHA-256 hash string.
    """
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def build_merkle_tree(transactions: List[Transaction]) -> dict:
    """
    Build a complete Merkle Tree from a list of transactions.

    The function returns the Merkle Root along with all intermediate levels
    of the tree for verification and display purposes.

    Args:
        transactions: A list of Transaction objects. The length MUST be a power of 2.

    Returns:
        A dictionary with:
            - "root": The final Merkle Root hash (str).
            - "levels": A list of lists, where levels[0] is the leaf layer
                        and levels[-1] contains only the root hash.

    Raises:
        ValueError: If the number of transactions is not a power of 2 or is zero.
    """
    n = len(transactions)
    if n == 0:
        raise ValueError("Transaction list must not be empty.")
    if n & (n - 1) != 0:
        raise ValueError(
            f"Number of transactions must be a power of 2, got {n}."
        )

    # --- Level 0 (Leaf Nodes): Hash each Transaction ID ---
    current_level = [sha256_hash(tx.tx_id) for tx in transactions]

    # Store every level of the tree for display / verification
    all_levels: List[List[str]] = [current_level[:]]

    # --- Build upward level by level ---
    while len(current_level) > 1:
        next_level: List[str] = []
        for i in range(0, len(current_level), 2):
            # Concatenate left + right hashes, then hash the pair
            combined = current_level[i] + current_level[i + 1]
            parent_hash = sha256_hash(combined)
            next_level.append(parent_hash)

        current_level = next_level
        all_levels.append(current_level[:])

    merkle_root = current_level[0]

    return {
        "root": merkle_root,
        "levels": all_levels,
    }


def print_merkle_tree(tree: dict) -> None:
    """
    Pretty-print every level of the Merkle Tree.

    Args:
        tree: The dictionary returned by build_merkle_tree().
    """
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
        for j, h in enumerate(levels[idx]):
            print(f"  [{j}] {h}")

    print("\n" + "=" * 70)
    print(f"  Merkle Root: {tree['root']}")
    print("=" * 70 + "\n")
