import os
import requests
import streamlit as st

st.set_page_config(
    page_title="OpportunityAI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 OpportunityAI")
st.subheader("Smart Student Opportunity Navigator")

st.write(
    "Find internships, scholarships, hackathons, competitions, "
    "and certifications using live web search."
)

# Get SerpApi key securely 
API_KEY = st.secrets.get("SERPAPI_KEY")

# Student profile
st.sidebar.header("👩‍🎓 Student Profile")

education = st.sidebar.text_input(
    "Education",
    "B.Tech"
)

skills = st.sidebar.text_input(
    "Skills",
    "Python, AI, Machine Learning"
)

location = st.sidebar.text_input(
    "Preferred Location",
    "India"
)

opportunity_type = st.sidebar.selectbox(
    "Opportunity Type",
    [
        "Internships",
        "Scholarships",
        "Hackathons",
        "Competitions",
        "Certifications",
        "Jobs"
    ]
)

search_button = st.button("🔎 Find Opportunities")


def search_serpapi(query):
    """Search Google through SerpApi."""

    if not API_KEY:
        st.error(
            "SerpApi API key is not configured. "
            "Please add SERPAPI_KEY to your environment."
        )
        return []

    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY,
        "num": 10
    }

    try:
        response = requests.get(
            "https://serpapi.com/search.json",
            params=params,
            timeout=20
        )

        data = response.json()

        if "error" in data:
            st.error(data["error"])
            return []

        return data.get("organic_results", [])

    except Exception as e:
        st.error(f"Search failed: {e}")
        return []


def calculate_match(title, snippet):
    """Simple profile-based relevance score."""

    text = (title + " " + snippet).lower()

    keywords = []

    keywords.extend(
        education.lower().split()
    )

    keywords.extend(
        skills.lower().replace(",", " ").split()
    )

    keywords.append(location.lower())
    keywords.append(opportunity_type.lower())

    matches = 0

    for word in keywords:
        if len(word) > 2 and word in text:
            matches += 1

    score = min(95, 40 + matches * 10)

    return score


if search_button:

    query = (
        f"{opportunity_type} for {education} students "
        f"{skills} {location} 2026"
    )

    st.info(f"Searching for: **{query}**")

    results = search_serpapi(query)

    if results:

        st.success(
            f"Found {len(results)} opportunities!"
        )

        for index, result in enumerate(results, start=1):

            title = result.get(
                "title",
                "Opportunity"
            )

            link = result.get(
                "link",
                "#"
            )

            snippet = result.get(
                "snippet",
                "No description available."
            )

            score = calculate_match(
                title,
                snippet
            )

            st.markdown("---")

            st.markdown(
                f"### {index}. {title}"
            )

            st.write(snippet)

            st.progress(
                score / 100,
                text=f"Profile Match: {score}%"
            )

            st.link_button(
                "🔗 View Opportunity",
                link
            )

    else:
        st.warning(
            "No opportunities found. "
            "Try changing your skills or opportunity type."
        )


st.markdown("---")

st.caption(
    "OpportunityAI | Built with Python, Streamlit and SerpApi"
                   )
