"""
Enhanced UI for Sundew Solutions Chatbot
Implements guided flows, service promotion, and personalized experience
"""

import streamlit as st
import re
from datetime import datetime
from utils.validation import validate_email, is_business_email
from utils.guided_flows import GuidedFlows

def display_chat_ui(chat_engine, session_manager, config):
    """Main chat interface with enhanced features"""
    
    # Header with company branding
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #2E8B57; margin-bottom: 0.5rem;'>💬 Sundew Solutions</h1>
        <h3 style='color: #666; font-weight: 300;'>Digital First. Digital Fast.</h3>
        <p style='color: #888; font-size: 1.1rem;'>Have a requirement? Let's chat and find the best solutions for your business.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with company info and navigation
    display_sidebar(config)
    
    # Main chat interface
    if 'chat_stage' not in st.session_state:
        st.session_state.chat_stage = 'welcome'
    
    if st.session_state.chat_stage == 'welcome':
        display_welcome_stage(session_manager)
    elif st.session_state.chat_stage == 'email_collection':
        display_email_collection_stage(session_manager)
    elif st.session_state.chat_stage == 'service_selection':
        display_service_selection_stage(session_manager)
    elif st.session_state.chat_stage == 'chat_active':
        display_active_chat_stage(chat_engine, session_manager)

def display_sidebar(config):
    """Enhanced sidebar with company information"""
    with st.sidebar:
        st.markdown("### 🌟 Quick Links")
        
        # Service categories with direct links
        services = {
            "🤖 AI Chatbots": "Our intelligent automation solutions",
            "🌐 Web Development": "Custom web applications",
            "📱 Mobile Solutions": "iOS and Android development",
            "☁️ Cloud & DevOps": "Scalable infrastructure solutions",
            "🎨 UX/UI Design": "User-centered design services"
        }
        
        for service, description in services.items():
            if st.button(service):
                st.session_state.selected_service = service
                st.session_state.chat_stage = 'service_selection'
                st.rerun()
        
        st.markdown("---")
        
        # Contact information
        st.markdown("""
        ### 📞 Contact Us
        - **Sales:** sales@sundewsolutions.com
        - **Support:** support@sundewsolutions.com
        - **Website:** [sundewsolutions.com](https://sundewsolutions.com)
        """)
        
        st.markdown("---")
        
        # Session info
        if hasattr(st.session_state, 'session_manager'):
            st.markdown(f"**Session:** {st.session_state.session_manager.session_id[:12]}...")
            st.markdown(f"**Messages:** {len(st.session_state.session_manager.conversation)}")

def display_welcome_stage(session_manager):
    """Initial welcome stage with service promotion"""
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; color: white; text-align: center; margin: 2rem 0;'>
        <h2>🚀 Welcome to Sundew Solutions!</h2>
        <p style='font-size: 1.2rem; margin: 1rem 0;'>
            We transform businesses through cutting-edge digital solutions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Service showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; border: 2px solid #e0e0e0; border-radius: 10px;'>
            <h4>🤖 AI Automation</h4>
            <p>Intelligent chatbots and workflow automation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; border: 2px solid #e0e0e0; border-radius: 10px;'>
            <h4>🌐 Custom Development</h4>
            <p>Web and mobile applications tailored to you</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; border: 2px solid #e0e0e0; border-radius: 10px;'>
            <h4>☁️ Cloud Solutions</h4>
            <p>Scalable infrastructure and DevOps</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### How can we help you today?")
    
    # Quick action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💼 I'm interested in your services", key="services_btn"):
            st.session_state.user_type = "potential_client"
            st.session_state.chat_stage = "email_collection"
            st.rerun()
            
        if st.button("📚 I want to learn about your company", key="info_btn"):
            st.session_state.user_type = "information_seeker"
            st.session_state.chat_stage = "email_collection"
            st.rerun()
    
    with col2:
        if st.button("💼 I'm looking for job opportunities", key="career_btn"):
            st.session_state.user_type = "job_seeker"
            st.session_state.chat_stage = "email_collection"
            st.rerun()
            
        if st.button("💬 I just want to chat", key="chat_btn"):
            st.session_state.user_type = "general"
            st.session_state.chat_stage = "email_collection"
            st.rerun()

def display_email_collection_stage(session_manager):
    """Email collection with validation"""
    
    st.markdown("### 📧 Let's get started!")
    
    user_type = st.session_state.get('user_type', 'general')
    
    if user_type == "potential_client":
        st.info("Great! We'd love to discuss how we can help your business grow.")
    elif user_type == "job_seeker":
        st.info("Excellent! We're always looking for talented people to join our team.")
    elif user_type == "information_seeker":
        st.info("Perfect! We're happy to share more about what we do.")
    
    # Email input
    email = st.text_input(
        "Please provide your email address:",
        placeholder="your.email@company.com",
        help="We'll use this to personalize your experience and follow up if needed."
    )
    
    # Name input (optional)
    name = st.text_input(
        "Your name (optional):",
        placeholder="John Doe"
    )
    
    if st.button("Continue", type="primary"):
        if not validate_email(email):
            st.error("❗ Please enter a valid email address.")
            return
        
        # Store user data
        session_manager.set_user_data("email", email)
        session_manager.set_user_data("name", name)
        session_manager.set_user_data("user_type", user_type)
        session_manager.set_user_data("timestamp", datetime.now().isoformat())
        
        # Check if business email is required for certain flows
        business_required_types = ["potential_client"]
        
        if user_type in business_required_types and not is_business_email(email):
            st.warning("❗ A business email is preferred for service inquiries. You can continue, but we recommend using your company email for better assistance.")
        
        st.success("✅ Email verified! Let's continue.")
        st.session_state.chat_stage = "service_selection"
        st.rerun()

def display_service_selection_stage(session_manager):
    """Service selection and guided flow"""
    
    user_data = session_manager.user_data
    name = user_data.get("name", "")
    user_type = user_data.get("user_type", "general")
    
    # Personalized greeting
    greeting = f"Hi {name}! " if name else "Hello! "
    st.markdown(f"### {greeting}👋")
    
    # Initialize guided flows
    guided_flows = GuidedFlows()
    
    if user_type == "potential_client":
        guided_flows.display_client_flow(session_manager)
    elif user_type == "job_seeker":
        guided_flows.display_career_flow(session_manager)
    elif user_type == "information_seeker":
        guided_flows.display_info_flow(session_manager)
    else:
        # General flow
        st.markdown("What would you like to know about Sundew Solutions?")
        if st.button("Start Chatting", type="primary"):
            st.session_state.chat_stage = "chat_active"
            st.rerun()

def display_active_chat_stage(chat_engine, session_manager):
    """Main chat interface"""
    
    user_data = session_manager.user_data
    name = user_data.get("name", "")
    
    # Chat header
    if name:
        st.markdown(f"### 💬 Chat with Chetan - Hello {name}!")
    else:
        st.markdown("### 💬 Chat with Chetan")
    
    st.markdown("*I'm here to help you with any questions about Sundew Solutions!*")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hello{' ' + name if name else ''}! I'm Chetan, your virtual assistant at Sundew Solutions. How can I help you today?"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Sundew Solutions..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.process_user_input(prompt, user_data)
                st.markdown(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Log the conversation
        session_manager.add_turn(
            bot=response,
            user=prompt
        )
    
    # Quick action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 New Topic"):
            st.session_state.messages = [
                {"role": "assistant", "content": "What else would you like to know about Sundew Solutions?"}
            ]
            st.rerun()
    
    with col2:
        if st.button("📞 Contact Sales"):
            contact_msg = "I'd like to speak with your sales team about your services. Please provide me with contact details."
            st.session_state.messages.append({"role": "user", "content": contact_msg})
            response = "Great! You can reach our sales team at sales@sundewsolutions.com or call us at +91-XXXXXXXXXX. Someone will get back to you within 24 hours. What specific services are you interested in?"
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("💼 View Careers"):
            career_msg = "I'm interested in career opportunities at Sundew Solutions."
            st.session_state.messages.append({"role": "user", "content": career_msg})
            response = "Excellent! We're always looking for talented individuals. Check out our careers page at https://sundewsolutions.com/careers for current openings. You can also send your resume to hr@sundewsolutions.com. What type of role are you looking for?"
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        if st.button("💾 Save Chat"):
            session_manager.save_log()
            st.success("Chat history saved!")
    
    # Progress indicator
    message_count = len(st.session_state.messages)
    if message_count > 5:
        st.info(f"🎉 Great conversation! We've exchanged {message_count} messages. Is there anything else I can help you with?")
