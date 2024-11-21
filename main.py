import os
import sys
from pathlib import Path
import streamlit as st
from my_project.src.core.coping_engine import CopingEngine
from my_project.src.education.coping_test import render_coping_test
from my_project.src.marketing.icp_questionnaire import render_icp_questionnaire
from my_project.src.marketing.seo_analyzer import render_seo_analyzer
from my_project.src.components.chat_interface import ChatInterface
from my_project.src.data.database import DatabaseManager
from my_project.src.auth.auth_service import AuthService
from my_project.src.core.embedding_service import EmbeddingService

# Add the my_project directory to Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

def main():
    """Main function to run the Clio AI app."""
    # Ensure 'authenticated' is initialized in session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False  # Initialize to False by default

    # Create database manager instance
    db_manager = DatabaseManager()

    try:
        # Get a session from the database manager
        session = db_manager.get_session()

        # Initialize services with the database session
        coping_engine = CopingEngine(db_session=session)
        auth_service = AuthService()
        embedding_service = EmbeddingService()

        st.set_page_config(page_title="Clio AI", layout="wide")

        # Sidebar navigation
        st.sidebar.title("Clio AI Tools")
        selected_tool = st.sidebar.selectbox(
            "Choose a tool", ["Coping Test", "ICP Questionnaire", "SEO Analyzer", "Chat"]
        )

        # Authentication check
        if not st.session_state.authenticated:
            render_authentication(auth_service)
        else:
            # Tool execution based on selection
            try:
                if selected_tool == "Coping Test":
                    render_coping_test()
                elif selected_tool == "ICP Questionnaire":
                    render_icp_questionnaire()
                elif selected_tool == "SEO Analyzer":
                    render_seo_analyzer()
                elif selected_tool == "Chat":
                    chat_interface = ChatInterface(db_manager, embedding_service)
                    chat_interface.display()
            except Exception as e:
                st.error(f"An error occurred while using {selected_tool}. Please try again.")
                raise e

    finally:
        # Close the session and database connection
        session.close()
        db_manager.close()

def render_authentication(auth_service):
    """Render the Authentication UI for login or registration."""
    st.title("Welcome to Clio AI")

    # Authentication options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            show_registration_form(auth_service)
    with col2:
        if st.button("Login"):
            show_login_form(auth_service)

def show_registration_form(auth_service):
    """Render the registration form UI."""
    with st.form("registration_form"):
        st.header("Register")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        name = st.text_input("Name")
        service = st.selectbox("Select Service", ["Education", "HHRR", "Marketing"])

        if st.form_submit_button("Register"):
            if auth_service.register(email, password, name, service):
                st.session_state.authenticated = True
                st.success("Registration successful!")
                st.experimental_rerun()
            else:
                st.error("Registration failed. Email may already exist.")

def show_login_form(auth_service):
    """Render the login form UI."""
    with st.form("login_form"):
        st.header("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Login"):
            user_data = auth_service.login(email, password)
            if user_data:
                st.session_state.authenticated = True
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials. Please try again.")

class MarketingFlow:
    """Class to manage the marketing workflow in the app."""

    def __init__(self, db, coping_engine):
        self.db = db
        self.coping_engine = coping_engine
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize session state for marketing workflow."""
        if "marketing_stage" not in st.session_state:
            st.session_state.marketing_stage = "brand_questionnaire"
        if "brand_data" not in st.session_state:
            st.session_state.brand_data = None
        if "icp_data" not in st.session_state:
            st.session_state.icp_data = None

    def display(self):
        """Display the appropriate UI based on the current stage."""
        if st.session_state.marketing_stage == "brand_questionnaire":
            self.brand_questionnaire()
        elif st.session_state.marketing_stage == "icp_questionnaire":
            self.icp_questionnaire()
        elif st.session_state.marketing_stage == "webpage_analyzer":
            self.webpage_analyzer()
        elif st.session_state.marketing_stage == "marketing_chat":
            self.marketing_chat()

    def brand_questionnaire(self):
        """Render the Brand Questionnaire stage."""
        st.title("Brand Questionnaire")
        with st.form("brand_form"):
            brand_name = st.text_input("What is your brand name?")
            industry = st.selectbox(
                "What industry are you in?",
                ["Technology", "Healthcare", "Education", "E-commerce", "Other"]
            )
            brand_values = st.text_area("What are your brand's core values?")
            target_audience = st.text_area("Who is your target audience?")

            if st.form_submit_button("Next"):
                st.session_state.brand_data = {
                    "brand_name": brand_name,
                    "industry": industry,
                    "brand_values": brand_values,
                    "target_audience": target_audience
                }
                st.session_state.marketing_stage = "icp_questionnaire"
                st.experimental_rerun()

    def icp_questionnaire(self):
        """Render the Ideal Customer Profile Questionnaire stage."""
        st.title("Ideal Customer Profile (ICP)")
        with st.form("icp_form"):
            demographics = st.text_area("Describe your ideal customer demographics")
            pain_points = st.text_area("What are their main pain points?")
            goals = st.text_area("What are their primary goals?")
            channels = st.multiselect(
                "Preferred communication channels",
                ["Email", "Social Media", "Phone", "Website", "Other"]
            )

            if st.form_submit_button("Next"):
                st.session_state.icp_data = {
                    "demographics": demographics,
                    "pain_points": pain_points,
                    "goals": goals,
                    "channels": channels
                }
                st.session_state.marketing_stage = "webpage_analyzer"
                st.experimental_rerun()

    def webpage_analyzer(self):
        """Render the Webpage Analyzer stage."""
        st.title("Webpage Analyzer")
        render_seo_analyzer()

        if st.session_state.webpage_analysis.get("is_completed"):
            st.session_state.marketing_stage = "marketing_chat"
            st.experimental_rerun()

    def marketing_chat(self):
        """Render the Marketing Chat stage."""
        st.title("Marketing AI Assistant")

        # Display brand and ICP data in the sidebar
        with st.sidebar:
            with st.expander("Brand Profile"):
                st.write(st.session_state.brand_data)
            with st.expander("ICP Profile"):
                st.write(st.session_state.icp_data)

        # Initialize chat interface
        chat_interface = ChatInterface(db=self.db, embedding_service=self.coping_engine)
        chat_interface.render(category="marketing")

if __name__ == "__main__":
    main()
