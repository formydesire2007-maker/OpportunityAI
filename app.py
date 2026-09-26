import requests
import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="OpportunityAI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

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

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

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


# ---------------- API KEY ----------------

API_KEY = st.secrets.get("SERPAPI_KEY")


# ---------------- SIDEBAR ----------------

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


# ---------------- SEARCH FUNCTION ----------------

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


# ---------------- MATCH SCORE ----------------

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

    matches = 0

    for word in keywords:

        if len(word) > 2 and word in text:
            matches += 1

    score = min(
        95,
        40 + matches * 10
    )

    return score


# ---------------- SEARCH ----------------

if search_button:

    # -------- QUERY TYPES --------

    if opportunity_type == "Internships":

        query = (
            f"{skills} internship "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )

    elif opportunity_type == "Jobs":

        query = (
            f"{skills} fresher jobs "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )

    elif opportunity_type == "Scholarships":

        query = (
            f"{education} scholarships "
            f"for students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )

    elif opportunity_type == "Hackathons":

        query = (
            f"{skills} hackathons "
            f"for students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )

    elif opportunity_type == "Competitions":

        query = (
            f"{skills} competitions "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )

    else:

        query = (
            f"{skills} free certifications "
            f"for {education} students "
            f"{location} 2026 "
            f"-site:linkedin.com "
            f"-site:youtube.com"
        )


    # -------- SEARCH INFO --------

    st.info(
        f"🔎 Searching for: **{query}**"
    )


    # -------- GET RESULTS --------

    results = search_serpapi(query)


    if results:

        st.success(
            f"🎉 Found {len(results)} opportunities!"
        )


        # -------- RESULT CARDS --------

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

            organization = result.get(
                "source",
                "Not specified"
            )

            location_text = result.get(
                "location",
                location
            )

            deadline = result.get(
                "deadline",
                "Check official website"
            )

            score = calculate_match(
                title,
                snippet
            )


            # -------- CARD --------

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )


            st.markdown(
                f'<div class="card-title">'
                f'{index}. {title}'
                f'</div>',
                unsafe_allow_html=True
            )


            st.markdown(
                f'<div class="info">'
                f'🏢 <b>Organization:</b> '
                f'{organization}'
                f'</div>',
                unsafe_allow_html=True
            )


            st.markdown(
                f'<div class="info">'
                f'📍 <b>Location:</b> '
                f'{location_text}'
                f'</div>',
                unsafe_allow_html=True
            )


            st.markdown(
                f'<div class="info">'
                f'📅 <b>Deadline:</b> '
                f'{deadline}'
                f'</div>',
                unsafe_allow_html=True
            )


            st.markdown(
                f'<div class="match">'
                f'⭐ Profile Match: {score}%'
                f'</div>',
                unsafe_allow_html=True
            )


            st.progress(
                score / 100
            )


            st.write(
                snippet
            )


            if link != "#":

                st.link_button(
                    "🔗 View Opportunity",
                    link
                )


            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    else:

        st.warning(
            "No opportunities found. "
            "Try changing your skills or location."
        )


# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "OpportunityAI | Python • Streamlit • SerpApi"
)
