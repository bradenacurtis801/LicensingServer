import platform
import uuid
import sys
import requests
import json
from typing import Optional, Dict, Any, Tuple
from urllib.error import URLError, HTTPError
from .internal import LicenseServerHelpers
from .models import *

class LicenseKey:
    
    """
    License key related methods adapted for your license server.
    """
    
    # Default server URL - can be overridden
    DEFAULT_SERVER_URL = "http://localhost:8999"
    
    # Default public key in XML format (matching private.pem in root)
    DEFAULT_PUBLIC_KEY = "<RSAKeyValue><Modulus>wVjDQCO05mCNDTgBMuCOXyFaQrxAwbpOS8NQ6pDDIBrrZqqhDZbrIWqM11P6tQsZ+ZoLbg+ZSRtBo/D9KEC61HkVrW6pP3GdOrvTpj/eOMKJAwaVnCLG8/PbnQz1u7FU9nadLRczW8YJ1fkPCtSL/3Uugfg8VRf/IaNPb2XxN3h8BfdAsqxv+Gtk7SbyPQRn3JDw338gwMO8b1f6rCc5SJKsF7vfihrQNbcqdr4OwPOScDhtriAuGlIHWXAz9K4W6KeLtqnjbRbXgFZOt5ROz2IojVlkRsahNQxrbpyaLjgDiuqcsjv5hj+n79uu7/r6jB28ztyqSHGjmHe+vlZ3PQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    
    @staticmethod
    def activate(server_url: str = None, license_key: str = None, machine_code: str = None, 
                 fields_to_return: int = 0, metadata: bool = False, 
                 floating_time_interval: int = 0, max_overdraft: int = 0, 
                 friendly_name: str = None, sign: bool = True, sign_method: int = 1) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Activate a license key with your license server (Cryptolens-compatible).
        
        Args:
            server_url: URL of your license server
            license_key: The license key to activate
            machine_code: Machine identifier (optional, will be generated if not provided)
            app_name: Application name
            app_version: Application version
            fields_to_return: Fields to return in response
            metadata: Include metadata in response
            floating_time_interval: Floating time interval
            max_overdraft: Max overdraft
            friendly_name: Friendly name for the activation
            sign: Whether to sign the response
            sign_method: Signature method
            
        Returns:
            Tuple of (license_info, message). If successful, license_info contains the license data.
            If failed, license_info is None and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        if machine_code is None:
            machine_code = Helpers.GetMachineCode(v=2)
        
        try:
            # Prepare activation data (Cryptolens-compatible)
            data = {
                "license_key": license_key,
                "machine_id": machine_code
            }
            
            # Add optional fields
            if fields_to_return:
                data["fields_to_return"] = fields_to_return
            if metadata:
                data["metadata"] = metadata
            if floating_time_interval:
                data["floating_time_interval"] = floating_time_interval
            if max_overdraft:
                data["max_overdraft"] = max_overdraft
            if friendly_name:
                data["friendly_name"] = friendly_name
            if sign:
                data["sign"] = sign
            if sign_method:
                data["sign_method"] = sign_method
            
            # Send activation request
            url = f"{server_url.rstrip('/')}/api/v1/activations/"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("valid", False):
                return (result, "")
            else:
                return (None, result.get("message", "Activation failed"))
                
        except requests.exceptions.RequestException as e:
            return (None, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (None, f"An error occurred: {str(e)}")
    
    @staticmethod
    def validate(server_url: str = None, license_key: str = None, machine_code: str = None) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Validate a license key with your license server.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to validate
            machine_code: Machine identifier (optional, will be generated if not provided)
            
        Returns:
            Tuple of (license_info, message). If successful, license_info contains the license data.
            If failed, license_info is None and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        if machine_code is None:
            machine_code = Helpers.GetMachineCode(v=2)
        
        try:
            # Prepare validation data
            data = {
                "license_key": license_key,
                "machine_id": machine_code
            }
            
            # Send validation request
            url = f"{server_url.rstrip('/')}/api/v1/validate/"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("valid", False):
                return (result, "")
            else:
                return (None, result.get("message", "Validation failed"))
                
        except requests.exceptions.RequestException as e:
            return (None, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (None, f"An error occurred: {str(e)}")
     
    @staticmethod
    def deactivate(server_url: str = None, license_key: str = None, machine_code: str = None) -> Tuple[bool, str]:
        """
        Deactivate a license key with your license server.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to deactivate
            machine_code: Machine identifier (optional, will be generated if not provided)
            
        Returns:
            Tuple of (success, message). If successful, success is True.
            If failed, success is False and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        if machine_code is None:
            machine_code = Helpers.GetMachineCode(v=2)
        
        try:
            # First, get the license ID from the license key
            license_info, message = LicenseKey.get_key(server_url, license_key)
            if not license_info:
                return (False, "License not found")
            
            license_id = license_info.get("id")
            if not license_id:
                return (False, "Could not determine license ID")
            
            # Prepare deactivation data
            data = {
                "license_key": license_key,
                "machine_id": machine_code
            }
            
            # Send deactivation request to activation service
            url = f"{server_url.rstrip('/')}/api/v1/activations/deactivate"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success", False):
                return (True, "")
            else:
                return (False, result.get("message", "Deactivation failed"))
           
        except requests.exceptions.RequestException as e:
            return (False, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (False, f"An error occurred: {str(e)}")
    
    @staticmethod
    def extend_license(server_url: str = None, license_key: str = None, no_of_days: int = 0) -> Tuple[bool, str]:
        """
        Extend a license by a certain number of days.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to extend
            no_of_days: Number of days to extend the license
            
        Returns:
            Tuple of (success, message). If successful, success is True.
            If failed, success is False and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        try:
            # First, get the license ID from the license key
            license_info, message = LicenseKey.get_key(server_url, license_key)
            if not license_info:
                return (False, "License not found")
            
            license_id = license_info.get("id")
            if not license_id:
                return (False, "Could not determine license ID")
            
            # Prepare extension data
            data = {
                "no_of_days": no_of_days
            }
            
            # Send extension request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/{license_id}/extend"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success", False):
                return (True, "")
            else:
                return (False, result.get("message", "License extension failed"))
                
        except requests.exceptions.RequestException as e:
            return (False, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (False, f"An error occurred: {str(e)}")
    
    @staticmethod
    def unblock_key(server_url: str = None, license_key: str = None) -> Tuple[bool, str]:
        """
        Unblock a license key so it can be activated.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to unblock
            
        Returns:
            Tuple of (success, message). If successful, success is True.
            If failed, success is False and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        try:
            # First, get the license ID from the license key
            license_info, message = LicenseKey.get_key(server_url, license_key)
            if not license_info:
                return (False, "License not found")
            
            license_id = license_info.get("id")
            if not license_id:
                return (False, "Could not determine license ID")
            
            # Send unblock request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/{license_id}/unblock"
            response = requests.post(url)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success", False):
                return (True, "")
            else:
                return (False, result.get("message", "Unblock failed"))
    
        except requests.exceptions.RequestException as e:
            return (False, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (False, f"An error occurred: {str(e)}")
    
    @staticmethod
    def block_key(server_url: str = None, license_key: str = None) -> Tuple[bool, str]:
        """
        Block a license key so it cannot be activated.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to block
            
        Returns:
            Tuple of (success, message). If successful, success is True.
            If failed, success is False and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        try:
            # First, get the license ID from the license key
            license_info, message = LicenseKey.get_key(server_url, license_key)
            if not license_info:
                return (False, "License not found")
            
            license_id = license_info.get("id")
            if not license_id:
                return (False, "Could not determine license ID")
            
            # Send block request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/{license_id}/block"
            response = requests.post(url)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success", False):
                return (True, "")
            else:
                return (False, result.get("message", "Block failed"))
           
        except requests.exceptions.RequestException as e:
            return (False, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (False, f"An error occurred: {str(e)}")
    
    @staticmethod
    def machine_lock_limit(server_url: str = None, license_key: str = None, number_of_machines: int = 0) -> Tuple[bool, str]:
        """
        Change the maximum number of machines a license can be activated on.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to modify
            number_of_machines: Maximum number of machines allowed
            
        Returns:
            Tuple of (success, message). If successful, success is True.
            If failed, success is False and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        try:
            # First, get the license ID from the license key
            license_info, message = LicenseKey.get_key(server_url, license_key)
            if not license_info:
                return (False, "License not found")
            
            license_id = license_info.get("id")
            if not license_id:
                return (False, "Could not determine license ID")
            
            # Prepare machine limit data
            data = {
                "max_activations": number_of_machines
            }
            
            # Send machine limit request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/{license_id}/machine-limit"
            response = requests.put(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success", False):
                return (True, "")
            else:
                return (False, result.get("message", "Machine limit change failed"))
           
        except requests.exceptions.RequestException as e:
            return (False, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (False, f"An error occurred: {str(e)}")
    
    @staticmethod
    def change_notes(server_url: str = None, license_key: str = None, notes: str = "") -> Tuple[bool, str]:
        """
        Change the notes field of a license key.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to modify
            notes: New notes for the license
            
        Returns:
            Tuple of (success, message). If successful, success is True.
            If failed, success is False and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        try:
            # First, get the license ID from the license key
            license_info, message = LicenseKey.get_key(server_url, license_key)
            if not license_info:
                return (False, "License not found")
            
            license_id = license_info.get("id")
            if not license_id:
                return (False, "Could not determine license ID")
            
            # Prepare notes change data
            data = {
                "notes": notes
            }
            
            # Send notes change request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/{license_id}"
            response = requests.put(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            # The server returns the full license object, not a success message
            # If we get here without an exception, the update was successful
            return (True, "")
                
        except requests.exceptions.RequestException as e:
            return (False, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (False, f"An error occurred: {str(e)}")
    
    @staticmethod
    def add_feature(server_url: str = None, license_key: str = None, feature_name: str = None) -> Tuple[bool, str]:
        """
        Add a feature to a license key.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to modify
            feature_name: Name of the feature to add
            
        Returns:
            Tuple of (success, message). If successful, success is True.
            If failed, success is False and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        try:
            # First, get the license ID from the license key
            license_info, message = LicenseKey.get_key(server_url, license_key)
            if not license_info:
                return (False, "License not found")
            
            license_id = license_info.get("id")
            if not license_id:
                return (False, "Could not determine license ID")
            
            # Prepare feature addition data
            data = {
                "feature_name": feature_name,
                "feature_value": True
            }
            
            # Send feature addition request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/{license_id}/features"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success", False):
                return (True, "")
            else:
                return (False, result.get("message", "Feature addition failed"))
                
        except requests.exceptions.RequestException as e:
            return (False, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (False, f"An error occurred: {str(e)}")
    
    @staticmethod
    def remove_feature(server_url: str = None, license_key: str = None, feature_name: str = None) -> Tuple[bool, str]:
        """
        Remove a feature from a license key.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to modify
            feature_name: Name of the feature to remove
            
        Returns:
            Tuple of (success, message). If successful, success is True.
            If failed, success is False and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        try:
            # First, get the license ID from the license key
            license_info, message = LicenseKey.get_key(server_url, license_key)
            if not license_info:
                return (False, "License not found")
            
            license_id = license_info.get("id")
            if not license_id:
                return (False, "Could not determine license ID")
            
            # Prepare feature removal data
            data = {
                "feature_name": feature_name,
                "feature_value": False
            }
            
            # Send feature removal request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/{license_id}/features"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success", False):
                return (True, "")
            else:
                return (False, result.get("message", "Feature removal failed"))
                
        except requests.exceptions.RequestException as e:
            return (False, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (False, f"An error occurred: {str(e)}")
    
    @staticmethod
    def create_key(server_url: str = None, customer_id: int = None, application_id: int = None,
                   max_activations: int = 1, expires_at: str = None, features: Dict[str, bool] = None,
                   notes: str = "") -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Create a new license key with your license server.
        
        Args:
            server_url: URL of your license server
            customer_id: Customer ID for the license
            application_id: Application ID for the license
            max_activations: Maximum number of activations allowed
            expires_at: Expiration date (ISO format string)
            features: Features dictionary
            notes: Optional notes for the license
            
        Returns:
            Tuple of (license_info, message). If successful, license_info contains the new license data.
            If failed, license_info is None and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        try:
            # Prepare license creation data
            data = {
                "customer_id": customer_id,
                "application_id": application_id,
                "max_activations": max_activations,
                "notes": notes
            }
            
            if expires_at:
                data["expires_at"] = expires_at
            
            if features:
                data["features"] = features
            
            # Send license creation request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/"
            
            response = requests.post(url, json=data, headers={
                'Content-Type': 'application/json',
                'accept': 'application/json'
            })
            
            response.raise_for_status()
            
            result = response.json()
            return (result, "")
                
        except requests.exceptions.RequestException as e:
            return (None, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (None, f"An error occurred: {str(e)}")
    
    @staticmethod
    def create_trial_key(server_url: str = None, customer_id: int = None, application_id: int = None,
                        machine_code: str = None, friendly_name: str = "") -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Create a trial license key with your license server.
        
        Args:
            server_url: URL of your license server
            customer_id: Customer ID for the license
            application_id: Application ID for the license
            machine_code: Machine identifier (optional, will be generated if not provided)
            friendly_name: Friendly name for the trial license
            
        Returns:
            Tuple of (license_info, message). If successful, license_info contains the new trial license data.
            If failed, license_info is None and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
        
        if machine_code is None:
            machine_code = Helpers.GetMachineCode(v=2)
        
        try:
            # Prepare trial license creation data
            data = {
                "customer_id": customer_id,
                "application_id": application_id,
                "machine_code": machine_code,
                "friendly_name": friendly_name,
                "is_trial": True
            }
            
            # Send trial license creation request
            url = f"{server_url.rstrip('/')}/api/v1/licenses/trial"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            return (result, "")
                
        except requests.exceptions.RequestException as e:
            return (None, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (None, f"An error occurred: {str(e)}")
    
    @staticmethod
    def get_key(server_url: str = None, license_key: str = None, rsa_pub_key: str = None) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Get detailed license information from your license server with signature verification.
        
        Args:
            server_url: URL of your license server
            license_key: The license key to get information for
            rsa_pub_key: RSA public key for signature verification
            
        Returns:
            Tuple of (license_info, message). If successful, license_info contains the license data.
            If failed, license_info is None and message contains the error.
        """
        
        if server_url is None:
            server_url = LicenseKey.DEFAULT_SERVER_URL
            
        if rsa_pub_key is None:
            rsa_pub_key = LicenseKey.DEFAULT_PUBLIC_KEY
        
        try:
            # Call the get_key endpoint directly with the license key
            url = f"{server_url.rstrip('/')}/api/v1/licenses/key/{license_key}"
            response = requests.get(url)
            response.raise_for_status()
            
            result = response.json()
            
            # Verify signature if RSA public key is provided
            if rsa_pub_key and result.get("signature"):
                try:
                    from .internal import LicenseServerHelpers
                    from .models import RSAPublicKey
                    
                    pubkey = RSAPublicKey.from_string(rsa_pub_key)
                    
                    # Create a response object for signature verification
                    from .models import Response
                    response_obj = Response.from_dict(result)
                    
                    if LicenseServerHelpers.verify_signature(response_obj, pubkey):
                        return (result, "")
                    else:
                        return (None, "The signature check failed.")
                except Exception as e:
                    return (None, f"Signature verification failed: {str(e)}")
            else:
                # If no signature verification is required, return the result directly
                return (result, "")
                
        except requests.exceptions.RequestException as e:
            return (None, f"Could not contact the server: {str(e)}")
        except Exception as e:
            return (None, f"An error occurred: {str(e)}")

    @staticmethod
    def decode_license_data(license_key_b64: str) -> dict:
        """
        Decode Base64-encoded license data back to JSON
        
        Args:
            license_key_b64: Base64-encoded license data
            
        Returns:
            Decoded license data dictionary
        """
        import base64
        import json
        
        try:
            # Decode Base64
            json_bytes = base64.b64decode(license_key_b64)
            json_str = json_bytes.decode('utf-8')
            
            # Parse JSON
            license_data = json.loads(json_str)
            
            return license_data
        except Exception as e:
            print(f"Failed to decode license data: {e}")
            return {}
    
    @staticmethod
    def extract_license_info(license_key_b64: str) -> dict:
        """
        Extract key information from license data
        
        Args:
            license_key_b64: Base64-encoded license data
            
        Returns:
            Dictionary with key license information
        """
        license_data = LicenseKey.decode_license_data(license_key_b64)
        
        return {
            "license_key": license_data.get("Key"),
            "license_id": license_data.get("ID"),
            "customer_id": license_data.get("GroupId"),
            "application_id": license_data.get("ProductId"),
            "created": license_data.get("Created"),
            "expires": license_data.get("Expires"),
            "features": license_data.get("Features", {}),  # Flexible features dictionary
            "blocked": license_data.get("Block", False),
            "trial_activation": license_data.get("TrialActivation", False),
            "max_machines": license_data.get("MaxNoOfMachines", 0),
            "notes": license_data.get("Notes"),
            "customer": license_data.get("Customer", {}),
            "activated_machines": license_data.get("ActivatedMachines", []),
            "sign_date": license_data.get("SignDate"),
            "custom_claims": license_data.get("CustomClaims", {})
        }

class Helpers:

    def __read_registry_value(key, subkey, value_name):

        import winreg

        """
        Reads a value from the Windows Registry.

        Parameters:
        key (int): The registry root key (e.g., winreg.HKEY_LOCAL_MACHINE).
        subkey (str): The path to the subkey.
        value_name (str): The name of the value to read.

        Returns:
        str: The value read from the registry, or an error message if not found.
        """
        try:
            # Open the registry key
            registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_READ)
            
            # Query the value
            value, reg_type = winreg.QueryValueEx(registry_key, value_name)
            
            # Close the registry key
            winreg.CloseKey(registry_key)
            
            return value
        
        except FileNotFoundError:
            return None
        except Exception as e:
            return None #str(e)
        
    
    @staticmethod
    def GetMachineCode(v=1):
        
        """
        Get a unique identifier for this device. If you want the machine code to be the same in .NET on Windows, you
        can set v=2. More information is available here: https://help.cryptolens.io/faq/index#machine-code-generation
        
        Note: if we are unable to compute the machine code, None will be returned. Please make sure
        to check this in production code.
        """
        
        if "windows" in platform.platform().lower():

            import winreg

            seed = ""
            
            if v==2:
                seed = LicenseServerHelpers.start_process_ps_v2()
            else:
                seed = LicenseServerHelpers.start_process(["cmd.exe", "/C", "wmic","csproduct", "get", "uuid"],v)
            
            if seed == "" or seed == None:
                machineGUID = LicenseServerHelpers.read_registry_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", "MachineGuid")
                
                if machineGUID != None and machineGUID != "":
                    return LicenseServerHelpers.get_sha256(machineGUID)
                return None
            else:
                return LicenseServerHelpers.get_sha256(seed)
            
            
        elif "mac" in platform.platform().lower() or "darwin" in platform.platform().lower():               
            res = LicenseServerHelpers.start_process(["system_profiler","SPHardwareDataType"])
            seed = res[res.index("UUID"):].strip()
            
            if seed == "":
                return None
            else:
                return LicenseServerHelpers.get_sha256(seed)
            
        elif "linux" in platform.platform().lower() :
            seed = LicenseServerHelpers.compute_machine_code()
            if seed == "":
                return None
            else:
                return LicenseServerHelpers.get_sha256(seed)
        else:
            seed = LicenseServerHelpers.compute_machine_code()
            if seed == "":
                return None
            else:
                return LicenseServerHelpers.get_sha256(seed)
    
    @staticmethod
    def IsOnRightMachine(license_key, is_floating_license = False, allow_overdraft=False, v = 1, custom_machine_code = None):
        
        """
        Check if the device is registered with the license key.
        The version parameter is related to the one in GetMachineCode method.
        """
        
        current_mid = ""
        
        if custom_machine_code == None:
            current_mid = Helpers.GetMachineCode(v)
        else:
            current_mid = custom_machine_code
        
        if license_key.activated_machines == None:
            return False
        
        if is_floating_license:
            for act_machine in license_key.activated_machines:
                if act_machine.Mid[9:] == current_mid or\
                   allow_overdraft and act_machine.Mid[19:] == current_mid:
                    return True
        else:
            for act_machine in license_key.activated_machines:
                if current_mid == act_machine.Mid:
                    return True
            
        return False
    
    
    @staticmethod
    def GetMACAddress():
        
        """
        An alternative way to compute the machine code (device identifier).
        This method is especially useful if you plan to target multiple platforms.
        """
        
        import uuid
        
        return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    
    def HasNotExpired(license_key, allow_usage_on_expiry_date=True):

        """
        Checks that the license key has not expired. Cryptolens offers automatic blocking of licenses
        on the server side, and it is recommended to set it up instead of relying on the client side (unless 
        your application is running in offline mode). For more details, please review
        https://help.cryptolens.io/web-interface/keys-that-dont-expire

        Parameters:
            @license_key The license key object.
            @allow_usage_on_expiry_date If set to true, the license will be considered valid on the day it expires.
        """

        import datetime

        if license_key == None:
            return False
        
        diff = license_key.expires.replace(tzinfo=datetime.timezone.utc) - datetime.datetime.now(datetime.timezone.utc)

        if allow_usage_on_expiry_date and diff >= datetime.timedelta(0) or not(allow_usage_on_expiry_date) and diff > 0:
            return True

        return False

    def HasFeature(license_key, feature_name):
        
        """
        Uses a special data object associated with the license key to determine if a certain feature exists.
        <strong>Formatting: </strong> The name of the data object should be 'license_features' and it should be structured as a JSON array.
        
        For example, <pre>["feature1", "feature2"]</pre><p>means feature1 and feature2 are true. You can also have feature bundling, eg. <pre>["feature1", ["feature2",["voice","image"]]]</pre>
        which means that feature1 and feature2 are true, as well as feature2.voice and feature2.image. You can set any depth, eg. you can have
        <pre>["feature1", ["feature2",[["voice",["all"]], "image"]]]</pre> means feature2.voice.all is true as well as feature2.voice and feature2.
        The dots symbol is used to specify the "sub-features". 
        
        Parameters:
            @license_key The license key object.
            @feature_name For example, "feature2.voice.all".
        
        """
        
        if license_key.data_objects == None:
            return False
        
        features = None
        
        for dobj in license_key.data_objects:
            
            if dobj["Name"] == 'license_features':
                features = dobj["StringValue"]
                break
            
        if features == None or features.strip() == "":
            return False
    
        array = json.loads(features)
            
        feature_path = feature_name.split(".")
        
        found = False
        
        for i in range(len(feature_path)):
            
            found = False
            index = -1
            
            for j in range(len(array)):
                
                if not(isinstance(array[j], list)) and array[j] == feature_path[i]:
                    found = True
                    break
                elif isinstance(array[j], list) and array[j][0] == feature_path[i]:
                    found = True
                    index = j
                    
            if not(found):
                return False
            
            if i+1 < len(feature_path) and index != -1:
                array = array[index][1]
            
        if not(found):
            return False
        
        return True