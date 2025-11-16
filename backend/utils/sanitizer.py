"""
Input Sanitization and Validation Utilities
Provides comprehensive input validation and sanitization functions
"""
import re
import html
from typing import Any, Dict, List, Optional

class InputSanitizer:
    """Utility class for sanitizing and validating user inputs"""
    
    @staticmethod
    def sanitize_string(input_str: str, max_length: int = 1000) -> str:
        """
        Sanitize string input by escaping HTML and limiting length
        
        Args:
            input_str: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not isinstance(input_str, str):
            return ""
        
        # Escape HTML entities
        sanitized = html.escape(input_str.strip())
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def sanitize_email(email: str) -> Optional[str]:
        """
        Validate and sanitize email address
        
        Args:
            email: Email address to sanitize
            
        Returns:
            Sanitized email or None if invalid
        """
        if not isinstance(email, str):
            return None
        
        email = email.lower().strip()
        
        # Validate email format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return None
        
        # Additional security checks
        if len(email) > 254:  # RFC 5321
            return None
        
        return email
    
    @staticmethod
    def sanitize_phone(phone: str) -> Optional[str]:
        """
        Validate and sanitize phone number
        
        Args:
            phone: Phone number to sanitize
            
        Returns:
            Sanitized phone or None if invalid
        """
        if not isinstance(phone, str):
            return None
        
        # Remove all non-digit characters except + at start
        phone = phone.strip()
        if phone.startswith('+'):
            phone = '+' + re.sub(r'\D', '', phone[1:])
        else:
            phone = re.sub(r'\D', '', phone)
        
        # Validate length (international phone numbers)
        if len(phone) < 10 or len(phone) > 15:
            return None
        
        return phone
    
    @staticmethod
    def sanitize_url(url: str) -> Optional[str]:
        """
        Validate and sanitize URL
        
        Args:
            url: URL to sanitize
            
        Returns:
            Sanitized URL or None if invalid
        """
        if not isinstance(url, str):
            return None
        
        url = url.strip()
        
        # Only allow http and https protocols
        if not url.startswith(('http://', 'https://')):
            return None
        
        # Basic URL validation
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        if not re.match(pattern, url):
            return None
        
        # Limit length
        if len(url) > 2048:
            return None
        
        return url
    
    @staticmethod
    def sanitize_integer(value: Any, min_val: int = None, max_val: int = None) -> Optional[int]:
        """
        Validate and sanitize integer input
        
        Args:
            value: Value to sanitize
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            Sanitized integer or None if invalid
        """
        try:
            int_val = int(value)
            
            if min_val is not None and int_val < min_val:
                return None
            
            if max_val is not None and int_val > max_val:
                return None
            
            return int_val
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def sanitize_list(input_list: Any, item_type: type = str, max_items: int = 100) -> List:
        """
        Validate and sanitize list input
        
        Args:
            input_list: List to sanitize
            item_type: Expected type of items
            max_items: Maximum number of items allowed
            
        Returns:
            Sanitized list
        """
        if not isinstance(input_list, list):
            return []
        
        # Limit number of items
        if len(input_list) > max_items:
            input_list = input_list[:max_items]
        
        # Validate and sanitize each item
        sanitized_list = []
        for item in input_list:
            if isinstance(item, item_type):
                if item_type == str:
                    sanitized_list.append(InputSanitizer.sanitize_string(item, max_length=200))
                else:
                    sanitized_list.append(item)
        
        return sanitized_list
    
    @staticmethod
    def sanitize_dict(input_dict: Any, allowed_keys: List[str]) -> Dict:
        """
        Validate and sanitize dictionary input
        
        Args:
            input_dict: Dictionary to sanitize
            allowed_keys: List of allowed keys
            
        Returns:
            Sanitized dictionary with only allowed keys
        """
        if not isinstance(input_dict, dict):
            return {}
        
        sanitized_dict = {}
        for key in allowed_keys:
            if key in input_dict:
                sanitized_dict[key] = input_dict[key]
        
        return sanitized_dict
    
    @staticmethod
    def sanitize_filename(filename: str) -> Optional[str]:
        """
        Sanitize filename to prevent directory traversal attacks
        
        Args:
            filename: Filename to sanitize
            
        Returns:
            Sanitized filename or None if invalid
        """
        if not isinstance(filename, str):
            return None
        
        filename = filename.strip()
        
        # Remove directory traversal attempts
        filename = filename.replace('..', '').replace('/', '').replace('\\', '')
        
        # Remove potentially dangerous characters
        filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
        
        # Limit length
        if len(filename) > 255 or len(filename) == 0:
            return None
        
        return filename
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': False,
            'errors': [],
            'strength': 'weak'
        }
        
        if len(password) < 8:
            result['errors'].append('Password must be at least 8 characters')
            return result
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        if not has_upper:
            result['errors'].append('Password must contain uppercase letters')
        if not has_lower:
            result['errors'].append('Password must contain lowercase letters')
        if not has_digit:
            result['errors'].append('Password must contain numbers')
        
        # Calculate strength
        if has_upper and has_lower and has_digit:
            result['valid'] = True
            if has_special and len(password) >= 12:
                result['strength'] = 'strong'
            elif has_special or len(password) >= 10:
                result['strength'] = 'medium'
            else:
                result['strength'] = 'acceptable'
        
        return result

# Global sanitizer instance
sanitizer = InputSanitizer()
