import hashlib
import platform
import uuid
import json
from typing import Dict, Any, Optional

class MachineFingerprint:
    """Utility class for generating machine fingerprints"""
    
    @staticmethod
    def generate_fingerprint(include_mac: bool = True) -> str:
        """
        Generate a unique machine fingerprint
        
        Args:
            include_mac: Whether to include MAC address in fingerprint
            
        Returns:
            32-character hexadecimal machine fingerprint
        """
        system_info = MachineFingerprint._collect_system_info(include_mac)
        
        # Create a consistent string representation
        info_string = json.dumps(system_info, sort_keys=True)
        
        # Generate SHA-256 hash
        fingerprint = hashlib.sha256(info_string.encode('utf-8')).hexdigest()
        
        # Return first 32 characters for brevity
        return fingerprint[:32]
    
    @staticmethod
    def _collect_system_info(include_mac: bool = True) -> Dict[str, Any]:
        """
        Collect system information for fingerprinting
        
        Args:
            include_mac: Whether to include MAC address
            
        Returns:
            Dictionary of system information
        """
        info = {
            'platform': platform.platform(),
            'system': platform.system(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'architecture': platform.architecture()[0],
            'node': platform.node()
        }
        
        # Add MAC address if requested and available
        if include_mac:
            try:
                mac = hex(uuid.getnode())
                info['mac_address'] = mac
            except Exception:
                # If MAC address is not available, use a placeholder
                info['mac_address'] = 'unavailable'
        
        # Add Python version for additional uniqueness
        info['python_version'] = platform.python_version()
        
        return info
    
    @staticmethod
    def validate_fingerprint(fingerprint: str) -> bool:
        """
        Validate that a fingerprint has the correct format
        
        Args:
            fingerprint: The fingerprint to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        # Should be 32 character hexadecimal string
        if len(fingerprint) != 32:
            return False
        
        try:
            int(fingerprint, 16)
            return True
        except ValueError:
            return False 