# Constants for Project Configuration

# Categories for Different Tools
CATEGORIES = {
    'education': {
        'name': 'Education',
        'description': 'Support for educational environments',
        'subcategories': [
            'Student Support',
            'Teacher Resources',
            'Classroom Management',
            'Educational Planning'
        ],
        'icon': '📚'
    },
    'hhrr': {
        'name': 'Human Resources',
        'description': 'Support for HR professionals',
        'subcategories': [
            'Employee Relations',
            'Workplace Culture',
            'Professional Development',
            'Conflict Resolution'
        ],
        'icon': '👔'
    },
    'marketing': {
        'name': 'Marketing',
        'description': 'Support for marketing professionals',
        'subcategories': [
            'Brand Strategy',
            'Market Analysis',
            'Campaign Planning',
            'Customer Insights'
        ],
        'icon': '📈'
    }
}

# Options for User Assessment Responses
ASSESSMENT_OPTIONS = [
    {"label": "Never", "value": 1},
    {"label": "Rarely", "value": 2},
    {"label": "Sometimes", "value": 3},
    {"label": "Often", "value": 4},
    {"label": "Very Often", "value": 5}
]

# Profile Types and Descriptions
PROFILE_TYPES = {
    "autonomous": {
        "name": "Autonomous",
        "description": "Independent and logical, but may struggle with stress or asking for help."
    },
    "impulsive": {
        "name": "Impulsive",
        "description": "Emotional and quick to react, often needing to focus on emotional regulation."
    },
    "avoidant": {
        "name": "Avoidant",
        "description": "Tends to shy away from challenges and prioritize comfort over confrontation."
    },
    "isolative": {
        "name": "Isolative",
        "description": "Prefers independence and may struggle with vulnerability in social contexts."
    }
}

# Streamlit Style Injection
def apply_styles():
    """
    Inject custom CSS styles into the Streamlit app for enhanced UI aesthetics.
    """
    st.markdown("""
        <style>
        /* General Content Styling */
        .main-content {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Section Descriptions */
        .section-description {
            padding: 1rem;
            background-color: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 2rem;
        }

        /* Footer Styling */
        .footer {
            margin-top: 3rem;
            padding: 1rem;
            background-color: #f8f9fa;
            border-radius: 8px;
            text-align: center;
        }

        /* Footer Links */
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 1rem;
        }

        .footer-links a {
            color: #666;
            text-decoration: none;
        }

        /* Social Icons */
        .social-icons {
            display: flex;
            justify-content: center;
            gap: 1rem;
        }

        .social-icon {
            text-decoration: none;
            font-size: 1.2rem;
        }

        /* Chat UI Enhancements */
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
        </style>
    """, unsafe_allow_html=True)
