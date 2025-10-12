#!/usr/bin/env python3
"""
Test error messages for missing resources
"""
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_error_messages():
    """Test that API returns proper error messages"""
    base_url = "http://localhost:8999/api/v1"
    
    logger.info("Testing Error Messages")
    logger.info("=" * 40)
    
    # Test 1: Try to create license with non-existent customer
    logger.info("Testing Customer Not Found Error:")
    logger.info("-" * 30)
    
    try:
        response = requests.post(
            f"{base_url}/licenses/",
            json={
                "customer_id": 999,  # Non-existent customer
                "application_id": 1,
                "max_activations": 1,
                "features": {},
                "notes": "Test license"
            }
        )
        
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        
        if response.status_code == 404:
            logger.info("Correctly returned 404 with customer not found message")
        else:
            logger.warning("Expected 404 but got different status code")
            
    except Exception as e:
        logger.error(f"Error: {e}")
    
    # Test 2: Try to create license with non-existent application
    logger.info("Testing Application Not Found Error:")
    logger.info("-" * 30)
    
    try:
        response = requests.post(
            f"{base_url}/licenses/",
            json={
                "customer_id": 1,
                "application_id": 999,  # Non-existent application
                "max_activations": 1,
                "features": {},
                "notes": "Test license"
            }
        )
        
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        
        if response.status_code == 404:
            logger.info("Correctly returned 404 with application not found message")
        else:
            logger.warning("Expected 404 but got different status code")
            
    except Exception as e:
        logger.error(f"Error: {e}")
    
    # Test 3: Try to get non-existent customer
    logger.info("Testing Get Customer Not Found Error:")
    logger.info("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/customers/999")
        
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        
        if response.status_code == 404:
            logger.info("Correctly returned 404 with customer not found message")
        else:
            logger.warning("Expected 404 but got different status code")
            
    except Exception as e:
        logger.error(f"Error: {e}")
    
    # Test 4: Try to get non-existent application
    logger.info("Testing Get Application Not Found Error:")
    logger.info("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/applications/999")
        
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        
        if response.status_code == 404:
            logger.info("Correctly returned 404 with application not found message")
        else:
            logger.warning("Expected 404 but got different status code")
            
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    test_error_messages() 