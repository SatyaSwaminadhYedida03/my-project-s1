"""
Create Sample Data for Testing Smart Hiring System
This script creates sample quizzes, questions, and jobs for testing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.database import get_db
from backend.models.assessment import Question, Quiz
from datetime import datetime
from bson import ObjectId

def create_sample_questions(creator_id):
    """Create sample questions"""
    db = get_db()
    questions_collection = db['questions']
    
    sample_questions = [
        {
            "question_text": "What is Python primarily used for?",
            "question_type": "multiple_choice",
            "options": ["Web Development", "Data Science", "Automation", "All of the above"],
            "correct_answer": "All of the above",
            "points": 10,
            "difficulty": "easy",
            "category": "Python",
            "tags": ["python", "basics"],
            "explanation": "Python is a versatile language used for web development, data science, automation, and more.",
            "created_by": creator_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "question_text": "Which framework is used for building React applications?",
            "question_type": "multiple_choice",
            "options": ["Django", "Flask", "Next.js", "Spring"],
            "correct_answer": "Next.js",
            "points": 10,
            "difficulty": "medium",
            "category": "JavaScript",
            "tags": ["react", "javascript", "frameworks"],
            "explanation": "Next.js is a React framework for building server-side rendered applications.",
            "created_by": creator_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "question_text": "What does SQL stand for?",
            "question_type": "multiple_choice",
            "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "Sequential Query Language"],
            "correct_answer": "Structured Query Language",
            "points": 5,
            "difficulty": "easy",
            "category": "Database",
            "tags": ["sql", "database"],
            "explanation": "SQL stands for Structured Query Language, used for managing relational databases.",
            "created_by": creator_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "question_text": "Which of the following is a NoSQL database?",
            "question_type": "multiple_choice",
            "options": ["PostgreSQL", "MongoDB", "MySQL", "Oracle"],
            "correct_answer": "MongoDB",
            "points": 10,
            "difficulty": "easy",
            "category": "Database",
            "tags": ["database", "nosql", "mongodb"],
            "explanation": "MongoDB is a popular NoSQL database that stores data in flexible JSON-like documents.",
            "created_by": creator_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "question_text": "What is the purpose of Docker?",
            "question_type": "multiple_choice",
            "options": ["Version control", "Containerization", "Database management", "Code editing"],
            "correct_answer": "Containerization",
            "points": 10,
            "difficulty": "medium",
            "category": "DevOps",
            "tags": ["docker", "devops", "containers"],
            "explanation": "Docker is a platform for containerizing applications, making them portable and consistent across environments.",
            "created_by": creator_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "question_text": "Which HTTP method is used to update a resource?",
            "question_type": "multiple_choice",
            "options": ["GET", "POST", "PUT", "DELETE"],
            "correct_answer": "PUT",
            "points": 10,
            "difficulty": "medium",
            "category": "Web Development",
            "tags": ["http", "rest", "api"],
            "explanation": "PUT is used to update an existing resource, while POST creates new resources.",
            "created_by": creator_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "question_text": "What is the main purpose of Git?",
            "question_type": "multiple_choice",
            "options": ["Database backup", "Version control", "Web hosting", "Code compilation"],
            "correct_answer": "Version control",
            "points": 5,
            "difficulty": "easy",
            "category": "Tools",
            "tags": ["git", "version control"],
            "explanation": "Git is a distributed version control system for tracking changes in source code.",
            "created_by": creator_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "question_text": "Which CSS framework is known for utility-first classes?",
            "question_type": "multiple_choice",
            "options": ["Bootstrap", "Foundation", "Tailwind CSS", "Bulma"],
            "correct_answer": "Tailwind CSS",
            "points": 10,
            "difficulty": "medium",
            "category": "Frontend",
            "tags": ["css", "tailwind", "frontend"],
            "explanation": "Tailwind CSS is a utility-first CSS framework that provides low-level utility classes.",
            "created_by": creator_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
    ]
    
    inserted_ids = []
    for q in sample_questions:
        result = questions_collection.insert_one(q)
        inserted_ids.append(str(result.inserted_id))
        print(f"✅ Created question: {q['question_text'][:50]}...")
    
    return inserted_ids

def create_sample_quizzes(creator_id, question_ids):
    """Create sample quizzes"""
    db = get_db()
    quizzes_collection = db['quizzes']
    
    sample_quizzes = [
        {
            "title": "Python Fundamentals",
            "description": "Test your Python knowledge with this comprehensive assessment",
            "created_by": creator_id,
            "questions": question_ids[:3],  # First 3 questions
            "duration": 1800,  # 30 minutes
            "passing_score": 70,
            "total_points": 25,
            "is_active": True,
            "max_attempts": 3,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Full Stack Development",
            "description": "Assess your full stack development skills including frontend, backend, and databases",
            "created_by": creator_id,
            "questions": question_ids[:6],  # First 6 questions
            "duration": 2400,  # 40 minutes
            "passing_score": 75,
            "total_points": 60,
            "is_active": True,
            "max_attempts": 2,
            "created_at": datetime.utcnow()
        },
        {
            "title": "DevOps & Cloud Basics",
            "description": "Test your knowledge of DevOps tools and cloud technologies",
            "created_by": creator_id,
            "questions": [question_ids[4], question_ids[6]],  # Docker and Git questions
            "duration": 1200,  # 20 minutes
            "passing_score": 70,
            "total_points": 15,
            "is_active": True,
            "max_attempts": 3,
            "created_at": datetime.utcnow()
        }
    ]
    
    inserted_ids = []
    for quiz in sample_quizzes:
        result = quizzes_collection.insert_one(quiz)
        inserted_ids.append(str(result.inserted_id))
        print(f"✅ Created quiz: {quiz['title']}")
        print(f"   - {len(quiz['questions'])} questions, {quiz['duration']//60} minutes, {quiz['passing_score']}% passing score")
    
    return inserted_ids

def create_sample_jobs(recruiter_id):
    """Create sample jobs"""
    db = get_db()
    jobs_collection = db['jobs']
    
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "description": """We are looking for an experienced Python developer to join our backend team.

Requirements:
- 5+ years of Python experience
- Strong knowledge of Django or Flask
- Experience with PostgreSQL and Redis
- Docker and Kubernetes experience
- AWS cloud experience preferred""",
            "company_name": "Tech Innovations Inc.",
            "location": "Remote",
            "job_type": "Full-time",
            "department": "Engineering",
            "required_skills": ["python", "django", "flask", "postgresql", "redis", "docker", "aws"],
            "experience_required": "5+ years",
            "salary_range": "$120,000 - $160,000",
            "recruiter_id": recruiter_id,
            "status": "open",
            "posted_date": datetime.utcnow(),
            "applications_count": 0,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Full Stack Developer",
            "description": """Join our dynamic team building modern web applications.

Requirements:
- 3+ years of full stack experience
- React and Node.js expertise
- MongoDB experience
- RESTful API design
- Git and CI/CD knowledge""",
            "company_name": "Digital Solutions LLC",
            "location": "San Francisco, CA / Remote",
            "job_type": "Full-time",
            "department": "Product",
            "required_skills": ["react", "node.js", "mongodb", "javascript", "typescript", "rest api", "git"],
            "experience_required": "3+ years",
            "salary_range": "$100,000 - $140,000",
            "recruiter_id": recruiter_id,
            "status": "open",
            "posted_date": datetime.utcnow(),
            "applications_count": 0,
            "created_at": datetime.utcnow()
        },
        {
            "title": "DevOps Engineer",
            "description": """Help us build and maintain our cloud infrastructure.

Requirements:
- Strong Kubernetes experience
- Docker containerization
- CI/CD pipeline setup (Jenkins, GitHub Actions)
- AWS or Azure cloud platforms
- Infrastructure as Code (Terraform)""",
            "company_name": "Cloud Systems Corp",
            "location": "Austin, TX",
            "job_type": "Full-time",
            "department": "Infrastructure",
            "required_skills": ["kubernetes", "docker", "jenkins", "terraform", "aws", "ci/cd", "linux"],
            "experience_required": "4+ years",
            "salary_range": "$130,000 - $170,000",
            "recruiter_id": recruiter_id,
            "status": "open",
            "posted_date": datetime.utcnow(),
            "applications_count": 0,
            "created_at": datetime.utcnow()
        }
    ]
    
    inserted_ids = []
    for job in sample_jobs:
        result = jobs_collection.insert_one(job)
        inserted_ids.append(str(result.inserted_id))
        print(f"✅ Created job: {job['title']} at {job['company_name']}")
        print(f"   - {job['location']}, {job['job_type']}")
        print(f"   - Skills: {', '.join(job['required_skills'][:5])}...")
    
    return inserted_ids

def main():
    print("\n" + "="*60)
    print("🚀 Creating Sample Data for Smart Hiring System")
    print("="*60 + "\n")
    
    # Get creator/recruiter ID
    db = get_db()
    users_collection = db['users']
    
    # Find recruiter account
    recruiter = users_collection.find_one({'role': 'company'})
    if not recruiter:
        print("❌ No recruiter account found!")
        print("💡 Please run create_test_accounts.py first")
        return
    
    recruiter_id = str(recruiter['_id'])
    print(f"✅ Found recruiter: {recruiter.get('email')}")
    print(f"   ID: {recruiter_id}\n")
    
    # Create questions
    print("📝 Creating sample questions...")
    question_ids = create_sample_questions(recruiter_id)
    print(f"\n✅ Created {len(question_ids)} questions\n")
    
    # Create quizzes
    print("📋 Creating sample quizzes...")
    quiz_ids = create_sample_quizzes(recruiter_id, question_ids)
    print(f"\n✅ Created {len(quiz_ids)} quizzes\n")
    
    # Create jobs
    print("💼 Creating sample jobs...")
    job_ids = create_sample_jobs(recruiter_id)
    print(f"\n✅ Created {len(job_ids)} jobs\n")
    
    print("="*60)
    print("✅ Sample data creation completed!")
    print("="*60)
    print("\nYou can now:")
    print("1. Login as candidate and see quizzes in Assessments tab")
    print("2. Browse available jobs")
    print("3. Upload resume and apply to jobs")
    print("4. Take assessments to test skills")
    print("\nTest accounts:")
    print("- Candidate: candidate@test.com / password123")
    print("- Recruiter: recruiter@test.com / password123")
    print("\n")

if __name__ == '__main__':
    main()
