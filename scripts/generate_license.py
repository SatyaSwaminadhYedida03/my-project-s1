"""
Deployment License Generator
Use this script to generate deployment licenses for authorized instances

USAGE:
    python generate_license.py --domain yourdomain.com --email client@email.com

This will generate:
- DEPLOYMENT_LICENSE_KEY
- DEPLOYMENT_SIGNATURE
- Configuration instructions
"""
import hashlib
import hmac
import secrets
import argparse
from datetime import datetime, timedelta

class LicenseGenerator:
    """Generate deployment licenses for authorized instances"""
    
    SECRET = "smart-hiring-system-2025-proprietary"  # Keep this secret!
    
    @staticmethod
    def generate_license_key(domain: str, email: str, expiry_days: int = 365) -> dict:
        """
        Generate a complete license package for a deployment
        
        Args:
            domain: Authorized domain (e.g., 'yourdomain.com')
            email: Client email for tracking
            expiry_days: License validity period
            
        Returns:
            dict with license_key, signature, and configuration
        """
        # Generate unique license key
        timestamp = datetime.now().isoformat()
        random_salt = secrets.token_urlsafe(16)
        
        license_data = f"{domain}:{email}:{timestamp}:{random_salt}"
        license_key = hashlib.sha256(license_data.encode()).hexdigest()
        
        # Generate signature
        signature = hmac.new(
            LicenseGenerator.SECRET.encode(),
            license_key.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Calculate expiry
        expiry_date = datetime.now() + timedelta(days=expiry_days)
        
        return {
            'license_key': license_key,
            'signature': signature,
            'domain': domain,
            'email': email,
            'issued_date': datetime.now().isoformat(),
            'expiry_date': expiry_date.isoformat(),
            'expiry_days': expiry_days
        }
    
    @staticmethod
    def print_license_config(license_data: dict):
        """Print formatted configuration for .env file"""
        print("\n" + "="*70)
        print("🔐 DEPLOYMENT LICENSE GENERATED")
        print("="*70)
        print(f"\nClient: {license_data['email']}")
        print(f"Domain: {license_data['domain']}")
        print(f"Issued: {license_data['issued_date']}")
        print(f"Expires: {license_data['expiry_date']}")
        print(f"Valid for: {license_data['expiry_days']} days")
        print("\n" + "-"*70)
        print("ADD THESE TO YOUR .env FILE:")
        print("-"*70)
        print(f"\nDEPLOYMENT_LICENSE_KEY={license_data['license_key']}")
        print(f"DEPLOYMENT_SIGNATURE={license_data['signature']}")
        print(f"DEPLOYMENT_DOMAIN={license_data['domain']}")
        print(f"AUTHORIZED_DOMAINS={license_data['domain']}")
        print(f"SKIP_LICENSE_CHECK=false")
        print("\n" + "="*70)
        print("⚠️  IMPORTANT: Keep these credentials SECRET!")
        print("="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description='Generate deployment license for Smart Hiring System'
    )
    parser.add_argument(
        '--domain',
        required=True,
        help='Authorized domain (e.g., yourdomain.com or IP address)'
    )
    parser.add_argument(
        '--email',
        required=True,
        help='Client email for license tracking'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=365,
        help='License validity in days (default: 365)'
    )
    
    args = parser.parse_args()
    
    # Generate license
    license_data = LicenseGenerator.generate_license_key(
        domain=args.domain,
        email=args.email,
        expiry_days=args.days
    )
    
    # Display configuration
    LicenseGenerator.print_license_config(license_data)
    
    # Save to file for record-keeping
    filename = f"license_{args.domain.replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w') as f:
        f.write(f"Smart Hiring System - Deployment License\n")
        f.write(f"="*70 + "\n\n")
        f.write(f"Client: {license_data['email']}\n")
        f.write(f"Domain: {license_data['domain']}\n")
        f.write(f"Issued: {license_data['issued_date']}\n")
        f.write(f"Expires: {license_data['expiry_date']}\n\n")
        f.write(f"DEPLOYMENT_LICENSE_KEY={license_data['license_key']}\n")
        f.write(f"DEPLOYMENT_SIGNATURE={license_data['signature']}\n")
        f.write(f"DEPLOYMENT_DOMAIN={license_data['domain']}\n")
        f.write(f"AUTHORIZED_DOMAINS={license_data['domain']}\n")
        f.write(f"SKIP_LICENSE_CHECK=false\n")
    
    print(f"📄 License saved to: {filename}\n")

if __name__ == "__main__":
    main()
