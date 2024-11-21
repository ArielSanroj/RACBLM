import streamlit as st
from datetime import datetime
from typing import Optional
from my_project.src.core.llm_service import LLMService
from my_project.src.core.embedding_service import EmbeddingService
from my_project.src.data.database import DatabaseManager
from my_project.src.utils.prompts import SYSTEM_PROMPTS
from my_project.src.utils.error_handler import handle_error
from my_project.src.utils.logger import setup_logger
from my_project.src.utils.constants import CATEGORIES
import openai
from my_project.src.core.chat_handler import ChatHandler
import os

logger = setup_logger(__name__)


class ChatInterface:
    def __init__(self, db: DatabaseManager, embedding_service: EmbeddingService):
        """
        Initialize the Chat Interface.
        Args:
            db (DatabaseManager): Database manager instance.
            embedding_service (EmbeddingService): Embedding service instance.
        """
        self.db = db
        self.embedding_service = embedding_service
        self.llm_service = LLMService()
        self.chat_handler = ChatHandler()
        self._initialize_session_state()
        self.apply_custom_styles()

    def _initialize_session_state(self):
        """Initialize session state variables."""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'current_category' not in st.session_state:
            st.session_state.current_category = 'general'  # Default category
        if 'assessment_results' not in st.session_state:
            st.session_state.assessment_results = None
        if 'user' not in st.session_state:
            st.session_state.user = {}  # Initialize user dictionary if not present

    def apply_custom_styles(self):
        """Apply custom CSS styles to the Streamlit app."""
        st.markdown("""
            <style>
            .chat-container {
                padding: 1rem;
                max-width: 800px;
                margin: 0 auto;
            }
            .message-container {
                margin-bottom: 1rem;
                display: flex;
                flex-direction: column;
            }
            .user-message {
                background-color: #f0f2f6;
                padding: 1rem;
                border-radius: 15px 15px 5px 15px;
                margin-left: auto;
                max-width: 80%;
            }
            .assistant-message {
                background-color: #e8f0fe;
                padding: 1rem;
                border-radius: 15px 15px 15px 5px;
                margin-right: auto;
                max-width: 80%;
            }
            .message-timestamp {
                font-size: 0.8rem;
                color: #666;
                margin-top: 0.25rem;
            }
            .chat-input {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 1rem;
                background: white;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            }
            </style>
        """, unsafe_allow_html=True)

    def display(self):
        """Display the chat interface."""
        st.title("Chat with Clio AI")

        # Sidebar for navigation
        self.render_sidebar()

        try:
            # Display chat history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if "timestamp" in message:
                        st.caption(f"{message['timestamp'].strftime('%I:%M %p')}")

            # Chat input
            if prompt := st.chat_input("Type your message here..."):
                # Add user message to chat
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt,
                    "timestamp": datetime.now()
                })

                # Get AI response
                response = self._get_ai_response(prompt)

                # Add and display assistant response
                self.add_message("assistant", response)
                with st.chat_message("assistant"):
                    st.markdown(response)

                # Save to database
                self.db.save_chat(
                    user_message=prompt,
                    assistant_message=response,
                    category=st.session_state.current_category,
                    timestamp=datetime.now()
                )

                st.rerun()

        except Exception as e:
            logger.error(f"Error in chat display: {str(e)}")
            st.error("An error occurred displaying the chat. Please refresh the page.")

    def _get_ai_response(self, prompt: str) -> str:
        """Generate AI response based on the user prompt."""
        try:
            # Get user profile from assessment results
            assessment_results = st.session_state.get('assessment_results', {})
            user_profile = assessment_results.get('emotion_profile', {})

            # Get current category
            category = st.session_state.get('current_category', 'general')

            # Get conversation history for context
            context = [
                msg["content"]
                for msg in st.session_state.messages[-5:]
                if msg["role"] == "user"
            ]

            # Generate response using chat handler
            response = self.chat_handler.generate_response(
                query=prompt,
                context=context,
                category=category,
                user_profile=user_profile  # Pass the entire user_profile dict
            )

            return response

        except Exception as e:
            logger.error(f"Error in _get_ai_response: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."

    def render_sidebar(self):
        """Render the sidebar with additional tools and options."""
        with st.sidebar:
            st.header("Analysis Tools")
            col1, col2 = st.columns(2)

            # Button for SEO Analyzer
            with col1:
                if st.button("SEO Analyzer"):
                    from src.marketing.seo_analyzer import render_seo_analyzer
                    render_seo_analyzer()
                    st.rerun()

            # Button for Webpage Analyzer
            with col2:
                if st.button("Webpage Analyzer"):
                    from my_project.src.marketing.webpage_analysis import render_webpage_analysis
                    render_webpage_analysis()
                    st.rerun()

            # View Coping Profile
            if st.button("See Coping Profile"):
                if st.session_state.assessment_results:
                    st.write("Your Coping Profile:")
                    st.json(st.session_state.assessment_results)
                else:
                    st.warning("No assessment results found.")

    def add_message(self, role: str, content: str):
        """Add a message to the chat history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        }
        st.session_state.messages.append(message)

    def clear_chat(self):
        """Clear chat history."""
        st.session_state.messages = []
        self.db.clear_chat_history()

    def render(self, category: Optional[str] = None, section: Optional[str] = None):
        """
        Main render method to display the chat interface.
        Can accept either a category or section parameter to customize the chat.
        """
        if category:
            st.session_state.current_category = category
        elif section:
            st.session_state.current_category = section
        else:
            st.session_state.current_category = 'general'

        self.display()

        # Additional functionality based on 'section' if needed
        if section:
            pass  # Implement as needed based on application requirements
