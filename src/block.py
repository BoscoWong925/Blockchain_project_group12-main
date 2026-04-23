"""Block model and proof-of-work helpers."""

import hashlib
import json
import time
from typing import List, Optional

from src.transaction import Transaction
from src.merkle_tree import build_merkle_tree


DIFFICULTY = 4


class Block:
    """Represent one block in the chain."""

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

        if transactions:
            self.merkle_root = build_merkle_tree(transactions)["root"]
        else:
            self.merkle_root = "0" * 64

        self.nonce = 0
        self.hash = ""

    def compute_hash(self) -> str:
        """Hash the block header."""
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
        """Update the nonce until the hash matches the difficulty target."""
        target = "0" * difficulty
        self.nonce = 0
        self.hash = self.compute_hash()

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()

    def is_valid_proof(self, difficulty: int = DIFFICULTY) -> bool:
        """Return True when the stored hash still satisfies proof of work."""
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


def create_genesis_block() -> Block:
    """Create the fixed genesis block."""
    genesis = Block(
        index=0,
        transactions=[],
        previous_hash="0" * 64,
        timestamp=0.0,
    )
    genesis.merkle_root = "0" * 64
    genesis.mine()
    return genesis
