"""
blockchain.py - Blockchain Construction & Integrity Verification for MiniChain

The Blockchain class manages:
    - A growing chain of Block objects starting with the Genesis Block.
    - Adding new mined blocks to the chain.
    - Integrity verification via is_chain_valid() which detects any tampering.
"""

import hashlib
from typing import List, Tuple

from src.account import Account
from src.block import Block, create_genesis_block, DIFFICULTY
from src.merkle_tree import build_merkle_tree
from src.transaction import (
    COINBASE_ADDRESS,
    CoinbaseTransaction,
    Transaction,
)


# BONUS: block reward (Lectures 05 & 06). Paid to the miner via a coinbase tx.
BLOCK_REWARD = 6.25


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

    def add_block(
        self,
        transactions: List[Transaction],
        miner: "Account | None" = None,
        reward: float = BLOCK_REWARD,
    ) -> Block:
        """
        Create, mine, and append a new block containing the given transactions.

        Args:
            transactions: List of Transaction objects to include.
                          Combined with the optional coinbase, the total
                          must be a power of 2 (Merkle Tree requirement).
            miner:        If provided, a CoinbaseTransaction paying `reward`
                          to this account is prepended to the block
                          (BONUS — Lectures 05 & 06).
            reward:       Coinbase reward amount. Defaults to BLOCK_REWARD.

        Returns:
            The newly mined and added Block.
        """
        block_txs: List[Transaction] = list(transactions)
        if miner is not None:
            coinbase = CoinbaseTransaction(miner, reward)
            block_txs = [coinbase] + block_txs

        new_block = Block(
            index=len(self.chain),
            transactions=block_txs,
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

        Layered checks, applied to every non-Genesis block:
          1. Block header self-consistency: stored hash == compute_hash()
             and satisfies the PoW difficulty target.
          2. Hash-link integrity: block.previous_hash == previous block's
             stored hash.
          3. Block-body integrity (NEW):
             a. At most one coinbase-like transaction per block, and if
                present it must sit at position 0.
             b. Each transaction is internally consistent:
                - stored tx_id equals SHA-256 of its current contents;
                - amount_hash equals SHA-256(str(amount));
                - coinbase-like transactions carry an empty signature and
                  input_address == COINBASE_ADDRESS;
                - normal transactions verify under ECDSA.
             c. The block's stored merkle_root equals the root of a tree
                rebuilt from the block's current transactions.
          4. Genesis self-consistency: stored hash equals its recomputed
             hash.

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

            # --- Check 3a: Coinbase structural rules ---
            coinbase_positions = [
                idx
                for idx, tx in enumerate(current.transactions)
                if tx.input_address == COINBASE_ADDRESS
            ]
            if len(coinbase_positions) > 1:
                return (
                    False,
                    f"❌ Block {current.index} contains {len(coinbase_positions)} "
                    f"coinbase transactions (at most 1 allowed).",
                )
            if coinbase_positions and coinbase_positions[0] != 0:
                return (
                    False,
                    f"❌ Block {current.index} has a coinbase transaction at "
                    f"position {coinbase_positions[0]}; coinbase must be at "
                    f"position 0.",
                )

            # --- Check 3b: Per-transaction field consistency ---
            for tx in current.transactions:
                is_coinbase_like = tx.input_address == COINBASE_ADDRESS

                # amount_hash must match SHA-256(str(amount))
                expected_amount_hash = hashlib.sha256(
                    str(tx.amount).encode("utf-8")
                ).hexdigest()
                if tx.amount_hash != expected_amount_hash:
                    return (
                        False,
                        f"❌ Block {current.index} has a transaction with a "
                        f"stale amount_hash. TX ID: {tx.tx_id[:16]}...",
                    )

                # tx_id must match a fresh recomputation of current contents
                if tx.tx_id != tx._calculate_tx_id():
                    return (
                        False,
                        f"❌ Block {current.index} has a transaction whose "
                        f"stored tx_id does not match its current contents. "
                        f"TX ID: {tx.tx_id[:16]}...",
                    )

                if is_coinbase_like:
                    # Coinbase must be structurally self-consistent.
                    if tx.signature != "":
                        return (
                            False,
                            f"❌ Block {current.index} has a coinbase-like "
                            f"transaction carrying a non-empty signature. "
                            f"TX ID: {tx.tx_id[:16]}...",
                        )
                else:
                    # Normal transactions must pass ECDSA verification.
                    if not tx.verify_signature():
                        return (
                            False,
                            f"❌ Block {current.index} contains a transaction "
                            f"with an invalid signature! TX ID: "
                            f"{tx.tx_id[:16]}...",
                        )

            # --- Check 3c: Merkle root matches current transactions ---
            if current.transactions:
                recomputed_root = build_merkle_tree(current.transactions)["root"]
                if recomputed_root != current.merkle_root:
                    return (
                        False,
                        f"❌ Block {current.index} has a stale merkle_root. "
                        f"Stored: {current.merkle_root[:16]}..., "
                        f"Recomputed: {recomputed_root[:16]}...",
                    )

        # --- Check 4: Genesis Block self-consistency ---
        genesis = self.chain[0]
        if genesis.hash != genesis.compute_hash():
            return (False, "❌ Genesis Block hash has been tampered with!")

        return (True, "✅ Blockchain is valid. All blocks and transactions are intact.")

    # ------------------------------------------------------------------
    # Ledger queries (BONUS — Lecture 06)
    # ------------------------------------------------------------------

    def get_balance(self, address: str) -> float:
        """
        Compute the balance of an address by walking the entire chain.

        For each transaction in every block:
          - credit the receiver (output_address) with `amount`
          - debit the sender (input_address) with `amount`

        Coinbase transactions only credit the miner; their sentinel
        input_address (COINBASE_ADDRESS) never matches a real public-key
        address, so no account is debited for newly minted coins.

        Args:
            address: hex public-key address (as returned by Account.get_address()).

        Returns:
            Net balance (float). May be negative if the query address sent
            more than it received (MiniChain does not enforce non-negative
            balances at mining time — this is a SISO simplification).
        """
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.output_address == address:
                    balance += tx.amount
                if tx.input_address == address:
                    balance -= tx.amount
        return balance

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
                    sender_label = (
                        tx.sender.name
                        if getattr(tx, "sender", None) is not None
                        else "COINBASE"
                    )
                    receiver_label = (
                        tx.receiver.name
                        if getattr(tx, "receiver", None) is not None
                        else tx.output_address[:16] + "..."
                    )
                    print(
                        f"      - {sender_label} → {receiver_label}  |  "
                        f"{tx.amount} coins  |  TX: {tx.tx_id[:16]}..."
                    )
            else:
                print(f"    Transactions : (none — Genesis Block)")
        print("\n" + "=" * 70)
