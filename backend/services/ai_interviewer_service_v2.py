"""
Enhanced AI Interviewer Service - Dynamic Role-Specific Questioning
Generates personalized interview questions based on job roles, skills, and experience levels
"""

import random
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import re


# ============================================================================
# COMPREHENSIVE ROLE-SPECIFIC QUESTION BANKS
# ============================================================================

ROLE_QUESTION_BANKS = {
    'software_developer': {
        'fundamentals': [
            {
                'id': 'SD_F1',
                'question': 'Explain the SOLID principles and provide a real-world example of how you\'ve applied at least two of them.',
                'difficulty': 'medium',
                'expected_keywords': ['single responsibility', 'open-closed', 'liskov', 'interface segregation', 'dependency inversion', 'maintainability', 'extensible'],
                'time_limit_minutes': 10,
                'follow_up': 'How do you balance adhering to SOLID principles with meeting tight deadlines?'
            },
            {
                'id': 'SD_F2',
                'question': 'What is your approach to error handling and logging in production applications? Describe a specific incident you debugged.',
                'difficulty': 'hard',
                'expected_keywords': ['try-catch', 'exception', 'logging levels', 'monitoring', 'stack trace', 'debugging', 'root cause'],
                'time_limit_minutes': 12,
                'follow_up': 'How do you prevent similar issues from recurring?'
            },
            {
                'id': 'SD_F3',
                'question': 'Describe your experience with version control. How do you handle merge conflicts and what branching strategy do you prefer?',
                'difficulty': 'easy',
                'expected_keywords': ['git', 'branch', 'merge', 'conflict', 'pull request', 'code review', 'gitflow'],
                'time_limit_minutes': 7,
                'follow_up': 'Tell me about a time when a merge went wrong and how you resolved it.'
            }
        ],
        'architecture': [
            {
                'id': 'SD_A1',
                'question': 'Design a URL shortener service like bit.ly. Discuss database schema, API endpoints, scaling strategy, and how you\'d handle 1 million requests per day.',
                'difficulty': 'hard',
                'expected_keywords': ['hash', 'database', 'redis', 'caching', 'load balancer', 'distributed', 'sharding', 'api design'],
                'time_limit_minutes': 15,
                'follow_up': 'How would you handle analytics and track click statistics?'
            },
            {
                'id': 'SD_A2',
                'question': 'Explain the difference between monolithic and microservices architecture. When would you choose one over the other?',
                'difficulty': 'medium',
                'expected_keywords': ['monolithic', 'microservices', 'scalability', 'deployment', 'communication', 'trade-offs', 'complexity'],
                'time_limit_minutes': 10,
                'follow_up': 'How do you handle distributed transactions in microservices?'
            }
        ],
        'problem_solving': [
            {
                'id': 'SD_PS1',
                'question': 'Write a function to find the longest palindromic substring in a given string. Explain your approach and analyze time/space complexity.',
                'difficulty': 'hard',
                'expected_keywords': ['palindrome', 'substring', 'algorithm', 'complexity', 'optimization', 'dynamic programming'],
                'time_limit_minutes': 15,
                'follow_up': 'Can you optimize this for very large strings?'
            },
            {
                'id': 'SD_PS2',
                'question': 'How would you detect a cycle in a linked list? Implement the solution and explain the algorithm.',
                'difficulty': 'medium',
                'expected_keywords': ['cycle', 'linked list', 'two pointers', 'floyd', 'tortoise and hare', 'time complexity'],
                'time_limit_minutes': 10,
                'follow_up': 'How would you find the start point of the cycle?'
            }
        ]
    },
    
    'data_analyst': {
        'fundamentals': [
            {
                'id': 'DA_F1',
                'question': 'Explain the difference between correlation and causation. Provide an example of when understanding this distinction prevented a bad business decision.',
                'difficulty': 'medium',
                'expected_keywords': ['correlation', 'causation', 'confounding', 'spurious', 'relationship', 'statistical', 'experiment'],
                'time_limit_minutes': 8,
                'follow_up': 'How would you design an experiment to establish causation?'
            },
            {
                'id': 'DA_F2',
                'question': 'Walk me through your process for cleaning and preparing messy data. What tools do you use and how do you handle missing values?',
                'difficulty': 'easy',
                'expected_keywords': ['cleaning', 'preprocessing', 'missing values', 'outliers', 'pandas', 'validation', 'imputation'],
                'time_limit_minutes': 7,
                'follow_up': 'How do you decide between removing or imputing missing data?'
            },
            {
                'id': 'DA_F3',
                'question': 'Describe a complex SQL query you\'ve written. What was the business problem and how did you optimize it?',
                'difficulty': 'hard',
                'expected_keywords': ['sql', 'join', 'subquery', 'cte', 'window function', 'optimization', 'index', 'performance'],
                'time_limit_minutes': 12,
                'follow_up': 'How did you validate the results were correct?'
            }
        ],
        'visualization': [
            {
                'id': 'DA_V1',
                'question': 'You need to present quarterly sales data to executives. What visualizations would you choose and why? How do you ensure your visualizations don\'t mislead?',
                'difficulty': 'medium',
                'expected_keywords': ['dashboard', 'chart', 'visualization', 'insight', 'clarity', 'audience', 'storytelling', 'misleading'],
                'time_limit_minutes': 10,
                'follow_up': 'Give an example of a misleading visualization you\'ve seen.'
            },
            {
                'id': 'DA_V2',
                'question': 'Explain when you would use a box plot vs. a histogram vs. a scatter plot. Provide specific business use cases.',
                'difficulty': 'easy',
                'expected_keywords': ['box plot', 'histogram', 'scatter plot', 'distribution', 'outliers', 'correlation', 'use case'],
                'time_limit_minutes': 6,
                'follow_up': 'How do you choose the right bin size for histograms?'
            }
        ],
        'statistics': [
            {
                'id': 'DA_S1',
                'question': 'Explain A/B testing. If you ran a test with 10,000 users and saw a 5% improvement with p-value 0.06, what would you recommend?',
                'difficulty': 'hard',
                'expected_keywords': ['a/b test', 'hypothesis', 'p-value', 'significance', 'sample size', 'statistical power', 'confidence'],
                'time_limit_minutes': 12,
                'follow_up': 'How would you detect and handle a novelty effect?'
            },
            {
                'id': 'DA_S2',
                'question': 'A company claims their new feature increased user retention by 20%. How would you verify this claim? What questions would you ask?',
                'difficulty': 'medium',
                'expected_keywords': ['retention', 'metric', 'cohort', 'baseline', 'statistical test', 'bias', 'confounding', 'validation'],
                'time_limit_minutes': 10,
                'follow_up': 'What are potential biases in measuring retention?'
            }
        ],
        'business_acumen': [
            {
                'id': 'DA_BA1',
                'question': 'Describe a time when your analysis led to a business decision that saved money or increased revenue. What was your approach?',
                'difficulty': 'medium',
                'expected_keywords': ['analysis', 'insight', 'recommendation', 'impact', 'stakeholder', 'data-driven', 'business value'],
                'time_limit_minutes': 10,
                'follow_up': 'How did you measure the impact of your recommendation?'
            },
            {
                'id': 'DA_BA2',
                'question': 'If you notice a sudden 30% drop in a key metric, what steps would you take to investigate?',
                'difficulty': 'hard',
                'expected_keywords': ['investigation', 'root cause', 'data quality', 'segmentation', 'timeline', 'hypothesis', 'debugging'],
                'time_limit_minutes': 12,
                'follow_up': 'How do you prioritize which hypotheses to test first?'
            }
        ]
    },
    
    'data_scientist': {
        'ml_fundamentals': [
            {
                'id': 'DS_ML1',
                'question': 'Explain bias-variance tradeoff. How do you diagnose and fix high bias vs. high variance in your models?',
                'difficulty': 'hard',
                'expected_keywords': ['bias', 'variance', 'overfitting', 'underfitting', 'regularization', 'cross-validation', 'learning curve'],
                'time_limit_minutes': 12,
                'follow_up': 'Give a real example from a project where you balanced this tradeoff.'
            },
            {
                'id': 'DS_ML2',
                'question': 'Walk me through building a machine learning model from scratch - data collection to deployment. What are the most common pitfalls?',
                'difficulty': 'hard',
                'expected_keywords': ['pipeline', 'feature engineering', 'training', 'validation', 'deployment', 'monitoring', 'data drift'],
                'time_limit_minutes': 15,
                'follow_up': 'How do you handle model decay in production?'
            },
            {
                'id': 'DS_ML3',
                'question': 'Compare Random Forest and Gradient Boosting. When would you choose one over the other?',
                'difficulty': 'medium',
                'expected_keywords': ['random forest', 'gradient boosting', 'ensemble', 'bagging', 'boosting', 'overfitting', 'interpretability'],
                'time_limit_minutes': 10,
                'follow_up': 'How do you tune hyperparameters for these models?'
            }
        ],
        'deep_learning': [
            {
                'id': 'DS_DL1',
                'question': 'Explain how backpropagation works. How would you debug a neural network that isn\'t learning?',
                'difficulty': 'hard',
                'expected_keywords': ['backpropagation', 'gradient', 'chain rule', 'loss function', 'vanishing gradient', 'learning rate', 'debugging'],
                'time_limit_minutes': 15,
                'follow_up': 'What techniques prevent vanishing/exploding gradients?'
            },
            {
                'id': 'DS_DL2',
                'question': 'Describe the architecture and use cases for: CNN, RNN, and Transformer models. Which would you use for sentiment analysis?',
                'difficulty': 'hard',
                'expected_keywords': ['cnn', 'rnn', 'transformer', 'architecture', 'sentiment analysis', 'nlp', 'attention mechanism'],
                'time_limit_minutes': 12,
                'follow_up': 'How do attention mechanisms improve performance?'
            }
        ],
        'feature_engineering': [
            {
                'id': 'DS_FE1',
                'question': 'You have a dataset with categorical variables that have high cardinality (thousands of unique values). How would you handle this?',
                'difficulty': 'medium',
                'expected_keywords': ['categorical', 'encoding', 'target encoding', 'embedding', 'dimensionality', 'curse of dimensionality'],
                'time_limit_minutes': 10,
                'follow_up': 'What are the risks of target encoding?'
            },
            {
                'id': 'DS_FE2',
                'question': 'Describe your approach to feature selection. What techniques do you use and how do you avoid data leakage?',
                'difficulty': 'hard',
                'expected_keywords': ['feature selection', 'importance', 'correlation', 'mutual information', 'data leakage', 'pipeline'],
                'time_limit_minutes': 12,
                'follow_up': 'Give an example of subtle data leakage you\'ve encountered.'
            }
        ]
    },
    
    'devops_engineer': {
        'fundamentals': [
            {
                'id': 'DO_F1',
                'question': 'Explain the CI/CD pipeline you\'ve implemented. What tools did you use and how did you ensure deployment safety?',
                'difficulty': 'hard',
                'expected_keywords': ['ci/cd', 'pipeline', 'jenkins', 'github actions', 'testing', 'deployment', 'rollback', 'blue-green'],
                'time_limit_minutes': 12,
                'follow_up': 'How do you handle failed deployments?'
            },
            {
                'id': 'DO_F2',
                'question': 'Describe your experience with containerization. How does Docker differ from virtual machines? When would you use each?',
                'difficulty': 'medium',
                'expected_keywords': ['docker', 'container', 'virtual machine', 'isolation', 'orchestration', 'kubernetes', 'lightweight'],
                'time_limit_minutes': 10,
                'follow_up': 'How do you optimize Docker image sizes?'
            },
            {
                'id': 'DO_F3',
                'question': 'Walk me through how you\'d troubleshoot a production server that\'s experiencing high latency.',
                'difficulty': 'hard',
                'expected_keywords': ['troubleshooting', 'latency', 'monitoring', 'logs', 'metrics', 'profiling', 'bottleneck', 'debugging'],
                'time_limit_minutes': 15,
                'follow_up': 'What monitoring tools do you use and why?'
            }
        ],
        'infrastructure': [
            {
                'id': 'DO_I1',
                'question': 'Explain Infrastructure as Code. Compare Terraform vs. CloudFormation. Which do you prefer and why?',
                'difficulty': 'medium',
                'expected_keywords': ['iac', 'terraform', 'cloudformation', 'declarative', 'state management', 'version control', 'automation'],
                'time_limit_minutes': 10,
                'follow_up': 'How do you manage secrets in IaC?'
            },
            {
                'id': 'DO_I2',
                'question': 'Design a highly available and scalable architecture for an e-commerce application. Consider database, caching, and disaster recovery.',
                'difficulty': 'hard',
                'expected_keywords': ['high availability', 'scalability', 'load balancer', 'database replication', 'caching', 'disaster recovery', 'failover'],
                'time_limit_minutes': 15,
                'follow_up': 'What\'s your RTO and RPO strategy?'
            }
        ]
    },
    
    'product_manager': {
        'strategy': [
            {
                'id': 'PM_S1',
                'question': 'Describe how you prioritize features when you have limited engineering resources and multiple stakeholder requests.',
                'difficulty': 'hard',
                'expected_keywords': ['prioritization', 'stakeholder', 'impact', 'effort', 'rice', 'moscow', 'roadmap', 'trade-offs'],
                'time_limit_minutes': 12,
                'follow_up': 'How do you say no to important stakeholders?'
            },
            {
                'id': 'PM_S2',
                'question': 'Tell me about a product you shipped that didn\'t perform as expected. What did you learn and how did you pivot?',
                'difficulty': 'medium',
                'expected_keywords': ['failure', 'learning', 'metrics', 'pivot', 'user feedback', 'iteration', 'retrospective'],
                'time_limit_minutes': 10,
                'follow_up': 'How did you communicate this to leadership?'
            }
        ],
        'metrics': [
            {
                'id': 'PM_M1',
                'question': 'How would you measure the success of [company\'s product]? What are the key metrics and why?',
                'difficulty': 'hard',
                'expected_keywords': ['metrics', 'kpi', 'success criteria', 'user engagement', 'retention', 'conversion', 'north star metric'],
                'time_limit_minutes': 12,
                'follow_up': 'How do you avoid vanity metrics?'
            }
        ]
    },
    
    'ui_ux_designer': {
        'design_process': [
            {
                'id': 'UX_DP1',
                'question': 'Walk me through your design process from user research to final implementation. How do you validate your designs?',
                'difficulty': 'medium',
                'expected_keywords': ['user research', 'wireframe', 'prototype', 'usability testing', 'iteration', 'feedback', 'validation'],
                'time_limit_minutes': 12,
                'follow_up': 'How do you balance user needs with business goals?'
            },
            {
                'id': 'UX_DP2',
                'question': 'Describe a time when user testing revealed your initial design was wrong. How did you respond?',
                'difficulty': 'hard',
                'expected_keywords': ['user testing', 'feedback', 'iteration', 'redesign', 'learning', 'humility', 'data-driven'],
                'time_limit_minutes': 10,
                'follow_up': 'How do you prevent confirmation bias in testing?'
            }
        ],
        'principles': [
            {
                'id': 'UX_P1',
                'question': 'Explain key accessibility principles. How do you ensure your designs are accessible to users with disabilities?',
                'difficulty': 'medium',
                'expected_keywords': ['accessibility', 'wcag', 'screen reader', 'contrast', 'keyboard navigation', 'inclusive design'],
                'time_limit_minutes': 10,
                'follow_up': 'Give an example of an accessibility issue you fixed.'
            }
        ]
    }
}

# Behavioral questions applicable to all roles
UNIVERSAL_BEHAVIORAL_QUESTIONS = [
    {
        'id': 'BEH_1',
        'question': 'Tell me about a time when you had to learn a new technology or skill quickly to complete a project. How did you approach it?',
        'difficulty': 'medium',
        'category': 'learning_agility',
        'expected_keywords': ['learning', 'self-taught', 'documentation', 'practice', 'deadline', 'resourceful'],
        'star_required': True
    },
    {
        'id': 'BEH_2',
        'question': 'Describe a situation where you disagreed with a team member or manager. How did you handle it and what was the outcome?',
        'difficulty': 'hard',
        'category': 'conflict_resolution',
        'expected_keywords': ['disagreement', 'communication', 'compromise', 'resolution', 'respect', 'outcome'],
        'star_required': True
    },
    {
        'id': 'BEH_3',
        'question': 'Give me an example of a project that didn\'t go as planned. What went wrong and what did you do about it?',
        'difficulty': 'medium',
        'category': 'problem_solving',
        'expected_keywords': ['challenge', 'problem', 'solution', 'adaptation', 'learning', 'outcome'],
        'star_required': True
    },
    {
        'id': 'BEH_4',
        'question': 'Tell me about your greatest professional achievement. What made it significant and what was your specific contribution?',
        'difficulty': 'easy',
        'category': 'achievement',
        'expected_keywords': ['achievement', 'impact', 'contribution', 'success', 'measurable', 'proud'],
        'star_required': True
    },
    {
        'id': 'BEH_5',
        'question': 'Describe a time when you had to work with a difficult stakeholder or client. How did you manage the relationship?',
        'difficulty': 'hard',
        'category': 'stakeholder_management',
        'expected_keywords': ['stakeholder', 'difficult', 'communication', 'expectations', 'relationship', 'diplomacy'],
        'star_required': True
    },
    {
        'id': 'BEH_6',
        'question': 'Tell me about a time when you identified a process improvement. How did you implement it and what was the impact?',
        'difficulty': 'medium',
        'category': 'initiative',
        'expected_keywords': ['improvement', 'initiative', 'process', 'efficiency', 'implementation', 'impact'],
        'star_required': True
    }
]


# ============================================================================
# ROLE DETECTION AND MAPPING
# ============================================================================

ROLE_KEYWORDS = {
    'software_developer': ['software', 'developer', 'programmer', 'backend', 'frontend', 'fullstack', 'full stack', 'engineer', 'sde', 'coding'],
    'data_analyst': ['data analyst', 'business analyst', 'analytics', 'bi developer', 'data visualization'],
    'data_scientist': ['data scientist', 'machine learning', 'ml engineer', 'ai engineer', 'deep learning', 'nlp'],
    'devops_engineer': ['devops', 'sre', 'site reliability', 'infrastructure', 'cloud engineer', 'platform engineer'],
    'product_manager': ['product manager', 'product owner', 'pm', 'product lead'],
    'ui_ux_designer': ['ui designer', 'ux designer', 'ui/ux', 'product designer', 'interaction designer']
}


def detect_role_from_job(job: Dict) -> str:
    """
    Intelligently detect the role category from job title and description
    """
    job_title = job.get('title', '').lower()
    job_desc = job.get('description', '').lower()
    combined_text = f"{job_title} {job_desc}"
    
    # Score each role category
    role_scores = {}
    for role, keywords in ROLE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in combined_text)
        if score > 0:
            role_scores[role] = score
    
    # Return role with highest score, default to software_developer
    if role_scores:
        return max(role_scores.items(), key=lambda x: x[1])[0]
    return 'software_developer'


# ============================================================================
# ENHANCED QUESTION GENERATION
# ============================================================================

def generate_dynamic_interview_questions(
    job: Dict,
    candidate: Optional[Dict] = None,
    num_questions: int = 10,
    include_behavioral: bool = True,
    difficulty_distribution: Optional[Dict] = None
) -> List[Dict]:
    """
    Generate highly personalized interview questions based on:
    - Job role and requirements
    - Candidate experience level
    - Required skills
    - Difficulty distribution
    
    Args:
        job: Job dictionary with title, description, required_skills, experience_level
        candidate: Optional candidate dictionary with skills, experience_years
        num_questions: Total number of questions to generate
        include_behavioral: Whether to include behavioral questions
        difficulty_distribution: {'easy': 0.2, 'medium': 0.5, 'hard': 0.3}
    
    Returns:
        List of personalized interview questions
    """
    
    # Detect role
    role = detect_role_from_job(job)
    print(f"🎯 Detected role: {role}")
    
    # Get role-specific question bank
    role_questions = ROLE_QUESTION_BANKS.get(role, ROLE_QUESTION_BANKS['software_developer'])
    
    # Determine candidate experience level
    experience_level = _determine_experience_level(job, candidate)
    print(f"📊 Experience level: {experience_level}")
    
    # Set difficulty distribution based on experience
    if not difficulty_distribution:
        if experience_level == 'entry':
            difficulty_distribution = {'easy': 0.5, 'medium': 0.4, 'hard': 0.1}
        elif experience_level == 'mid':
            difficulty_distribution = {'easy': 0.2, 'medium': 0.5, 'hard': 0.3}
        else:  # senior
            difficulty_distribution = {'easy': 0.1, 'medium': 0.4, 'hard': 0.5}
    
    # Calculate question counts
    behavioral_count = min(3, num_questions // 3) if include_behavioral else 0
    technical_count = num_questions - behavioral_count
    
    # Generate technical questions
    technical_questions = _generate_technical_questions(
        role_questions,
        technical_count,
        difficulty_distribution,
        job,
        candidate
    )
    
    # Generate behavioral questions
    behavioral_questions = []
    if include_behavioral:
        behavioral_questions = _generate_behavioral_questions(
            behavioral_count,
            experience_level
        )
    
    # Combine and add metadata
    all_questions = technical_questions + behavioral_questions
    
    # Add job-specific context
    for q in all_questions:
        q['job_title'] = job.get('title')
        q['job_id'] = str(job.get('_id', ''))
        q['generated_at'] = datetime.utcnow().isoformat()
        q['candidate_level'] = experience_level
    
    print(f"✅ Generated {len(all_questions)} questions ({len(technical_questions)} technical, {len(behavioral_questions)} behavioral)")
    
    return all_questions


def _determine_experience_level(job: Dict, candidate: Optional[Dict]) -> str:
    """
    Determine appropriate experience level for question difficulty
    """
    # Check job requirements first
    job_min_exp = job.get('min_experience_years', 0)
    job_title = job.get('title', '').lower()
    
    # Determine from job posting
    if 'senior' in job_title or 'lead' in job_title or 'principal' in job_title or job_min_exp >= 5:
        job_level = 'senior'
    elif 'junior' in job_title or 'entry' in job_title or 'associate' in job_title or job_min_exp <= 1:
        job_level = 'entry'
    else:
        job_level = 'mid'
    
    # If candidate info available, consider it
    if candidate:
        candidate_exp = candidate.get('experience_years', 0)
        if candidate_exp >= 5:
            candidate_level = 'senior'
        elif candidate_exp <= 1:
            candidate_level = 'entry'
        else:
            candidate_level = 'mid'
        
        # Use the higher of job or candidate level (challenge them appropriately)
        levels = {'entry': 1, 'mid': 2, 'senior': 3}
        return 'entry' if levels.get(job_level, 2) > levels.get(candidate_level, 2) else candidate_level
    
    return job_level


def _generate_technical_questions(
    role_questions: Dict,
    count: int,
    difficulty_dist: Dict,
    job: Dict,
    candidate: Optional[Dict]
) -> List[Dict]:
    """
    Generate technical questions based on role and difficulty distribution
    """
    questions = []
    
    # Flatten all role questions
    all_role_questions = []
    for category, category_questions in role_questions.items():
        for q in category_questions:
            q['category'] = category
            all_role_questions.append(q)
    
    # Calculate how many of each difficulty
    easy_count = int(count * difficulty_dist.get('easy', 0.2))
    hard_count = int(count * difficulty_dist.get('hard', 0.3))
    medium_count = count - easy_count - hard_count
    
    # Select questions by difficulty
    easy_questions = [q for q in all_role_questions if q['difficulty'] == 'easy']
    medium_questions = [q for q in all_role_questions if q['difficulty'] == 'medium']
    hard_questions = [q for q in all_role_questions if q['difficulty'] == 'hard']
    
    # Randomly sample from each difficulty
    if easy_questions:
        questions.extend(random.sample(easy_questions, min(easy_count, len(easy_questions))))
    if medium_questions:
        questions.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
    if hard_questions:
        questions.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))
    
    # If we don't have enough, fill with any available
    if len(questions) < count:
        remaining = [q for q in all_role_questions if q not in questions]
        questions.extend(random.sample(remaining, min(count - len(questions), len(remaining))))
    
    # Add points based on difficulty
    for q in questions:
        if q['difficulty'] == 'easy':
            q['points'] = 5
        elif q['difficulty'] == 'medium':
            q['points'] = 10
        else:
            q['points'] = 15
    
    return questions


def _generate_behavioral_questions(count: int, experience_level: str) -> List[Dict]:
    """
    Generate behavioral questions appropriate for experience level
    """
    # Filter questions by experience level
    if experience_level == 'entry':
        # For entry level, avoid questions requiring extensive experience
        suitable = [q for q in UNIVERSAL_BEHAVIORAL_QUESTIONS 
                   if q['category'] in ['learning_agility', 'achievement', 'problem_solving']]
    else:
        suitable = UNIVERSAL_BEHAVIORAL_QUESTIONS
    
    # Randomly select
    selected = random.sample(suitable, min(count, len(suitable)))
    
    # Add metadata
    for q in selected:
        q['type'] = 'behavioral'
        q['time_limit_minutes'] = 8 if q['difficulty'] == 'easy' else 12
        q['points'] = 10
    
    return selected


# ============================================================================
# ADVANCED ANSWER EVALUATION
# ============================================================================

def evaluate_answer_advanced(question: Dict, answer: str) -> Dict:
    """
    Enhanced answer evaluation with deeper analysis
    """
    if not answer or len(answer.strip()) < 10:
        return {
            'score': 0,
            'max_score': question.get('points', 10),
            'percentage': 0,
            'feedback': '❌ Answer too short or empty',
            'keyword_match_count': 0,
            'total_keywords': len(question.get('expected_keywords', [])),
            'strengths': [],
            'areas_for_improvement': ['Provide more detail', 'Address the question directly'],
            'follow_up_questions': [question.get('follow_up', '')]
        }
    
    answer_lower = answer.lower()
    expected_keywords = question.get('expected_keywords', [])
    
    # Keyword matching
    matched_keywords = [kw for kw in expected_keywords if kw.lower() in answer_lower]
    keyword_score = (len(matched_keywords) / len(expected_keywords)) * 100 if expected_keywords else 50
    
    # Length analysis (should be substantial but not rambling)
    word_count = len(answer.split())
    if word_count < 30:
        length_score = word_count / 30 * 100
        length_feedback = "Too brief - provide more detail"
    elif word_count > 500:
        length_score = 85  # Penalize excessive length slightly
        length_feedback = "Very detailed - ensure you're staying on topic"
    else:
        length_score = 100
        length_feedback = "Good length"
    
    # STAR method check for behavioral questions
    star_score = 0
    star_feedback = ""
    if question.get('star_required', False):
        star_components = {
            'situation': any(word in answer_lower for word in ['when', 'situation', 'context', 'background']),
            'task': any(word in answer_lower for word in ['needed', 'had to', 'responsible', 'goal', 'objective']),
            'action': any(word in answer_lower for word in ['i did', 'i implemented', 'i created', 'i developed', 'my approach']),
            'result': any(word in answer_lower for word in ['result', 'outcome', 'achieved', 'impact', 'improved', 'increased'])
        }
        star_score = (sum(star_components.values()) / 4) * 100
        missing_components = [k.upper() for k, v in star_components.items() if not v]
        if missing_components:
            star_feedback = f"Consider adding: {', '.join(missing_components)}"
    
    # Technical depth indicators
    technical_depth = any(word in answer_lower for word in 
                         ['because', 'therefore', 'however', 'specifically', 'for example', 'such as'])
    depth_score = 100 if technical_depth else 70
    
    # Calculate final score
    max_score = question.get('points', 10)
    if question.get('star_required'):
        final_percentage = (keyword_score * 0.4 + length_score * 0.2 + star_score * 0.3 + depth_score * 0.1)
    else:
        final_percentage = (keyword_score * 0.6 + length_score * 0.2 + depth_score * 0.2)
    
    final_score = (final_percentage / 100) * max_score
    
    # Generate feedback
    strengths = []
    improvements = []
    
    if len(matched_keywords) >= len(expected_keywords) * 0.7:
        strengths.append(f"✅ Covered key concepts: {', '.join(matched_keywords[:3])}")
    else:
        improvements.append(f"Missing key concepts: {', '.join([kw for kw in expected_keywords if kw not in matched_keywords][:3])}")
    
    if word_count >= 50:
        strengths.append("✅ Provided detailed explanation")
    else:
        improvements.append("Provide more detail and examples")
    
    if technical_depth:
        strengths.append("✅ Demonstrated reasoning and examples")
    else:
        improvements.append("Add more reasoning and concrete examples")
    
    if question.get('star_required'):
        if star_score >= 75:
            strengths.append("✅ Clear STAR structure")
        else:
            improvements.append(star_feedback)
    
    # Generate feedback summary
    if final_percentage >= 80:
        feedback = "🌟 Excellent answer! Strong understanding demonstrated."
    elif final_percentage >= 60:
        feedback = "👍 Good answer with room for improvement."
    elif final_percentage >= 40:
        feedback = "⚠️ Acceptable but needs more depth and detail."
    else:
        feedback = "❌ Insufficient answer. Please elaborate more."
    
    return {
        'score': round(final_score, 1),
        'max_score': max_score,
        'percentage': round(final_percentage, 1),
        'feedback': feedback,
        'detailed_scores': {
            'keyword_coverage': round(keyword_score, 1),
            'length_appropriateness': round(length_score, 1),
            'star_structure': round(star_score, 1) if question.get('star_required') else None,
            'technical_depth': round(depth_score, 1)
        },
        'keyword_match_count': len(matched_keywords),
        'total_keywords': len(expected_keywords),
        'matched_keywords': matched_keywords,
        'word_count': word_count,
        'strengths': strengths,
        'areas_for_improvement': improvements,
        'follow_up_questions': [question.get('follow_up', '')],
        'length_feedback': length_feedback
    }


# ============================================================================
# INTERVIEW SCHEDULE GENERATION
# ============================================================================

def create_interview_schedule_advanced(
    questions: List[Dict],
    total_duration_minutes: int = 60,
    include_breaks: bool = True
) -> Dict:
    """
    Create a detailed interview schedule with time allocation
    """
    # Calculate total question time
    total_question_time = sum(q.get('time_limit_minutes', 10) for q in questions)
    
    # Add intro (5 min) and outro (5 min)
    intro_time = 5
    outro_time = 5
    break_time = 5 if include_breaks and total_duration_minutes >= 45 else 0
    
    available_time = total_duration_minutes - intro_time - outro_time - break_time
    
    # Scale question times if needed
    scale_factor = available_time / total_question_time if total_question_time > available_time else 1
    
    # Build schedule
    schedule = {
        'total_duration_minutes': total_duration_minutes,
        'sections': [
            {
                'section': 'Introduction',
                'duration_minutes': intro_time,
                'description': 'Welcome, role overview, interview structure explanation'
            }
        ],
        'questions': [],
        'break_included': include_breaks
    }
    
    current_time = intro_time
    for i, q in enumerate(questions, 1):
        allocated_time = int(q.get('time_limit_minutes', 10) * scale_factor)
        schedule['questions'].append({
            'question_number': i,
            'question_id': q.get('id'),
            'question': q.get('question'),
            'start_time_minutes': current_time,
            'allocated_minutes': allocated_time,
            'difficulty': q.get('difficulty'),
            'points': q.get('points'),
            'category': q.get('category', q.get('type', 'technical'))
        })
        current_time += allocated_time
        
        # Add break after halfway point
        if include_breaks and i == len(questions) // 2:
            schedule['sections'].append({
                'section': 'Break',
                'duration_minutes': break_time,
                'start_time_minutes': current_time,
                'description': 'Short break'
            })
            current_time += break_time
    
    schedule['sections'].append({
        'section': 'Closing',
        'duration_minutes': outro_time,
        'start_time_minutes': current_time,
        'description': 'Q&A, next steps, thank you'
    })
    
    # Summary
    schedule['summary'] = {
        'total_questions': len(questions),
        'technical_questions': len([q for q in questions if q.get('type') != 'behavioral']),
        'behavioral_questions': len([q for q in questions if q.get('type') == 'behavioral']),
        'total_points': sum(q.get('points', 0) for q in questions),
        'difficulty_breakdown': {
            'easy': len([q for q in questions if q.get('difficulty') == 'easy']),
            'medium': len([q for q in questions if q.get('difficulty') == 'medium']),
            'hard': len([q for q in questions if q.get('difficulty') == 'hard'])
        }
    }
    
    return schedule


# ============================================================================
# PUBLIC API
# ============================================================================

# Keep backward compatibility
generate_interview_questions = generate_dynamic_interview_questions
evaluate_answer = evaluate_answer_advanced
create_interview_schedule = create_interview_schedule_advanced
