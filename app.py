import requests
import streamlit as st
import re

# ============================================================
#                    PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OpportunityAI",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
#                    CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 20px;
    color: #666;
    margin-bottom: 25px;
}

.card {
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #ddd;
    margin-bottom: 20px;
    background-color: #ffffff;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.card-title {
    font-size: 23px;
    font-weight: 650;
    margin-bottom: 12px;
}

.info {
    font-size: 15px;
    margin: 6px 0;
}

.match {
    font-size: 18px;
    font-weight: 600;
}

.ai-box {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-top: 12px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
#                    SESSION STATE
# ============================================================

if "saved_opportunities" not in st.session_state:
    st.session_state.saved_opportunities = []

if "search_results" not in st.session_state:
    st.session_state.search_results = []


# ============================================================
#                       HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 OpportunityAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Smart Student Opportunity Navigator'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "🔎 Discover internships, jobs, scholarships, "
    "hackathons, competitions and certifications "
    "based on your profile."
)


# ============================================================
#                       API KEY
# ============================================================

API_KEY = st.secrets.get("SERPAPI_KEY")


# ============================================================
#                       SIDEBAR
# ============================================================

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
        "Jobs",
        "Scholarships",
        "Hackathons",
        "Competitions",
        "Certifications"
    ]
)


search_button = st.sidebar.button(
    "🔎 Find Opportunities",
    use_container_width=True
)


# ============================================================
#                  SAVED COUNT
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader(
    "🔖 Saved Opportunities"
)

st.sidebar.write(
    f"Saved: **{len(st.session_state.saved_opportunities)}**"
)


# ============================================================
#                  SEARCH FUNCTION
# ============================================================

def search_serpapi(query):

    if not API_KEY:

        st.error(
            "SerpApi API key is not configured."
        )

        return []

    params = {

        "engine": "google",

        "q": query,

        "api_key": API_KEY,

        "safe": "active",

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

            st.error(
                data["error"]
            )

            return []


        return data.get(
            "organic_results",
            []
        )


    except Exception as e:

        st.error(
            f"Search failed: {e}"
        )

        return []


# ============================================================
#                       SEARCH
# ============================================================

if search_button:

    # --------------------------------------------------------
    # INTERNSHIPS
    # --------------------------------------------------------

    if opportunity_type == "Internships":

        query = (
            f"{skills} internship "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # --------------------------------------------------------
    # JOBS
    # --------------------------------------------------------

    elif opportunity_type == "Jobs":

        query = (
            f"{skills} fresher jobs "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # --------------------------------------------------------
    # SCHOLARSHIPS
    # --------------------------------------------------------

    elif opportunity_type == "Scholarships":

        query = (
            f"{education} scholarships "
            f"for students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # --------------------------------------------------------
    # HACKATHONS
    # --------------------------------------------------------

    elif opportunity_type == "Hackathons":

        query = (
            f"{skills} hackathons "
            f"for students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # --------------------------------------------------------
    # COMPETITIONS
    # --------------------------------------------------------

    elif opportunity_type == "Competitions":

        query = (
            f"{skills} competitions "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # --------------------------------------------------------
    # CERTIFICATIONS
    # --------------------------------------------------------

    else:

        query = (
            f"{skills} free certifications "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # --------------------------------------------------------
    # SHOW SEARCH QUERY
    # --------------------------------------------------------

    st.info(
        f"🔎 Searching for: **{query}**"
    )


    # --------------------------------------------------------
    # SEARCH SERPAPI
    # --------------------------------------------------------

    results = search_serpapi(
        query
    )


    # --------------------------------------------------------
    # STORE RAW RESULTS
    # --------------------------------------------------------

    if results:

        st.session_state.raw_results = results

        st.success(
            f"🎉 Found {len(results)} opportunities!"
        )

    else:

        st.session_state.raw_results = []

        st.warning(
            "No opportunities found. "
            "Try changing your skills or opportunity type."
        )
