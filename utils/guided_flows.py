"""
Guided conversation flows for different user types
"""

import streamlit as st

class GuidedFlows:
    """Handles guided conversation flows based on user intent"""
    
    def display_client_flow(self, session_manager):
        """Flow for potential clients interested in services"""
        
        st.markdown("#### 🎯 Let's find the perfect solution for your business!")
        
        # Service categories
        st.markdown("**What type of solution are you looking for?**")
        
        services = {
            "🤖 AI & Automation": {
                "description": "Chatbots, workflow automation, intelligent document processing",
                "benefits": "Reduce manual work by 70%, improve customer service 24/7"
            },
            "🌐 Custom Development": {
                "description": "Web applications, mobile apps, custom software solutions",
                "benefits": "Tailored to your exact needs, scalable and secure"
            },
            "☁️ Cloud & Infrastructure": {
                "description": "Cloud migration, DevOps, system integration",
                "benefits": "99.9% uptime, reduced costs, enhanced security"
            },
            "🎨 Digital Experience": {
                "description": "UX/UI design, digital transformation consulting",
                "benefits": "Increase user engagement by 50%, modern user experience"
            }
        }
        
        selected_service = st.selectbox(
            "Choose a service category:",
            list(services.keys())
        )
        
        if selected_service:
            service_info = services[selected_service]
            
            st.markdown(f"""
            <div style='background: #f0f8ff; padding: 1rem; border-radius: 8px; margin: 1rem 0;'>
                <h4>{selected_service}</h4>
                <p><strong>What we offer:</strong> {service_info['description']}</p>
                <p><strong>Key benefits:</strong> {service_info['benefits']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Company size for better recommendations
            company_size = st.selectbox(
                "What's your company size?",
                ["Startup (1-10 employees)", "Small Business (11-50 employees)", 
                 "Medium Business (51-200 employees)", "Enterprise (200+ employees)"]
            )
            
            # Budget range
            budget = st.selectbox(
                "What's your approximate budget range?",
                ["Under $10K", "$10K - $50K", "$50K - $100K", "Above $100K", "Let's discuss"]
            )
            
            # Timeline
            timeline = st.selectbox(
                "When would you like to start?",
                ["ASAP", "Within 1 month", "Within 3 months", "Within 6 months", "Just exploring"]
            )
            
            if st.button("Get Personalized Recommendation", type="primary"):
                # Store selections
                session_manager.set_user_data("selected_service", selected_service)
                session_manager.set_user_data("company_size", company_size)
                session_manager.set_user_data("budget", budget)
                session_manager.set_user_data("timeline", timeline)
                
                # Generate personalized message
                self._show_client_recommendation(selected_service, company_size, budget, timeline)
                
                st.session_state.chat_stage = "chat_active"
                st.experimental_rerun()
    
    def display_career_flow(self, session_manager):
        """Flow for job seekers"""
        
        st.markdown("#### 🚀 Join the Sundew Solutions Team!")
        
        st.markdown("""
        We're building the future of digital transformation and we want you to be part of it!
        
        **Current openings include:**
        - Software Developers (Python, JavaScript, React)
        - AI/ML Engineers
        - DevOps Engineers
        - UX/UI Designers
        - Business Analysts
        - Project Managers
        """)
        
        # Experience level
        experience = st.selectbox(
            "What's your experience level?",
            ["Fresh Graduate", "1-3 years", "3-5 years", "5-10 years", "10+ years"]
        )
        
        # Skills
        skills = st.multiselect(
            "What are your key skills?",
            ["Python", "JavaScript", "React", "Node.js", "AI/ML", "Cloud (AWS/Azure)", 
             "DevOps", "UI/UX Design", "Project Management", "Business Analysis", "Other"]
        )
        
        # Role type
        role_type = st.selectbox(
            "What type of role interests you?",
            ["Full-time", "Part-time", "Contract", "Internship"]
        )
        
        if st.button("Explore Opportunities", type="primary"):
            session_manager.set_user_data("experience", experience)
            session_manager.set_user_data("skills", skills)
            session_manager.set_user_data("role_type", role_type)
            
            self._show_career_recommendation(experience, skills, role_type)
            
            st.session_state.chat_stage = "chat_active"
            st.experimental_rerun()
    
    def display_info_flow(self, session_manager):
        """Flow for information seekers"""
        
        st.markdown("#### 📚 Learn More About Sundew Solutions")
        
        info_topics = [
            "🏢 About the Company",
            "💼 Our Services & Solutions", 
            "🎯 Industry Expertise",
            "📈 Success Stories & Case Studies",
            "🌟 Company Culture & Values",
            "📰 Latest News & Insights"
        ]
        
        selected_topic = st.selectbox("What would you like to know about?", info_topics)
        
        if st.button("Learn More", type="primary"):
            session_manager.set_user_data("info_topic", selected_topic)
            
            self._show_info_response(selected_topic)
            
            st.session_state.chat_stage = "chat_active"
            st.experimental_rerun()
    
    def _show_client_recommendation(self, service, company_size, budget, timeline):
        """Show personalized recommendation for clients"""
        
        st.success("🎉 Perfect! Based on your requirements, here's what we recommend:")
        
        recommendations = {
            "🤖 AI & Automation": "Our AI chatbot solutions can automate 70% of your customer interactions and streamline internal processes.",
            "🌐 Custom Development": "A custom web/mobile solution tailored to your business processes will give you a competitive edge.",
            "☁️ Cloud & Infrastructure": "Cloud migration will reduce your IT costs by 30-40% while improving scalability and security.",
            "🎨 Digital Experience": "A modern, user-friendly design will increase customer engagement and conversion rates significantly."
        }
        
        st.markdown(f"**For {service}:** {recommendations.get(service, 'We have the perfect solution for your needs!')}")
        
        if "Startup" in company_size:
            st.info("💡 **Startup Special**: We offer flexible payment plans and MVP development to help you get to market faster!")
        elif "Enterprise" in company_size:
            st.info("🏢 **Enterprise Focus**: We provide dedicated project managers and enterprise-grade security for large-scale implementations.")
        
        st.markdown("**Next Steps:**")
        st.markdown("1. Our solution architect will contact you within 24 hours")
        st.markdown("2. We'll schedule a detailed requirements discussion")
        st.markdown("3. You'll receive a custom proposal with timeline and pricing")
        st.markdown("4. We can start with a pilot project to demonstrate value")
    
    def _show_career_recommendation(self, experience, skills, role_type):
        """Show career recommendations"""
        
        st.success("🌟 Great! Based on your profile, here are some opportunities:")
        
        # Match experience to roles
        if "Fresh Graduate" in experience:
            st.markdown("**Perfect for you:**")
            st.markdown("- Junior Developer positions with mentorship")
            st.markdown("- Graduate trainee programs")
            st.markdown("- Internships with conversion opportunities")
        elif "10+ years" in experience:
            st.markdown("**Senior opportunities:**")
            st.markdown("- Tech Lead positions")
            st.markdown("- Solution Architect roles")
            st.markdown("- Team management positions")
        
        # Skill-based recommendations
        if "AI/ML" in skills:
            st.info("🤖 We're actively hiring for AI/ML Engineer positions!")
        if "DevOps" in skills:
            st.info("☁️ Our cloud team is expanding - DevOps engineers needed!")
        if "UI/UX Design" in skills:
            st.info("🎨 Join our design team to create amazing user experiences!")
        
        st.markdown("**What's next:**")
        st.markdown("1. Send your resume to careers@sundewsolutions.com")
        st.markdown("2. Mention this chat conversation in your application")
        st.markdown("3. Our HR team will contact you within 3-5 business days")
        st.markdown("4. If there's a match, we'll schedule interviews")
    
    def _show_info_response(self, topic):
        """Show information based on selected topic"""
        
        responses = {
            "🏢 About the Company": """
                **Sundew Solutions** is a leading digital transformation company founded with the vision of helping businesses thrive in the digital age.
                
                **Founded**: 2015
                **Headquarters**: India
                **Team Size**: 50+ experts
                **Mission**: Digital First. Digital Fast.
            """,
            "💼 Our Services & Solutions": """
                We offer comprehensive digital solutions:
                - **AI & Automation**: Chatbots, workflow automation
                - **Custom Development**: Web & mobile applications  
                - **Cloud Solutions**: AWS, Azure, DevOps
                - **Digital Design**: UX/UI, digital transformation
            """,
            "🎯 Industry Expertise": """
                We serve clients across multiple industries:
                - Healthcare & Life Sciences
                - Financial Services & Insurance
                - Retail & E-commerce
                - Manufacturing & Logistics
                - Media & Entertainment
            """,
            "📈 Success Stories & Case Studies": """
                **Recent achievements:**
                - Automated customer service for 100+ businesses
                - Reduced operational costs by 40% for clients
                - Improved user engagement by 60% through redesigns
                - Successfully migrated 50+ applications to cloud
            """,
            "🌟 Company Culture & Values": """
                **Our Values:**
                - Innovation-driven development
                - Client-centric approach
                - Continuous learning and growth
                - Collaborative team environment
                - Work-life balance
            """,
            "📰 Latest News & Insights": """
                **Recent highlights:**
                - Launched new AI chatbot platform
                - Expanded cloud services portfolio
                - Won 'Best Digital Transformation Partner' award
                - Published thought leadership on AI trends
            """
        }
        
        st.markdown(responses.get(topic, "Learn more about this topic by chatting with me!"))
        st.markdown("💬 **Ask me specific questions about any of these topics!**")