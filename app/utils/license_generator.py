import secrets
import hashlib
import re
from typing import Optional
from app.config import settings

class LicenseKeyGenerator:
    """Utility class for generating and validating license keys"""
    
    def __init__(self, key_length: int = None):
        self.key_length = key_length or settings.license_key_length
    
    def generate_key(self) -> str:
        """
        Generate a secure random license key
        
        Returns:
            Formatted license key (e.g., "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY")
        """
        # Generate random bytes and convert to alphanumeric string
        # Using base32 encoding to avoid confusing characters (0, O, 1, I, etc.)
        key_bytes = secrets.token_bytes(self.key_length)
        
        # Create a clean alphanumeric string
        raw_key = secrets.token_urlsafe(self.key_length * 2)
        # Remove special characters and make uppercase
        clean_key = re.sub(r'[^A-Za-z0-9]', '', raw_key).upper()
        
        # Ensure we have enough characters
        while len(clean_key) < self.key_length:
            additional = secrets.token_urlsafe(10)
            clean_key += re.sub(r'[^A-Za-z0-9]', '', additional).upper()
        
        # Trim to exact length
        key = clean_key[:self.key_length]
        
        # Format with dashes (5 character groups)
        formatted_key = '-'.join([key[i:i+5] for i in range(0, len(key), 5)])
        
        return formatted_key
    
    def hash_key(self, key: str) -> str:
        """
        Create a SHA-256 hash of the license key for database storage
        
        Args:
            key: The original license key
            
        Returns:
            SHA-256 hash of the key
        """
        return hashlib.sha256(key.encode('utf-8')).hexdigest()
    
    def validate_key_format(self, key: str) -> bool:
        """
        Validate that a license key has the correct format
        
        Args:
            key: The license key to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        # Remove dashes for validation
        clean_key = key.replace('-', '').replace(' ', '')
        
        # Check length and that it's alphanumeric
        if len(clean_key) != self.key_length:
            return False
        
        if not clean_key.isalnum():
            return False
        
        # Check format pattern (groups of 5 separated by dashes)
        expected_pattern = r'^[A-Z0-9]{5}(-[A-Z0-9]{5})*$'
        return bool(re.match(expected_pattern, key.upper()))
    
    def normalize_key(self, key: str) -> str:
        """
        Normalize a license key by removing spaces and converting to uppercase
        
        Args:
            key: The license key to normalize
            
        Returns:
            Normalized license key
        """
        return key.replace(' ', '').upper()