import re
from typing import Optional
from email_validator import validate_email, EmailNotValidError

class ValidationHelper:
    """Utility class for various validation operations"""
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email format is valid, False otherwise
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    @staticmethod
    def validate_version_format(version: str) -> bool:
        """
        Validate semantic version format (e.g., "1.0.0", "2.1.3-beta")
        
        Args:
            version: Version string to validate
            
        Returns:
            True if version format is valid, False otherwise
        """
        # Semantic versioning pattern
        pattern = r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
        return bool(re.match(pattern, version))
    
    @staticmethod
    def sanitize_string(input_string: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize input string by removing/escaping potentially harmful characters
        
        Args:
            input_string: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not input_string:
            return ""
        
        # Remove or replace potentially harmful characters
        sanitized = input_string.strip()
        
        # Remove null bytes and control characters
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\t\n\r')
        
        # Truncate if max_length is specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def validate_machine_id_format(machine_id: str) -> bool:
        """
        Validate machine ID format
        
        Args:
            machine_id: Machine ID to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        # Should be alphanumeric, 16-64 characters
        if not machine_id or len(machine_id) < 16 or len(machine_id) > 64:
            return False
        
        return bool(re.match(r'^[a-zA-Z0-9]+$', machine_id))
    
    @staticmethod
    def validate_ip_address(ip: str) -> bool:
        """
        Validate IP address format (IPv4 or IPv6)
        
        Args:
            ip: IP address to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        # IPv4 pattern
        ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        
        # IPv6 pattern (simplified)
        ipv6_pattern = r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$'
        
        return bool(re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip))