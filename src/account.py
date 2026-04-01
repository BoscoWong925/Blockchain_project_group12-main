"""
account.py - Account Creation for MiniChain

Generates blockchain accounts using Elliptic Curve Cryptography (ECC).
Each account holds a private key and a public key (used as the account address).
Algorithm: SECP256K1 (the same curve used in Bitcoin)
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


class Account:
    """
    Represents a blockchain account (wallet).

    Attributes:
        name (str): A human-readable label for the account (e.g., "Alice").
        private_key: The ECC private key object used for signing transactions.
        public_key: The ECC public key object used as the account address.
    """

    def __init__(self, name: str):
        """
        Create a new blockchain account by generating an ECC key pair.

        Args:
            name: A human-readable label for this account.
        """
        self.name = name
        # Generate a private key using the SECP256K1 elliptic curve
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        # Derive the corresponding public key
        self.public_key = self.private_key.public_key()

    def get_address(self) -> str:
        """
        Return the account's public key serialized as a hex string.
        This hex string serves as the user's unique blockchain address.

        Returns:
            A hex-encoded string of the compressed public key bytes.
        """
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.CompressedPoint,
        )
        return public_key_bytes.hex()

    def get_private_key_pem(self) -> str:
        """
        Return the private key in PEM format (for display/debugging purposes).

        Returns:
            A PEM-encoded string of the private key.
        """
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pem.decode("utf-8")

    def __repr__(self) -> str:
        return f"Account(name={self.name}, address={self.get_address()[:16]}...)"
