import streamlit as st
import requests
import pandas as pd
import logging
import traceback
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure the page
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("SHL Assessment Recommendation System")
st.markdown("""
This tool helps you find the most suitable SHL assessments based on job descriptions or specific requirements.
Simply enter your query or job description below, and we'll recommend the most relevant assessments.
""")

API_URL = "http://localhost:8000/api/recommend"
HEALTH_CHECK_URL = "http://localhost:8000/health"

def check_api_connection():
    """Check if the API server is running and healthy."""
    try:
        response = requests.get(HEALTH_CHECK_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"API health check response: {data}")
            return data.get("status") == "healthy"
        else:
            logger.error(f"API health check failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"API connection error: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def get_recommendations(query: str, max_results: int = 10):
    """Get assessment recommendations from the API."""
    try:
        logger.info(f"Sending recommendation request for query: {query}")
        response = requests.post(
            API_URL,
            json={"query": query, "max_results": max_results},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        logger.info(f"Received {len(data['recommendations'])} recommendations")
        return data["recommendations"]
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to the API server")
        st.error("Failed to connect to the API server. Please make sure the API server is running.")
        return None
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        st.error("The request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        logger.error(traceback.format_exc())
        st.error(f"An error occurred: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        st.error("An unexpected error occurred. Please try again.")
        return None

# Check API connection
if not check_api_connection():
    st.warning("""
    ⚠️ The API server is not running or is not accessible.
    
    To start the API server:
    1. Open a new terminal
    2. Navigate to the project directory
    3. Run: `cd api && uvicorn main:app --reload --host 0.0.0.0 --port 8000`
    
    Once the server is running, refresh this page.
    """)
    st.stop()

# Input section
st.header("Enter Job Description or Query")
query = st.text_area(
    "Describe the job role, requirements, or skills you want to assess:",
    height=150,
    placeholder="Example: I need to assess candidates for a software engineering position. The role requires strong problem-solving skills, technical knowledge, and ability to work in a team."
)

max_results = st.slider("Maximum number of recommendations:", 1, 10, 5)

if st.button("Get Recommendations"):
    if not query:
        st.warning("Please enter a job description or query.")
    else:
        with st.spinner("Getting recommendations..."):
            recommendations = get_recommendations(query, max_results)
            
            if recommendations:
                # Convert to DataFrame for better display
                df = pd.DataFrame([{
                    "Assessment": rec["name"],
                    "Type": rec["test_type"],
                    "Duration": rec["duration"],
                    "Remote Testing": "Yes" if rec["remote_testing"] else "No",
                    "Adaptive/IRT": "Yes" if rec["adaptive_irt"] else "No",
                    "Description": rec["description"],
                    "Link": f"[View Details]({rec['url']})"
                } for rec in recommendations])
                
                # Display results
                st.header("Recommended Assessments")
                st.dataframe(
                    df,
                    column_config={
                        "Link": st.column_config.LinkColumn("Link"),
                        "Description": st.column_config.TextColumn("Description", width="large")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Add download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Recommendations",
                    data=csv,
                    file_name="shl_recommendations.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No recommendations found. Please try a different query.")

# Footer
st.markdown("---")
st.markdown("""
### About
This recommendation system uses advanced AI to match job requirements with the most suitable SHL assessments.
The system considers various factors including assessment type, duration, and testing capabilities.
""") 