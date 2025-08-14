"""
Intent detection utilities for understanding user queries
"""

import streamlit as st
from transformers import pipeline

class IntentDetector:
    """Detects user intents and maps to appropriate content categories"""
    
    def __init__(self, config):
        self.config = config
        self.classifier = pipeline(
            "zero-shot-classification", 
            model=config['intent_model']
        )
        self.categories = config['categories']
        self.category_folders = config['category_folders']
        self.category_keywords = config['category_keywords']
        self.min_confidence = config['min_confidence']
    
    def detect_intents(self, user_prompt, min_confidence=None, score_margin=0.05):
        """
        Detect user intents using both keyword matching and ML classification
        
        Args:
            user_prompt: User's input text
            min_confidence: Minimum confidence threshold
            score_margin: Margin for including multiple intents
            
        Returns:
            Dictionary with detected intents and relevant folders
        """
        if min_confidence is None:
            min_confidence = self.min_confidence
        
        # First try keyword-based detection (faster and more reliable)
        keyword_matches = self._detect_by_keywords(user_prompt)
        
        if keyword_matches:
            st.write("✅ Intent detected using keyword matching:")
            for match in keyword_matches:
                st.write(f"  - {match['category']} (keyword: '{match['keyword']}')")
            
            return {
                'method': 'keyword',
                'categories': [match['category'] for match in keyword_matches],
                'folders': [self.category_folders[match['category']] for match in keyword_matches],
                'confidence': 1.0,
                'details': keyword_matches
            }
        
        # Fallback to ML-based classification
        return self._detect_by_ml(user_prompt, min_confidence, score_margin)
    
    def _detect_by_keywords(self, user_prompt):
        """Detect intents using keyword matching"""
        prompt_lower = user_prompt.lower()
        matches = []
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in prompt_lower:
                    matches.append({
                        'category': category,
                        'keyword': keyword,
                        'method': 'keyword'
                    })
                    break  # Only count each category once
        
        return matches
    
    def _detect_by_ml(self, user_prompt, min_confidence, score_margin):
        """Detect intents using machine learning classification"""
        try:
            result = self.classifier(user_prompt, self.categories)
            
            top_score = result['scores'][0]
            selected = []
            
            for label, score in zip(result['labels'], result['scores']):
                if score >= min_confidence and (top_score - score) <= score_margin:
                    selected.append({
                        'category': label,
                        'confidence': score,
                        'method': 'ml'
                    })
            
            # Fallback to general information if nothing detected
            if not selected:
                selected.append({
                    'category': "general information about the company",
                    'confidence': 1.0,
                    'method': 'fallback'
                })
            
            st.write("🤖 Intent detected using ML classification:")
            for item in selected:
                st.write(f"  - {item['category']} ({item['confidence']:.3f})")
            
            return {
                'method': 'ml',
                'categories': [item['category'] for item in selected],
                'folders': [self.category_folders[item['category']] for item in selected],
                'confidence': top_score,
                'details': selected
            }
            
        except Exception as e:
            st.warning(f"ML classification error: {str(e)}")
            return self._get_fallback_intent()
    
    def _get_fallback_intent(self):
        """Return fallback intent when detection fails"""
        return {
            'method': 'fallback',
            'categories': ["general information about the company"],
            'folders': [self.category_folders["general information about the company"]],
            'confidence': 1.0,
            'details': [{'category': "general information about the company", 'method': 'fallback'}]
        }
    
    def analyze_user_journey(self, conversation_history):
        """Analyze user's journey through the conversation"""
        if not conversation_history:
            return {}
        
        intents_over_time = []
        topics_discussed = set()
        
        for turn in conversation_history:
            user_message = turn.get('user', '')
            if user_message:
                intent_result = self.detect_intents(user_message)
                intents_over_time.append({
                    'turn': turn.get('turn', 0),
                    'intents': intent_result['categories'],
                    'confidence': intent_result['confidence']
                })
                
                # Track topics
                topics_discussed.update(intent_result['categories'])
        
        # Analyze patterns
        journey_analysis = {
            'total_intents': len(intents_over_time),
            'unique_topics': len(topics_discussed),
            'topics_discussed': list(topics_discussed),
            'intent_progression': intents_over_time,
            'primary_focus': self._get_primary_focus(intents_over_time),
            'user_engagement_level': self._calculate_engagement_level(intents_over_time)
        }
        
        return journey_analysis
    
    def _get_primary_focus(self, intents_over_time):
        """Determine the user's primary focus area"""
        if not intents_over_time:
            return None
        
        # Count intent occurrences
        intent_counts = {}
        for item in intents_over_time:
            for intent in item['intents']:
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        if not intent_counts:
            return None
        
        # Return most common intent
        return max(intent_counts.items(), key=lambda x: x[1])
    
    def _calculate_engagement_level(self, intents_over_time):
        """Calculate user engagement level based on intent patterns"""
        if not intents_over_time:
            return 'none'
        
        total_turns = len(intents_over_time)
        unique_intents = len(set(intent for item in intents_over_time for intent in item['intents']))
        avg_confidence = sum(item['confidence'] for item in intents_over_time) / total_turns
        
        # Simple engagement scoring
        engagement_score = (total_turns * 0.4) + (unique_intents * 0.3) + (avg_confidence * 0.3)
        
        if engagement_score > 3.0:
            return 'high'
        elif engagement_score > 1.5:
            return 'medium'
        else:
            return 'low'
    
    def get_suggested_followups(self, detected_intents, conversation_context=None):
        """Suggest follow-up questions based on detected intents"""
        suggestions = []
        
        for category in detected_intents.get('categories', []):
            if 'service' in category.lower():
                suggestions.extend([
                    "Would you like to see our case studies?",
                    "What's your timeline for implementation?",
                    "Can I connect you with our solutions expert?"
                ])
            elif 'career' in category.lower():
                suggestions.extend([
                    "What type of role are you interested in?",
                    "Would you like to know about our company culture?",
                    "Can I help you find current job openings?"
                ])
            elif 'company' in category.lower() or 'about' in category.lower():
                suggestions.extend([
                    "Would you like to know about our leadership team?",
                    "Are you interested in our company values?",
                    "Can I tell you about our recent achievements?"
                ])
        
        # Remove duplicates and limit suggestions
        unique_suggestions = list(dict.fromkeys(suggestions))[:3]
        return unique_suggestions
    
    def classify_user_type(self, user_data, conversation_history):
        """Classify user type based on available data"""
        email = user_data.get('email', '')
        explicit_type = user_data.get('user_type', '')
        
        if explicit_type:
            return explicit_type
        
        # Analyze conversation for clues
        service_mentions = 0
        career_mentions = 0
        info_mentions = 0
        
        for turn in conversation_history:
            user_msg = turn.get('user', '').lower()
            if any(word in user_msg for word in ['service', 'solution', 'help', 'business', 'project']):
                service_mentions += 1
            if any(word in user_msg for word in ['job', 'career', 'position', 'hiring', 'work']):
                career_mentions += 1
            if any(word in user_msg for word in ['about', 'company', 'information', 'know']):
                info_mentions += 1
        
        # Determine type based on patterns
        if service_mentions > career_mentions and service_mentions > info_mentions:
            return 'potential_client'
        elif career_mentions > service_mentions and career_mentions > info_mentions:
            return 'job_seeker'
        elif info_mentions > service_mentions and info_mentions > career_mentions:
            return 'information_seeker'
        else:
            return 'general'