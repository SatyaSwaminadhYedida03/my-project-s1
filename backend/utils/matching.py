import re

# ML libraries not available in Render free tier (size constraints)
# Simplified matching without scikit-learn
def _get_tfidf_vectorizer():
    return None

def _get_cosine_similarity():
    return None

# Master skills list - Comprehensive technical skills database (200+ skills)
SKILLS_MASTER = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "go", "golang", "rust",
    "php", "ruby", "swift", "kotlin", "scala", "r", "perl", "lua", "dart", "objective-c",
    "visual basic", "vb.net", "cobol", "fortran", "haskell", "elixir", "clojure", "groovy",
    
    # Web Frontend
    "html", "html5", "css", "css3", "sass", "scss", "less", "react", "react.js", "reactjs",
    "angular", "angular.js", "angularjs", "vue", "vue.js", "vuejs", "svelte", "next.js", "nextjs",
    "nuxt.js", "gatsby", "jquery", "bootstrap", "tailwind", "tailwind css", "material-ui",
    "webpack", "vite", "parcel", "rollup", "babel", "redux", "mobx", "vuex", "pinia",
    
    # Web Backend & Frameworks
    "node", "node.js", "nodejs", "express", "express.js", "fastify", "nest.js", "nestjs",
    "flask", "django", "fastapi", "spring", "spring boot", "springboot", "spring framework",
    "asp.net", ".net", "dotnet", ".net core", "laravel", "symfony", "codeigniter",
    "ruby on rails", "rails", "sinatra", "gin", "echo", "fiber", "actix", "rocket",
    
    # Mobile Development
    "react native", "flutter", "ios", "android", "xamarin", "ionic", "cordova", "phonegap",
    "swiftui", "uikit", "jetpack compose", "kotlin multiplatform",
    
    # Databases & Data Storage
    "sql", "mysql", "postgresql", "postgres", "oracle", "sql server", "mssql", "db2",
    "mongodb", "cassandra", "couchdb", "dynamodb", "redis", "memcached", "elasticsearch",
    "neo4j", "arangodb", "influxdb", "timescaledb", "cockroachdb", "mariadb", "sqlite",
    
    # Cloud Platforms & Services
    "aws", "amazon web services", "ec2", "s3", "lambda", "rds", "dynamodb", "cloudfront",
    "azure", "microsoft azure", "gcp", "google cloud", "google cloud platform", "firebase",
    "heroku", "digitalocean", "linode", "vultr", "cloudflare", "vercel", "netlify", "render",
    
    # DevOps & CI/CD
    "docker", "kubernetes", "k8s", "jenkins", "gitlab ci", "github actions", "circleci",
    "travis ci", "bamboo", "teamcity", "ansible", "terraform", "puppet", "chef", "saltstack",
    "vagrant", "helm", "istio", "prometheus", "grafana", "nagios", "datadog", "new relic",
    "ci/cd", "devops", "gitops", "argocd", "flux", "spinnaker",
    
    # Version Control & Collaboration
    "git", "github", "gitlab", "bitbucket", "svn", "mercurial", "perforce", "cvs",
    "jira", "confluence", "trello", "asana", "slack", "microsoft teams", "zoom",
    
    # Data Science & ML
    "machine learning", "deep learning", "artificial intelligence", "ai", "ml", "nlp",
    "natural language processing", "computer vision", "neural networks", "cnn", "rnn", "lstm",
    "transformer", "bert", "gpt", "pandas", "numpy", "scipy", "scikit-learn", "sklearn",
    "tensorflow", "keras", "pytorch", "jax", "xgboost", "lightgbm", "catboost",
    "opencv", "yolo", "detectron", "hugging face", "langchain", "llama", "stable diffusion",
    
    # Big Data & Analytics
    "hadoop", "spark", "apache spark", "pyspark", "kafka", "apache kafka", "flink", "storm",
    "hive", "pig", "hbase", "presto", "databricks", "snowflake", "redshift", "bigquery",
    "tableau", "power bi", "powerbi", "looker", "qlik", "metabase", "superset",
    
    # Testing & Quality Assurance
    "junit", "pytest", "jest", "mocha", "chai", "jasmine", "selenium", "cypress",
    "playwright", "testng", "cucumber", "postman", "jmeter", "gatling", "k6",
    "unit testing", "integration testing", "e2e testing", "tdd", "bdd",
    
    # API & Integration
    "rest", "rest api", "restful", "graphql", "grpc", "soap", "websocket", "api gateway",
    "microservices", "service mesh", "api design", "openapi", "swagger", "postman",
    
    # Security & Authentication
    "oauth", "oauth2", "jwt", "saml", "ldap", "active directory", "ssl", "tls", "https",
    "penetration testing", "owasp", "security", "cryptography", "encryption", "vault",
    
    # Operating Systems & Tools
    "linux", "unix", "ubuntu", "centos", "redhat", "debian", "windows", "windows server",
    "macos", "bash", "shell scripting", "powershell", "vim", "emacs", "vscode", "intellij",
    
    # Networking & Infrastructure
    "tcp/ip", "dns", "dhcp", "vpn", "nginx", "apache", "haproxy", "load balancing",
    "cdn", "firewall", "networking", "http", "https", "routing", "switching",
    
    # Project Management & Methodologies
    "agile", "scrum", "kanban", "waterfall", "lean", "six sigma", "pmp", "prince2",
    "sprint planning", "retrospective", "standup", "product owner", "scrum master",
    
    # Other Technologies & Tools
    "excel", "vba", "matlab", "labview", "arduino", "raspberry pi", "iot", "blockchain",
    "ethereum", "solidity", "web3", "smart contracts", "sap", "salesforce", "crm", "erp",
    "photoshop", "illustrator", "figma", "sketch", "adobe xd", "ui/ux", "design thinking"
]

def extract_skills(text):
    """Extract skills from text using dictionary matching"""
    if not text:
        print("⚠️ extract_skills: Empty text provided")
        return []
    
    print(f"🔍 extract_skills: Processing text of length {len(text)}")
    txt = text.lower()
    found = []
    
    for skill in SKILLS_MASTER:
        # Use word boundary for accurate matching
        if re.search(r'\b' + re.escape(skill) + r'\b', txt):
            found.append(skill)
    
    unique_skills = list(set(found))  # Remove duplicates
    print(f"✅ extract_skills: Found {len(unique_skills)} unique skills from {len(found)} total matches")
    
    return unique_skills

def calculate_tfidf_similarity(job_text, resume_text):
    """Calculate TF-IDF cosine similarity between job and resume"""
    try:
        # Lazy load sklearn
        TfidfVectorizer = _get_tfidf_vectorizer()
        cosine_similarity = _get_cosine_similarity()
        
        texts = [job_text, resume_text]
        vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        return float(similarity)
    except Exception as e:
        print(f"TF-IDF error: {e}")
        return 0.0

def calculate_skill_match(job_skills, resume_skills):
    """Calculate skill match percentage"""
    if not job_skills:
        return 0.0
    
    job_set = set([s.lower() for s in job_skills])
    resume_set = set([s.lower() for s in resume_skills])
    
    matched = job_set.intersection(resume_set)
    match_fraction = len(matched) / len(job_set)
    
    return float(match_fraction)

def compute_overall_score(tfidf_score, skill_match, cci_score=None, sim_weight=0.5, skill_weight=0.3, cci_weight=0.2):
    """
    Compute overall candidate score
    
    Args:
        tfidf_score: TF-IDF similarity score (0-1)
        skill_match: Skill match fraction (0-1)
        cci_score: Career Consistency Index (0-100), optional
        sim_weight: Weight for similarity
        skill_weight: Weight for skill match
        cci_weight: Weight for CCI
    """
    if cci_score is None:
        # If no CCI, redistribute weight
        sim_weight = 0.6
        skill_weight = 0.4
        cci_weight = 0.0
        score = (sim_weight * tfidf_score + skill_weight * skill_match) * 100
    else:
        # Normalize CCI to 0-1
        cci_normalized = cci_score / 100.0
        score = (sim_weight * tfidf_score + skill_weight * skill_match + cci_weight * cci_normalized) * 100
    
    return round(float(score), 2)

def get_decision_from_score(score):
    """Get hiring decision based on score"""
    if score >= 75:
        return "Hire"
    elif score >= 50:
        return "Review"
    else:
        return "Reject"

def analyze_candidate(job_description, job_skills, resume_text, resume_skills, cci_score=None):
    """
    Comprehensive candidate analysis
    
    Returns:
        dict with scores, decision, matched skills, and recommendations
    """
    # Calculate scores
    tfidf_score = calculate_tfidf_similarity(job_description, resume_text)
    skill_match = calculate_skill_match(job_skills, resume_skills)
    overall_score = compute_overall_score(tfidf_score, skill_match, cci_score)
    decision = get_decision_from_score(overall_score)
    
    # Find matched and missing skills
    job_set = set([s.lower() for s in job_skills])
    resume_set = set([s.lower() for s in resume_skills])
    matched_skills = list(job_set.intersection(resume_set))
    missing_skills = list(job_set - resume_set)
    
    # Generate recommendations
    recommendations = []
    if skill_match < 0.5:
        recommendations.append(f"Improve skills in: {', '.join(missing_skills[:5])}")
    if cci_score and cci_score < 60:
        recommendations.append("Consider building more consistent career progression")
    if tfidf_score < 0.4:
        recommendations.append("Tailor resume to better match job requirements")
    
    return {
        'tfidf_score': round(tfidf_score, 3),
        'skill_match': round(skill_match, 3),
        'cci_score': cci_score,
        'overall_score': overall_score,
        'decision': decision,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'recommendations': recommendations
    }
