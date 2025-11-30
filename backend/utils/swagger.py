"""
OpenAPI/Swagger documentation generator
"""

from flask import Blueprint, jsonify
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

# Create APISpec
spec = APISpec(
    title="Smart Hiring System API",
    version="2.0.0",
    openapi_version="3.0.2",
    info=dict(
        description="Complete API documentation for Smart Hiring System - Enterprise Edition",
        contact=dict(
            name="API Support",
            email="support@smarthiring.com"
        ),
        license=dict(
            name="MIT",
            url="https://opensource.org/licenses/MIT"
        )
    ),
    servers=[
        dict(
            url="https://my-project-smart-hiring.onrender.com/api",
            description="Production server"
        ),
        dict(
            url="http://localhost:5000/api",
            description="Development server"
        )
    ],
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Security schemes
spec.components.security_scheme(
    "bearerAuth",
    {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT token obtained from /auth/login endpoint"
    }
)

# Common schemas
spec.components.schema(
    "Error",
    {
        "type": "object",
        "properties": {
            "error": {"type": "string", "description": "Error message"}
        },
        "required": ["error"]
    }
)

spec.components.schema(
    "User",
    {
        "type": "object",
        "properties": {
            "id": {"type": "string", "example": "507f1f77bcf86cd799439011"},
            "email": {"type": "string", "format": "email"},
            "name": {"type": "string"},
            "role": {"type": "string", "enum": ["candidate", "company", "admin"]}
        }
    }
)

spec.components.schema(
    "Job",
    {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "required_skills": {"type": "array", "items": {"type": "string"}},
            "location": {"type": "string"},
            "salary_range": {"type": "string"},
            "status": {"type": "string", "enum": ["open", "closed"]},
            "created_at": {"type": "string", "format": "date-time"}
        }
    }
)

spec.components.schema(
    "Question",
    {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "question_text": {"type": "string"},
            "question_type": {"type": "string", "enum": ["multiple_choice", "true_false", "short_answer"]},
            "options": {"type": "array", "items": {"type": "string"}},
            "points": {"type": "integer"},
            "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
            "category": {"type": "string"}
        }
    }
)

# API Blueprint
swagger_bp = Blueprint('swagger', __name__)

@swagger_bp.route('/swagger.json')
def swagger_json():
    """Return OpenAPI specification as JSON"""
    return jsonify(spec.to_dict())

@swagger_bp.route('/docs')
def swagger_ui():
    """Render Swagger UI"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Hiring API Documentation</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = function() {{
                SwaggerUIBundle({{
                    url: '/api/swagger.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    layout: "BaseLayout"
                }})
            }}
        </script>
    </body>
    </html>
    """


def document_endpoint(blueprint, rule, **kwargs):
    """Helper to document an endpoint"""
    def decorator(func):
        # Add path to spec
        operations = kwargs.get('operations', {})
        if operations:
            with blueprint.app.app_context():
                spec.path(
                    path=rule,
                    operations=operations,
                    **{k: v for k, v in kwargs.items() if k != 'operations'}
                )
        return func
    return decorator


# Export
__all__ = ['spec', 'swagger_bp', 'document_endpoint']
