# 📋 API Documentation

Complete API reference for Smart Hiring System v2.0

## 🌐 Base URL

- **Production**: `https://my-project-smart-hiring.onrender.com/api`
- **Local**: `http://localhost:5000/api`

## 🔐 Authentication

All protected endpoints require JWT token:
```http
Authorization: Bearer <your-jwt-token>
```

## 📌 Endpoints Summary

| Category | Endpoint | Method | Auth | Description |
|----------|----------|--------|------|-------------|
| **Auth** | `/auth/register` | POST | ❌ | Register new user |
| **Auth** | `/auth/login` | POST | ❌ | Login and get token |
| **Auth** | `/auth/profile` | GET | ✅ | Get user profile |
| **Jobs** | `/jobs/create` | POST | ✅ | Create job (Company/Admin) |
| **Jobs** | `/jobs/list` | GET | ✅ | List all jobs |
| **Jobs** | `/jobs/<id>` | GET | ✅ | Get job details |
| **Jobs** | `/jobs/<id>` | PUT | ✅ | Update job (Owner/Admin) |
| **Jobs** | `/jobs/<id>` | DELETE | ✅ | Delete job (Owner/Admin) |
| **Applications** | `/candidates/apply` | POST | ✅ | Apply to job (Candidate) |
| **Applications** | `/candidates/applications` | GET | ✅ | Get my applications |
| **Applications** | `/candidates/applications/<id>/status` | PUT | ✅ | Update status (Recruiter) |
| **Assessments** | `/assessments/questions` | POST | ✅ | Create question (Recruiter) |
| **Assessments** | `/assessments/questions` | GET | ✅ | List questions |
| **Assessments** | `/assessments/questions/<id>` | DELETE | ✅ | Delete question |
| **Assessments** | `/assessments/quizzes` | POST | ✅ | Create quiz (Recruiter) |
| **Assessments** | `/assessments/quizzes` | GET | ✅ | List quizzes |
| **Assessments** | `/assessments/quizzes/<id>` | GET | ✅ | Get quiz details |
| **Assessments** | `/assessments/quizzes/<id>/start` | POST | ✅ | Start quiz (Candidate) |
| **Assessments** | `/assessments/attempts/<id>/submit` | POST | ✅ | Submit quiz answers |
| **Assessments** | `/assessments/attempts/<id>` | GET | ✅ | Get quiz results |
| **Assessments** | `/assessments/quizzes/<id>/analytics` | GET | ✅ | Quiz analytics (Recruiter) |
| **Email** | `/email/preferences` | GET | ✅ | Get email preferences |
| **Email** | `/email/preferences` | PUT | ✅ | Update preferences |

---

## 🔑 Authentication Endpoints

### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "role": "candidate",
  "name": "John Doe"
}
```

**Roles**: `candidate`, `company`, `admin`

**Response (201)**:
```json
{
  "message": "User registered successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200)**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "role": "candidate",
    "name": "John Doe"
  }
}
```

---

## 💼 Job Endpoints

### Create Job
```http
POST /api/jobs/create
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Senior Software Engineer",
  "description": "We are looking for...",
  "requirements": "5+ years experience...",
  "required_skills": ["Python", "Flask", "MongoDB"],
  "location": "Remote",
  "salary_range": "$100k - $150k"
}
```

**Response (201)**:
```json
{
  "message": "Job created successfully",
  "job_id": "507f1f77bcf86cd799439011"
}
```

### List Jobs
```http
GET /api/jobs/list?status=open
Authorization: Bearer <token>
```

**Response (200)**:
```json
{
  "jobs": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "Senior Software Engineer",
      "required_skills": ["Python", "Flask"],
      "location": "Remote",
      "status": "open",
      "applications_count": 15
    }
  ]
}
```

---

## 📝 Assessment Endpoints

### Create Question
```http
POST /api/assessments/questions
Authorization: Bearer <token>
Content-Type: application/json

{
  "question_text": "What is polymorphism?",
  "question_type": "multiple_choice",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "B",
  "points": 10,
  "difficulty": "medium",
  "category": "OOP"
}
```

**Question Types**: `multiple_choice`, `true_false`, `short_answer`

**Response (201)**:
```json
{
  "message": "Question created successfully",
  "question_id": "507f1f77bcf86cd799439013"
}
```

### Create Quiz
```http
POST /api/assessments/quizzes
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Python Developer Assessment",
  "description": "Test your skills",
  "question_ids": ["id1", "id2", "id3"],
  "duration": 30,
  "passing_score": 70,
  "randomize_questions": true,
  "max_attempts": 3
}
```

**Response (201)**:
```json
{
  "message": "Quiz created successfully",
  "quiz_id": "507f1f77bcf86cd799439014",
  "total_points": 50
}
```

### Start Quiz
```http
POST /api/assessments/quizzes/<quiz_id>/start
Authorization: Bearer <token>
```

**Response (200)**:
```json
{
  "message": "Quiz started successfully",
  "attempt_id": "507f1f77bcf86cd799439015",
  "quiz": {
    "title": "Python Developer Assessment",
    "questions": [...],
    "duration": 30
  },
  "expires_at": "2025-01-16T11:30:00Z"
}
```

### Submit Quiz
```http
POST /api/assessments/attempts/<attempt_id>/submit
Authorization: Bearer <token>
Content-Type: application/json

{
  "answers": {
    "question_id_1": "selected_answer",
    "question_id_2": "true"
  },
  "time_spent": {
    "question_id_1": 45,
    "question_id_2": 30
  }
}
```

**Response (200)**:
```json
{
  "message": "Quiz submitted successfully",
  "score": 45,
  "total_points": 50,
  "percentage": 90,
  "passed": true,
  "feedback": {...}
}
```

### Get Quiz Analytics
```http
GET /api/assessments/quizzes/<quiz_id>/analytics
Authorization: Bearer <token>
```

**Response (200)**:
```json
{
  "quiz_title": "Python Developer Assessment",
  "total_attempts": 25,
  "average_score": 42.5,
  "pass_rate": 91.3,
  "average_time_minutes": 27,
  "question_analytics": [...]
}
```

---

## 📧 Email Preference Endpoints

### Get Preferences
```http
GET /api/email/preferences
Authorization: Bearer <token>
```

**Response (200)**:
```json
{
  "preferences": {
    "new_job_alerts": true,
    "newsletter": false,
    "marketing": true
  }
}
```

### Update Preferences
```http
PUT /api/email/preferences
Authorization: Bearer <token>
Content-Type: application/json

{
  "new_job_alerts": true,
  "newsletter": false,
  "marketing": true
}
```

**Response (200)**:
```json
{
  "message": "Email preferences updated successfully"
}
```

---

## 📋 Application Status Management

### Update Application Status
```http
PUT /api/candidates/applications/<application_id>/status
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "interview_scheduled",
  "notes": "Interview on Monday at 10 AM"
}
```

**Status Values**: 
- `applied`
- `under_review`
- `interview_scheduled`
- `rejected`
- `accepted`

**Response (200)**:
```json
{
  "message": "Application status updated successfully"
}
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required field: email"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "You don't have permission"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Server Error
```json
{
  "error": "An unexpected error occurred"
}
```

---

## 🧪 Testing with curl

### Register
```bash
curl -X POST https://my-project-smart-hiring.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","role":"candidate","name":"Test User"}'
```

### Login
```bash
curl -X POST https://my-project-smart-hiring.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### List Jobs (with token)
```bash
curl https://my-project-smart-hiring.onrender.com/api/jobs/list \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📊 Rate Limits

- **Limit**: 100 requests/minute per IP
- **Headers**:
  - `X-RateLimit-Limit`: Total allowed
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

---

**Last Updated**: January 2025  
**Version**: 2.0.0

---

## 🔧 Developer Tools

### Swagger UI (Interactive Documentation)
Visit `/api/docs` for interactive API exploration:
- Try endpoints directly from browser
- View request/response schemas
- See authentication requirements
- Download OpenAPI specification

### Postman Collection
Import `Smart_Hiring_API.postman_collection.json` into Postman:
1. Open Postman → **Import** → **Upload Files**
2. Select the collection file from project root
3. Update `baseUrl` variable if needed (defaults to production)
4. Login via the "Login" request to auto-populate JWT token
5. All subsequent requests will use the token automatically

### Response Format Standard

All API responses follow a standardized format:

#### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "errors": {
    "field": ["Validation error"]
  }
}
```

#### Paginated Response
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

### HTTP Status Code Reference

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Best Practices

#### 1. Token Management
```javascript
// Store token securely
localStorage.setItem('jwt_token', token);

// Include in requests
fetch('/api/jobs/list', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  }
});
```

#### 2. Error Handling
```javascript
try {
  const response = await fetch('/api/jobs/list');
  const data = await response.json();
  
  if (!data.success) {
    console.error(data.error);
    return;
  }
  
  // Process data
} catch (error) {
  console.error('Network error:', error);
}
```

#### 3. Rate Limit Handling
```javascript
const retryAfter = response.headers.get('Retry-After');
if (response.status === 429) {
  setTimeout(() => retryRequest(), retryAfter * 1000);
}
```

---

## 🚀 Quick Start Examples

### Python Example
```python
import requests

# Login
response = requests.post(
    'https://my-project-smart-hiring.onrender.com/api/auth/login',
    json={'email': 'user@example.com', 'password': 'password123'}
)
token = response.json()['token']

# List jobs
jobs = requests.get(
    'https://my-project-smart-hiring.onrender.com/api/jobs/list',
    headers={'Authorization': f'Bearer {token}'}
).json()
```

### JavaScript Example
```javascript
// Login
const login = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', password: 'password123' })
});
const { token } = await login.json();

// List jobs
const jobs = await fetch('/api/jobs/list', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());
```

---

## 📚 Additional Resources

- **OpenAPI Spec**: `/api/swagger.json`
- **Support**: support@smarthiring.com
- **Security Runbook**: See `SECURITY_RUNBOOK.md`
- **Backup Guide**: See `BACKUP_GUIDE.md`
