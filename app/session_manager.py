"""
Enhanced Session Manager with analytics and logging
"""

import json
import uuid
import csv
import os
from datetime import datetime
from pathlib import Path

class SessionManager:
    """Enhanced session manager with analytics and logging capabilities"""
    
    def __init__(self):
        self.session_id = f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        self.conversation = []
        self.counter = 0
        self.user_data = {}
        self.session_start = datetime.now()
        self.last_activity = datetime.now()
        
        # Create necessary directories
        self._create_directories()
        
        # Initialize session
        self._log_session_start()
    
    def _create_directories(self):
        """Create necessary directories for logging"""
        directories = ['chat_logs', 'logs', 'analytics']
        for dir_name in directories:
            Path(dir_name).mkdir(exist_ok=True)
    
    def _log_session_start(self):
        """Log session initialization"""
        log_entry = {
            'session_id': self.session_id,
            'timestamp': self.session_start.isoformat(),
            'event': 'session_start'
        }
        self._append_to_analytics(log_entry)
    
    def add_turn(self, bot, user):
        """Add a conversation turn with enhanced tracking"""
        turn_data = {
            "turn": len(self.conversation) + 1,
            "timestamp": datetime.now().isoformat(),
            "bot": bot,
            "user": user,
            "user_message_length": len(user) if user else 0,
            "bot_message_length": len(bot) if bot else 0
        }
        
        self.conversation.append(turn_data)
        self.counter += 1
        self.last_activity = datetime.now()
        
        # Log turn for analytics
        self._log_turn_analytics(turn_data)
    
    def set_user_data(self, key, value):
        """Set user data with logging"""
        old_value = self.user_data.get(key)
        self.user_data[key] = value
        
        # Log data change
        if old_value != value:
            log_entry = {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'event': 'user_data_update',
                'key': key,
                'old_value': old_value,
                'new_value': value
            }
            self._append_to_analytics(log_entry)
    
    def get_session_duration(self):
        """Get session duration in minutes"""
        return (datetime.now() - self.session_start).total_seconds() / 60
    
    def get_conversation_stats(self):
        """Get conversation statistics"""
        if not self.conversation:
            return {}
        
        user_messages = [turn for turn in self.conversation if turn.get('user')]
        bot_messages = [turn for turn in self.conversation if turn.get('bot')]
        
        stats = {
            'total_turns': len(self.conversation),
            'user_messages': len(user_messages),
            'bot_messages': len(bot_messages),
            'avg_user_message_length': sum(len(turn.get('user', '')) for turn in user_messages) / len(user_messages) if user_messages else 0,
            'avg_bot_message_length': sum(len(turn.get('bot', '')) for turn in bot_messages) / len(bot_messages) if bot_messages else 0,
            'session_duration_minutes': self.get_session_duration(),
            'messages_per_minute': len(self.conversation) / max(self.get_session_duration(), 1)
        }
        
        return stats
    
    def save_log(self):
        """Save detailed conversation log"""
        log_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "session_start": self.session_start.isoformat(),
            "session_duration_minutes": self.get_session_duration(),
            "user": self.user_data,
            "conversation": self.conversation,
            "stats": self.get_conversation_stats(),
            "summary": self._generate_conversation_summary()
        }
        
        # Save JSON log
        log_file = f"chat_logs/{self.session_id}.json"
        with open(log_file, "w", encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        # Append to CSV for easy analysis
        self._append_to_csv_log(log_data)
        
        return log_file
    
    def _generate_conversation_summary(self):
        """Generate a summary of the conversation"""
        if not self.conversation:
            return "No conversation"
        
        user_intents = []
        topics_mentioned = []
        
        for turn in self.conversation:
            user_msg = turn.get('user', '').lower()
            if 'service' in user_msg or 'solution' in user_msg:
                user_intents.append('service_inquiry')
            if 'career' in user_msg or 'job' in user_msg:
                user_intents.append('career_inquiry')
            if 'about' in user_msg or 'company' in user_msg:
                user_intents.append('company_info')
            
            # Extract topics
            topics = ['ai', 'automation', 'web', 'mobile', 'cloud', 'design']
            for topic in topics:
                if topic in user_msg and topic not in topics_mentioned:
                    topics_mentioned.append(topic)
        
        summary = {
            'primary_intent': max(set(user_intents), key=user_intents.count) if user_intents else 'general',
            'topics_discussed': topics_mentioned,
            'conversation_type': self.user_data.get('user_type', 'unknown'),
            'engaged': len(self.conversation) > 5,
            'business_email_provided': self.user_data.get('email') and '@' in str(self.user_data.get('email', '')),
            'contact_info_shared': bool(self.user_data.get('email') or self.user_data.get('phone')),
            'final_status': self._determine_final_status()
        }
        
        return summary
    
    def _determine_final_status(self):
        """Determine the final status of the conversation"""
        if not self.conversation:
            return 'no_interaction'
        
        if len(self.conversation) < 3:
            return 'early_exit'
        
        user_type = self.user_data.get('user_type', '')
        if user_type == 'potential_client':
            return 'sales_lead'
        elif user_type == 'job_seeker':
            return 'hr_lead'
        elif len(self.conversation) > 10:
            return 'highly_engaged'
        else:
            return 'completed_interaction'
    
    def _append_to_csv_log(self, log_data):
        """Append session data to CSV for analytics"""
        csv_file = "chat_history.csv"
        file_exists = os.path.exists(csv_file)
        
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header if file doesn't exist
            if not file_exists:
                writer.writerow([
                    'timestamp', 'session_id', 'email', 'user_type', 'user_intent', 
                    'conversation_turns', 'session_duration', 'final_status',
                    'topics_discussed', 'business_email', 'engaged'
                ])
            
            summary = log_data['summary']
            writer.writerow([
                log_data['timestamp'],
                log_data['session_id'],
                self.user_data.get('email', ''),
                self.user_data.get('user_type', ''),
                summary['primary_intent'],
                len(self.conversation),
                round(log_data['session_duration_minutes'], 2),
                summary['final_status'],
                ','.join(summary['topics_discussed']),
                summary['business_email_provided'],
                summary['engaged']
            ])
    
    def _log_turn_analytics(self, turn_data):
        """Log individual turn for real-time analytics"""
        analytics_entry = {
            'session_id': self.session_id,
            'timestamp': turn_data['timestamp'],
            'event': 'conversation_turn',
            'turn_number': turn_data['turn'],
            'user_message_length': turn_data['user_message_length'],
            'bot_message_length': turn_data['bot_message_length'],
            'session_duration': self.get_session_duration()
        }
        self._append_to_analytics(analytics_entry)
    
    def _append_to_analytics(self, entry):
        """Append entry to analytics log"""
        analytics_file = f"analytics/daily_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(analytics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    
    def export_conversation_text(self):
        """Export conversation as readable text"""
        if not self.conversation:
            return "No conversation to export."
        
        text_lines = []
        text_lines.append(f"Sundew Solutions Chat Log")
        text_lines.append(f"Session: {self.session_id}")
        text_lines.append(f"Date: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        text_lines.append(f"Duration: {self.get_session_duration():.1f} minutes")
        
        if self.user_data.get('email'):
            text_lines.append(f"Email: {self.user_data['email']}")
        if self.user_data.get('name'):
            text_lines.append(f"Name: {self.user_data['name']}")
        
        text_lines.append("\n" + "="*50 + "\n")
        
        for turn in self.conversation:
            if turn.get('user'):
                text_lines.append(f"User: {turn['user']}")
            if turn.get('bot'):
                text_lines.append(f"Chetan: {turn['bot']}")
            text_lines.append("")
        
        return '\n'.join(text_lines)