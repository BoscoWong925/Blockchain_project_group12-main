"""
transaction.py - SISO Transaction Generation for MiniChain

Implements Single-Input-Single-Output (SISO) transactions.
Each transaction contains:
    1. Transaction ID  - SHA-256 hash of the transaction contents
    2. Input           - Sender's public key (address)
    3. Output          - Receiver's public key (address)
    4. Data            - { amount, amount_hash } where amount_hash = SHA-256(amount)
                         (per spec §5.1: "amount of virtual coins AND the
                         crypto-hash of the amount of virtual coins")
    5. Signature       - Digital signature created with sender's private key
"""

import hashlib
import json

from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes, serialization

from src.account import Account


class Transaction:
    """
    Represents a Single-Input-Single-Output (SISO) blockchain transaction.

    Attributes:
        sender (Account): The account sending the coins.
        receiver (Account): The account receiving the coins.
        amount (float): The number of virtual coins being transferred.
        input_address (str): The sender's public key hex string (address).
        output_address (str): The receiver's public key hex string (address).
        signature (str): Hex-encoded digital signature of the transaction details.
        tx_id (str): The unique transaction ID (SHA-256 hash of tx contents).
    """

    def __init__(self, sender: Account, receiver: Account, amount: float):
        """
        Create and sign a new SISO transaction.

        Args:
            sender: The Account object of the sender.
            receiver: The Account object of the receiver.
            amount: The number of virtual coins to transfer.
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

        # Data field (spec §5.1): amount + SHA-256(amount)
        self.amount_hash = hashlib.sha256(str(amount).encode("utf-8")).hexdigest()

        # Input: sender's address (public key)
        self.input_address = sender.get_address()
        # Output: receiver's address (public key)
        self.output_address = receiver.get_address()

        # Sign the transaction details with the sender's private key
        self.signature = self._sign_transaction()

        # Calculate the unique Transaction ID (hash of all contents)
        self.tx_id = self._calculate_tx_id()

    def _get_signable_data(self) -> bytes:
        """
        Build the byte string of transaction details to be signed.
        Combines sender address + receiver address + amount into a single string.

        Returns:
            UTF-8 encoded bytes of the combined transaction data.
        """
        # Include amount_hash so signature covers the full data field (§5.1)
        data_string = (
            f"{self.input_address}{self.output_address}"
            f"{self.amount}{self.amount_hash}"
        )
        return data_string.encode("utf-8")

    def _sign_transaction(self) -> str:
        """
        Sign the transaction data using the sender's ECC private key (ECDSA).

        Returns:
            Hex-encoded string of the digital signature.
        """
        signable_data = self._get_signable_data()
        signature_bytes = self.sender.private_key.sign(
            signable_data,
            ec.ECDSA(hashes.SHA256()),
        )
        return signature_bytes.hex()

    def _calculate_tx_id(self) -> str:
        """
        Calculate the Transaction ID by hashing the full transaction contents
        (input, output, data/amount, signature) with SHA-256.

        Returns:
            A hex-encoded SHA-256 hash string serving as the transaction ID.
        """
        tx_contents = json.dumps(
            {
                "input": self.input_address,
                "output": self.output_address,
                "amount": self.amount,
                "amount_hash": self.amount_hash,
                "signature": self.signature,
            },
            sort_keys=True,
        )
        return hashlib.sha256(tx_contents.encode("utf-8")).hexdigest()

    def verify_signature(self) -> bool:
        """
        Verify the transaction's digital signature using the sender's public key.

        Returns:
            True if the signature is valid, False otherwise.
        """
        signable_data = self._get_signable_data()
        signature_bytes = bytes.fromhex(self.signature)
        try:
            self.sender.public_key.verify(
                signature_bytes,
                signable_data,
                ec.ECDSA(hashes.SHA256()),
            )
            return True
        except Exception:
            return False

    def to_dict(self) -> dict:
        """
        Serialize the transaction into a dictionary for display/storage.

        Returns:
            A dictionary containing all transaction fields.
        """
        return {
            "tx_id": self.tx_id,
            "input": self.input_address,
            "output": self.output_address,
            "amount": self.amount,
            "amount_hash": self.amount_hash,
            "signature": self.signature,
        }

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.tx_id[:16]}..., "
            f"from={self.sender.name}, to={self.receiver.name}, "
            f"amount={self.amount})"
        )


# ---------------------------------------------------------------------------
# Coinbase transaction (BONUS — Lectures 05 & 06)
# ---------------------------------------------------------------------------

COINBASE_ADDRESS = "COINBASE"  # sentinel sender address for newly minted coins


class CoinbaseTransaction(Transaction):
    """
    A coinbase transaction creates new coins and pays them to a miner.
    It has no real sender, so it is not ECDSA-signed; it is trusted by virtue
    of being the first transaction in a block (see Lecture 05, §"Block
    Subsidy / Coinbase Transaction").

    For simplicity, this class reuses the Transaction serialisation format
    but sets:
        - input_address = COINBASE_ADDRESS
        - signature     = "" (empty)
        - verify_signature() returns True unconditionally
    """

    def __init__(self, miner, reward: float):
        self.sender = None
        self.receiver = miner
        self.amount = reward
        self.amount_hash = hashlib.sha256(str(reward).encode("utf-8")).hexdigest()

        self.input_address = COINBASE_ADDRESS
        self.output_address = miner.get_address()

        self.signature = ""  # coinbase has no ECDSA signature
        self.tx_id = self._calculate_tx_id()

    def verify_signature(self) -> bool:
        # Coinbase transactions are valid by protocol, not by signature.
        return True

    def __repr__(self) -> str:
        return (
            f"CoinbaseTransaction(id={self.tx_id[:16]}..., "
            f"to={self.receiver.name}, reward={self.amount})"
        )
