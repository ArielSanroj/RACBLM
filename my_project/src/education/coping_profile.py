from my_project.src.core.coping_engine import CopingEngine
import streamlit as st

def render_coping_profile():
    """Render a detailed coping profile based on user responses."""
    st.title("Coping Profile")

    engine = CopingEngine()  # Initialize CopingEngine
    user_responses = collect_user_responses()  # Collect user responses

    if st.button("Analyze Profile"):
        results = engine.analyze_responses(user_responses)
        display_profile(results)

def display_profile(results):
    """Display detailed archetype and subscale analysis."""
    st.subheader("Your Coping Profile")
    archetype = results["profile_analysis"]["dominant_profile"].capitalize()
    st.markdown(f"### Dominant Archetype: **{archetype}**")

    st.markdown("### Subscale Analysis:")
    for subscale, score in results["subscale_scores"].items():
        st.write(f"{subscale.title()}: {score * 100:.2f}%")

    st.markdown("### Recommendations:")
    recommendations = results["profile_analysis"]["recommendations"]
    for rec in recommendations:
        st.write(f"- {rec}")
