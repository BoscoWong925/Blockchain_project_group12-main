"""Blockchain container and validation logic."""

import hashlib
from typing import List, Optional, Tuple

from src.account import Account
from src.block import Block, create_genesis_block, DIFFICULTY
from src.merkle_tree import build_merkle_tree
from src.transaction import (
    COINBASE_ADDRESS,
    CoinbaseTransaction,
    Transaction,
)

BLOCK_REWARD = 6.25


class Blockchain:
    """Store blocks and provide mining and validation helpers."""

    def __init__(self, difficulty: int = DIFFICULTY):
        self.difficulty = difficulty
        self.chain: List[Block] = []

        print("Mining genesis block...")
        genesis = create_genesis_block()
        self.chain.append(genesis)
        print(f"Genesis block mined: {genesis.hash}")

    @property
    def last_block(self) -> Block:
        """Return the last block in the chain."""
        return self.chain[-1]

    def add_block(
        self,
        transactions: List[Transaction],
        miner: Optional[Account] = None,
        reward: float = BLOCK_REWARD,
    ) -> Block:
        """Mine a block and append it to the chain."""
        block_txs: List[Transaction] = list(transactions)
        if miner is not None:
            coinbase = CoinbaseTransaction(miner, reward)
            block_txs = [coinbase] + block_txs

        new_block = Block(
            index=len(self.chain),
            transactions=block_txs,
            previous_hash=self.last_block.hash,
        )

        print(f"\nMining block {new_block.index} (difficulty={self.difficulty})...")
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        print(
            f"Block {new_block.index} mined. "
            f"Nonce={new_block.nonce}, Hash={new_block.hash}"
        )

        return new_block

    def is_chain_valid(self) -> Tuple[bool, str]:
        """Check hashes, links, transactions, and Merkle roots."""
        for i in range(len(self.chain) - 1, 0, -1):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if not current.is_valid_proof(self.difficulty):
                return (
                    False,
                    f"Block {current.index} has an invalid hash or broken PoW. "
                    f"Stored: {current.hash[:16]}..., "
                    f"Recomputed: {current.compute_hash()[:16]}...",
                )

            if current.previous_hash != previous.hash:
                return (
                    False,
                    f"Block {current.index} has a broken link. "
                    f"previous_hash field ({current.previous_hash[:16]}...) "
                    f"does not match Block {previous.index}'s hash ({previous.hash[:16]}...).",
                )

            coinbase_positions = [
                idx
                for idx, tx in enumerate(current.transactions)
                if tx.input_address == COINBASE_ADDRESS
            ]
            if len(coinbase_positions) > 1:
                return (
                    False,
                    f"Block {current.index} contains {len(coinbase_positions)} "
                    f"coinbase transactions (at most 1 allowed).",
                )
            if coinbase_positions and coinbase_positions[0] != 0:
                return (
                    False,
                    f"Block {current.index} has a coinbase transaction at "
                    f"position {coinbase_positions[0]}; coinbase must be at "
                    f"position 0.",
                )

            for tx in current.transactions:
                is_coinbase_like = tx.input_address == COINBASE_ADDRESS

                expected_amount_hash = hashlib.sha256(
                    str(tx.amount).encode("utf-8")
                ).hexdigest()
                if tx.amount_hash != expected_amount_hash:
                    return (
                        False,
                        f"Block {current.index} has a transaction with a "
                        f"stale amount_hash. TX ID: {tx.tx_id[:16]}...",
                    )

                if tx.tx_id != tx._calculate_tx_id():
                    return (
                        False,
                        f"Block {current.index} has a transaction whose "
                        f"stored tx_id does not match its current contents. "
                        f"TX ID: {tx.tx_id[:16]}...",
                    )

                if is_coinbase_like:
                    if tx.signature != "":
                        return (
                            False,
                            f"Block {current.index} has a coinbase-like "
                            f"transaction carrying a non-empty signature. "
                            f"TX ID: {tx.tx_id[:16]}...",
                        )
                else:
                    if not tx.verify_signature():
                        return (
                            False,
                            f"Block {current.index} contains a transaction "
                            f"with an invalid signature! TX ID: "
                            f"{tx.tx_id[:16]}...",
                        )

            if current.transactions:
                recomputed_root = build_merkle_tree(current.transactions)["root"]
                if recomputed_root != current.merkle_root:
                    return (
                        False,
                        f"Block {current.index} has a stale merkle_root. "
                        f"Stored: {current.merkle_root[:16]}..., "
                        f"Recomputed: {recomputed_root[:16]}...",
                    )

        genesis = self.chain[0]
        if genesis.hash != genesis.compute_hash():
            return (False, "Genesis block hash has been tampered with.")

        return (True, "Blockchain is valid.")

    def get_balance(self, address: str) -> float:
        """Compute the balance of one address by scanning the whole chain."""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.output_address == address:
                    balance += tx.amount
                if tx.input_address == address:
                    balance -= tx.amount
        return balance

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
                        f"      - {sender_label} -> {receiver_label}  |  "
                        f"{tx.amount} coins  |  TX: {tx.tx_id[:16]}..."
                    )
            else:
                print("    Transactions : (none - genesis block)")
        print("\n" + "=" * 70)
