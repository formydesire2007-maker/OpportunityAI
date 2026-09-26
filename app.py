import requests
import streamlit as st


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="OpportunityAI",
    page_icon="🎓",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title("🎓 OpportunityAI")
st.subheader("Smart Student Opportunity Navigator")

st.write(
    "Find internships, jobs, scholarships, hackathons, "
    "competitions, and certifications using live web search."
)


# ==================================================
# SERPAPI API KEY
# ==================================================

API_KEY = st.secrets.get("SERPAPI_KEY")


# ==================================================
# STUDENT PROFILE
# ==================================================

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

search_button = st.button(
    "🔎 Find Opportunities"
)


# ==================================================
# SERPAPI SEARCH FUNCTION
# ==================================================

def search_serpapi(query):

    if not API_KEY:

        st.error(
            "SerpApi API key is not configured. "
            "Please add SERPAPI_KEY in Streamlit Secrets."
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


# ==================================================
# PROFILE MATCH FUNCTION
# ==================================================

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


# ==================================================
# SEARCH BUTTON
# ==================================================

if search_button:

    # ------------------------------------------------
    # INTERNSHIPS
    # ------------------------------------------------

    if opportunity_type == "Internships":

        query = (
            f"{skills} internship "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # ------------------------------------------------
    # JOBS
    # ------------------------------------------------

    elif opportunity_type == "Jobs":

        query = (
            f"{skills} fresher jobs "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # ------------------------------------------------
    # SCHOLARSHIPS
    # ------------------------------------------------

    elif opportunity_type == "Scholarships":

        query = (
            f"{education} scholarships "
            f"for students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # ------------------------------------------------
    # HACKATHONS
    # ------------------------------------------------

    elif opportunity_type == "Hackathons":

        query = (
            f"{skills} hackathons "
            f"for students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # ------------------------------------------------
    # COMPETITIONS
    # ------------------------------------------------

    elif opportunity_type == "Competitions":

        query = (
            f"{skills} competitions "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # ------------------------------------------------
    # CERTIFICATIONS
    # ------------------------------------------------

    else:

        query = (
            f"{skills} free certifications "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # ==================================================
    # SHOW SEARCH QUERY
    # ==================================================

    st.info(
        f"Searching for: **{query}**"
    )


    # ==================================================
    # GET RESULTS
    # ==================================================

    results = search_serpapi(
        query
    )


    # ==================================================
    # DISPLAY RESULTS
    # ==================================================

    if results:

        st.success(
            f"Found {len(results)} opportunities!"
        )


        for index, result in enumerate(
            results,
            start=1
        ):

            # ------------------------------------------
            # TITLE
            # ------------------------------------------

            title = result.get(
                "title",
                "Opportunity"
            )


            # ------------------------------------------
            # LINK
            # ------------------------------------------

            link = result.get(
                "link",
                "#"
            )


            # ------------------------------------------
            # DESCRIPTION
            # ------------------------------------------

            snippet = result.get(
                "snippet",
                "No description available."
            )


            # ------------------------------------------
            # ORGANIZATION
            # ------------------------------------------

            organization = result.get(
                "source",
                "Not specified"
            )


            # ------------------------------------------
            # LOCATION
            # ------------------------------------------

            location_text = result.get(
                "location",
                location
            )


            # ------------------------------------------
            # DEADLINE
            # ------------------------------------------

            deadline = result.get(
                "deadline",
                "Check official website"
            )


            # ------------------------------------------
            # PROFILE MATCH
            # ------------------------------------------

            score = calculate_match(
                title,
                snippet
            )


            # ------------------------------------------
            # RESULT CARD
            # ------------------------------------------

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

            if link != "#":

                st.link_button(
                    "🔗 View Opportunity",
                    link
                )


    # ==================================================
    # NO RESULTS
    # ==================================================

    else:

        st.warning(
            "No opportunities found. "
            "Try changing your skills or location."
        )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "OpportunityAI | Built with Python, "
    "Streamlit and SerpApi"
)
