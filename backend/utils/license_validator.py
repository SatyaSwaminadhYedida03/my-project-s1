"""
License Validation System
Prevents unauthorized deployment and usage of the Smart Hiring System
"""
import os
import hashlib
import hmac
from datetime import datetime
from functools import wraps
from flask import jsonify

class LicenseValidator:
    """Validates deployment authorization and prevents unauthorized usage"""
    
    def __init__(self):
        self.license_key = os.getenv('DEPLOYMENT_LICENSE_KEY', '')
        self.deployment_signature = os.getenv('DEPLOYMENT_SIGNATURE', '')
        self.authorized_domains = os.getenv('AUTHORIZED_DOMAINS', '').split(',')
        
    def generate_signature(self, license_key: str) -> str:
        """Generate deployment signature from license key"""
        secret = "smart-hiring-system-2025-proprietary"
        return hmac.new(
            secret.encode(),
            license_key.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def is_valid_license(self) -> bool:
        """Check if deployment has valid license"""
        if not self.license_key or not self.deployment_signature:
            return False
        
        expected_signature = self.generate_signature(self.license_key)
        return hmac.compare_digest(expected_signature, self.deployment_signature)
    
    def is_authorized_domain(self, domain: str) -> bool:
        """Check if domain is authorized for deployment"""
        if not self.authorized_domains:
            return False
        return domain in self.authorized_domains
    
    def validate_deployment(self) -> dict:
        """Comprehensive deployment validation"""
        validation_result = {
            'authorized': False,
            'license_valid': False,
            'domain_authorized': False,
            'expiry_date': None,
            'message': ''
        }
        
        # Check license key
        if not self.is_valid_license():
            validation_result['message'] = 'UNAUTHORIZED: Invalid or missing deployment license'
            return validation_result
        
        validation_result['license_valid'] = True
        
        # Check domain authorization
        current_domain = os.getenv('DEPLOYMENT_DOMAIN', 'localhost')
        if not self.is_authorized_domain(current_domain):
            validation_result['message'] = f'UNAUTHORIZED: Domain {current_domain} not authorized'
            return validation_result
        
        validation_result['domain_authorized'] = True
        validation_result['authorized'] = True
        validation_result['message'] = 'Deployment authorized'
        
        return validation_result

# Global validator instance
license_validator = LicenseValidator()

def require_valid_license(f):
    """Decorator to protect routes with license validation"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip validation in development mode
        if os.getenv('FLASK_ENV') == 'development' and os.getenv('SKIP_LICENSE_CHECK') == 'true':
            return f(*args, **kwargs)
        
        validation = license_validator.validate_deployment()
        
        if not validation['authorized']:
            return jsonify({
                'error': 'Unauthorized Deployment',
                'message': validation['message'],
                'code': 'LICENSE_VIOLATION'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def check_deployment_authorization():
    """Startup validation - prevents app from running without valid license"""
    # Allow development without license
    if os.getenv('FLASK_ENV') == 'development' and os.getenv('SKIP_LICENSE_CHECK') == 'true':
        print("⚠️  WARNING: Running in development mode with license check disabled")
        return True
    
    validation = license_validator.validate_deployment()
    
    if not validation['authorized']:
        print("\n" + "="*70)
        print("🚨 UNAUTHORIZED DEPLOYMENT DETECTED 🚨")
        print("="*70)
        print(f"Error: {validation['message']}")
        print("\nThis software is proprietary and requires authorization.")
        print("Contact: admin@smarthiring.com for licensing information")
        print("="*70 + "\n")
        return False
    
    print("✅ Deployment authorized - License validated")
    return True
