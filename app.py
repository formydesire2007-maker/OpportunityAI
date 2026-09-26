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
        # ============================================================
#                  AI SMART SKILL MATCHING
# ============================================================

def extract_skills(text):

    """
    Detect commonly used technical skills
    from opportunity title and description.
    """

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

        if skill in text:

            if skill not in found_skills:

                found_skills.append(
                    skill
                )

    return found_skills


# ============================================================
#                    SMART MATCHING
# ============================================================

def smart_skill_matching(
    student_skills,
    opportunity_text
):

    # --------------------------------------------------------
    # STUDENT SKILLS
    # --------------------------------------------------------

    student_skills_list = [

        skill.strip().lower()

        for skill in student_skills.split(",")

        if skill.strip()
    ]


    # --------------------------------------------------------
    # OPPORTUNITY REQUIRED SKILLS
    # --------------------------------------------------------

    required_skills = extract_skills(
        opportunity_text
    )


    # --------------------------------------------------------
    # MATCHING SKILLS
    # --------------------------------------------------------

    matching_skills = []

    for student_skill in student_skills_list:

        for required_skill in required_skills:

            student_clean = (
                student_skill.lower()
            )

            required_clean = (
                required_skill.lower()
            )


            if (
                student_clean == required_clean
                or student_clean in required_clean
                or required_clean in student_clean
            ):

                if required_skill not in matching_skills:

                    matching_skills.append(
                        required_skill
                    )


    # --------------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------------

    missing_skills = [

        skill

        for skill in required_skills

        if skill not in matching_skills
    ]


    # --------------------------------------------------------
    # AI MATCH SCORE
    # --------------------------------------------------------

    if len(required_skills) > 0:

        skill_score = (

            len(matching_skills)
            /
            len(required_skills)

        ) * 100

        score = int(
            skill_score
        )

    else:

        # No technical skills detected
        score = 50


    # Keep score between 0 and 100

    score = max(
        0,
        min(
            score,
            100
        )
    )


    return (
        matching_skills,
        missing_skills,
        score
    )


# ============================================================
#                AI EXPLANATION
# ============================================================

def generate_ai_explanation(
    matching_skills,
    missing_skills,
    score
):

    # --------------------------------------------------------
    # MATCHING EXPLANATION
    # --------------------------------------------------------

    if matching_skills:

        explanation = (

            "This opportunity matches your profile "
            "because you have experience or skills in "
            + ", ".join(matching_skills)
            + "."
        )

    else:

        explanation = (

            "No direct technical skill match was detected "
            "from the available opportunity description."
        )


    # --------------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------------

    if missing_skills:

        explanation += (

            " To improve your fit, consider learning "
            + ", ".join(
                missing_skills[:3]
            )
            + "."
        )


    # --------------------------------------------------------
    # SCORE EXPLANATION
    # --------------------------------------------------------

    if score >= 80:

        explanation += (

            " Your current skills show a strong "
            "technical match for this opportunity."
        )

    elif score >= 50:

        explanation += (

            " Your profile has a partial skill match, "
            "so learning the missing skills can improve "
            "your preparation."
        )

    else:

        explanation += (

            " This opportunity may require additional "
            "skills before you apply."
        )


    return explanation


# ============================================================
#                 SKILL GAP SUGGESTIONS
# ============================================================

def get_skill_gap_suggestions(
    missing_skills
):

    skill_learning_map = {

        "python":
            "Practice Python basics, functions, OOP and projects.",

        "java":
            "Learn Java OOP, collections, exception handling and DSA.",

        "c":
            "Practice C programming, arrays, pointers and functions.",

        "c++":
            "Learn C++ OOP, STL and competitive programming basics.",

        "javascript":
            "Learn JavaScript basics, DOM and modern ES6 concepts.",

        "html":
            "Learn HTML5 structure, forms and semantic elements.",

        "css":
            "Practice CSS layouts, Flexbox, Grid and responsive design.",

        "sql":
            "Practice SQL queries, joins, grouping and database design.",

        "machine learning":
            "Learn supervised learning, preprocessing and model evaluation.",

        "deep learning":
            "Learn neural networks, CNNs and model training.",

        "artificial intelligence":
            "Study AI fundamentals, search, reasoning and machine learning.",

        "ai":
            "Learn AI fundamentals and build small AI projects.",

        "ml":
            "Practice machine learning algorithms with real datasets.",

        "data science":
            "Learn Python, statistics, data preprocessing and visualization.",

        "data analysis":
            "Practice Pandas, NumPy, Excel and data visualization.",

        "tensorflow":
            "Learn TensorFlow model building and neural network training.",

        "pytorch":
            "Practice PyTorch tensors, models and training workflows.",

        "flask":
            "Learn Flask routing, APIs, templates and deployment.",

        "django":
            "Learn Django models, views, URLs and REST APIs.",

        "react":
            "Learn React components, props, state and hooks.",

        "node.js":
            "Learn Node.js, Express and backend API development.",

        "git":
            "Practice Git commands, branches, commits and merging.",

        "github":
            "Learn GitHub repositories, branches, issues and pull requests.",

        "aws":
            "Learn AWS cloud basics, EC2, S3 and IAM.",

        "azure":
            "Learn Azure cloud services and deployment basics.",

        "cloud":
            "Learn cloud computing, deployment and basic cloud services.",

        "docker":
            "Learn Docker images, containers and Dockerfiles.",

        "kubernetes":
            "Learn Kubernetes pods, deployments and services.",

        "mongodb":
            "Learn MongoDB collections, documents and CRUD operations.",

        "mysql":
            "Practice MySQL databases, queries and joins.",

        "excel":
            "Learn Excel formulas, charts, filters and data analysis.",

        "power bi":
            "Learn Power BI dashboards, data modeling and visualization.",

        "tableau":
            "Practice Tableau dashboards and data visualization.",

        "nlp":
            "Learn text preprocessing, embeddings and NLP models.",

        "computer vision":
            "Learn image processing, CNNs and computer vision projects.",

        "opencv":
            "Practice OpenCV image processing and computer vision.",

        "android":
            "Learn Android development, activities, layouts and APIs.",

        "flutter":
            "Learn Flutter widgets, Dart and mobile app development."
    }


    suggestions = []

    for skill in missing_skills:

        if skill in skill_learning_map:

            suggestions.append(
                skill_learning_map[skill]
            )

        else:

            suggestions.append(
                f"Learn the fundamentals of {skill} "
                "and build a small practical project."
            )


    return suggestions


# ============================================================
#                SAVE OPPORTUNITY
# ============================================================

def save_opportunity(
    opportunity
):

    existing_links = [

        item["link"]

        for item
        in st.session_state.saved_opportunities
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


# ============================================================
#                REMOVE OPPORTUNITY
# ============================================================

def remove_opportunity(
    link
):

    st.session_state.saved_opportunities = [

        item

        for item
        in st.session_state.saved_opportunities

        if item["link"] != link
    ]


    st.toast(
        "Opportunity removed."
    )


# ============================================================
#             FORMAT SEARCH RESULTS
# ============================================================

if search_button and st.session_state.get(
    "raw_results"
):

    formatted_results = []


    for result in st.session_state.raw_results:

        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # COMBINE TEXT FOR AI ANALYSIS
        # ----------------------------------------------------

        opportunity_text = (

            title
            + " "
            + snippet
        )


        # ----------------------------------------------------
        # AI SMART MATCHING
        # ----------------------------------------------------

        (
            matching_skills,
            missing_skills,
            ai_score
        ) = smart_skill_matching(

            skills,

            opportunity_text
        )


        # ----------------------------------------------------
        # AI EXPLANATION
        # ----------------------------------------------------

        ai_explanation = generate_ai_explanation(

            matching_skills,

            missing_skills,

            ai_score
        )


        # ----------------------------------------------------
        # SKILL GAP SUGGESTIONS
        # ----------------------------------------------------

        skill_gap_suggestions = get_skill_gap_suggestions(

            missing_skills
        )


        # ----------------------------------------------------
        # CREATE OPPORTUNITY OBJECT
        # ----------------------------------------------------

        opportunity = {

            "title":
                title,

            "link":
                link,

            "snippet":
                snippet,

            "organization":
                organization,

            "location":
                location_text,

            "deadline":
                deadline,

            "score":
                ai_score,

            "matching_skills":
                matching_skills,

            "missing_skills":
                missing_skills,

            "ai_explanation":
                ai_explanation,

            "skill_gap_suggestions":
                skill_gap_suggestions,

            "type":
                opportunity_type
        }


        formatted_results.append(
            opportunity
        )


    # --------------------------------------------------------
    # STORE FINAL RESULTS
    # --------------------------------------------------------

    st.session_state.search_results = (
        formatted_results
    )
