# License Management Client SDK

A comprehensive Python SDK for integrating license management into your applications. This SDK provides easy-to-use methods for license validation, feature restriction, and offline activation.

## Features

- ✅ **Easy Integration** - Simple API for license validation
- ✅ **Feature Management** - Restrict features based on license
- ✅ **Offline Activation** - Support for air-gapped environments
- ✅ **Machine Fingerprinting** - Secure device identification
- ✅ **Caching** - Performance optimization with license caching
- ✅ **Error Handling** - Comprehensive error management

## Installation

```bash
pip install requests
```

## Quick Start

### 1. Basic License Validation

```python
from license_client import LicenseClient

# Initialize the client
client = LicenseClient(
    server_url="http://localhost:8999",
    app_name="MyApp",
    app_version="1.0.0"
)

# Validate a license
try:
    license_info = client.validate_license("YOUR-LICENSE-KEY-HERE")
    print(f"License valid: {license_info.status.value}")
    print(f"Features: {license_info.features}")
except Exception as e:
    print(f"License validation failed: {e}")
```

### 2. Feature Restriction

```python
from license_client import LicenseClient, FeatureManager

# Initialize client and feature manager
client = LicenseClient("http://localhost:8999", "MyApp", "1.0.0")
feature_manager = FeatureManager(client)

# Set the license key
feature_manager.set_license_key("YOUR-LICENSE-KEY-HERE")

# Check if features are enabled
if feature_manager.is_feature_enabled("advanced_editing"):
    print("Advanced editing is available")
else:
    print("Advanced editing requires a license")

# Use decorator to require features
@feature_manager.require_feature("file_export")
def export_document(filename):
    print(f"Exporting {filename}...")
    # Export logic here
```

### 3. Offline Activation

```python
from license_client import LicenseClient

client = LicenseClient("http://localhost:8999", "MyApp", "1.0.0")

# Create activation request (offline computer)
activation_form = client.create_activation_request(
    license_key="YOUR-LICENSE-KEY-HERE",
    machine_name="My Computer"
)

print(f"Request Code: {activation_form.request_code}")
print("Provide this code to your software provider")

# Complete activation (after getting activation code from provider)
completed_form = client.complete_activation(
    request_code=activation_form.request_code,
    activation_code="ACTIVATION-CODE-FROM-PROVIDER"
)

print("Activation completed successfully!")
```

## Complete Examples

### Product Registration Example

See `examples/product_registration_example.py` for a complete example showing:

- Application registration with the license server
- Feature-based access control
- Demo mode vs. full license mode
- Individual feature checking

### Offline Activation Example

See `examples/offline_activation_example.py` for a complete example showing:

- Offline activation workflow
- Request code generation
- Activation completion
- Feature restriction based on activation status

## API Reference

### LicenseClient

Main client for interacting with the license server.

#### Constructor

```python
LicenseClient(server_url: str, app_name: str, app_version: str)
```

**Parameters:**
- `server_url`: URL of the license server
- `app_name`: Name of your application
- `app_version`: Version of your application

#### Methods

##### `register_application(description: str = None, features: Dict[str, Any] = None)`

Register your application with the license server.

**Parameters:**
- `description`: Application description
- `features`: Dictionary of available features

**Returns:** Application registration response

##### `validate_license(license_key: str, force_refresh: bool = False)`

Validate a license key.

**Parameters:**
- `license_key`: The license key to validate
- `force_refresh`: Force refresh the cache

**Returns:** `LicenseInfo` object

##### `create_activation_request(license_key: str, machine_name: str = None)`

Create an offline activation request.

**Parameters:**
- `license_key`: The license key to activate
- `machine_name`: Optional machine name

**Returns:** `ActivationFormInfo` object

##### `complete_activation(request_code: str, activation_code: str)`

Complete an offline activation.

**Parameters:**
- `request_code`: The request code from `create_activation_request`
- `activation_code`: The activation code from the provider

**Returns:** `ActivationFormInfo` object

##### `is_feature_enabled(license_key: str, feature_name: str)`

Check if a specific feature is enabled.

**Parameters:**
- `license_key`: The license key to check
- `feature_name`: The name of the feature

**Returns:** `bool`

##### `get_available_features(license_key: str)`

Get all available features for a license.

**Parameters:**
- `license_key`: The license key to check

**Returns:** Dictionary of available features

##### `is_license_valid(license_key: str)`

Check if a license is valid.

**Parameters:**
- `license_key`: The license key to check

**Returns:** `bool`

##### `clear_cache()`

Clear the license validation cache.

##### `set_cache_duration(seconds: int)`

Set the cache duration for license validation.

**Parameters:**
- `seconds`: Cache duration in seconds

### FeatureManager

Utility for managing feature restrictions in your application.

#### Constructor

```python
FeatureManager(license_client: LicenseClient)
```

**Parameters:**
- `license_client`: The license client instance

#### Methods

##### `set_license_key(license_key: str)`

Set the license key for feature checking.

**Parameters:**
- `license_key`: The license key to use

##### `is_feature_enabled(feature_name: str)`

Check if a feature is enabled.

**Parameters:**
- `feature_name`: The name of the feature

**Returns:** `bool`

##### `require_feature(feature_name: str)`

Decorator to require a specific feature.

**Parameters:**
- `feature_name`: The name of the feature required

**Returns:** Decorator function

##### `get_enabled_features()`

Get list of enabled features.

**Returns:** List of enabled feature names

##### `get_disabled_features()`

Get list of disabled features.

**Returns:** List of disabled feature names

### Data Classes

#### LicenseInfo

Container for license information.

**Attributes:**
- `license_id`: License ID
- `customer_id`: Customer ID
- `application_id`: Application ID
- `status`: License status (LicenseStatus enum)
- `expires_at`: Expiration date (optional)
- `features`: Dictionary of available features
- `remaining_activations`: Number of remaining activations
- `message`: License message

#### ActivationFormInfo

Container for activation form information.

**Attributes:**
- `id`: Form ID
- `request_code`: Request code for offline activation
- `machine_id`: Machine fingerprint
- `machine_name`: Machine name (optional)
- `expires_at`: Expiration date
- `status`: Form status

### Enums

#### LicenseStatus

- `ACTIVE`: License is active
- `EXPIRED`: License has expired
- `SUSPENDED`: License is suspended
- `REVOKED`: License is revoked

#### ActivationStatus

- `ACTIVE`: Activation is active
- `INACTIVE`: Activation is inactive

### Exceptions

#### FeatureNotEnabledError

Raised when a required feature is not enabled.

#### LicenseValidationError

Raised when license validation fails.

## Integration Examples

### Web Application

```python
from flask import Flask, request, jsonify
from license_client import LicenseClient, FeatureManager

app = Flask(__name__)

# Initialize license client
client = LicenseClient("http://localhost:8999", "WebApp", "1.0.0")
feature_manager = FeatureManager(client)

@app.route('/api/validate-license', methods=['POST'])
def validate_license():
    data = request.get_json()
    license_key = data.get('license_key')
    
    try:
        license_info = client.validate_license(license_key)
        return jsonify({
            'valid': True,
            'features': license_info.features,
            'expires_at': license_info.expires_at
        })
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 400

@app.route('/api/export-document', methods=['POST'])
def export_document():
    data = request.get_json()
    license_key = data.get('license_key')
    
    # Check if export feature is enabled
    if not client.is_feature_enabled(license_key, "file_export"):
        return jsonify({'error': 'Export feature requires a license'}), 403
    
    # Export logic here
    return jsonify({'success': True, 'file': 'exported.pdf'})
```

### Desktop Application

```python
import tkinter as tk
from license_client import LicenseClient, FeatureManager

class MyApp:
    def __init__(self):
        self.client = LicenseClient("http://localhost:8999", "DesktopApp", "1.0.0")
        self.feature_manager = FeatureManager(self.client)
        
        self.root = tk.Tk()
        self.setup_ui()
    
    def setup_ui(self):
        # License key entry
        tk.Label(self.root, text="License Key:").pack()
        self.license_entry = tk.Entry(self.root)
        self.license_entry.pack()
        
        # Validate button
        tk.Button(self.root, text="Validate License", command=self.validate_license).pack()
        
        # Feature buttons
        self.export_button = tk.Button(self.root, text="Export", command=self.export_document)
        self.export_button.pack()
        
        self.advanced_button = tk.Button(self.root, text="Advanced Features", command=self.advanced_features)
        self.advanced_button.pack()
    
    def validate_license(self):
        license_key = self.license_entry.get()
        try:
            self.feature_manager.set_license_key(license_key)
            tk.messagebox.showinfo("Success", "License validated successfully!")
            self.update_ui()
        except Exception as e:
            tk.messagebox.showerror("Error", f"License validation failed: {e}")
    
    def update_ui(self):
        # Enable/disable buttons based on features
        self.export_button.config(state='normal' if self.feature_manager.is_feature_enabled("file_export") else 'disabled')
        self.advanced_button.config(state='normal' if self.feature_manager.is_feature_enabled("advanced_features") else 'disabled')
    
    def export_document(self):
        if not self.feature_manager.is_feature_enabled("file_export"):
            tk.messagebox.showerror("Error", "Export feature requires a license")
            return
        # Export logic here
        tk.messagebox.showinfo("Success", "Document exported!")
    
    def advanced_features(self):
        if not self.feature_manager.is_feature_enabled("advanced_features"):
            tk.messagebox.showerror("Error", "Advanced features require a license")
            return
        # Advanced features logic here
        tk.messagebox.showinfo("Success", "Advanced features activated!")
```

### Command Line Application

```python
import argparse
from license_client import LicenseClient, FeatureManager

def main():
    parser = argparse.ArgumentParser(description='License-managed application')
    parser.add_argument('--license-key', required=True, help='License key')
    parser.add_argument('--feature', choices=['basic', 'advanced', 'export'], help='Feature to use')
    
    args = parser.parse_args()
    
    client = LicenseClient("http://localhost:8999", "CLIApp", "1.0.0")
    feature_manager = FeatureManager(client)
    
    try:
        feature_manager.set_license_key(args.license_key)
        
        if args.feature == 'basic':
            print("Basic feature activated")
        elif args.feature == 'advanced':
            if feature_manager.is_feature_enabled("advanced_features"):
                print("Advanced features activated")
            else:
                print("Advanced features require a license")
        elif args.feature == 'export':
            if feature_manager.is_feature_enabled("file_export"):
                print("Export feature activated")
            else:
                print("Export feature requires a license")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Error Handling

Always wrap license validation in try-catch blocks:

```python
try:
    license_info = client.validate_license(license_key)
    # Use license
except Exception as e:
    # Handle error gracefully
    print(f"License validation failed: {e}")
    # Fall back to demo mode or show error
```

### 2. Caching

Use the built-in caching for better performance:

```python
# Set cache duration (default is 5 minutes)
client.set_cache_duration(600)  # 10 minutes

# Force refresh when needed
license_info = client.validate_license(license_key, force_refresh=True)
```

### 3. Feature Checking

Check features before using them:

```python
# Always check if feature is enabled
if feature_manager.is_feature_enabled("advanced_editing"):
    # Use advanced editing
    advanced_edit_text()
else:
    # Show upgrade message
    show_upgrade_message()
```

### 4. Offline Activation

For applications that need to work offline:

```python
# Create activation request
activation_form = client.create_activation_request(license_key)

# Show request code to user
print(f"Request Code: {activation_form.request_code}")
print("Contact your software provider with this code")

# Later, complete activation
client.complete_activation(request_code, activation_code)
```

### 5. Security

- Never hardcode license keys
- Use environment variables for server URLs
- Validate all user inputs
- Implement proper error handling

## Troubleshooting

### Common Issues

1. **Connection Error**
   - Check if the license server is running
   - Verify the server URL is correct
   - Check network connectivity

2. **License Validation Failed**
   - Verify the license key is correct
   - Check if the license has expired
   - Ensure the license is for the correct application

3. **Feature Not Enabled**
   - Check if the feature is included in the license
   - Verify the license is valid
   - Contact your software provider

4. **Offline Activation Issues**
   - Ensure the request code is correct
   - Check if the activation code is valid
   - Verify the activation hasn't expired

### Debug Mode

Enable debug mode for more detailed error messages:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Support

For support and questions:

1. Check the examples in the `examples/` directory
2. Review the API reference above
3. Test with the provided sample data
4. Contact your software provider for license issues

## License

This SDK is provided as-is for use with the license management system. 