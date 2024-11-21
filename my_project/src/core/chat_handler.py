import streamlit as st
import os
import openai
from typing import Dict, List, Optional
from my_project.src.utils.prompts import SYSTEM_PROMPTS, get_system_prompt
from my_project.src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ChatHandler:
    """
    Handles chat interactions by managing prompt construction, OpenAI API integration,
    and response generation tailored to user profiles and categories.
    """

    def __init__(self):
        """
        Initialize the ChatHandler by setting up the OpenAI API key.
        Raises:
            ValueError: If the OpenAI API key is not found in environment variables.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables.")
        openai.api_key = self.api_key

    def generate_response(
        self,
        query: str,
        context: Optional[List[str]] = None,
        category: str = "general",
        user_profile: Optional[Dict] = None
    ) -> str:
        """
        Generate AI response based on query, context, category, and user profile.

        Args:
            query (str): User's input message.
            context (List[str], optional): Previous conversation context.
            category (str, optional): Type of conversation (default: "general").
            user_profile (Dict, optional): User's profile information.

        Returns:
            str: AI-generated response.
        """
        try:
            # Ensure context is initialized
            context = context or []

            # Retrieve the appropriate system prompt based on category and user profile
            system_prompt = get_system_prompt(category, user_profile)

            # Log the input details for debugging
            logger.info(f"Generating response for category: {category}")
            logger.debug(f"System Prompt: {system_prompt}")
            logger.debug(f"Query: {query}")
            logger.debug(f"Context: {context}")

            # Construct the messages payload for OpenAI API
            messages = [{"role": "system", "content": system_prompt}] + [
                {"role": "user", "content": ctx} for ctx in context
            ]
            messages.append({"role": "user", "content": query})

            # Query OpenAI API for response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            # Extract the assistant's reply
            assistant_reply = response.choices[0].message["content"].strip()

            logger.info("Response generated successfully.")
            logger.debug(f"Assistant Reply: {assistant_reply}")

            return assistant_reply

        except openai.error.OpenAIError as oe:
            logger.error(f"OpenAI API Error: {str(oe)}")
            return "I encountered an issue accessing the AI service. Please try again later."

        except Exception as e:
            logger.error(f"Unexpected error generating response: {str(e)}")
            return "I'm sorry, I encountered an error while processing your request. Could you rephrase it?"

    def generate_contextual_prompt(
        self,
        category: str,
        user_profile: Optional[Dict] = None
    ) -> str:
        """
        Generate a contextual system prompt based on the given category and user profile.

        Args:
            category (str): Conversation category (e.g., "education", "marketing").
            user_profile (Dict, optional): User profile information.

        Returns:
            str: Generated contextual system prompt.
        """
        try:
            prompt = get_system_prompt(category, user_profile)
            logger.debug(f"Generated contextual prompt: {prompt}")
            return prompt
        except Exception as e:
            logger.error(f"Error generating contextual prompt: {str(e)}")
            return "Let's continue with our conversation. How can I help you today?"

    def log_chat_history(
        self,
        user_message: str,
        assistant_message: str,
        category: str,
        user_id: Optional[str] = None
    ):
        """
        Log chat messages to a persistent storage or logger.

        Args:
            user_message (str): User's input message.
            assistant_message (str): Assistant's response message.
            category (str): Conversation category.
            user_id (str, optional): ID of the user (if available).
        """
        try:
            logger.info(f"Logging chat history for user {user_id or 'unknown'}")
            logger.debug(f"Category: {category}")
            logger.debug(f"User Message: {user_message}")
            logger.debug(f"Assistant Message: {assistant_message}")

            # Placeholder for database logging
            # Example: Save to database (if implemented)
            # self.database.save_chat(user_id, user_message, assistant_message, category)

        except Exception as e:
            logger.error(f"Error logging chat history: {str(e)}")

    def get_archetype_suggestions(self, archetype_name: str) -> Dict:
        """
        Retrieve archetype-specific context and strategies.

        Args:
            archetype_name (str): Name of the archetype.

        Returns:
            Dict: Archetype-specific information and strategies.
        """
        try:
            context = get_archetype_context(archetype_name)
            logger.debug(f"Archetype Context for {archetype_name}: {context}")
            return context
        except Exception as e:
            logger.error(f"Error retrieving archetype context: {str(e)}")
            return {}

    def suggest_category(self, query: str) -> str:
        """
        Suggest a category based on the query using predefined keywords or AI analysis.

        Args:
            query (str): User's query.

        Returns:
            str: Suggested category (default to "general" if no match).
        """
        try:
            # Example keyword-based categorization (expandable)
            keywords_to_categories = {
                "education": ["study", "learn", "teach", "student"],
                "marketing": ["brand", "SEO", "advertising", "campaign"],
                "human resources": ["employee", "HR", "workplace", "conflict"]
            }

            for category, keywords in keywords_to_categories.items():
                if any(keyword in query.lower() for keyword in keywords):
                    logger.info(f"Suggested category: {category}")
                    return category

            # Default fallback
            logger.info("Default category: general")
            return "general"

        except Exception as e:
            logger.error(f"Error suggesting category: {str(e)}")
            return "general"
