"""
Standardized API response formats
"""

from flask import jsonify
from typing import Any, Optional, Dict


def success_response(data: Any, message: Optional[str] = None, status_code: int = 200):
    """
    Standard success response format
    
    Args:
        data: Response payload
        message: Optional success message
        status_code: HTTP status code (default 200)
    
    Returns:
        Flask JSON response
    """
    response = {
        "success": True,
        "data": data
    }
    
    if message:
        response["message"] = message
    
    return jsonify(response), status_code


def error_response(message: str, errors: Optional[Dict] = None, status_code: int = 400):
    """
    Standard error response format
    
    Args:
        message: Error message
        errors: Optional validation errors dict
        status_code: HTTP status code (default 400)
    
    Returns:
        Flask JSON response
    """
    response = {
        "success": False,
        "error": message
    }
    
    if errors:
        response["errors"] = errors
    
    return jsonify(response), status_code


def paginated_response(data: list, page: int, per_page: int, total: int, **kwargs):
    """
    Paginated response format
    
    Args:
        data: List of items for current page
        page: Current page number
        per_page: Items per page
        total: Total number of items
        **kwargs: Additional metadata
    
    Returns:
        Flask JSON response
    """
    total_pages = (total + per_page - 1) // per_page
    
    response = {
        "success": True,
        "data": data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
    
    # Add any additional metadata
    if kwargs:
        response["meta"] = kwargs
    
    return jsonify(response), 200


def created_response(data: Any, message: str = "Resource created successfully"):
    """
    Response for resource creation (201)
    
    Args:
        data: Created resource data
        message: Success message
    
    Returns:
        Flask JSON response with 201 status
    """
    return success_response(data, message, status_code=201)


def no_content_response():
    """
    Response for successful operations with no content (204)
    
    Returns:
        Empty response with 204 status
    """
    return '', 204


# Common error responses
def unauthorized(message: str = "Authentication required"):
    """401 Unauthorized"""
    return error_response(message, status_code=401)


def forbidden(message: str = "You don't have permission to access this resource"):
    """403 Forbidden"""
    return error_response(message, status_code=403)


def not_found(message: str = "Resource not found"):
    """404 Not Found"""
    return error_response(message, status_code=404)


def validation_error(errors: Dict, message: str = "Validation failed"):
    """422 Unprocessable Entity"""
    return error_response(message, errors=errors, status_code=422)


def conflict(message: str = "Resource already exists"):
    """409 Conflict"""
    return error_response(message, status_code=409)


def rate_limited(message: str = "Too many requests", retry_after: Optional[int] = None):
    """429 Too Many Requests"""
    response = error_response(message, status_code=429)
    if retry_after:
        response[0].headers['Retry-After'] = str(retry_after)
    return response


def server_error(message: str = "Internal server error"):
    """500 Internal Server Error"""
    return error_response(message, status_code=500)


# Export all functions
__all__ = [
    'success_response',
    'error_response',
    'paginated_response',
    'created_response',
    'no_content_response',
    'unauthorized',
    'forbidden',
    'not_found',
    'validation_error',
    'conflict',
    'rate_limited',
    'server_error'
]
