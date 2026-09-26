import requests
import streamlit as st


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="OpportunityAI",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎓 OpportunityAI")
st.subheader("Smart Student Opportunity Navigator")

st.write(
    "Find internships, scholarships, hackathons, competitions, "
    "certifications, and jobs using live web search."
)


# --------------------------------------------------
# SERPAPI KEY
# --------------------------------------------------

API_KEY = st.secrets.get("SERPAPI_KEY")


# --------------------------------------------------
# STUDENT PROFILE
# --------------------------------------------------

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


# --------------------------------------------------
# SERPAPI SEARCH FUNCTION
# --------------------------------------------------

def search_serpapi(query):

    if not API_KEY:

        st.error(
            "SerpApi API key is not configured. "
            "Please add SERPAPI_KEY to Streamlit Secrets."
        )

        return []

    params = {
        "engine": "google",
        "q": query,
        "safe": "active",
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

        return data.get(
            "organic_results",
            []
        )

    except Exception as e:

        st.error(
            f"Search failed: {e}"
        )

        return []


# --------------------------------------------------
# PROFILE MATCH FUNCTION
# --------------------------------------------------

def calculate_match(title, snippet):

    text = (
        title + " " + snippet
    ).lower()

    keywords = []

    keywords.extend(
        education.lower().split()
    )

    keywords.extend(
        skills.lower()
        .replace(",", " ")
        .split()
    )

    keywords.append(
        location.lower()
    )

    keywords.append(
        opportunity_type.lower()
    )

    matches = 0

    for word in keywords:

        if len(word) > 2 and word in text:

            matches += 1

    score = min(
        95,
        40 + matches * 10
    )

    return score


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

if search_button:

    # Internship search
    if opportunity_type == "Internships":

        query = (
            f"{skills} internship "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )

    # Jobs search
    
      elif opportunity_type == "Jobs":

    query = (
        f"{skills} fresher jobs "
        f"{education} students "
        f"{location} 2026 "
        f"-site:linkedin.com "
        f"-site:youtube.com"
    )

    # Other opportunities
    else:

        query = (
            f"{opportunity_type} "
            f"for {education} students "
            f"{skills} "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # Show search query
    st.info(
        f"Searching for: **{query}**"
    )


    # Search SerpApi
    results = search_serpapi(query)


    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    if results:

        st.success(
            f"Found {len(results)} opportunities!"
        )


        for index, result in enumerate(
            results,
            start=1
        ):

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


            # Profile score
            score = calculate_match(
                title,
                snippet
            )


            # Organization
            organization = result.get(
                "source",
                "Not specified"
            )


            # Location
            location_text = result.get(
                "location",
                "Not specified"
            )


            # Deadline
            deadline = result.get(
                "deadline",
                "Not specified"
            )


            # --------------------------------------------------
            # DISPLAY RESULT
            # --------------------------------------------------

            st.markdown("---")

            st.subheader(
                f"{index}. {title}"
            )

            st.write(
                f"🏢 **Organization:** "
                f"{organization}"
            )

            st.write(
                f"📍 **Location:** "
                f"{location_text}"
            )

            st.write(
                f"📅 **Deadline:** "
                f"{deadline}"
            )

            st.write(
                f"⭐ **Profile Match:** "
                f"{score}%"
            )

            st.write(
                snippet
            )

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
            "Try changing your skills, "
            "location, or opportunity type."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "OpportunityAI | Built with Python, "
    "Streamlit and SerpApi"
)
