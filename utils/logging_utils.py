"""
Logging utilities for the chatbot application
"""

import logging
import os
from pathlib import Path
from datetime import datetime

def setup_logging(log_level='INFO', log_file=None):
    """Setup logging configuration"""
    
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    if not log_file:
        log_file = f"logs/chatbot_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Create logger
    logger = logging.getLogger('sundew_chatbot')
    
    # Log startup
    logger.info("Logging system initialized")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Log level: {log_level}")
    
    return logger

def log_user_interaction(logger, session_id, event, data=None):
    """Log user interaction events"""
    log_data = {
        'session_id': session_id,
        'event': event,
        'timestamp': datetime.now().isoformat()
    }
    
    if data:
        log_data.update(data)
    
    logger.info(f"User Interaction: {log_data}")

def log_error(logger, error, context=None):
    """Log errors with context"""
    error_data = {
        'error': str(error),
        'type': type(error).__name__,
        'timestamp': datetime.now().isoformat()
    }
    
    if context:
        error_data['context'] = context
    
    logger.error(f"Error occurred: {error_data}")

def log_performance(logger, operation, duration, success=True):
    """Log performance metrics"""
    performance_data = {
        'operation': operation,
        'duration_seconds': duration,
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    logger.info(f"Performance: {performance_data}")

class ChatLogger:
    """Specialized logger for chat operations"""
    
    def __init__(self, logger_name='chat_operations'):
        self.logger = logging.getLogger(logger_name)
    
    def log_message_processed(self, session_id, user_message, bot_response, processing_time):
        """Log message processing"""
        self.logger.info(f"Message processed - Session: {session_id}, "
                        f"User msg length: {len(user_message)}, "
                        f"Bot response length: {len(bot_response)}, "
                        f"Processing time: {processing_time:.2f}s")
    
    def log_intent_detection(self, session_id, user_message, detected_intents, confidence):
        """Log intent detection results"""
        self.logger.info(f"Intent detection - Session: {session_id}, "
                        f"Intents: {detected_intents}, "
                        f"Confidence: {confidence}")
    
    def log_document_retrieval(self, session_id, query, documents_found, top_similarity):
        """Log document retrieval results"""
        self.logger.info(f"Document retrieval - Session: {session_id}, "
                        f"Query: '{query[:50]}...', "
                        f"Documents found: {documents_found}, "
                        f"Top similarity: {top_similarity:.3f}")
    
    def log_user_data_collection(self, session_id, data_type, value):
        """Log user data collection (privacy-safe)"""
        # Don't log actual values for privacy
        self.logger.info(f"User data collected - Session: {session_id}, "
                        f"Type: {data_type}, "
                        f"Length: {len(str(value)) if value else 0}")
    
    def log_session_end(self, session_id, duration, message_count, final_status):
        """Log session completion"""
        self.logger.info(f"Session ended - Session: {session_id}, "
                        f"Duration: {duration:.1f}min, "
                        f"Messages: {message_count}, "
                        f"Status: {final_status}")