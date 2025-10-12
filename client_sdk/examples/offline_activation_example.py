#!/usr/bin/env python3
"""
Offline Activation Example

This example demonstrates how to:
1. Create activation requests for offline computers
2. Handle the offline activation workflow
3. Complete activation with activation codes
"""
import sys
from pathlib import Path

# Add the root project directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from client_sdk.license_client import LicenseClient, FeatureManager, FeatureNotEnabledError

class OfflineApplication:
    """Example application that supports offline activation"""
    
    def __init__(self, server_url: str = "http://localhost:8999"):
        """
        Initialize the offline application
        
        Args:
            server_url: URL of the license server
        """
        # Initialize the license client
        self.license_client = LicenseClient(
            server_url=server_url,
            app_name="OfflineTextEditor",
            app_version="1.0.0"
        )
        
        # Initialize the feature manager
        self.feature_manager = FeatureManager(self.license_client)
        
        # Application state
        self.license_key = None
        self.is_activated = False
        
        # Register the application
        self._register_application()
    
    def _register_application(self):
        """Register the application with the license server"""
        try:
            # Define available features
            available_features = {
                "basic_editing": True,
                "advanced_editing": False,
                "file_export": False,
                "cloud_sync": False,
                "offline_mode": True
            }
            
            # Register the application
            app_info = self.license_client.register_application(
                description="Text editor with offline activation support",
                features=available_features
            )
            
            print(f"✅ Application registered successfully!")
            print(f"   App ID: {app_info['id']}")
            print(f"   Name: {app_info['name']}")
            print(f"   Version: {app_info['version']}")
            print()
            
        except Exception as e:
            print(f"⚠️  Application registration failed: {e}")
            print("   Continuing with limited functionality...")
            print()
    
    def set_license_key(self, license_key: str):
        """
        Set the license key for the application
        
        Args:
            license_key: The license key to use
        """
        self.license_key = license_key
        print(f"🔑 License key set: {license_key}")
        print()
    
    def create_offline_activation_request(self):
        """
        Create an offline activation request
        
        Returns:
            ActivationFormInfo object with request details
        """
        if not self.license_key:
            raise ValueError("License key must be set before creating activation request")
        
        try:
            # Create activation form request
            activation_form = self.license_client.create_activation_request(
                license_key=self.license_key,
                machine_name="Offline Computer"
            )
            
            print("📋 Offline Activation Request Created")
            print("=" * 50)
            print(f"Request Code: {activation_form.request_code}")
            print(f"Machine ID: {activation_form.machine_id}")
            print(f"Expires: {activation_form.expires_at}")
            print()
            print("📝 Instructions for User:")
            print("1. Write down the Request Code above")
            print("2. Go to a computer with internet access")
            print("3. Contact your software provider")
            print("4. Provide them with the Request Code")
            print("5. They will give you an Activation Code")
            print("6. Return to this computer and enter the Activation Code")
            print("=" * 50)
            
            return activation_form
            
        except Exception as e:
            print(f"❌ Failed to create activation request: {e}")
            return None
    
    def complete_offline_activation(self, request_code: str, activation_code: str):
        """
        Complete the offline activation with an activation code
        
        Args:
            request_code: The request code from create_offline_activation_request
            activation_code: The activation code from the provider
        """
        try:
            # Complete the activation
            completed_form = self.license_client.complete_activation(
                request_code=request_code,
                activation_code=activation_code
            )
            
            print("✅ Offline Activation Completed Successfully!")
            print("=" * 50)
            print(f"Form ID: {completed_form.id}")
            print(f"Status: {completed_form.status}")
            print(f"Completed: {completed_form.completed_at}")
            print()
            
            # Set the license key in the feature manager
            self.feature_manager.set_license_key(self.license_key)
            self.is_activated = True
            
            # Show available features
            self.show_available_features()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to complete activation: {e}")
            return False
    
    def show_available_features(self):
        """Show which features are available"""
        if not self.is_activated:
            print("⚠️  Application not activated - limited features available")
            return
        
        enabled_features = self.feature_manager.get_enabled_features()
        disabled_features = self.feature_manager.get_disabled_features()
        
        print("📋 Available Features:")
        print("   Enabled:")
        for feature in enabled_features:
            print(f"     ✅ {feature}")
        
        print("   Disabled:")
        for feature in disabled_features:
            print(f"     ❌ {feature}")
        print()
    
    def validate_license(self):
        """Validate the current license"""
        if not self.license_key:
            print("❌ No license key set")
            return False
        
        try:
            license_info = self.license_client.validate_license(self.license_key)
            
            print("✅ License Validation Successful!")
            print("=" * 40)
            print(f"Status: {license_info.status.value}")
            print(f"Expires: {license_info.expires_at or 'Never'}")
            print(f"Remaining Activations: {license_info.remaining_activations}")
            print(f"Features: {license_info.features}")
            print("=" * 40)
            
            return True
            
        except Exception as e:
            print(f"❌ License validation failed: {e}")
            return False
    
    # Feature-restricted methods
    
    def edit_text(self, text: str):
        """Basic text editing"""
        if self.feature_manager.is_feature_enabled("basic_editing"):
            print(f"📝 Editing text: {text}")
            return f"Edited: {text}"
        else:
            print("❌ Basic editing not available")
            return None
    
    def advanced_edit_text(self, text: str):
        """Advanced text editing (requires activation)"""
        if not self.is_activated:
            print("❌ Advanced editing requires activation")
            return None
        
        if not self.feature_manager.is_feature_enabled("advanced_editing"):
            print("❌ Advanced editing not enabled for this license")
            return None
        
        print(f"🔧 Advanced editing: {text}")
        return f"Advanced edited: {text.upper()}"
    
    def export_file(self, filename: str, content: str):
        """Export file (requires activation)"""
        if not self.is_activated:
            print("❌ File export requires activation")
            return None
        
        if not self.feature_manager.is_feature_enabled("file_export"):
            print("❌ File export not enabled for this license")
            return None
        
        print(f"💾 Exporting file: {filename}")
        return f"Exported: {filename}"
    
    def sync_to_cloud(self, data: str):
        """Sync to cloud (requires activation)"""
        if not self.is_activated:
            print("❌ Cloud sync requires activation")
            return None
        
        if not self.feature_manager.is_feature_enabled("cloud_sync"):
            print("❌ Cloud sync not enabled for this license")
            return None
        
        print(f"☁️  Syncing to cloud: {data}")
        return f"Synced: {data}"
    
    def run_demo(self):
        """Run a demo of the application features"""
        print("🎮 Offline Application Demo")
        print("=" * 50)
        
        # Set a sample license key
        sample_license = "ALKZV-EUHQC-AGSCZ-5LNKA-2NUFY"
        self.set_license_key(sample_license)
        
        # Show current state
        print("Current State:")
        print(f"   License Key: {self.license_key}")
        print(f"   Activated: {self.is_activated}")
        print()
        
        # Try features before activation
        print("Before Activation:")
        self.edit_text("Hello World")
        self.advanced_edit_text("Advanced text")
        self.export_file("demo.txt", "content")
        print()
        
        # Simulate activation process
        print("Simulating Activation Process:")
        print("1. Creating activation request...")
        activation_form = self.create_offline_activation_request()
        
        if activation_form:
            print("2. Simulating completion with dummy activation code...")
            # In real usage, this would be the actual activation code from the provider
            success = self.complete_offline_activation(
                request_code=activation_form.request_code,
                activation_code="DEMO123ACTIVATION456"
            )
            
            if success:
                print("3. Testing features after activation:")
                self.edit_text("Hello World")
                self.advanced_edit_text("Advanced text")
                self.export_file("demo.txt", "content")
                self.sync_to_cloud("demo data")
        
        print("=" * 50)

def main():
    """Main example function"""
    print("🖥️  Offline Activation Example")
    print("=" * 60)
    
    # Create the offline application
    app = OfflineApplication()
    
    # Run the demo
    app.run_demo()
    
    print("\n✅ Offline activation example completed!")
    print("\n📝 Key Points:")
    print("• Applications can work offline")
    print("• Activation requires internet only once")
    print("• Machine fingerprinting prevents sharing")
    print("• Features are restricted based on license")
    print("• Offline mode supports air-gapped environments")

if __name__ == "__main__":
    main() 