"""
Main entry point for Sundew Solutions Chatbot
Enhanced version with better organization and features
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Add the project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ui import display_chat_ui
from app.chat_engine import ChatEngine
from app.session_manager import SessionManager
from utils.config import load_config
from utils.logging_utils import setup_logging

# Page configuration
st.set_page_config(
    page_title="Sundew Solutions - Digital First. Digital Fast",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Sundew Solutions Chatbot")
    
    # Load configuration
    config = load_config()
    
    # Initialize session manager
    if 'session_manager' not in st.session_state:
        st.session_state.session_manager = SessionManager()
        logger.info(f"New session started: {st.session_state.session_manager.session_id}")
    
    # Initialize chat engine
    if 'chat_engine' not in st.session_state:
        st.session_state.chat_engine = ChatEngine(config)
    
    # Main UI
    display_chat_ui(
        st.session_state.chat_engine, 
        st.session_state.session_manager,
        config
    )

if __name__ == "__main__":
    main()