import streamlit as st
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Union, Optional
from my_project.src.utils.prompts import prompts, SYSTEM_PROMPTS 
import openai
import os
from my_project.src.utils.logger import setup_logger

logger = setup_logger(__name__)


class EmbeddingService:
    def __init__(self, model_name: str = "bert-base-uncased", device: Optional[str] = None, openai_api_key: Optional[str] = None):
        """
        Initialize the embedding service with a pre-trained model, tokenizer, emotion engine, and OpenAI API key.

        Args:
            model_name (str): Name of the pre-trained model to use for embeddings.
            device (str, optional): Device to run the model on. Defaults to "cuda" if available, else "cpu".
            openai_api_key (str, optional): OpenAI API key for generating responses. If None, the API won't be used.
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

    def get_embeddings(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for the given text or list of texts.

        Args:
            text (str or List[str]): The input text(s) for embedding.

        Returns:
            np.ndarray: The mean-pooled embeddings.
        """
        if isinstance(text, str):
            text = [text]  # Convert single text to a list

        try:
            # Tokenize input with padding and truncation
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)

            # Perform mean pooling on token embeddings
            embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return np.array([])

    def get_relevant_content(self, text: str, database: List[str]) -> List[str]:
        """
        Find relevant content based on embeddings by calculating similarity to the database.

        Args:
            text (str): The input text for which to find relevant content.
            database (List[str]): List of text entries to compare against.

        Returns:
            List[str]: A list of relevant content sorted by similarity.
        """
        try:
            # Get the embedding for the input text
            query_embedding = self.get_embeddings(text)

            # Get embeddings for the database entries
            database_embeddings = np.array([self.get_embeddings(entry) for entry in database])

            # Calculate cosine similarity
            similarities = cosine_similarity(query_embedding, database_embeddings).flatten()

            # Rank entries by similarity (higher is better)
            ranked_indices = similarities.argsort()[::-1]
            return [database[idx] for idx in ranked_indices]

        except Exception as e:
            logger.error(f"Error finding relevant content: {str(e)}")
            return []

    def find_similar(self, query: str, database: List[str]) -> List[str]:
        """
        Find the most similar entries in a database to a given query.

        Args:
            query (str): The input query text.
            database (List[str]): The database of text entries to compare against.

        Returns:
            List[str]: Ranked list of similar entries.
        """
        return self.get_relevant_content(query, database)

    def get_response(self, prompt: str, context: Optional[dict] = None) -> str:
        """
        Generate a response based on the given prompt and context using both the emotion engine and embeddings.

        Args:
            prompt (str): The user input text.
            context (dict, optional): Additional context to tailor the response.

        Returns:
            str: The generated response.
        """
        try:
            # Check for relevant prompt template from prompts.py
            response_prompt = prompts.get("general_query", "How can I assist you today?")
            if "hello" in prompt.lower():
                response_prompt = prompts.get("greeting", response_prompt)
            elif "bye" in prompt.lower():
                response_prompt = prompts.get("goodbye", response_prompt)

            # If OpenAI API key is provided, use it to get a response
            if self.openai_api_key:
                openai.api_key = self.openai_api_key

                # Construct the prompt for OpenAI API
                full_prompt = f"{response_prompt}\nUser: {prompt}\nAssistant:"

                # Make a call to the OpenAI API for a response
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Replace with desired OpenAI model
                    prompt=full_prompt,
                    max_tokens=150,
                    temperature=0.7
                )

                # Extract the assistant's response
                return response.choices[0].text.strip()

            else:
                # Fallback response if no API key is provided
                return f"Response based on the prompt: '{response_prompt}'"

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I encountered an error. Please try again."

    def generate_coping_response(self, responses: List[str]) -> dict:
        """
        Generate a coping response using the emotion engine.

        Args:
            responses (List[str]): List of user responses to analyze.

        Returns:
            dict: Analysis results from the emotion engine.
        """
        try:
            return self.emotion_engine.analyze_responses(responses)
        except Exception as e:
            logger.error(f"Error generating coping response: {str(e)}")
            return {"error": "Could not generate coping response."}
