import streamlit as st
from typing import Dict, List
from enum import Enum
from datetime import datetime


class Subscale(Enum):
    """Enumeration of coping subscales."""
    PROBLEM_SOLVING = "problem_solving"
    STRIVING_SUCCESS = "striving_success"
    WORRYING = "worrying"
    IGNORE_PROBLEM = "ignore_problem"
    LACK_COPING = "lack_coping"
    TENSION_REDUCTION = "tension_reduction"
    SELF_BLAME = "self_blame"
    RELAXING_DIVERSIONS = "relaxing_diversions"
    POSITIVE_FOCUS = "positive_focus"
    BUILD_HOPES = "build_hopes"
    SEEK_BELONGING = "seek_belonging"
    INVEST_FRIENDS = "invest_friends"
    SPIRITUAL_SUPPORT = "spiritual_support"
    PROFESSIONAL_HELP = "professional_help"
    KEEP_TO_SELF = "keep_to_self"
    SOCIAL_SUPPORT = "social_support"
    SOCIAL_ACTION = "social_action"
    PHYSICAL_RECREATION = "physical_recreation"


class CopingEngine:
    def __init__(self, db_session=None):
        """
        Initialize the CopingEngine.

        Args:
            db_session: SQLAlchemy database session
        """
        self.db_session = db_session
        self.archetypes = self._initialize_archetypes()
        self.subscales = self._initialize_subscales()
        self.archetype_subscale_mapping = self._initialize_archetype_subscale_mapping()

    def _initialize_archetypes(self) -> Dict[str, Dict]:
        """Define the coping archetypes."""
        return {
            "autonomous": {
                "description": "You seek to solve problems quickly through your skills, but might struggle with stress or asking for help.",
                "recommendations": [
                    "Practice active listening and empathetic communication",
                    "Set realistic goals and maintain work-life balance",
                    "Develop stress management techniques",
                    "Learn to delegate and collaborate effectively"
                ]
            },
            "impulsive": {
                "description": "You may struggle with self-doubt and emotional expression, potentially experiencing challenges in managing emotions effectively.",
                "recommendations": [
                    "Develop anger management skills",
                    "Build frustration tolerance",
                    "Practice mindfulness techniques",
                    "Focus on accountability without blame",
                    "Promote balanced self-perception"
                ]
            },
            "avoidant": {
                "description": "You enjoy leisure but may struggle with decision-making if it conflicts with the group consensus.",
                "recommendations": [
                    "Encourage active listening",
                    "Practice problem-solving from different perspectives",
                ]
            },
            "isolative": {
                "description": "You prefer independence and may struggle with vulnerability in social contexts.",
                "recommendations": [
                    "Gradually build trusted support networks",
                    "Balance solitude with social interaction",
                    "Practice sharing thoughts and feelings",
                    "Explore group activities aligned with your interests"
                ]
            }
        }

    def _initialize_subscales(self):
        """Initialize subscales for coping assessment."""
        return {
            "problem_solving": 0.0,
            "emotional_regulation": 0.0,
            "social_support": 0.0,
            "avoidance": 0.0
        }

    def _initialize_archetype_subscale_mapping(self):
        """Initialize mapping between archetypes and subscales."""
        return {
            "autonomous": ["problem_solving", "emotional_regulation"],
            "impulsive": ["emotional_regulation", "avoidance"],
            "avoidant": ["social_support", "avoidance"],
            "isolative": ["social_support", "problem_solving"]
        }

    def analyze_responses(self, responses: Dict[str, str]) -> Dict:
        """Analyze user responses and compute scores."""
        subscale_scores = self._calculate_subscale_scores(responses)
        archetype_scores = self._calculate_archetype_scores(subscale_scores)

        dominant_archetype = max(archetype_scores.items(), key=lambda x: x[1])[0]

        return {
            "dominant_archetype": dominant_archetype,
            "archetype_scores": archetype_scores,
            "subscale_scores": subscale_scores,
            "timestamp": datetime.now().isoformat()
        }

    def _calculate_subscale_scores(self, responses: Dict[str, str]) -> Dict[str, float]:
        """Calculate normalized scores for each subscale."""
        response_to_score = {"Never": 1, "Rarely": 2, "Sometimes": 3, "Often": 4, "Very Often": 5}
        subscale_scores = {}

        for question_id, response in responses.items():
            subscale = question_id.split('_')[0]
            score = response_to_score.get(response, 0)

            if subscale not in subscale_scores:
                subscale_scores[subscale] = []

            subscale_scores[subscale].append(score)

        # Average and normalize scores
        return {
            subscale: sum(scores) / len(scores) / 5
            for subscale, scores in subscale_scores.items()
        }

    def _calculate_archetype_scores(self, subscale_scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate scores for each archetype based on subscale correlations."""
        archetype_scores = {}

        for archetype, subscales in self.archetype_subscale_mapping.items():
            scores = [
                subscale_scores.get(subscale, 0)
                for subscale in subscales
            ]
            archetype_scores[archetype] = sum(scores) / len(scores)

        return archetype_scores

    def get_archetype_details(self, archetype: str) -> Dict:
        """Retrieve details about a specific archetype."""
        return self.archetypes.get(archetype, {})
