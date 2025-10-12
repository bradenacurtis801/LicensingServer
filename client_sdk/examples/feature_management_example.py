#!/usr/bin/env python3
"""
Feature Management Example using Updated Key Class

This example demonstrates how to use the updated Key class for feature management
with your license server.
"""

import sys
from pathlib import Path

# Add the root project directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from client_sdk.methods import LicenseKey, Helpers

class FeatureManager:
    """Simple feature manager using the Key class"""
    
    def __init__(self, server_url: str = None, app_name: str = None, app_version: str = None):
        """
        Initialize the feature manager
        
        Args:
            server_url: URL of your license server
            app_name: Application name
            app_version: Application version
        """
        self.server_url = server_url or LicenseKey.DEFAULT_SERVER_URL
        self.app_name = app_name
        self.app_version = app_version
        self.license_key = None
        self.license_info = None
        
        # Get machine code
        self.machine_code = LicenseKey.get_machine_code(version=2)
        
        print(f"🔧 Feature Manager initialized:")
        print(f"   Server: {self.server_url}")
        print(f"   App: {self.app_name} v{self.app_version}")
        print(f"   Machine Code: {self.machine_code[:16]}...")
        print()
    
    def register_application(self, description: str = "", features: dict = None):
        """
        Register application with license server
        
        Args:
            description: Application description
            features: Available features dictionary
        """
        print("📝 Registering application...")
        
        result, message = LicenseKey.register_application(
            server_url=self.server_url,
            app_name=self.app_name,
            app_version=self.app_version,
            description=description,
            features=features
        )
        
        if result:
            print(f"✅ Application registered: {result.get('name')} v{result.get('version')}")
        else:
            print(f"⚠️  Application registration: {message}")
        
        print()
    
    def set_license_key(self, license_key: str):
        """
        Set and validate license key
        
        Args:
            license_key: The license key to set
        """
        self.license_key = license_key
        
        print(f"🔑 Setting license key: {license_key[:16]}...")
        
        # Validate the license
        result, message = LicenseKey.validate(
            server_url=self.server_url,
            license_key=license_key,
            machine_code=self.machine_code
        )
        
        if result:
            self.license_info = result
            print("✅ License key set and validated successfully!")
            print(f"   License ID: {result.get('license_id')}")
            print(f"   Customer ID: {result.get('customer_id')}")
            print(f"   Status: {result.get('status')}")
            print(f"   Features: {result.get('features')}")
        else:
            print(f"❌ License validation failed: {message}")
            self.license_info = None
        
        print()
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a feature is enabled
        
        Args:
            feature_name: Name of the feature to check
            
        Returns:
            True if feature is enabled, False otherwise
        """
        if not self.license_info or not self.license_info.get('valid'):
            return False
        
        features = self.license_info.get('features', {})
        
        # Check direct feature
        if feature_name in features:
            return bool(features[feature_name])
        
        # Check nested features (e.g., "advanced.sub_feature")
        parts = feature_name.split('.')
        current = features
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        return bool(current)
    
    def get_enabled_features(self) -> list:
        """
        Get list of enabled features
        
        Returns:
            List of enabled feature names
        """
        if not self.license_info or not self.license_info.get('valid'):
            return []
        
        features = self.license_info.get('features', {})
        enabled = []
        
        def collect_enabled(feature_dict, prefix=""):
            for feature_name, is_enabled in feature_dict.items():
                if isinstance(is_enabled, bool) and is_enabled:
                    full_name = f"{prefix}.{feature_name}" if prefix else feature_name
                    enabled.append(full_name)
                elif isinstance(is_enabled, dict):
                    new_prefix = f"{prefix}.{feature_name}" if prefix else feature_name
                    collect_enabled(is_enabled, new_prefix)
        
        collect_enabled(features)
        return enabled
    
    def require_feature(self, feature_name: str):
        """
        Require a feature to be enabled, raise exception if not
        
        Args:
            feature_name: Name of the required feature
            
        Raises:
            ValueError: If feature is not enabled
        """
        if not self.is_feature_enabled(feature_name):
            raise ValueError(f"Feature '{feature_name}' is not enabled")
    
    def activate_license(self):
        """
        Activate the current license key
        
        Returns:
            True if activation successful, False otherwise
        """
        if not self.license_key:
            print("❌ No license key set")
            return False
        
        print("🔑 Activating license...")
        
        result, message = LicenseKey.activate(
            server_url=self.server_url,
            license_key=self.license_key,
            machine_code=self.machine_code,
            app_name=self.app_name,
            app_version=self.app_version
        )
        
        if result:
            print("✅ License activated successfully!")
            return True
        else:
            print(f"❌ License activation failed: {message}")
            return False

class MyApplication:
    """Example application using feature management"""
    
    def __init__(self, license_key: str = None):
        """
        Initialize the application
        
        Args:
            license_key: Optional license key for testing
        """
        # Initialize feature manager
        self.feature_manager = FeatureManager(
            server_url="http://localhost:8999",
            app_name="FeatureTestApp",
            app_version="1.0.0"
        )
        
        # Register application
        self.feature_manager.register_application(
            description="Test application for feature management",
            features={
                "basic_editing": True,
                "advanced_editing": False,
                "file_export": False,
                "cloud_sync": False,
                "team_collaboration": False,
                "premium_support": False,
                "custom_themes": False,
                "api_access": False,
                "enhanced_security": False,
                "offline_mode": False
            }
        )
        
        # Set license key if provided
        if license_key:
            self.feature_manager.set_license_key(license_key)
    
    def edit_text(self, text: str):
        """Basic text editing (always available)"""
        if self.feature_manager.is_feature_enabled("basic_editing"):
            print(f"📝 Basic editing: {text}")
            return f"Edited: {text}"
        else:
            raise ValueError("Basic editing requires a valid license")
    
    def advanced_edit_text(self, text: str):
        """Advanced text editing (requires license)"""
        if self.feature_manager.is_feature_enabled("advanced_editing"):
            print(f"🔧 Advanced editing: {text}")
            return f"Advanced edited: {text}"
        else:
            raise ValueError("Advanced editing requires a valid license")
    
    def export_file(self, filename: str, content: str):
        """Export file (requires license)"""
        if self.feature_manager.is_feature_enabled("file_export"):
            print(f"📁 Exporting file: {filename}")
            return f"Exported: {filename}"
        else:
            raise ValueError("File export requires a valid license")
    
    def sync_to_cloud(self, data: str):
        """Sync to cloud (requires license)"""
        if self.feature_manager.is_feature_enabled("cloud_sync"):
            print(f"☁️  Syncing to cloud: {data}")
            return f"Synced: {data}"
        else:
            raise ValueError("Cloud sync requires a valid license")
    
    def collaborate_with_team(self, message: str):
        """Team collaboration (requires license)"""
        if self.feature_manager.is_feature_enabled("team_collaboration"):
            print(f"👥 Team collaboration: {message}")
            return f"Collaborated: {message}"
        else:
            raise ValueError("Team collaboration requires a valid license")
    
    def get_premium_support(self, issue: str):
        """Premium support (requires license)"""
        if self.feature_manager.is_feature_enabled("premium_support"):
            print(f"🎯 Premium support: {issue}")
            return f"Supported: {issue}"
        else:
            raise ValueError("Premium support requires a valid license")
    
    def apply_custom_theme(self, theme_name: str):
        """Apply custom theme (requires license)"""
        if self.feature_manager.is_feature_enabled("custom_themes"):
            print(f"🎨 Custom theme: {theme_name}")
            return f"Themed: {theme_name}"
        else:
            raise ValueError("Custom themes require a valid license")
    
    def access_api(self, endpoint: str):
        """API access (requires license)"""
        if self.feature_manager.is_feature_enabled("api_access"):
            print(f"🔌 API access: {endpoint}")
            return f"API accessed: {endpoint}"
        else:
            raise ValueError("API access requires a valid license")
    
    def use_enhanced_security(self, data: str):
        """Enhanced security (requires license)"""
        if self.feature_manager.is_feature_enabled("enhanced_security"):
            print(f"🔒 Enhanced security: {data}")
            return f"Secured: {data}"
        else:
            raise ValueError("Enhanced security requires a valid license")
    
    def use_offline_mode(self, data: str):
        """Offline mode (requires license)"""
        if self.feature_manager.is_feature_enabled("offline_mode"):
            print(f"📱 Offline mode: {data}")
            return f"Offline: {data}"
        else:
            raise ValueError("Offline mode requires a valid license")
    
    def show_available_features(self):
        """Show all available features and their status"""
        print("📋 Available Features:")
        print("=" * 30)
        
        features = [
            "basic_editing",
            "advanced_editing", 
            "file_export",
            "cloud_sync",
            "team_collaboration",
            "premium_support",
            "custom_themes",
            "api_access",
            "enhanced_security",
            "offline_mode"
        ]
        
        for feature in features:
            status = "✅" if self.feature_manager.is_feature_enabled(feature) else "❌"
            print(f"   {status} {feature}")
        
        print()
        
        # Show enabled features list
        enabled_features = self.feature_manager.get_enabled_features()
        if enabled_features:
            print(f"🎯 Enabled Features: {', '.join(enabled_features)}")
        else:
            print("🎯 No features currently enabled")
        print()
    
    def demo_mode(self):
        """Run in demo mode (no license required)"""
        print("🎮 Running in DEMO MODE")
        print("=" * 30)
        
        # Basic features only
        print("📝 Basic editing is available")
        self.edit_text("Hello, this is basic editing!")
        
        print("\n❌ Advanced features are disabled:")
        print("   - Advanced editing")
        print("   - File export")
        print("   - Cloud sync")
        print("   - Team collaboration")
        print("   - Premium support")
        print("   - Custom themes")
        print("   - API access")
        print("   - Enhanced security")
        print("   - Offline mode")
        
        print("\n💡 To enable advanced features, set a valid license key:")
        print("   app.feature_manager.set_license_key('YOUR-ACTUAL-LICENSE-KEY-HERE')")
        print()
    
    def full_mode(self):
        """Run in full mode (license required)"""
        print("🚀 Running in FULL MODE")
        print("=" * 30)
        
        try:
            # Test all features
            print("📝 Testing basic editing...")
            self.edit_text("Hello, this is basic editing!")
            
            print("\n🔧 Testing advanced editing...")
            self.advanced_edit_text("Hello, this is advanced editing!")
            
            print("\n📁 Testing file export...")
            self.export_file("test.txt", "Hello, world!")
            
            print("\n☁️  Testing cloud sync...")
            self.sync_to_cloud("Important data")
            
            print("\n👥 Testing team collaboration...")
            self.collaborate_with_team("Great work, team!")
            
            print("\n🎯 Testing premium support...")
            self.get_premium_support("Need help with advanced features")
            
            print("\n🎨 Testing custom themes...")
            self.apply_custom_theme("Dark Mode")
            
            print("\n🔌 Testing API access...")
            self.access_api("/api/v1/data")
            
            print("\n🔒 Testing enhanced security...")
            self.use_enhanced_security("Sensitive data")
            
            print("\n📱 Testing offline mode...")
            self.use_offline_mode("Working offline")
            
            print("\n✅ All features working correctly!")
            
        except Exception as e:
            print(f"❌ Error in full mode: {e}")
        
        print()

def main():
    """Main function to demonstrate feature management"""
    print("🚀 Feature Management Example")
    print("=" * 40)
    print()
    
    # Create the application
    app = MyApplication()
    
    # Show available features
    app.show_available_features()
    
    # Run in demo mode first
    app.demo_mode()
    
    # Try to set a license key (replace with actual key)
    license_key = "YOUR-ACTUAL-LICENSE-KEY-HERE"
    
    if license_key != "YOUR-ACTUAL-LICENSE-KEY-HERE":
        try:
            print("🔑 Setting license key...")
            app.feature_manager.set_license_key(license_key)
            
            # Show updated features
            app.show_available_features()
            
            # Run in full mode
            app.full_mode()
            
        except Exception as e:
            print(f"❌ Failed to set license key: {e}")
            print("   Continuing in demo mode...")
    else:
        print("💡 To test with a real license:")
        print("   1. Run the sample data script to create licenses")
        print("   2. Replace 'YOUR-ACTUAL-LICENSE-KEY-HERE' with a real key")
        print("   3. Run this script again")
        print()
    
    print("🎉 Feature management example completed!")

if __name__ == "__main__":
    main() 