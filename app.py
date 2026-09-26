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


# ---------------- SESSION STATE ----------------

if "saved_opportunities" not in st.session_state:
    st.session_state.saved_opportunities = []


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


# ---------------- SAVED SECTION ----------------

st.sidebar.markdown("---")

st.sidebar.subheader("🔖 Saved Opportunities")

saved_count = len(
    st.session_state.saved_opportunities
)

st.sidebar.write(
    f"You have saved **{saved_count}** opportunities."
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


# ---------------- SAVE FUNCTION ----------------

def save_opportunity(opportunity):

    existing_links = [
        item["link"]
        for item in st.session_state.saved_opportunities
    ]

    if opportunity["link"] not in existing_links:

        st.session_state.saved_opportunities.append(
            opportunity
        )

        st.toast(
            "🔖 Opportunity saved!"
        )

    else:

        st.toast(
            "Already saved!"
        )


# ---------------- REMOVE FUNCTION ----------------

def remove_opportunity(link):

    st.session_state.saved_opportunities = [
        item
        for item in st.session_state.saved_opportunities
        if item["link"] != link
    ]

    st.toast(
        "Opportunity removed."
    )


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


            opportunity = {
                "title": title,
                "link": link,
                "snippet": snippet,
                "organization": organization,
                "location": location_text,
                "deadline": deadline,
                "score": score
            }


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


            # -------- BUTTONS --------

            col1, col2 = st.columns(2)


            with col1:

                if link != "#":

                    st.link_button(
                        "🔗 View Opportunity",
                        link,
                        use_container_width=True
                    )


            with col2:

                st.button(
                    "🔖 Save Opportunity",
                    key=f"save_{index}_{link}",
                    on_click=save_opportunity,
                    args=(opportunity,),
                    use_container_width=True
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


# ---------------- SAVED OPPORTUNITIES ----------------

if st.session_state.saved_opportunities:

    st.markdown("---")

    st.header("🔖 Saved Opportunities")

    st.write(
        "Your bookmarked opportunities are shown below."
    )


    for index, item in enumerate(
        st.session_state.saved_opportunities,
        start=1
    ):

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader(
            f"{index}. {item['title']}"
        )

        st.write(
            f"🏢 **Organization:** "
            f"{item['organization']}"
        )

        st.write(
            f"📍 **Location:** "
            f"{item['location']}"
        )

        st.write(
            f"⭐ **Profile Match:** "
            f"{item['score']}%"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "🔗 Open Opportunity",
                item["link"],
                use_container_width=True
            )

        with col2:

            st.button(
                "❌ Remove",
                key=f"remove_{index}",
                on_click=remove_opportunity,
                args=(item["link"],),
                use_container_width=True
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "OpportunityAI | Python • Streamlit • SerpApi"
)
