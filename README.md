# 🎯 Smart Hiring System

**AI-Powered Fair Recruitment Platform** - Proprietary Software

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB Atlas](https://img.shields.io/badge/Database-MongoDB%20Atlas-green.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

---

## 🔒 **PROPRIETARY SOFTWARE - PRIVATE REPOSITORY**

**⚠️ IMPORTANT NOTICE:**
- This software is **PROPRIETARY and CONFIDENTIAL**
- All rights reserved © 2025 Smart Hiring System
- **NO UNAUTHORIZED USE, COPYING, OR DISTRIBUTION**
- Access restricted to authorized developers only
- Requires explicit written permission for any use
- See [LICENSE](LICENSE) file for complete terms

**For authorization requests, contact:** admin@smarthiring.com

---

## 🚀 Development Status

**Current Phase:** Active Development (Private)

### 💼 **Job Management**
- ✅ Post & manage job openings
- ✅ Job description with required skills
- ✅ Location, type, salary range
- ✅ Application deadline tracking

### 👤 **Candidate Features**
- ✅ Resume upload (text format)
- ✅ PII anonymization (removes emails, phones, gender)
- ✅ Skill extraction & matching
- ✅ Job application tracking

### 🏢 **Company Dashboard**
- ✅ Post unlimited jobs
- ✅ View applicants
- ✅ Basic candidate screening

### 📊 **Smart Features** (Simplified)
- ✅ Skill-based matching
- ✅ Resume anonymization
- ✅ Basic scoring algorithm
- ⚠️ Advanced ML features disabled (deployment size constraints)

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0
- MongoDB Atlas (Cloud Database)
- JWT Authentication
- Gunicorn (Production Server)

**Frontend:**
- Vanilla JavaScript
- HTML5/CSS3
- Responsive Design

**Deployment:**
- Render.com (Backend)
- MongoDB Atlas (Database)
- GitHub (Version Control)

---

## 📦 Installation & Local Setup

### Prerequisites
- Python 3.11+
- MongoDB (or use MongoDB Atlas)
- Git

### Quick Start

```bash
# Clone repository
git clone https://github.com/SatyaSwaminadhYedida03/my-project-s1.git
cd smart-hiring-system

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your MongoDB URI and secrets

# Run locally
python app.py
```

Access at: http://localhost:5000

---

## 🔧 Environment Variables

Create a `.env` file with:

```env
# Database
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/smart_hiring_db

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Environment
FLASK_ENV=development  # or 'production'
```

> ⚠️ **Never commit `.env` files to git!**

---

## 🚀 Deployment

### Deploy to Render.com

1. Fork this repository
2. Create account on [Render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Set environment variables
6. Deploy!

**Environment Variables to Set:**
- `MONGODB_URI`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `FLASK_ENV=production`

---

## 📚 API Endpoints

### Authentication
```
POST /api/auth/register  - Register new user
POST /api/auth/login     - User login
GET  /api/auth/profile   - Get user profile
```

### Jobs
```
POST /api/jobs/create    - Create job (Company/Admin only)
GET  /api/jobs/list      - List all jobs
GET  /api/jobs/<id>      - Get job details
```

### Candidates
```
POST /api/candidates/upload-resume  - Upload resume
POST /api/candidates/apply          - Apply to job
GET  /api/candidates/applications   - View applications
```

### Health Check
```
GET /api/health - System status
```

---

## 🎯 Current Limitations

**Due to deployment size constraints, the following are disabled:**

- ❌ PDF/DOCX resume parsing (use text format)
- ❌ Advanced ML matching (scikit-learn removed)
- ❌ Automated assessments (ML dependencies removed)
- ❌ Dashboard analytics (pandas removed)

**Workaround:** These can be re-enabled by:
1. Deploying ML as separate microservice, OR
2. Using paid hosting tier with more resources, OR
3. Building desktop application with local processing

---

## 🔮 Roadmap

- [ ] AI Interviewer Integration (OpenAI GPT-4)
- [ ] Re-enable ML features (separate microservice)
- [ ] Email notifications (SMTP)
- [ ] Advanced analytics dashboard
- [ ] Video interview integration
- [ ] Skills assessment library
- [ ] Desktop application (Electron)
- [ ] Mobile app (React Native)

---

## 🤝 Contributing

This is currently a demo/portfolio project. For collaboration:

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 👨‍💻 Developer

**Satya Swaminadh Yedida**
- GitHub: [@SatyaSwaminadhYedida03](https://github.com/SatyaSwaminadhYedida03)

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Email: [Your Email]

---

## ⚡ Quick Links

- [Live Demo](https://smart-hiring-k1pb.onrender.com)
- [API Documentation](API_DOCUMENTATION.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

---

**⭐ Star this repo if you find it useful!**
