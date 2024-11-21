import openai
from my_project.src.utils.prompts import generate_coping_prompt
from typing import List, Dict

class LLMService:
    def __init__(self, api_key: str = None):
        """
        Initialize LLMService with OpenAI API key.
        Args:
            api_key (str, optional): OpenAI API key. Defaults to environment variable.
        """
        self.api_key = api_key or openai.api_key
        if not self.api_key:
            raise ValueError("OpenAI API key not provided or found in environment variables.")
        openai.api_key = self.api_key

    def generate_coping_response(self, responses: List[str]) -> Dict:
        """
        Generate a response analyzing coping mechanisms.
        Args:
            responses (list): User responses to coping test.
        Returns:
            dict: JSON response with archetypes, subscales, and recommendations.
        """
        # Generate a tailored prompt for coping responses
        prompt = generate_coping_prompt(responses)

        # Example static response to simulate the function's intent
        return {
            "archetypes": {
                "dominant": "Problem Solver"
            },
            "subscales": {
                "problem_solving": 0.8,
                "emotional_regulation": 0.7
            },
            "recommendations": [
                "Focus on breaking down problems",
                "Practice stress management"
            ]
        }

    def generate_response(self, prompt: str, model: str = "gpt-4", max_tokens: int = 1000) -> Dict:
        """
        Generate a response from OpenAI API.
        Args:
            prompt (str): Prompt for OpenAI.
            model (str, optional): Model name. Defaults to "gpt-4".
            max_tokens (int, optional): Maximum number of tokens. Defaults to 1000.
        Returns:
            dict: Parsed response from OpenAI.
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            content = response.choices[0].message["content"]
            return content
        except Exception as e:
            raise RuntimeError(f"Error generating response: {str(e)}")
