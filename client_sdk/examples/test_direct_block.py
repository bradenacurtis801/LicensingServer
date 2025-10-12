#!/usr/bin/env python3
"""
Direct test for block functionality using known license ID
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import requests

def test_direct_block():
    """Test block functionality directly using requests"""
    
    server_url = "http://localhost:8999"
    
    print("🔧 Testing Direct Block Functionality")
    print("=" * 40)
    
    # Test with license ID 106 (from your database output)
    license_id = 1
    
    print(f"\n1. Testing block for license ID {license_id}...")
    
    # Test block
    url = f"{server_url}/api/v1/licenses/{license_id}/block"
    response = requests.post(url)
    print(f"Block response status: {response.status_code}")
    print(f"Block response: {response.text}")
    
    # Test unblock
    print(f"\n2. Testing unblock for license ID {license_id}...")
    url = f"{server_url}/api/v1/licenses/{license_id}/unblock"
    response = requests.post(url)
    print(f"Unblock response status: {response.status_code}")
    print(f"Unblock response: {response.text}")
    
    # Test feature management
    print(f"\n3. Testing add feature for license ID {license_id}...")
    url = f"{server_url}/api/v1/licenses/{license_id}/features"
    data = {"feature_name": "test_feature", "feature_value": True}
    response = requests.post(url, json=data)
    print(f"Add feature response status: {response.status_code}")
    print(f"Add feature response: {response.text}")
    
    # Test machine limit
    print(f"\n4. Testing machine limit for license ID {license_id}...")
    url = f"{server_url}/api/v1/licenses/{license_id}/machine-limit"
    data = {"max_activations": 10}
    response = requests.put(url, json=data)
    print(f"Machine limit response status: {response.status_code}")
    print(f"Machine limit response: {response.text}")

if __name__ == "__main__":
    test_direct_block() 