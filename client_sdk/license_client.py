#!/usr/bin/env python3
"""
License Management Client SDK
"""
import requests
import json
import hashlib
import platform
import uuid
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

class LicenseStatus(Enum):
    """License status enumeration"""
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"

class ActivationStatus(Enum):
    """Activation status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class LicenseInfo:
    """License information container"""
    license_id: int
    customer_id: int
    application_id: int
    status: LicenseStatus
    expires_at: Optional[str]
    features: Dict[str, Any]
    remaining_activations: int
    message: str

@dataclass
class ActivationFormInfo:
    """Activation form information container"""
    id: int
    request_code: str
    machine_id: str
    machine_name: Optional[str]
    expires_at: str
    status: str

from .utils.machine_fingerprint import MachineFingerprint

class LicenseClient:
    """Main license client for interacting with the license server"""
    
    def __init__(self, server_url: str, app_name: str, app_version: str):
        """
        Initialize the license client
        
        Args:
            server_url: URL of the license server
            app_name: Name of the application
            app_version: Version of the application
        """
        self.server_url = server_url.rstrip('/')
        self.app_name = app_name
        self.app_version = app_version
        self.machine_id = MachineFingerprint.generate_fingerprint()
        self._license_cache = {}
        self._last_validation = 0
        self._cache_duration = 300  # 5 minutes cache
        
    def register_application(self, description: str = None, features: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Register the application with the license server
        
        Args:
            description: Application description
            features: Dictionary of available features
            
        Returns:
            Application registration response
        """
        app_data = {
            "name": self.app_name,
            "version": self.app_version,
            "description": description or f"{self.app_name} {self.app_version}",
            "features": features or {}
        }
        
        response = requests.post(
            f"{self.server_url}/api/v1/applications/",
            json=app_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to register application: {response.text}")
    
    def validate_license(self, license_key: str, force_refresh: bool = False) -> LicenseInfo:
        """
        Validate a license key
        
        Args:
            license_key: The license key to validate
            force_refresh: Force refresh the cache
            
        Returns:
            LicenseInfo object with validation results
        """
        # Check cache first
        cache_key = f"{license_key}_{self.machine_id}"
        current_time = time.time()
        
        if not force_refresh and cache_key in self._license_cache:
            cached_data = self._license_cache[cache_key]
            if current_time - cached_data['timestamp'] < self._cache_duration:
                return cached_data['license_info']
        
        # Perform validation
        validation_data = {
            "license_key": license_key,
            "machine_id": self.machine_id
        }
        
        response = requests.post(
            f"{self.server_url}/api/v1/validate/",
            json=validation_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            license_info = LicenseInfo(
                license_id=data.get('license_id'),
                customer_id=data.get('customer_id'),
                application_id=data.get('application_id'),
                status=LicenseStatus(data.get('status', 'unknown')),
                expires_at=data.get('expires_at'),
                features=data.get('features', {}),
                remaining_activations=data.get('remaining_activations', 0),
                message=data.get('message', '')
            )
            
            # Cache the result
            self._license_cache[cache_key] = {
                'license_info': license_info,
                'timestamp': current_time
            }
            
            return license_info
        else:
            raise Exception(f"License validation failed: {response.text}")
    
    def create_activation_request(self, license_key: str, machine_name: str = None) -> ActivationFormInfo:
        """
        Create an activation form request for offline activation
        
        Args:
            license_key: The license key to activate
            machine_name: Optional machine name
            
        Returns:
            ActivationFormInfo object
        """
        form_data = {
            "license_key": license_key,
            "machine_id": self.machine_id,
            "machine_name": machine_name or f"{self.app_name} Machine"
        }
        
        response = requests.post(
            f"{self.server_url}/api/v1/activation-forms/",
            json=form_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            return ActivationFormInfo(
                id=data['id'],
                request_code=data['request_code'],
                machine_id=data['machine_id'],
                machine_name=data['machine_name'],
                expires_at=data['expires_at'],
                status=data['status']
            )
        else:
            raise Exception(f"Failed to create activation request: {response.text}")
    
    def complete_activation(self, request_code: str, activation_code: str) -> ActivationFormInfo:
        """
        Complete an activation form with an activation code
        
        Args:
            request_code: The request code from create_activation_request
            activation_code: The activation code from the admin
            
        Returns:
            ActivationFormInfo object
        """
        complete_data = {
            "request_code": request_code,
            "activation_code": activation_code
        }
        
        response = requests.post(
            f"{self.server_url}/api/v1/activation-forms/complete",
            json=complete_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            return ActivationFormInfo(
                id=data['id'],
                request_code=data['request_code'],
                machine_id=data['machine_id'],
                machine_name=data['machine_name'],
                expires_at=data['expires_at'],
                status=data['status']
            )
        else:
            raise Exception(f"Failed to complete activation: {response.text}")
    
    def is_feature_enabled(self, license_key: str, feature_name: str) -> bool:
        """
        Check if a specific feature is enabled for the license
        
        Args:
            license_key: The license key to check
            feature_name: The name of the feature to check
            
        Returns:
            True if the feature is enabled, False otherwise
        """
        try:
            license_info = self.validate_license(license_key)
            return license_info.features.get(feature_name, False)
        except Exception:
            return False
    
    def get_available_features(self, license_key: str) -> Dict[str, Any]:
        """
        Get all available features for a license
        
        Args:
            license_key: The license key to check
            
        Returns:
            Dictionary of available features
        """
        try:
            license_info = self.validate_license(license_key)
            return license_info.features
        except Exception:
            return {}
    
    def is_license_valid(self, license_key: str) -> bool:
        """
        Check if a license is valid
        
        Args:
            license_key: The license key to check
            
        Returns:
            True if the license is valid, False otherwise
        """
        try:
            license_info = self.validate_license(license_key)
            return license_info.status == LicenseStatus.ACTIVE
        except Exception:
            return False
    
    def clear_cache(self):
        """Clear the license validation cache"""
        self._license_cache.clear()
    
    def set_cache_duration(self, seconds: int):
        """
        Set the cache duration for license validation
        
        Args:
            seconds: Cache duration in seconds
        """
        self._cache_duration = seconds

class FeatureManager:
    """Feature management utility for restricting application features"""
    
    def __init__(self, license_client: LicenseClient):
        """
        Initialize the feature manager
        
        Args:
            license_client: The license client instance
        """
        self.license_client = license_client
        self._license_key = None
        self._features = {}
    
    def set_license_key(self, license_key: str):
        """
        Set the license key for feature checking
        
        Args:
            license_key: The license key to use
        """
        self._license_key = license_key
        self._features = self.license_client.get_available_features(license_key)
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a feature is enabled
        
        Args:
            feature_name: The name of the feature to check
            
        Returns:
            True if the feature is enabled, False otherwise
        """
        if not self._license_key:
            return False
        
        return self._features.get(feature_name, False)
    
    def require_feature(self, feature_name: str):
        """
        Decorator to require a specific feature
        
        Args:
            feature_name: The name of the feature required
            
        Returns:
            Decorator function
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.is_feature_enabled(feature_name):
                    raise FeatureNotEnabledError(f"Feature '{feature_name}' is not enabled for this license")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def get_enabled_features(self) -> List[str]:
        """
        Get list of enabled features
        
        Returns:
            List of enabled feature names
        """
        return [name for name, enabled in self._features.items() if enabled]
    
    def get_disabled_features(self) -> List[str]:
        """
        Get list of disabled features
        
        Returns:
            List of disabled feature names
        """
        return [name for name, enabled in self._features.items() if not enabled]

class FeatureNotEnabledError(Exception):
    """Exception raised when a required feature is not enabled"""
    pass

class LicenseValidationError(Exception):
    """Exception raised when license validation fails"""
    pass
