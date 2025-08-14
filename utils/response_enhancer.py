"""
Response enhancement utilities for personalizing and improving bot responses
"""

import re
import random
from datetime import datetime

class ResponseEnhancer:
    """Enhances bot responses with personalization and company-specific elements"""
    
    def __init__(self, config):
        self.config = config
        self.company_name = config['company_name']
        self.bot_name = config['bot_name']
        self.contact_info = config['contact']
        
    def build_professional_prompt(self, user_question, user_data=None, intents=None):
        """Build enhanced prompt for better AI responses"""
        
        # Base professional prompt
        base_prompt = f"""
        You are {self.bot_name}, a professional business assistant at {self.company_name}.
        
        Your role:
        - Answer user questions clearly, concisely, and accurately using company-provided data
        - Maintain a helpful, professional, and business-appropriate tone
        - If unsure about specific details, acknowledge limitations and offer to connect with human experts
        - Always include relevant resource links when available
        - Focus on providing value to the user
        
        Company Context:
        - {self.company_name}: Digital transformation company
        - Tagline: {self.config['company_tagline']}
        - Services: AI/Automation, Custom Development, Cloud Solutions, Digital Experience
        - Contact: {self.contact_info['sales_email']} for sales, {self.contact_info['support_email']} for support
        """
        
        # Add user context if available
        if user_data:
            user_context = self._build_user_context(user_data)
            base_prompt += f"\n\nUser Context:\n{user_context}"
        
        # Add intent context
        if intents:
            intent_context = self._build_intent_context(intents)
            base_prompt += f"\n\nDetected Intent:\n{intent_context}"
        
        # Add the actual question
        base_prompt += f"\n\nUser Question: {user_question}\n\nProvide a helpful, accurate response:"
        
        return base_prompt
    
    def _build_user_context(self, user_data):
        """Build user context for personalization"""
        context_parts = []
        
        if user_data.get('name'):
            context_parts.append(f"- User name: {user_data['name']}")
        
        if user_data.get('email'):
            email = user_data['email']
            domain = email.split('@')[1] if '@' in email else ''
            context_parts.append(f"- Email domain: {domain}")
        
        if user_data.get('user_type'):
            context_parts.append(f"- User type: {user_data['user_type']}")
        
        if user_data.get('company_size'):
            context_parts.append(f"- Company size: {user_data['company_size']}")
        
        if user_data.get('selected_service'):
            context_parts.append(f"- Interested in: {user_data['selected_service']}")
        
        return '\n'.join(context_parts) if context_parts else "- New user interaction"
    
    def _build_intent_context(self, intents):
        """Build intent context for better responses"""
        context_parts = []
        
        if intents.get('categories'):
            context_parts.append(f"- Primary topics: {', '.join(intents['categories'][:2])}")
        
        if intents.get('method'):
            context_parts.append(f"- Detection method: {intents['method']}")
        
        if intents.get('confidence'):
            context_parts.append(f"- Confidence: {intents['confidence']:.2f}")
        
        return '\n'.join(context_parts) if context_parts else "- General inquiry"
    
    def enhance_response(self, base_response, intents=None, user_data=None):
        """Enhance the base AI response with personalization and CTAs"""
        
        enhanced_response = base_response
        
        # Add personalization
        enhanced_response = self._add_personalization(enhanced_response, user_data)
        
        # Add relevant CTAs based on intent
        enhanced_response = self._add_contextual_ctas(enhanced_response, intents, user_data)
        
        # Add company branding elements
        enhanced_response = self._add_branding_elements(enhanced_response, intents)
        
        # Format for better readability
        enhanced_response = self._format_response(enhanced_response)
        
        return enhanced_response
    
    def _add_personalization(self, response, user_data):
        """Add personal touches to the response"""
        if not user_data:
            return response
        
        name = user_data.get('name', '')
        user_type = user_data.get('user_type', '')
        
        # Add name if available
        if name and not name.lower() in response.lower():
            # Try to naturally incorporate the name
            if response.startswith("Hi") or response.startswith("Hello"):
                response = response.replace("Hi", f"Hi {name}", 1).replace("Hello", f"Hello {name}", 1)
            else:
                response = f"Hi {name}! " + response
        
        # Add user-type specific language
        if user_type == 'potential_client' and 'business' not in response.lower():
            response += "\n\nAs a business looking for solutions, I'd be happy to discuss how we can specifically help your company grow."
        elif user_type == 'job_seeker' and 'career' not in response.lower():
            response += "\n\nSince you're interested in career opportunities, I can also share information about our company culture and current openings."
        
        return response
    
    def _add_contextual_ctas(self, response, intents, user_data):
        """Add relevant call-to-action elements"""
        if not intents:
            return response
        
        ctas = []
        categories = intents.get('categories', [])
        
        for category in categories:
            if 'service' in category.lower():
                ctas.extend([
                    f"📞 **Ready to discuss your project?** Contact our sales team at {self.contact_info['sales_email']}",
                    f"📋 **Want to see similar projects?** Check out our case studies",
                    f"💬 **Need a custom solution?** Let's schedule a consultation"
                ])
                break
            elif 'career' in category.lower():
                ctas.extend([
                    f"💼 **Ready to apply?** Send your resume to {self.contact_info.get('careers_email', 'careers@sundewsolutions.com')}",
                    f"🌟 **Learn about our culture:** Visit our careers page",
                    f"📝 **Current openings:** Check our latest job postings"
                ])
                break
            elif 'case' in category.lower() or 'success' in category.lower():
                ctas.extend([
                    f"🎯 **Interested in similar results?** Let's discuss your requirements",
                    f"📈 **Want to see more examples?** Browse our complete case studies",
                    f"💡 **Have a similar challenge?** Get a free consultation"
                ])
                break
        
        # Add one relevant CTA
        if ctas:
            selected_cta = random.choice(ctas[:2])  # Choose from top 2 most relevant
            response += f"\n\n---\n\n{selected_cta}"
        
        return response
    
    def _add_branding_elements(self, response, intents):
        """Add subtle branding elements"""
        
        # Add tagline occasionally for brand reinforcement
        if random.random() < 0.3:  # 30% chance
            response += f"\n\n*{self.company_name}: {self.config['company_tagline']}*"
        
        # Add expertise highlight for service inquiries
        categories = intents.get('categories', []) if intents else []
        if any('service' in cat.lower() for cat in categories):
            response += f"\n\n💡 *With 8+ years of digital transformation expertise, {self.company_name} has helped 100+ businesses achieve their goals.*"
        
        return response
    
    def _format_response(self, response):
        """Format response for better readability"""
        
        # Ensure proper spacing around headers
        response = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', response)
        
        # Ensure proper spacing around bullet points
        response = re.sub(r'\n-\s', r'\n\n- ', response)
        response = re.sub(r'\n\*\s', r'\n\n* ', response)
        
        # Clean up multiple newlines
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        # Ensure final response ends cleanly
        response = response.strip()
        
        return response
    
    def generate_conversation_starter(self, user_data):
        """Generate personalized conversation starters"""
        
        user_type = user_data.get('user_type', 'general')
        name = user_data.get('name', '')
        
        greeting = f"Hello {name}! " if name else "Hello! "
        
        starters = {
            'potential_client': [
                f"{greeting}I'm excited to help you find the perfect digital solution for your business. What challenges are you looking to solve?",
                f"{greeting}Welcome to {self.company_name}! I'd love to learn about your business needs and how we can help you grow.",
                f"{greeting}Great to meet you! What type of digital transformation are you considering for your company?"
            ],
            'job_seeker': [
                f"{greeting}Welcome to {self.company_name}! I'm thrilled you're interested in joining our team. What type of role are you looking for?",
                f"{greeting}Thanks for your interest in careers at {self.company_name}! Tell me about your background and what excites you about working with us.",
                f"{greeting}I'd love to help you explore opportunities at {self.company_name}. What skills and experience do you bring?"
            ],
            'information_seeker': [
                f"{greeting}I'm here to share information about {self.company_name} and our digital solutions. What would you like to know?",
                f"{greeting}Welcome! I'm happy to tell you about {self.company_name}, our services, and our approach to digital transformation.",
                f"{greeting}Great to meet you! What aspects of {self.company_name} are you most curious about?"
            ],
            'general': [
                f"{greeting}I'm {self.bot_name}, your virtual assistant at {self.company_name}. How can I help you today?",
                f"{greeting}Welcome to {self.company_name}! I'm here to answer any questions about our services, company, or opportunities.",
                f"{greeting}Hi there! I'm ready to help with any questions about {self.company_name}. What can I assist you with?"
            ]
        }
        
        return random.choice(starters.get(user_type, starters['general']))
    
    def suggest_next_questions(self, current_topic, conversation_history):
        """Suggest relevant follow-up questions"""
        
        suggestions = {
            'services': [
                "What's your timeline for implementation?",
                "What's your approximate budget range?",
                "Would you like to see some case studies?",
                "Can I connect you with our solutions architect?"
            ],
            'careers': [
                "What type of role interests you most?",
                "Are you looking for remote or on-site positions?",
                "Would you like to know about our company culture?",
                "Can I help you find current job openings?"
            ],
            'company': [
                "Would you like to know about our leadership team?",
                "Are you interested in our recent projects?",
                "Would you like to hear about our company values?",
                "Can I tell you about our industry expertise?"
            ],
            'technical': [
                "Would you like a technical deep-dive?",
                "Are you interested in implementation details?",
                "Would you like to speak with our technical team?",
                "Can I share relevant case studies?"
            ]
        }
        
        # Determine current topic from conversation
        topic_key = 'services'  # default
        if any('career' in turn.get('user', '').lower() for turn in conversation_history[-3:]):
            topic_key = 'careers'
        elif any('about' in turn.get('user', '').lower() for turn in conversation_history[-3:]):
            topic_key = 'company'
        elif any(tech in turn.get('user', '').lower() for turn in conversation_history[-3:] 
                for tech in ['technical', 'api', 'integration', 'architecture']):
            topic_key = 'technical'
        
        return suggestions.get(topic_key, suggestions['services'])[:3]
    
    def add_urgency_elements(self, response, user_data):
        """Add appropriate urgency elements for business leads"""
        
        user_type = user_data.get('user_type', '')
        timeline = user_data.get('timeline', '')
        
        if user_type == 'potential_client':
            if 'asap' in timeline.lower() or 'urgent' in timeline.lower():
                response += "\n\n⚡ **Fast-track available:** We can prioritize your project for immediate start."
            elif any(phrase in response.lower() for phrase in ['limited time', 'offer', 'discount']):
                response += "\n\n🎯 **Act now:** This consultation offer is available for a limited time."
        
        return response
    
    def add_social_proof(self, response, intent_categories):
        """Add relevant social proof elements"""
        
        social_proof_elements = {
            'services': [
                "✨ *Trusted by 100+ businesses across various industries*",
                "🏆 *Award-winning digital transformation partner*", 
                "📈 *Average 40% efficiency improvement for our clients*"
            ],
            'careers': [
                "🌟 *Rated as 'Great Place to Work' by our employees*",
                "📚 *Comprehensive training and career development programs*",
                "🤝 *Collaborative and inclusive work environment*"
            ],
            'company': [
                "🚀 *8+ years of digital innovation excellence*",
                "🌍 *Serving clients globally with local expertise*",
                "💡 *Leading digital transformation thought leadership*"
            ]
        }
        
        # Add relevant social proof
        for category in intent_categories:
            if 'service' in category.lower():
                proof = random.choice(social_proof_elements['services'])
                response += f"\n\n{proof}"
                break
            elif 'career' in category.lower():
                proof = random.choice(social_proof_elements['careers'])  
                response += f"\n\n{proof}"
                break
            elif 'company' in category.lower() or 'about' in category.lower():
                proof = random.choice(social_proof_elements['company'])
                response += f"\n\n{proof}"
                break
        
        return response