from my_project.src.core.coping_engine import CopingEngine
from my_project.src.core.llm_service import LLMService
import streamlit as st



# Define question metadata
QUESTIONS = [
    {
        "id": "q1",
        "text": "I talk to others to find out what they would do if they had the same problem.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Social Support Seeking",
        "weight": 4
    },
    {
        "id": "q2",
        "text": "I dedicate myself to solving the problem using all my capabilities.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Focus on Solving the Problem",
        "weight": 4
    },
    {
        "id": "q3",
        "text": "I strive to succeed in the things I'm doing.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Striving and Achieving",
        "weight": 4
    },
    {
        "id": "q4",
        "text": "I worry about what is happening.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Worrying",
        "weight": 4
    },
    {
        "id": "q5",
        "text": "I consciously decide to ignore the problem.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Ignoring the Problem",
        "weight": 4
    },
    {
        "id": "q6",
        "text": "I find a way to relax, such as listening to music, reading, or watching TV.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Reducing Tension",
        "weight": 4
    },
    {
        "id": "q7",
        "text": "I tend to blame myself when things go wrong.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Self-Blame",
        "weight": 4
    },
    {
        "id": "q8",
        "text": "I focus on enjoyable activities or having fun to feel better.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Seeking Relaxing Diversions",
        "weight": 7
    },
    {
        "id": "q9",
        "text": "I try to see the good side of things and focus on positive thoughts.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Focusing on the Positive",
        "weight": 7
    },
    {
        "id": "q10",
        "text": "I hope for a positive outcome and believe everything will work out in the end.",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
        "subscale": "Building Hopes",
        "weight": 7
    }
]

def collect_user_responses():
    """
    UI logic to collect user responses for the coping test.
    Returns:
        dict: User responses mapped to question IDs.
    """
    responses = {}
    for question in QUESTIONS:
        response = st.radio(
            question["text"],
            options=question["options"],
            key=f"q_{question['id']}"
        )
        responses[question["id"]] = response

    return responses

def render_coping_test():
    """
    Render the Coping Test UI and process results.
    """
    st.title("Coping Mechanisms Test")
    st.markdown(
        """
        This test will help you identify your dominant coping mechanisms and strategies.
        Please answer the following questions honestly. There are no right or wrong answers.
        """
    )

    # Collect user responses
    responses = collect_user_responses()

    # Submit Button
    if st.button("Submit"):
        engine = CopingEngine()
        # Analyze responses with metadata (questions)
        results = engine.analyze_responses(responses, questions=QUESTIONS)
        display_coping_results(results)

def display_coping_results(results):
    """
    Display coping test results.
    Args:
        results (dict): Results from the CopingEngine analysis.
    """
    st.subheader("Coping Test Results")

    # Display dominant archetype
    st.markdown("### Dominant Archetype:")
    dominant_profile = results.get("profile_analysis", {}).get("dominant_profile", "Unknown")
    st.write(f"**{dominant_profile.capitalize()}**")

    # Display archetype scores
    st.markdown("### Archetype Scores:")
    archetype_scores = results.get("profile_analysis", {}).get("profile_scores", {})
    for archetype, score in archetype_scores.items():
        st.write(f"- **{archetype.capitalize()}**: {score:.2f}%")

    # Display subscale scores
    st.markdown("### Subscale Scores:")
    subscale_scores = results.get("subscale_scores", {})
    for subscale, score in subscale_scores.items():
        st.write(f"- **{subscale.replace('_', ' ').title()}**: {score * 100:.2f}%")

    # Display recommendations
    recommendations = results.get("recommendations", [])
    if recommendations:
        st.markdown("### Recommendations:")
        for recommendation in recommendations:
            st.write(f"- {recommendation}")
    else:
        st.info("No specific recommendations available.")

def save_results_to_database(user_id, responses):
    """
    Save assessment results to the database (placeholder).
    Args:
        user_id (str): The user ID.
        responses (dict): User responses.
    """
    # Placeholder for saving to the database
    st.success(f"Results saved for User ID: {user_id}")

if __name__ == "__main__":
    render_coping_test()
