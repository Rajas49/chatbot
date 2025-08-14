"""
Enhanced Chat Engine for Sundew Solutions
Handles all AI processing, document retrieval, and response generation
"""

import os
import streamlit as st
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv

from utils.document_processor import DocumentProcessor
from utils.intent_detector import IntentDetector
from utils.response_enhancer import ResponseEnhancer

load_dotenv()

class ChatEngine:
    """Main chat processing engine"""
    
    def __init__(self, config):
        self.config = config
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.setup_models()
        self.document_processor = DocumentProcessor(config)
        self.intent_detector = IntentDetector(config)
        self.response_enhancer = ResponseEnhancer(config)
        
    def setup_models(self):
        """Initialize AI models"""
        os.environ["TRANSFORMERS_NO_TF"] = "1"
        
        # Intent classification model
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="valhalla/distilbart-mnli-12-1"
        )
        
        # Embedding model for document similarity
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # LLM for response generation
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = ChatOpenAI(
                model_name="gpt-4",
                temperature=0.2,
                openai_api_key=api_key
            )
        else:
            st.warning("OpenAI API key not found. Some features may be limited.")
            self.llm = None
    
    def process_user_input(self, user_input: str, user_data: dict = None) -> str:
        """
        Main method to process user input and generate response
        
        Args:
            user_input: The user's question/message
            user_data: Additional user context (email, name, etc.)
            
        Returns:
            Generated response string
        """
        try:
            # Detect user intent and relevant categories
            intents = self.intent_detector.detect_intents(user_input)
            
            # Find and rank relevant documents
            matched_docs = self.document_processor.rank_documents(
                user_input, 
                intents.get('folders', []),
                top_k=3
            )
            
            if matched_docs and self.llm:
                # Create retriever from matched documents
                retriever = self._build_temp_retriever(matched_docs)
                
                # Build enhanced prompt
                enhanced_prompt = self.response_enhancer.build_professional_prompt(
                    user_input, user_data, intents
                )
                
                # Generate response using RAG chain
                chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    memory=self.memory
                )
                
                response = chain.run({
                    "question": enhanced_prompt, 
                    "chat_history": self.memory.chat_memory.messages
                })
                
                # Enhance response with company-specific elements
                enhanced_response = self.response_enhancer.enhance_response(
                    response, intents, user_data
                )
                
                return enhanced_response
            else:
                # Fallback response with helpful guidance
                return self._generate_fallback_response(intents, user_data)
                
        except Exception as e:
            st.error(f"Error processing input: {str(e)}")
            return "I apologize, but I encountered an error. Please try rephrasing your question."
    
    def _build_temp_retriever(self, matched_docs):
        """Build temporary FAISS retriever from documents"""
        langchain_docs = [
            Document(page_content=doc_text, metadata={"source": fname}) 
            for _, fname, doc_text in matched_docs
        ]
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        temp_faiss = FAISS.from_documents(langchain_docs, embedding=embeddings)
        return temp_faiss.as_retriever()
    
    def _generate_fallback_response(self, intents, user_data=None):
        """Generate helpful fallback response when no documents match"""
        response = "I'd be happy to help you with information about Sundew Solutions! "
        
        if intents.get('categories'):
            category = intents['categories'][0]
            if 'service' in category.lower():
                response += "We offer comprehensive digital transformation services including AI chatbots, custom web development, and automation solutions. "
            elif 'career' in category.lower():
                response += "We're always looking for talented individuals! Check out our careers page for current openings. "
            elif 'case' in category.lower():
                response += "Our case studies showcase successful projects across various industries. "
        
        response += "For specific information, please contact our team at sales@sundewsolutions.com or visit our website."
        return response
    
    def get_conversation_summary(self):
        """Get summary of current conversation"""
        if hasattr(self.memory, 'chat_memory') and self.memory.chat_memory.messages:
            return f"Conversation with {len(self.memory.chat_memory.messages)} messages"
        return "New conversation"