"""Account helpers."""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


class Account:
    """Simple account backed by an ECC key pair."""

    def __init__(self, name: str):
        """Create an account with a new SECP256K1 key pair."""
        self.name = name
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()

    def get_address(self) -> str:
        """Return the compressed public key as a hex string."""
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.CompressedPoint,
        )
        return public_key_bytes.hex()

    def get_private_key_pem(self) -> str:
        """Return the private key in PEM format."""
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pem.decode("utf-8")

    def __repr__(self) -> str:
        return f"Account(name={self.name}, address={self.get_address()[:16]}...)"
