"""
Rate Limiting Middleware for Flask
Protects against brute force attacks and API abuse
"""
from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
import threading

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_rate_limited(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if a key has exceeded rate limit
        
        Args:
            key: Unique identifier (e.g., IP address, user ID)
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds
            
        Returns:
            True if rate limited, False otherwise
        """
        with self.lock:
            now = datetime.utcnow()
            cutoff_time = now - timedelta(seconds=window_seconds)
            
            # Remove old requests outside the window
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > cutoff_time
            ]
            
            # Check if limit exceeded
            if len(self.requests[key]) >= max_requests:
                return True
            
            # Add current request
            self.requests[key].append(now)
            return False
    
    def clear(self):
        """Clear all rate limit data"""
        with self.lock:
            self.requests.clear()

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit(max_requests: int = 5, window_seconds: int = 60, key_func=None):
    """
    Decorator to apply rate limiting to Flask routes
    
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
        key_func: Optional function to generate rate limit key (default: IP address)
        
    Example:
        @bp.route('/login', methods=['POST'])
        @rate_limit(max_requests=5, window_seconds=300)  # 5 attempts per 5 minutes
        def login():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Determine rate limit key
            if key_func:
                key = key_func()
            else:
                # Use IP address as default key
                key = request.remote_addr or 'unknown'
            
            # Check rate limit
            if rate_limiter.is_rate_limited(key, max_requests, window_seconds):
                return jsonify({
                    'error': 'Too many requests. Please try again later.',
                    'retry_after': window_seconds
                }), 429
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def get_user_rate_limit_key():
    """Get rate limit key based on user identity (IP + User-Agent)"""
    ip = request.remote_addr or 'unknown'
    user_agent = request.headers.get('User-Agent', 'unknown')
    return f"{ip}:{user_agent}"
