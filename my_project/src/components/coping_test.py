from my_project.src.core.coping_engine import CopingEngine
import streamlit as st

def render_coping_test():
    st.title("Coping Test")
    st.markdown("Answer the following questions to understand your coping style.")

    # Collect user responses
    questions = [
        "I solve problems using logical reasoning.",
        "I focus on my goals even when facing difficulties.",
        "I avoid dealing with problems.",
        "I tend to blame myself when things go wrong."
    ]
    responses = {}
    for idx, question in enumerate(questions):
        response = st.radio(
            f"Q{idx + 1}: {question}",
            options=["Never", "Rarely", "Sometimes", "Often", "Very Often"],
            key=f"q_{idx}"
        )
        responses[f"q_{idx}"] = response

    # Submit and analyze responses
    if st.button("Submit"):
        llm_service = LLMService()  # Initialize LLMService
        results = llm_service.generate_coping_response(list(responses.values()))  # Get AI analysis
        display_results(results)

def display_results(results):
    st.subheader("Coping Test Results")
    st.write("### Dominant Archetype:")
    st.write(f"**{results['archetypes']['dominant']}**")
    st.write("### Subscale Scores:")
    for subscale, score in results['subscales'].items():
        st.write(f"- {subscale}: {score}")
    st.write("### Recommendations:")
    for recommendation in results['recommendations']:
        st.write(f"- {recommendation}")
