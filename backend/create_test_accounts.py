"""
Script to create test user accounts for Smart Hiring System
Run this script to create admin, company, and candidate test accounts
"""

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from bson import ObjectId
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# MongoDB connection from environment
MONGO_URI = os.getenv('MONGODB_URI')
if not MONGO_URI:
    print("ERROR: MONGODB_URI environment variable not set")
    print("Please create a .env file with MONGODB_URI")
    sys.exit(1)

def create_test_accounts():
    """Create test user accounts"""
    client = MongoClient(MONGO_URI)
    db = client['smart_hiring_db']
    users_collection = db['users']
    candidates_collection = db['candidates']
    companies_collection = db['companies']
    
    # Hash password
    password_hash = generate_password_hash('test123')
    
    # Test accounts
    test_users = [
        {
            'email': 'admin@test.com',
            'password': password_hash,
            'role': 'admin',
            'name': 'Admin User',
            'created_at': datetime.utcnow(),
            'profile_completed': True
        },
        {
            'email': 'company@test.com',
            'password': password_hash,
            'role': 'company',
            'name': 'Tech Corp',
            'created_at': datetime.utcnow(),
            'profile_completed': True
        },
        {
            'email': 'candidate@test.com',
            'password': password_hash,
            'role': 'candidate',
            'name': 'John Doe',
            'created_at': datetime.utcnow(),
            'profile_completed': False
        }
    ]
    
    print("Creating test user accounts...")
    
    for user in test_users:
        # Check if user already exists
        existing = users_collection.find_one({'email': user['email']})
        
        if existing:
            # Update password to ensure it works
            users_collection.update_one(
                {'email': user['email']},
                {'$set': {'password': password_hash, 'name': user['name']}}
            )
            print(f"✓ Updated existing user: {user['email']}")
            user_id = str(existing['_id'])
        else:
            # Create new user
            result = users_collection.insert_one(user)
            user_id = str(result.inserted_id)
            print(f"✓ Created new user: {user['email']}")
        
        # Create profile for company
        if user['role'] == 'company':
            existing_company = companies_collection.find_one({'user_id': user_id})
            if not existing_company:
                companies_collection.insert_one({
                    'user_id': user_id,
                    'company_name': 'Tech Corp',
                    'industry': 'Technology',
                    'size': '50-200',
                    'website': 'https://techcorp.com',
                    'description': 'Leading technology company',
                    'created_at': datetime.utcnow()
                })
                print(f"  ✓ Created company profile for {user['email']}")
        
        # Create profile for candidate
        if user['role'] == 'candidate':
            existing_candidate = candidates_collection.find_one({'user_id': user_id})
            if not existing_candidate:
                candidates_collection.insert_one({
                    'user_id': user_id,
                    'phone': '+1-555-0100',
                    'location': 'San Francisco, CA',
                    'bio': 'Experienced software developer',
                    'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'MongoDB'],
                    'experience': [
                        {
                            'title': 'Software Engineer',
                            'company': 'Tech Startup',
                            'duration': '2 years',
                            'description': 'Full-stack development'
                        }
                    ],
                    'education': [
                        {
                            'degree': "Bachelor's in Computer Science",
                            'institution': 'University of California',
                            'year': '2020'
                        }
                    ],
                    'created_at': datetime.utcnow()
                })
                print(f"  ✓ Created candidate profile for {user['email']}")
    
    print("\n" + "="*60)
    print("Test accounts created successfully!")
    print("="*60)
    print("\nCredentials:")
    print("Admin:     admin@test.com / test123")
    print("Company:   company@test.com / test123") 
    print("Candidate: candidate@test.com / test123")
    print("\nNote: Use password 'test123' (not 'admin123', 'company123', 'candidate123')")
    print("="*60)
    
    client.close()

if __name__ == '__main__':
    create_test_accounts()
