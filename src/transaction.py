"""Transaction models."""

import hashlib
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from src.account import Account


class Transaction:
    """Represent a signed transfer from one account to another."""

    def __init__(self, sender: Account, receiver: Account, amount: float):
        """Create and sign a transaction."""
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

        self.amount_hash = hashlib.sha256(str(amount).encode("utf-8")).hexdigest()
        self.input_address = sender.get_address()
        self.output_address = receiver.get_address()
        self.signature = self._sign_transaction()
        self.tx_id = self._calculate_tx_id()

    def _get_signable_data(self) -> bytes:
        """Return the byte string covered by the signature."""
        data_string = (
            f"{self.input_address}{self.output_address}"
            f"{self.amount}{self.amount_hash}"
        )
        return data_string.encode("utf-8")

    def _sign_transaction(self) -> str:
        """Sign the transaction with the sender's private key."""
        signable_data = self._get_signable_data()
        signature_bytes = self.sender.private_key.sign(
            signable_data,
            ec.ECDSA(hashes.SHA256()),
        )
        return signature_bytes.hex()

    def _calculate_tx_id(self) -> str:
        """Hash the transaction contents to produce a stable transaction ID."""
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
        """Check the stored signature against the sender's public key."""
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
        """Return a dictionary form of the transaction."""
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

COINBASE_ADDRESS = "COINBASE"


class CoinbaseTransaction(Transaction):
    """Special transaction used to pay a miner a block reward."""

    def __init__(self, miner, reward: float):
        self.sender = None
        self.receiver = miner
        self.amount = reward
        self.amount_hash = hashlib.sha256(str(reward).encode("utf-8")).hexdigest()

        self.input_address = COINBASE_ADDRESS
        self.output_address = miner.get_address()

        self.signature = ""
        self.tx_id = self._calculate_tx_id()

    def verify_signature(self) -> bool:
        return True

    def __repr__(self) -> str:
        return (
            f"CoinbaseTransaction(id={self.tx_id[:16]}..., "
            f"to={self.receiver.name}, reward={self.amount})"
        )
