import streamlit as st
import os
import json
from enum import Enum

class PromptCategory(Enum):
    """Enum representing categories of prompts."""
    GENERAL = "general"
    EMOTIONAL_SUPPORT = "emotional_support"
    CAREER_GUIDANCE = "career_guidance"
    PERSONAL_DEVELOPMENT = "personal_development"
    MARKETING = "marketing"

# Default prompts dictionary with proper structure
SYSTEM_PROMPTS = {
    "general": {
        "system": "You are a helpful AI assistant.",
        "profiles": {
            "autonomous": "For autonomous individuals, focus on logical reasoning and goal-oriented approaches.",
            "avoidant": "For avoidant individuals, provide gentle encouragement and validation.",
            "isolative": "For isolative individuals, respect personal space while offering support.",
            "impulsive": "For impulsive individuals, help with structured decision-making."
        }
    },
    "emotional_support": {
        "system": "You are an empathetic AI assistant focused on emotional support.",
        "profiles": {
            "autonomous": "Consider signals like breathing and heart rate changes.",
            "avoidant": "Notice contradictory signals between feelings and expressions.",
            "isolative": "Notice changes in breathing patterns and tendency to withdraw.",
            "impulsive": "Notice signs of agitation and intense emotional responses."
        }
    },
    "marketing": {
        "system": "You are a marketing AI assistant specialized in business strategy.",
        "profiles": {
            "autonomous": "Focus on data-driven decisions and measurable outcomes.",
            "avoidant": "Provide structured frameworks and clear guidelines.",
            "isolative": "Offer independent analysis tools and self-paced strategies.",
            "impulsive": "Help with systematic approach to market analysis."
        }
    }
}

# Create prompts dictionary for backward compatibility
prompts = {
    "general_query": "How can I assist you today?",
    "greeting": "Hello! How can I help you?",
    "goodbye": "Goodbye! Have a great day!",
    **{k: v["system"] for k, v in SYSTEM_PROMPTS.items()}
}

def get_system_prompt(category: str = "general", user_profile: dict = None) -> str:
    """Get a system prompt for the specified category and user profile."""
    if category not in SYSTEM_PROMPTS:
        category = "general"

    base_prompt = SYSTEM_PROMPTS[category]["system"]

    if user_profile and "profile_type" in user_profile:
        profile_type = user_profile["profile_type"].lower()
        if profile_type in SYSTEM_PROMPTS[category]["profiles"]:
            profile_guidance = SYSTEM_PROMPTS[category]["profiles"][profile_type]
            base_prompt += f"\n\nProfile-specific guidance: {profile_guidance}"

    return base_prompt

def generate_coping_prompt(responses: list) -> dict:
    """Generate a prompt for coping analysis based on responses."""
    return {
        "context": "Analyze the following responses to determine coping style:",
        "responses": responses,
        "instruction": "Based on these responses, identify the dominant coping style and provide relevant recommendations."
    }

# Export both SYSTEM_PROMPTS and prompts
__all__ = ['SYSTEM_PROMPTS', 'prompts', 'PromptCategory', 'get_system_prompt', 'generate_coping_prompt']
