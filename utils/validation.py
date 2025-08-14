"""
Validation utilities for email, phone, and other user inputs
"""

import re
import streamlit as st

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_business_email(email):
    """Check if email is from a business domain (not personal)"""
    if not email:
        return False
    
    personal_domains = [
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
        "icloud.com", "aol.com", "protonmail.com", "live.com",
        "msn.com", "ymail.com", "rediffmail.com", "mail.com"
    ]
    
    try:
        domain = email.split("@")[1].lower()
        return domain not in personal_domains
    except:
        return False

def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return True  # Phone is optional
    
    # Remove spaces, dashes, and brackets
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check for valid phone patterns
    patterns = [
        r'^\+?91[6789]\d{9}$',  # Indian mobile
        r'^\+?1[2-9]\d{9}$',    # US phone
        r'^\+?[1-9]\d{10,14}$', # International
        r'^[6789]\d{9}$'        # Indian mobile without country code
    ]
    
    return any(re.match(pattern, clean_phone) for pattern in patterns)

def sanitize_input(text):
    """Sanitize user input to prevent basic security issues"""
    if not text:
        return ""
    
    # Remove potential HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Limit length
    if len(text) > 1000:
        text = text[:1000]
        st.warning("Input was truncated to 1000 characters.")
    
    return text

def validate_company_name(name):
    """Validate company name"""
    if not name:
        return False
    
    # Basic validation
    if len(name.strip()) < 2:
        return False
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r'^test\d*$',
        r'^temp\d*$',
        r'^fake\d*$',
        r'^demo\d*$'
    ]
    
    name_lower = name.lower().strip()
    return not any(re.match(pattern, name_lower) for pattern in suspicious_patterns)

def extract_domain_info(email):
    """Extract information about the email domain"""
    if not validate_email(email):
        return None
    
    try:
        domain = email.split("@")[1].lower()
        
        # Common business domains
        business_indicators = {
            '.com': 'Commercial',
            '.org': 'Organization', 
            '.edu': 'Educational',
            '.gov': 'Government',
            '.co.': 'Company',
            '.inc': 'Incorporated',
            '.ltd': 'Limited',
            '.corp': 'Corporation'
        }
        
        domain_type = 'Personal'
        for indicator, type_name in business_indicators.items():
            if indicator in domain:
                domain_type = type_name
                break
        
        return {
            'domain': domain,
            'type': domain_type,
            'is_business': is_business_email(email)
        }
    except:
        return None