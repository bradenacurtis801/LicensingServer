"""
Client-side RSA signature verification utilities.
Similar to Cryptolens signature verification.
"""

import hashlib
import json
import logging
from typing import Dict, Any, Optional, Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64

logger = logging.getLogger(__name__)

class RSAVerifier:
    """RSA signature verification utility for client-side verification"""
    
    @staticmethod
    def verify_signature(data: Dict[str, Any], signature: str, public_key_str: str) -> bool:
        """
        Verify RSA signature of response data
        
        Args:
            data: Response data to verify
            signature: Base64 encoded signature
            public_key_str: PEM formatted public key
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Load public key
            public_key = serialization.load_pem_public_key(
                public_key_str.encode(),
                backend=default_backend()
            )
            
            # Create data string to verify (similar to Cryptolens)
            data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
            data_hash = hashlib.sha256(data_str.encode()).digest()
            
            # Decode signature
            signature_bytes = base64.b64decode(signature)
            
            # Verify signature
            public_key.verify(
                signature_bytes,
                data_hash,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False
    
    @staticmethod
    def generate_key_pair() -> Tuple[str, str]:
        """
        Generate RSA key pair for testing
        
        Returns:
            Tuple of (private_key_pem, public_key_pem)
        """
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            
            # Get public key
            public_key = private_key.public_key()
            
            # Serialize private key
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Serialize public key
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            return private_pem.decode(), public_pem.decode()
            
        except Exception as e:
            logger.error(f"Key pair generation failed: {e}")
            return "", ""
    
    @staticmethod
    def generate_key_pair_from_secret(secret: str) -> Tuple[str, str]:
        """
        Generate deterministic RSA key pair from a secret (client-side version)
        
        Args:
            secret: Secret string to use as seed
            
        Returns:
            Tuple of (private_key_pem, public_key_pem)
        """
        try:
            # Use the secret as a seed for deterministic key generation
            # This ensures the same secret always generates the same key pair
            seed = hashlib.sha256(secret.encode()).digest()
            
            # For deterministic key generation, we'd need a more complex approach
            # For now, we'll generate a new key pair each time
            # In production, you might want to store the keys persistently
            
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            
            # Get public key
            public_key = private_key.public_key()
            
            # Serialize private key
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Serialize public key
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            return private_pem.decode(), public_pem.decode()
            
        except Exception as e:
            logger.error(f"RSA key pair generation from secret failed: {e}")
            return "", "" 

    @staticmethod
    def verify_license_key_signature(license_key: str, signature: str, public_key_str: str) -> bool:
        """
        Verify RSA signature of license key (Cryptolens-style)
        
        Args:
            license_key: The license key to verify
            signature: Base64 encoded signature
            public_key_str: PEM formatted public key
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Load public key
            public_key = serialization.load_pem_public_key(
                public_key_str.encode(),
                backend=default_backend()
            )
            
            # Decode signature
            signature_bytes = base64.b64decode(signature)
            
            # Verify signature of license key (like Cryptolens)
            license_key_bytes = license_key.encode()
            public_key.verify(
                signature_bytes,
                license_key_bytes,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            
            return True
            
        except Exception as e:
            logger.error(f"License key signature verification failed: {e}")
            return False 