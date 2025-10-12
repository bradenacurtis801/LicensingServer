"""Advanced usage examples for the License Client SDK"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import time
import threading
from client_sdk.license_client import LicenseClient

class LicenseManager:
    """Advanced license manager with caching and periodic validation"""
    
    def __init__(self, server_url: str, license_key: str):
        self.client = LicenseClient(server_url)
        self.license_key = license_key
        self.is_valid = False
        self.last_check = 0
        self.cache_duration = 300  # 5 minutes
        self.features = {}
        self.lock = threading.Lock()
        
    def is_license_valid(self, force_check: bool = False) -> bool:
        """Check if license is valid with caching"""
        current_time = time.time()
        
        with self.lock:
            # Use cached result if not expired
            if not force_check and (current_time - self.last_check) < self.cache_duration:
                return self.is_valid
            
            # Perform validation
            result = self.client.validate_license(self.license_key)
            self.is_valid = result.get('valid', False)
            self.features = result.get('features', {})
            self.last_check = current_time
            
            return self.is_valid
    
    def has_feature(self, feature_name: str) -> bool:
        """Check if license has a specific feature"""
        if not self.is_license_valid():
            return False
        
        return self.features.get(feature_name, False)
    
    def start_heartbeat(self, interval: int = 300):
        """Start periodic heartbeat to keep license active"""
        def heartbeat():
            while True:
                time.sleep(interval)
                self.is_license_valid(force_check=True)
                print(f"Heartbeat sent - License valid: {self.is_valid}")
        
        thread = threading.Thread(target=heartbeat, daemon=True)
        thread.start()

def application_integration_example():
    """Example of integrating license checking into an application"""
    print("🔗 Application Integration Example")
    print("=" * 40)
    
    # Replace with actual license key
    license_key = "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY"
    license_manager = LicenseManager("http://localhost:8000", license_key)
    
    # Check license at startup
    if not license_manager.is_license_valid():
        print("❌ Invalid license - application cannot start")
        return
    
    print("✅ License validated - starting application")
    
    # Start heartbeat
    license_manager.start_heartbeat(60)  # Every minute
    
    # Simulate application features
    features_to_test = [
        ("basic_features", "Basic functionality"),
        ("advanced_features", "Advanced tools"),
        ("premium_support", "Premium support access")
    ]
    
    for feature_key, feature_name in features_to_test:
        if license_manager.has_feature(feature_key):
            print(f"✅ {feature_name} - ENABLED")
        else:
            print(f"❌ {feature_name} - DISABLED")
    
    print("\n🔄 Application running... (simulated)")
    print("Heartbeat will run in background")

def offline_validation_simulation():
    """Simulate handling offline scenarios"""
    print("\n📡 Offline Validation Simulation")
    print("=" * 40)
    
    client = LicenseClient("http://nonexistent-server:8000", timeout=5)
    license_key = "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY"
    
    print("Attempting validation with unreachable server...")
    result = client.validate_license(license_key)
    
    if not result.get('valid'):
        print(f"❌ Validation failed: {result.get('message')}")
        print("In a real application, you might:")
        print("- Use cached validation results")
        print("- Allow limited offline functionality")
        print("- Show 'unable to verify license' warning")

def multi_application_example():
    """Example of managing licenses for multiple applications"""
    print("\n🏢 Multi-Application License Example")
    print("=" * 40)
    
    # Simulate different applications with different license keys
    applications = {
        "MyAwesomeApp": "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY",
        "WebToolSuite": "ZYXWV-UTSRQ-PONML-KJIHG-FEDCB"
    }
    
    client = LicenseClient("http://localhost:8000")
    
    for app_name, license_key in applications.items():
        print(f"\nValidating license for {app_name}:")
        result = client.validate_license(license_key)
        
        if result.get('valid'):
            print(f"✅ {app_name} - License valid")
            expires = result.get('expires_at')
            if expires:
                print(f"   Expires: {expires}")
            else:
                print("   Expires: Never")
        else:
            print(f"❌ {app_name} - {result.get('message')}")

if __name__ == "__main__":
    print("🚀 Advanced License Client SDK Examples")
    print("=" * 50)
    print("Make sure the license server is running on http://localhost:8000")
    print()
    
    try:
        application_integration_example()
        offline_validation_simulation()
        multi_application_example()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the license server is running!")