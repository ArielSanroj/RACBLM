from my_project.src.core.llm_service import LLMService
import streamlit as st

def render_seo_analyzer():
    """
    Render the SEO Analyzer tool UI.
    Collects a URL input, sends it to LLMService for analysis, and displays results.
    """
    st.title("SEO Analyzer")
    url = st.text_input("Enter webpage URL:", placeholder="https://example.com")

    if st.button("Analyze Website"):
        if url:
            # Initialize LLMService and create a prompt for analysis
            llm_service = LLMService()
            prompt = (
                f"Analyze the content of this URL: {url}. "
                "Provide archetype-driven suggestions based on its meta content and structure. "
                "Suggest improvements for readability, SEO, and user engagement."
            )

            # Call LLMService to generate the analysis
            with st.spinner("Analyzing webpage content..."):
                try:
                    results = llm_service.generate_response(prompt)
                    display_results(results)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")

def display_results(results):
    """
    Display the results of the SEO analysis.
    Args:
        results (dict): The analysis results from LLMService.
    """
    st.subheader("SEO Analysis Results")

    # Display archetype suggestions
    st.write(f"**Archetype Suggestions:** {results.get('archetypes', 'No archetypes identified')}")

    # Display content recommendations
    st.write("### Content Recommendations")
    recommendations = results.get("recommendations", [])
    if recommendations:
        for rec in recommendations:
            st.write(f"- {rec}")
    else:
        st.write("No specific recommendations were generated.")

    # Display additional insights if available
    if "meta" in results:
        st.write("### Meta Information")
        st.write(f"**Title:** {results['meta'].get('title', 'N/A')}")
        st.write(f"**Meta Description:** {results['meta'].get('description', 'N/A')}")

    if "seo_score" in results:
        st.write(f"**SEO Score:** {results['seo_score']}")

    if "readability" in results:
        st.write(f"**Readability Score:** {results['readability']}")

    if "word_count" in results:
        st.write(f"**Estimated Word Count:** {results['word_count']}")

    # Add a button to run another analysis
    if st.button("Analyze Another Website"):
        st.session_state.seo_analysis = None
        st.experimental_rerun()
