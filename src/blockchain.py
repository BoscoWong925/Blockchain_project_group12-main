"""
blockchain.py - Blockchain Construction & Integrity Verification for MiniChain

The Blockchain class manages:
    - A growing chain of Block objects starting with the Genesis Block.
    - Adding new mined blocks to the chain.
    - Integrity verification via is_chain_valid() which detects any tampering.
"""

from typing import List, Tuple

from src.block import Block, create_genesis_block, DIFFICULTY
from src.transaction import Transaction


class Blockchain:
    """
    Represents the MiniChain blockchain.

    Attributes:
        chain (List[Block]): The ordered list of blocks, starting with Genesis.
        difficulty (int)   : The PoW difficulty level applied to all blocks.
    """

    def __init__(self, difficulty: int = DIFFICULTY):
        self.difficulty = difficulty
        self.chain: List[Block] = []

        # Create and append the Genesis Block automatically
        print("  ⛏️  Mining Genesis Block...")
        genesis = create_genesis_block()
        self.chain.append(genesis)
        print(f"  ✅ Genesis Block mined! Hash: {genesis.hash}")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def last_block(self) -> Block:
        """Return the most recently added block."""
        return self.chain[-1]

    # ------------------------------------------------------------------
    # Adding Blocks
    # ------------------------------------------------------------------

    def add_block(self, transactions: List[Transaction]) -> Block:
        """
        Create, mine, and append a new block containing the given transactions.

        Args:
            transactions: List of Transaction objects to include.
                          Length must be a power of 2 (Merkle Tree requirement).

        Returns:
            The newly mined and added Block.
        """
        new_block = Block(
            index=len(self.chain),
            transactions=transactions,
            previous_hash=self.last_block.hash,
        )

        print(f"\n  ⛏️  Mining Block {new_block.index} (difficulty={self.difficulty})...")
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        print(f"  ✅ Block {new_block.index} mined! Nonce={new_block.nonce}, Hash={new_block.hash}")

        return new_block

    # ------------------------------------------------------------------
    # Integrity Verification
    # ------------------------------------------------------------------

    def is_chain_valid(self) -> Tuple[bool, str]:
        """
        Verify the integrity of the entire blockchain.

        Iterates from the last block back to the Genesis Block and checks:
          1. The block's stored hash matches its recomputed hash (PoW check).
          2. The previous_hash field matches the actual hash of the prior block.
          3. Every transaction signature in the block is valid.

        Returns:
            A tuple (is_valid: bool, message: str) describing the result.
        """
        for i in range(len(self.chain) - 1, 0, -1):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # --- Check 1: Block's own hash is still valid (PoW) ---
            if not current.is_valid_proof(self.difficulty):
                return (
                    False,
                    f"❌ Block {current.index} has an invalid hash or broken PoW. "
                    f"Stored: {current.hash[:16]}..., "
                    f"Recomputed: {current.compute_hash()[:16]}...",
                )

            # --- Check 2: Previous hash link is intact ---
            if current.previous_hash != previous.hash:
                return (
                    False,
                    f"❌ Block {current.index} has a broken link! "
                    f"previous_hash field ({current.previous_hash[:16]}...) "
                    f"does not match Block {previous.index}'s hash ({previous.hash[:16]}...).",
                )

            # --- Check 3: All transaction signatures are valid ---
            for tx in current.transactions:
                if not tx.verify_signature():
                    return (
                        False,
                        f"❌ Block {current.index} contains a transaction with an "
                        f"invalid signature! TX ID: {tx.tx_id[:16]}...",
                    )

        # Also verify the Genesis Block's own hash
        genesis = self.chain[0]
        if genesis.hash != genesis.compute_hash():
            return (False, "❌ Genesis Block hash has been tampered with!")

        return (True, "✅ Blockchain is valid. All blocks and transactions are intact.")

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def print_chain(self) -> None:
        """Pretty-print every block in the chain."""
        print("\n" + "=" * 70)
        print("                     BLOCKCHAIN STATE")
        print("=" * 70)
        for block in self.chain:
            label = "Genesis Block" if block.index == 0 else f"Block {block.index}"
            print(f"\n  [{label}]")
            print(f"    Index        : {block.index}")
            print(f"    Timestamp    : {block.timestamp}")
            print(f"    Prev Hash    : {block.previous_hash[:32]}...")
            print(f"    Merkle Root  : {block.merkle_root[:32]}...")
            print(f"    Nonce        : {block.nonce}")
            print(f"    Hash         : {block.hash}")
            if block.transactions:
                print(f"    Transactions : {len(block.transactions)}")
                for tx in block.transactions:
                    print(f"      - {tx.sender.name} → {tx.receiver.name}  |  {tx.amount} coins  |  TX: {tx.tx_id[:16]}...")
            else:
                print(f"    Transactions : (none — Genesis Block)")
        print("\n" + "=" * 70)
