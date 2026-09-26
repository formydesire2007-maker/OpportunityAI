import requests
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OpportunityAI",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f8f9ff, #eef7ff);
}

.main-title {
    font-size: 46px;
    font-weight: 800;
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.subtitle {
    font-size: 19px;
    color: #666;
    margin-bottom: 20px;
}

.hero-box {
    padding: 42px;
    border-radius: 25px;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    box-shadow: 0 10px 30px rgba(60, 80, 180, 0.25);
    margin-top: 20px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 12px;
}

.hero-text {
    font-size: 18px;
    line-height: 1.7;
}

.feature-box {
    padding: 22px;
    border-radius: 18px;
    background: white;
    border: 1px solid #e5e7eb;
    text-align: center;
    box-shadow: 0 5px 18px rgba(0,0,0,0.07);
    min-height: 125px;
}

.feature-icon {
    font-size: 30px;
}

.feature-title {
    font-size: 17px;
    font-weight: 700;
}

.card {
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #ddd;
    margin-bottom: 20px;
    background-color: white;
    box-shadow: 0 5px 18px rgba(0,0,0,0.07);
}

.card-title {
    font-size: 23px;
    font-weight: 700;
    margin-bottom: 12px;
}

.info {
    font-size: 15px;
    margin: 7px 0;
}

.match {
    font-size: 19px;
    font-weight: 700;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    margin-top: 20px;
}

.small-text {
    color: #666;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "saved_opportunities" not in st.session_state:
    st.session_state.saved_opportunities = []

if "search_results" not in st.session_state:
    st.session_state.search_results = []


# ============================================================
# API KEY
# ============================================================

API_KEY = st.secrets.get("SERPAPI_KEY")


# ============================================================
# FUNCTIONS
# ============================================================

def search_serpapi(query):

    if not API_KEY:
        st.error("SerpApi API key is not configured.")
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

        return data.get("organic_results", [])

    except Exception as e:

        st.error(f"Search failed: {e}")
        return []


# ============================================================
# SKILL DATABASE
# ============================================================

def extract_skills(text):

    text = text.lower()

    skill_database = [
        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "html",
        "css",
        "sql",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "ai",
        "ml",
        "data science",
        "data analysis",
        "tensorflow",
        "pytorch",
        "flask",
        "django",
        "react",
        "node.js",
        "git",
        "github",
        "aws",
        "azure",
        "cloud",
        "docker",
        "kubernetes",
        "mongodb",
        "mysql",
        "excel",
        "power bi",
        "tableau",
        "nlp",
        "computer vision",
        "opencv",
        "android",
        "flutter"
    ]

    found_skills = []

    for skill in skill_database:

        if skill in text and skill not in found_skills:
            found_skills.append(skill)

    return found_skills


# ============================================================
# SMART SKILL MATCHING
# ============================================================

def smart_skill_matching(student_skills, opportunity_text):

    student_skills_list = [
        skill.strip().lower()
        for skill in student_skills.split(",")
        if skill.strip()
    ]

    required_skills = extract_skills(opportunity_text)

    matching_skills = []

    for student_skill in student_skills_list:

        for required_skill in required_skills:

            if (
                student_skill == required_skill
                or student_skill in required_skill
                or required_skill in student_skill
            ):

                if required_skill not in matching_skills:
                    matching_skills.append(required_skill)

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in matching_skills
    ]

    if required_skills:

        score = int(
            len(matching_skills) /
            len(required_skills) * 100
        )

    else:

        score = 50

    score = max(0, min(score, 100))

    return matching_skills, missing_skills, score


# ============================================================
# AI EXPLANATION
# ============================================================

def generate_ai_explanation(
    matching_skills,
    missing_skills,
    score
):

    if matching_skills:

        explanation = (
            "This opportunity matches your profile because "
            "you have skills in "
            + ", ".join(matching_skills)
            + "."
        )

    else:

        explanation = (
            "No direct technical skill match was detected "
            "from the available description."
        )

    if missing_skills:

        explanation += (
            " You can improve your profile by learning "
            + ", ".join(missing_skills[:3])
            + "."
        )

    if score >= 80:

        explanation += (
            " Your current skills show a strong technical match."
        )

    elif score >= 50:

        explanation += (
            " Your profile has a partial skill match."
        )

    else:

        explanation += (
            " This opportunity may require additional skills."
        )

    return explanation


# ============================================================
# SKILL GAP SUGGESTIONS
# ============================================================

def get_skill_gap_suggestions(missing_skills):

    learning_map = {

        "python":
            "Practice Python basics, OOP and projects.",

        "java":
            "Learn Java OOP, collections and DSA.",

        "c":
            "Practice C arrays, pointers and functions.",

        "c++":
            "Learn C++ OOP, STL and problem solving.",

        "javascript":
            "Learn JavaScript, DOM and ES6.",

        "html":
            "Learn HTML5, forms and semantic elements.",

        "css":
            "Practice CSS, Flexbox and responsive design.",

        "sql":
            "Practice SQL queries, joins and databases.",

        "machine learning":
            "Learn ML algorithms and model evaluation.",

        "deep learning":
            "Learn neural networks and CNNs.",

        "artificial intelligence":
            "Learn AI fundamentals and practical projects.",

        "ai":
            "Learn AI fundamentals and build small projects.",

        "ml":
            "Practice machine learning with datasets.",

        "data science":
            "Learn Python, statistics and data visualization.",

        "data analysis":
            "Practice Pandas, NumPy and visualization.",

        "tensorflow":
            "Learn TensorFlow model building.",

        "pytorch":
            "Practice PyTorch models and training.",

        "flask":
            "Learn Flask routing, APIs and deployment.",

        "django":
            "Learn Django models, views and APIs.",

        "react":
            "Learn React components, props and hooks.",

        "node.js":
            "Learn Node.js and Express APIs.",

        "git":
            "Practice Git commands, branches and commits.",

        "github":
            "Learn repositories, branches and pull requests.",

        "aws":
            "Learn AWS basics such as EC2 and S3.",

        "azure":
            "Learn Azure cloud fundamentals.",

        "cloud":
            "Learn cloud computing and deployment.",

        "docker":
            "Learn Docker images and containers.",

        "kubernetes":
            "Learn Kubernetes pods and deployments.",

        "mongodb":
            "Learn MongoDB CRUD operations.",

        "mysql":
            "Practice MySQL queries and joins.",

        "excel":
            "Learn Excel formulas and data analysis.",

        "power bi":
            "Learn Power BI dashboards.",

        "tableau":
            "Practice Tableau visualization.",

        "nlp":
            "Learn text preprocessing and NLP models.",

        "computer vision":
            "Learn image processing and CNNs.",

        "opencv":
            "Practice OpenCV image processing.",

        "android":
            "Learn Android activities and layouts.",

        "flutter":
            "Learn Flutter widgets and Dart."
    }

    suggestions = []

    for skill in missing_skills:

        if skill in learning_map:
            suggestions.append(learning_map[skill])

        else:
            suggestions.append(
                f"Learn the fundamentals of {skill}."
            )

    return suggestions


# ============================================================
# SAVE / REMOVE
# ============================================================

def save_opportunity(opportunity):

    existing_links = [
        item["link"]
        for item in st.session_state.saved_opportunities
    ]

    if opportunity["link"] not in existing_links:

        st.session_state.saved_opportunities.append(
            opportunity
        )

        st.toast("🔖 Opportunity saved!")

    else:

        st.toast("Already saved!")


def remove_opportunity(link):

    st.session_state.saved_opportunities = [
        item
        for item in st.session_state.saved_opportunities
        if item["link"] != link
    ]

    st.toast("Opportunity removed.")


# ============================================================
# HEADER
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


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    hero_col1, hero_col2 = st.columns(
        [1.2, 1],
        vertical_alignment="center"
    )

    with hero_col1:

        st.markdown("""
        <div class="hero-box">

            <div class="hero-title">
                🚀 Find Your Next Opportunity
            </div>

            <div class="hero-text">
                Discover internships, jobs, scholarships,
                hackathons, competitions and certifications
                based on your education, skills and location.
            </div>

            <br>

            <div class="hero-text">
                🤖 AI Skill Matching &nbsp; • &nbsp;
                🎯 AI Match Score &nbsp; • &nbsp;
                📚 Skill Gap Suggestions
            </div>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "🚀 FIND OPPORTUNITIES",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.page = "search"
            st.rerun()

    with hero_col2:

        st.image(
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=85",
            use_container_width=True
        )

    st.markdown(
        '<h2 class="section-title">✨ Everything You Need in One Place</h2>',
        unsafe_allow_html=True
    )

    st.write(
        "OpportunityAI helps students discover relevant opportunities "
        "without searching multiple websites."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎓</div>
            <div class="feature-title">Student Profile</div>
            Education & Skills
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🔎</div>
            <div class="feature-title">Smart Search</div>
            Powered by SerpApi
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Matching</div>
            Smart Match Score
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Skill Gap</div>
            Improve Your Skills
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        "<h3>💡 How OpportunityAI Works</h3>",
        unsafe_allow_html=True
    )

    step1, step2, step3 = st.columns(3)

    with step1:
        st.info(
            "1️⃣ **Enter Profile**\n\n"
            "Add your education, skills and location."
        )

    with step2:
        st.info(
            "2️⃣ **Search Opportunities**\n\n"
            "SerpApi searches relevant opportunities."
        )

    with step3:
        st.info(
            "3️⃣ **Get AI Matching**\n\n"
            "See match score, missing skills and suggestions."
        )

    st.markdown("---")

    st.caption(
        "OpportunityAI | Python • Streamlit • SerpApi • "
        "AI Smart Matching"
    )


# ============================================================
# SEARCH PAGE
# ============================================================

else:

    top_col1, top_col2 = st.columns([5, 1])

    with top_col1:

        st.markdown(
            '<h2 class="section-title">🔎 Find Opportunities</h2>',
            unsafe_allow_html=True
        )

        st.write(
            "Enter your profile details and discover opportunities "
            "matched to your skills."
        )

    with top_col2:

        if st.button(
            "🏠 Home",
            use_container_width=True
        ):

            st.session_state.page = "home"
            st.rerun()

    # ========================================================
    # SIDEBAR
    # ========================================================

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
        use_container_width=True,
        type="primary"
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader(
        "🔖 Saved Opportunities"
    )

    st.sidebar.write(
        f"Saved: **{len(st.session_state.saved_opportunities)}**"
    )

    # ========================================================
    # SEARCH
    # ========================================================

    if search_button:

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

        st.info(
            f"🔎 Searching for: **{query}**"
        )

        results = search_serpapi(query)

        if results:

            formatted_results = []

            for result in results:

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

                opportunity_text = (
                    title + " " + snippet
                )

                (
                    matching_skills,
                    missing_skills,
                    ai_score
                ) = smart_skill_matching(
                    skills,
                    opportunity_text
                )

                ai_explanation = generate_ai_explanation(
                    matching_skills,
                    missing_skills,
                    ai_score
                )

                skill_gap_suggestions = (
                    get_skill_gap_suggestions(
                        missing_skills
                    )
                )

                opportunity = {

                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "organization": organization,
                    "location": location_text,
                    "deadline": deadline,
                    "score": ai_score,
                    "matching_skills": matching_skills,
                    "missing_skills": missing_skills,
                    "ai_explanation": ai_explanation,
                    "skill_gap_suggestions": skill_gap_suggestions,
                    "type": opportunity_type
                }

                formatted_results.append(
                    opportunity
                )

            st.session_state.search_results = (
                formatted_results
            )

            st.success(
                f"🎉 Found {len(formatted_results)} opportunities!"
            )

        else:

            st.session_state.search_results = []

            st.warning(
                "No opportunities found. "
                "Try changing your skills or opportunity type."
            )

    # ========================================================
    # DASHBOARD
    # ========================================================

    if st.session_state.search_results:

        results = st.session_state.search_results

        total_opportunities = len(results)

        saved_count = len(
            st.session_state.saved_opportunities
        )

        average_match = int(
            sum(
                item["score"]
                for item in results
            ) / total_opportunities
        )

        st.markdown("---")

        st.markdown(
            '<h2 class="section-title">📊 Student Dashboard</h2>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎯 Opportunities Found",
                total_opportunities
            )

        with col2:

            st.metric(
                "🔖 Saved",
                saved_count
            )

        with col3:

            st.metric(
                "🤖 Average AI Match",
                f"{average_match}%"
            )

        # ====================================================
        # TOP RECOMMENDATIONS
        # ====================================================

        st.markdown("---")

        st.subheader(
            "🌟 Top Recommended Opportunities"
        )

        st.write(
            "AI-powered recommendations based on your skills."
        )

        recommended_results = sorted(
            results,
            key=lambda item: item["score"],
            reverse=True
        )

        top_results = recommended_results[:3]

        for rank, item in enumerate(
            top_results,
            start=1
        ):

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="card-title">'
                f'🏆 #{rank} {item["title"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.write(
                f"🏢 **Organization:** "
                f"{item['organization']}"
            )

            st.write(
                f"🤖 **AI Match Score:** "
                f"{item['score']}%"
            )

            st.progress(
                item["score"] / 100
            )

            if item["matching_skills"]:

                st.success(
                    "✅ Matching Skills: "
                    + ", ".join(
                        item["matching_skills"]
                    )
                )

            if item["missing_skills"]:

                st.warning(
                    "📚 Skills to Improve: "
                    + ", ".join(
                        item["missing_skills"]
                    )
                )

            if item["link"] != "#":

                st.link_button(
                    "🔗 View Opportunity",
                    item["link"],
                    use_container_width=True
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        # ====================================================
        # FILTERS
        # ====================================================

        st.markdown("---")

        st.subheader(
            "🔎 Filter Opportunities"
        )

        col1, col2 = st.columns(2)

        with col1:

            search_text = st.text_input(
                "Search by keyword",
                placeholder="Example: Python, AI, internship..."
            )

        with col2:

            minimum_match = st.slider(
                "Minimum AI Match",
                0,
                100,
                0,
                5
            )

        filtered_results = []

        for item in results:

            searchable_text = (
                item["title"]
                + " "
                + item["snippet"]
                + " "
                + item["organization"]
            )

            keyword_match = (
                search_text.lower()
                in searchable_text.lower()
            )

            score_match = (
                item["score"] >= minimum_match
            )

            if keyword_match and score_match:

                filtered_results.append(item)

        st.write(
            f"Showing **{len(filtered_results)}** opportunities."
        )

        # ====================================================
        # AVAILABLE OPPORTUNITIES
        # ====================================================

        st.markdown("---")

        st.subheader(
            "🎯 Available Opportunities"
        )

        for index, item in enumerate(
            filtered_results,
            start=1
        ):

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="card-title">'
                f'{index}. {item["title"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="info">'
                f'🏢 <b>Organization:</b> '
                f'{item["organization"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="info">'
                f'📍 <b>Location:</b> '
                f'{item["location"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="info">'
                f'📅 <b>Deadline:</b> '
                f'{item["deadline"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="match">'
                f'🤖 AI Match Score: '
                f'{item["score"]}%'
                f'</div>',
                unsafe_allow_html=True
            )

            st.progress(
                item["score"] / 100
            )

            if item["matching_skills"]:

                st.success(
                    "✅ Matching Skills: "
                    + ", ".join(
                        item["matching_skills"]
                    )
                )

            else:

                st.info(
                    "ℹ️ No direct matching skills detected."
                )

            if item["missing_skills"]:

                st.warning(
                    "❌ Missing Skills: "
                    + ", ".join(
                        item["missing_skills"]
                    )
                )

            else:

                st.success(
                    "🎉 No major missing skills detected!"
                )

            st.info(
                "💡 **Why this matches you:**\n\n"
                + item["ai_explanation"]
            )

            if item["skill_gap_suggestions"]:

                with st.expander(
                    "📚 View Skill Gap Suggestions"
                ):

                    for suggestion in item[
                        "skill_gap_suggestions"
                    ]:

                        st.write(
                            "• " + suggestion
                        )

            st.write(
                item["snippet"]
            )

            col1, col2 = st.columns(2)

            with col1:

                if item["link"] != "#":

                    st.link_button(
                        "🔗 View Opportunity",
                        item["link"],
                        use_container_width=True
                    )

            with col2:

                st.button(
                    "🔖 Save Opportunity",
                    key=f"save_{index}_{item['link']}",
                    on_click=save_opportunity,
                    args=(item,),
                    use_container_width=True
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# ============================================================
# SAVED OPPORTUNITIES
# ============================================================

if st.session_state.saved_opportunities:

    st.markdown("---")

    st.header(
        "🔖 Saved Opportunities"
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
            f"🤖 **AI Match Score:** "
            f"{item['score']}%"
        )

        st.progress(
            item["score"] / 100
        )

        if item.get("matching_skills"):

            st.write(
                "✅ **Matching Skills:** "
                + ", ".join(
                    item["matching_skills"]
                )
            )

        if item.get("missing_skills"):

            st.write(
                "❌ **Missing Skills:** "
                + ", ".join(
                    item["missing_skills"]
                )
            )

        if item.get("ai_explanation"):

            st.info(
                "💡 " + item["ai_explanation"]
            )

        col1, col2 = st.columns(2)

        with col1:

            if item["link"] != "#":

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


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎓 OpportunityAI | Python • Streamlit • SerpApi • "
    "AI Smart Matching • Skill Gap Analysis"
)
