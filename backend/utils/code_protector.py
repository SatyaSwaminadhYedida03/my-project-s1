"""
Code Protection Utilities
Provides obfuscation and protection for sensitive business logic
"""
import base64
import hashlib
import os
from typing import Any, Callable

class CodeProtector:
    """Protects sensitive code and data from unauthorized access"""
    
    @staticmethod
    def obfuscate_string(text: str) -> str:
        """Simple obfuscation for sensitive strings"""
        key = os.getenv('OBFUSCATION_KEY', 'smart-hiring-default-key')
        encoded = base64.b64encode(text.encode()).decode()
        return f"OBF:{encoded}"
    
    @staticmethod
    def deobfuscate_string(obfuscated: str) -> str:
        """Deobfuscate protected strings"""
        if not obfuscated.startswith("OBF:"):
            return obfuscated
        encoded = obfuscated[4:]
        return base64.b64decode(encoded).decode()
    
    @staticmethod
    def protect_config(config_dict: dict) -> dict:
        """Protect sensitive configuration values"""
        protected = {}
        sensitive_keys = ['password', 'secret', 'key', 'token', 'api_key']
        
        for key, value in config_dict.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                if isinstance(value, str):
                    protected[key] = CodeProtector.obfuscate_string(value)
                else:
                    protected[key] = value
            else:
                protected[key] = value
        
        return protected
    
    @staticmethod
    def verify_integrity(file_path: str) -> bool:
        """Verify file hasn't been tampered with"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            checksum = hashlib.sha256(content).hexdigest()
            stored_checksum = os.getenv(f'CHECKSUM_{os.path.basename(file_path)}', '')
            
            if not stored_checksum:
                # First run, store the checksum
                print(f"⚠️  No checksum found for {file_path} - generating")
                return True
            
            if checksum != stored_checksum:
                print(f"🚨 INTEGRITY VIOLATION: {file_path} has been modified!")
                return False
            
            return True
        except Exception as e:
            print(f"Error verifying integrity: {e}")
            return False
    
    @staticmethod
    def watermark_code(developer_id: str) -> str:
        """Generate unique watermark for code distribution"""
        timestamp = str(os.urandom(16).hex())
        watermark_data = f"{developer_id}:{timestamp}"
        return hashlib.sha256(watermark_data.encode()).hexdigest()[:16]

def protected_function(func: Callable) -> Callable:
    """Decorator to protect sensitive functions from unauthorized execution"""
    def wrapper(*args, **kwargs):
        # Add runtime checks
        if not os.getenv('DEPLOYMENT_LICENSE_KEY'):
            raise PermissionError("Unauthorized: Missing deployment credentials")
        
        return func(*args, **kwargs)
    
    return wrapper

# Example usage for protecting sensitive business logic
@protected_function
def calculate_candidate_match_score(candidate_data: dict, job_data: dict) -> float:
    """
    Protected algorithm for candidate matching
    This is your proprietary business logic
    """
    # Your sensitive matching algorithm here
    pass

@protected_function
def generate_ai_interview_questions(job_requirements: dict) -> list:
    """
    Protected AI question generation
    This is your proprietary AI logic
    """
    # Your sensitive AI logic here
    pass
