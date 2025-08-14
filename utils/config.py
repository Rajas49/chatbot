"""
Configuration management for the chatbot
"""

import os
import json
from pathlib import Path

def load_config():
    """Load configuration from files and environment"""
    
    config = {
        # API Configuration
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-4'),
        'openai_temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.2')),
        
        # Document Processing
        'data_folder': os.getenv('DATA_FOLDER', 'data'),
        'min_similarity_threshold': float(os.getenv('MIN_SIMILARITY', '0.21')),
        'max_documents': int(os.getenv('MAX_DOCUMENTS', '3')),
        
        # Intent Detection
        'intent_model': 'valhalla/distilbart-mnli-12-1',
        'embedding_model': 'all-MiniLM-L6-v2',
        'min_confidence': float(os.getenv('MIN_CONFIDENCE', '0.5')),
        
        # Categories and mappings
        'categories': [
            "general information about the company",
            "company blog posts", 
            "career opportunities, vacancies, and recruitment",
            "case studies of past projects",
            "services offered by the company",
            "success stories and client achievements",
            "industry-specific expertise and domain knowledge",
            "company policy and disclaimers"
        ],
        
        'category_folders': {
            "general information about the company": "data/General/",
            "company blog posts": "data/Blog/",
            "career opportunities, vacancies, and recruitment": "data/Career and Vacancies/",
            "case studies of past projects": "data/Case Studies/",
            "services offered by the company": "data/Services/",
            "success stories and client achievements": "data/Success Stories/",
            "industry-specific expertise and domain knowledge": "data/Industry Expertise/",
            "company policy and disclaimers": "data/Policy and Disclaimer/",
        },
        
        'category_keywords': {
            "general information about the company": [
                "about the company", "overview", "mission", "vision", "culture", 
                "contact", "email", "leadership", "ceo", "who we are", "company background"
            ],
            "company blog posts": [
                "blog", "insights", "articles", "write-up"
            ],
            "career opportunities, vacancies, and recruitment": [
                "vacancy", "vacancies", "openings", "job position", "job opening", 
                "hiring", "hire", "job post", "recruitment", "career", "career path", 
                "opportunities", "job opportunities", "career growth", "roles available", 
                "employment", "work at"
            ],
            "case studies of past projects": [
                "case study", "case studies", "project example", "project case", 
                "real-world project"
            ],
            "services offered by the company": [
                "services", "solutions", "offerings", "what you provide", 
                "automation service", "AI services", "document processing", 
                "consulting services", "rpa services", "domain knowledge"
            ],
            "success stories and client achievements": [
                "success story", "client success", "testimonial", "achievement", 
                "result", "outcome", "benefits for client", "transformation"
            ],
            "industry-specific expertise and domain knowledge": [
                "industry expertise", "domain knowledge", "healthcare expertise", 
                "insurance knowledge", "finance domain", "logistics industry", 
                "bank", "health", "media", "Food", "beverage", "travel", 
                "hospitality", "sector-specific knowledge"
            ],
            "company policy and disclaimers": [
                "privacy policy", "disclaimer", "terms", "conditions", "legal", 
                "cookie policy"
            ]
        },
        
        # Logging
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'log_file': os.getenv('LOG_FILE', 'logs/chatbot.log'),
        'chat_logs_folder': os.getenv('CHAT_LOGS_FOLDER', 'chat_logs'),
        
        # UI Configuration  
        'company_name': 'Sundew Solutions',
        'company_tagline': 'Digital First. Digital Fast.',
        'bot_name': 'Chetan',
        'primary_color': '#2E8B57',
        'secondary_color': '#667eea',
        
        # Contact Information
        'contact': {
            'sales_email': 'sales@sundewsolutions.com',
            'support_email': 'support@sundewsolutions.com',
            'careers_email': 'careers@sundewsolutions.com',
            'website': 'https://sundewsolutions.com',
            'phone': '+91-XXXXXXXXXX'
        },
        
        # Business Rules
        'require_business_email_for_services': True,
        'max_conversation_length': 50,
        'session_timeout_minutes': 30,
        
        # Feature Flags
        'features': {
            'guided_flows': True,
            'service_promotion': True,
            'chat_logging': True,
            'email_validation': True,
            'analytics': True,
            'export_conversations': True
        }
    }
    
    # Load questions.json if exists
    questions_file = Path('questions.json')
    if questions_file.exists():
        with open(questions_file, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
            config['questions'] = questions_data
    
    return config

def get_company_services():
    """Get list of company services for display"""
    return {
        "🤖 AI & Automation": {
            "description": "Intelligent chatbots, workflow automation, document processing",
            "keywords": ["ai", "automation", "chatbot", "workflow", "intelligent"],
            "benefits": ["24/7 availability", "70% cost reduction", "Improved accuracy"]
        },
        "🌐 Custom Development": {
            "description": "Web applications, mobile apps, custom software solutions",
            "keywords": ["web", "mobile", "app", "development", "custom"],
            "benefits": ["Tailored solutions", "Scalable architecture", "Modern technology"]
        },
        "☁️ Cloud & DevOps": {
            "description": "Cloud migration, infrastructure, CI/CD, system integration",
            "keywords": ["cloud", "devops", "aws", "azure", "infrastructure"],
            "benefits": ["99.9% uptime", "Cost optimization", "Enhanced security"]
        },
        "🎨 Digital Experience": {
            "description": "UX/UI design, digital transformation, user experience",
            "keywords": ["design", "ux", "ui", "experience", "digital"],
            "benefits": ["Better engagement", "Modern design", "User-friendly"]
        },
        "🔧 Integration Services": {
            "description": "API integration, system connectivity, data migration",
            "keywords": ["integration", "api", "connect", "migrate", "sync"],
            "benefits": ["Seamless connectivity", "Data consistency", "Process automation"]
        }
    }

def get_industry_expertise():
    """Get list of industries we serve"""
    return [
        "Healthcare & Life Sciences",
        "Financial Services & Insurance", 
        "Retail & E-commerce",
        "Manufacturing & Logistics",
        "Media & Entertainment",
        "Education & Training",
        "Government & Public Sector",
        "Real Estate & Construction"
    ]