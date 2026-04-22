"""
block.py - Block Structure & Proof-of-Work Mining for MiniChain

Each block contains:
    Header:
        - previous_hash : Hash of the previous block in the chain
        - timestamp     : Time the block was created
        - nonce         : Number incremented during PoW mining
        - merkle_root   : Root hash of the Merkle tree of transactions
    Body:
        - transactions  : List of Transaction objects confirmed in this block

Mining uses SHA-256 Proof-of-Work: the block hash must start with
a required number of leading zeros (difficulty target).
"""

import hashlib
import json
import time
from typing import List, Optional

from src.transaction import Transaction
from src.merkle_tree import build_merkle_tree


DIFFICULTY = 4          # PoW target: hash must start with this many zeros
DIFFICULTY_TARGET = "0" * DIFFICULTY


class Block:
    """
    Represents a single block in the MiniChain blockchain.

    Attributes:
        index (int)          : Position of the block in the chain (0 = Genesis).
        previous_hash (str)  : Hash of the preceding block.
        timestamp (float)    : Unix timestamp of block creation.
        transactions (list)  : List of Transaction objects inside the block.
        merkle_root (str)    : Merkle root of the transactions.
        nonce (int)          : Value found during Proof-of-Work mining.
        hash (str)           : The valid SHA-256 hash of this block's header.
    """

    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        timestamp: Optional[float] = None,
    ):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.transactions = transactions

        # Build the Merkle tree from the block's transactions
        if transactions:
            tree = build_merkle_tree(transactions)
            self.merkle_root = tree["root"]
        else:
            # Genesis block has no transactions
            self.merkle_root = "0" * 64

        # Nonce starts at 0; incremented during mining
        self.nonce = 0
        # Hash is computed after mining
        self.hash = ""

    def compute_hash(self) -> str:
        """
        Compute the SHA-256 hash of the block header fields.
        The hash covers: index, previous_hash, timestamp, merkle_root, nonce.

        Returns:
            Hex-encoded SHA-256 hash string.
        """
        header = json.dumps(
            {
                "index": self.index,
                "previous_hash": self.previous_hash,
                "timestamp": self.timestamp,
                "merkle_root": self.merkle_root,
                "nonce": self.nonce,
            },
            sort_keys=True,
        )
        return hashlib.sha256(header.encode("utf-8")).hexdigest()

    def mine(self, difficulty: int = DIFFICULTY) -> None:
        """
        Proof-of-Work mining loop.
        Increments the nonce until the block hash starts with `difficulty` zeros.

        Args:
            difficulty: Number of leading zeros required in the hash.
        """
        target = "0" * difficulty
        self.nonce = 0
        self.hash = self.compute_hash()

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()

    def is_valid_proof(self, difficulty: int = DIFFICULTY) -> bool:
        """
        Check whether the block's stored hash satisfies the PoW difficulty target
        and matches the recomputed hash.

        Returns:
            True if valid, False otherwise.
        """
        target = "0" * difficulty
        recomputed = self.compute_hash()
        return self.hash.startswith(target) and self.hash == recomputed

    def to_dict(self) -> dict:
        """Serialize the block to a dictionary (for display)."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "hash": self.hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
        }

    def __repr__(self) -> str:
        return (
            f"Block(index={self.index}, hash={self.hash[:16]}..., "
            f"nonce={self.nonce}, txs={len(self.transactions)})"
        )


# ---------------------------------------------------------------------------
# Genesis Block Factory
# ---------------------------------------------------------------------------

def create_genesis_block() -> Block:
    """
    Generate the Genesis Block — the very first block in the chain.
    It has no previous hash (represented as 64 zeros) and no transactions.

    Returns:
        A mined Block object at index 0.
    """
    genesis = Block(
        index=0,
        transactions=[],
        previous_hash="0" * 64,
        timestamp=0.0,          # Fixed timestamp so genesis hash is deterministic
    )
    genesis.merkle_root = "0" * 64
    genesis.mine()
    return genesis
