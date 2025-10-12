# Activation Forms Testing Guide

## Overview

Activation forms enable offline license validation for computers without internet access. This guide covers testing the complete workflow and provides examples for developers and clients.

## Prerequisites

1. **Server Running**: Ensure the license server is running on `http://localhost:8999`
2. **Sample Data**: Run `python scripts/create_sample_data.py` to create test licenses
3. **Dependencies**: Install `requests` library: `pip install requests`

## Quick Start Testing

### Step 1: Start the Server
```bash
python run_server.py
```

### Step 2: Run the Test Script
```bash
python scripts/test_activation_forms.py
```

This will test the complete workflow automatically.

## Manual Testing Workflow

### Phase 1: Offline Computer (Client Side)

#### 1. Generate Machine Fingerprint
```python
from app.utils.machine_fingerprint import MachineFingerprint

machine_id = MachineFingerprint.generate_fingerprint()
print(f"Machine ID: {machine_id}")
```

#### 2. Create Activation Form Request
```bash
curl -X POST "http://localhost:8999/api/v1/activation-forms/" \
  -H "Content-Type: application/json" \
  -d '{
    "license_key": "ALKZV-EUHQC-AGSCZ-5LNKA-2NUFY",
    "machine_id": "YOUR_MACHINE_FINGERPRINT",
    "machine_name": "My Offline Computer"
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "license_key_id": 1,
  "machine_id": "YOUR_MACHINE_FINGERPRINT",
  "machine_name": "My Offline Computer",
  "request_code": "ABC123DEF456",
  "activation_code": null,
  "status": "pending",
  "expires_at": "2024-01-02T12:00:00",
  "created_at": "2024-01-01T12:00:00",
  "completed_at": null
}
```

#### 3. Display Request Code to User
The application should display the `request_code` to the user, who will manually transfer it to an online computer.

### Phase 2: Online Computer (Admin/Server Side)

#### 4. Generate Offline Activation Codes
```bash
curl -X POST "http://localhost:8999/api/v1/activation-forms/offline-codes" \
  -H "Content-Type: application/json" \
  -d '{
    "license_key_id": 1,
    "machine_id": "YOUR_MACHINE_FINGERPRINT",
    "quantity": 3
  }'
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "license_key_id": 1,
    "activation_code": "XYZ789ABC123",
    "machine_id": "YOUR_MACHINE_FINGERPRINT",
    "is_used": false,
    "expires_at": "2024-02-01T12:00:00",
    "created_at": "2024-01-01T12:00:00",
    "used_at": null
  }
]
```

#### 5. Provide Activation Code to User
The admin provides one of the activation codes to the user, who returns to the offline computer.

### Phase 3: Offline Computer (Client Side)

#### 6. Complete Activation Form
```bash
curl -X POST "http://localhost:8999/api/v1/activation-forms/complete" \
  -H "Content-Type: application/json" \
  -d '{
    "request_code": "ABC123DEF456",
    "activation_code": "XYZ789ABC123"
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "license_key_id": 1,
  "machine_id": "YOUR_MACHINE_FINGERPRINT",
  "machine_name": "My Offline Computer",
  "request_code": "ABC123DEF456",
  "activation_code": "XYZ789ABC123",
  "status": "completed",
  "expires_at": "2024-01-02T12:00:00",
  "created_at": "2024-01-01T12:00:00",
  "completed_at": "2024-01-01T12:05:00"
}
```

#### 7. Validate License
```bash
curl -X POST "http://localhost:8999/api/v1/validate/license" \
  -H "Content-Type: application/json" \
  -d '{
    "license_key": "ALKZV-EUHQC-AGSCZ-5LNKA-2NUFY",
    "machine_id": "YOUR_MACHINE_FINGERPRINT"
  }'
```

**Expected Response:**
```json
{
  "valid": true,
  "license_id": 1,
  "customer_id": 1,
  "application_id": 1,
  "status": "active",
  "expires_at": "2025-07-31T17:57:50.759028",
  "features": {
    "basic_features": true,
    "advanced_features": true,
    "premium_support": true
  },
  "remaining_activations": 1,
  "message": "License is valid"
}
```

## Error Testing Scenarios

### 1. Invalid License Key
```bash
curl -X POST "http://localhost:8999/api/v1/activation-forms/" \
  -H "Content-Type: application/json" \
  -d '{
    "license_key": "INVALID-KEY-HERE",
    "machine_id": "YOUR_MACHINE_FINGERPRINT",
    "machine_name": "Test Machine"
  }'
```

**Expected Response:** 404 Not Found

### 2. Invalid Request Code
```bash
curl -X POST "http://localhost:8999/api/v1/activation-forms/complete" \
  -H "Content-Type: application/json" \
  -d '{
    "request_code": "INVALID-REQUEST-CODE",
    "activation_code": "INVALID-ACTIVATION-CODE"
  }'
```

**Expected Response:** 404 Not Found

### 3. Expired Activation Form
Manually set the `expires_at` field in the database to a past date, then try to complete the activation.

### 4. Already Used Activation Code
Try to use the same activation code twice.

## Client Implementation Examples

### Python Client Example
```python
import requests
from app.utils.machine_fingerprint import MachineFingerprint

class LicenseClient:
    def __init__(self, server_url):
        self.server_url = server_url
    
    def create_activation_request(self, license_key, machine_name="My Computer"):
        """Create an activation form request"""
        machine_id = MachineFingerprint.generate_fingerprint()
        
        response = requests.post(
            f"{self.server_url}/api/v1/activation-forms/",
            json={
                "license_key": license_key,
                "machine_id": machine_id,
                "machine_name": machine_name
            }
        )
        
        if response.status_code == 201:
            data = response.json()
            return {
                "request_code": data["request_code"],
                "machine_id": machine_id,
                "expires_at": data["expires_at"]
            }
        else:
            raise Exception(f"Failed to create activation request: {response.text}")
    
    def complete_activation(self, request_code, activation_code):
        """Complete an activation form"""
        response = requests.post(
            f"{self.server_url}/api/v1/activation-forms/complete",
            json={
                "request_code": request_code,
                "activation_code": activation_code
            }
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to complete activation: {response.text}")
    
    def validate_license(self, license_key):
        """Validate a license"""
        machine_id = MachineFingerprint.generate_fingerprint()
        
        response = requests.post(
            f"{self.server_url}/api/v1/validate/license",
            json={
                "license_key": license_key,
                "machine_id": machine_id
            }
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"License validation failed: {response.text}")

# Usage Example
client = LicenseClient("http://localhost:8999")

# Step 1: Create activation request
try:
    result = client.create_activation_request("ALKZV-EUHQC-AGSCZ-5LNKA-2NUFY")
    print(f"Request Code: {result['request_code']}")
    print(f"Machine ID: {result['machine_id']}")
    print(f"Expires: {result['expires_at']}")
except Exception as e:
    print(f"Error: {e}")

# Step 2: Complete activation (after getting activation code from admin)
try:
    result = client.complete_activation("ABC123DEF456", "XYZ789ABC123")
    print(f"Activation completed: {result['status']}")
except Exception as e:
    print(f"Error: {e}")

# Step 3: Validate license
try:
    result = client.validate_license("ALKZV-EUHQC-AGSCZ-5LNKA-2NUFY")
    print(f"License valid: {result['valid']}")
    print(f"Features: {result['features']}")
except Exception as e:
    print(f"Error: {e}")
```

### JavaScript Client Example
```javascript
class LicenseClient {
    constructor(serverUrl) {
        this.serverUrl = serverUrl;
    }
    
    async createActivationRequest(licenseKey, machineName = "My Computer") {
        const machineId = await this.generateMachineFingerprint();
        
        const response = await fetch(`${this.serverUrl}/api/v1/activation-forms/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                license_key: licenseKey,
                machine_id: machineId,
                machine_name: machineName
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            return {
                requestCode: data.request_code,
                machineId: machineId,
                expiresAt: data.expires_at
            };
        } else {
            throw new Error(`Failed to create activation request: ${response.text()}`);
        }
    }
    
    async completeActivation(requestCode, activationCode) {
        const response = await fetch(`${this.serverUrl}/api/v1/activation-forms/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                request_code: requestCode,
                activation_code: activationCode
            })
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error(`Failed to complete activation: ${response.text()}`);
        }
    }
    
    async validateLicense(licenseKey) {
        const machineId = await this.generateMachineFingerprint();
        
        const response = await fetch(`${this.serverUrl}/api/v1/validate/license`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                license_key: licenseKey,
                machine_id: machineId
            })
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error(`License validation failed: ${response.text()}`);
        }
    }
    
    async generateMachineFingerprint() {
        // Implementation would depend on the client environment
        // This is a simplified example
        const systemInfo = {
            platform: navigator.platform,
            userAgent: navigator.userAgent,
            language: navigator.language,
            // Add more system-specific information
        };
        
        const infoString = JSON.stringify(systemInfo);
        const encoder = new TextEncoder();
        const data = encoder.encode(infoString);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        
        return hashHex.substring(0, 32).toUpperCase();
    }
}

// Usage Example
const client = new LicenseClient('http://localhost:8999');

// Step 1: Create activation request
client.createActivationRequest('ALKZV-EUHQC-AGSCZ-5LNKA-2NUFY')
    .then(result => {
        console.log(`Request Code: ${result.requestCode}`);
        console.log(`Machine ID: ${result.machineId}`);
        console.log(`Expires: ${result.expiresAt}`);
    })
    .catch(error => console.error(`Error: ${error}`));

// Step 2: Complete activation
client.completeActivation('ABC123DEF456', 'XYZ789ABC123')
    .then(result => {
        console.log(`Activation completed: ${result.status}`);
    })
    .catch(error => console.error(`Error: ${error}`));

// Step 3: Validate license
client.validateLicense('ALKZV-EUHQC-AGSCZ-5LNKA-2NUFY')
    .then(result => {
        console.log(`License valid: ${result.valid}`);
        console.log(`Features: ${JSON.stringify(result.features)}`);
    })
    .catch(error => console.error(`Error: ${error}`));
```

## Testing Checklist

- [ ] Server starts successfully
- [ ] Sample data is created
- [ ] Machine fingerprint generation works
- [ ] Activation form creation succeeds
- [ ] Offline activation code generation works
- [ ] Activation form completion succeeds
- [ ] License validation works after activation
- [ ] Error handling works for invalid inputs
- [ ] Expired activation forms are handled correctly
- [ ] Used activation codes cannot be reused
- [ ] Different machines generate different fingerprints
- [ ] Same license works on different machines (up to max_activations)

## Troubleshooting

### Common Issues

1. **Server Connection Error**
   - Ensure server is running on `http://localhost:8999`
   - Check firewall settings
   - Verify port 8999 is not in use

2. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Run `python scripts/debug_database.py` to diagnose

3. **Machine Fingerprint Issues**
   - Ensure consistent fingerprint generation
   - Test on different machines to verify uniqueness
   - Check for system-specific information collection

4. **Activation Code Issues**
   - Verify activation codes are generated correctly
   - Check expiration times
   - Ensure codes are not reused

### Debug Commands

```bash
# Check database status
python scripts/debug_database.py

# Test machine fingerprinting
python scripts/test_machine_fingerprint.py

# Test activation forms
python scripts/test_activation_forms.py

# Check server health
curl http://localhost:8999/health
```

## Security Considerations

1. **Machine Fingerprinting**: Ensure consistent and unique fingerprints
2. **Request Code Security**: Request codes should be time-limited
3. **Activation Code Security**: Codes should be single-use and time-limited
4. **Network Security**: Use HTTPS in production
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Audit Logging**: Log all activation attempts for security monitoring

## Performance Testing

1. **Concurrent Activations**: Test multiple simultaneous activations
2. **Large Scale**: Test with hundreds of activation codes
3. **Database Performance**: Monitor database performance under load
4. **Network Latency**: Test with simulated network delays
5. **Memory Usage**: Monitor memory usage during peak loads 