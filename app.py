import streamlit as st
from agents import RecruitmentSystem, Candidate
import pandas as pd

st.set_page_config(page_title="AI Recruitment Agent System", layout="wide")

st.markdown("""
    <style>
    .agent-box { padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 20px; background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 AI Multi-Agent Recruitment Pipeline")
st.markdown("An automated end-to-end system for requirement extraction, sourcing, filtering, and submittal.")

if 'rec_sys' not in st.session_state:
    st.session_state.rec_sys = RecruitmentSystem()
if 'pipeline_results' not in st.session_state:
    st.session_state.pipeline_results = {}

# --- SIDEBAR ---
st.sidebar.header("⚙️ System Configuration")
jd_input = st.sidebar.text_area(
    "Job Description (JD)", 
    "Looking for a Senior Python Developer with 5+ years of experience in FastAPI, React, and AWS. Budget is 150k. Must be US Citizen or Green Card holder.",
    height=200
)

source_option = st.sidebar.selectbox(
    "Candidate Source",
    ("Web Scraping (AI Search)", "Manual Upload (CSV)", "Internal Mock Database")
)

uploaded_file = None
if source_option == "Manual Upload (CSV)":
    uploaded_file = st.sidebar.file_uploader("Upload Candidates CSV", type=["csv"])

if st.sidebar.button("🚀 Execute Pipeline"):
    with st.status("Agent Coordination in Progress...", expanded=True) as status:
        st.write("🤖 **Agent 1: Extracting Requirements...**")
        reqs = st.session_state.rec_sys.agent_extract_requirements(jd_input)
        st.session_state.pipeline_results['reqs'] = reqs
        st.markdown(f"✅ **Extracted:** Skills: `{reqs.skills}`, Exp: `{reqs.min_experience}+ yrs`")

        st.write("🤖 **Agent 2: Generating Sourcing Strings...**")
        bool_str = st.session_state.rec_sys.agent_generate_booleans(reqs)
        st.session_state.pipeline_results['boolean'] = bool_str
        st.markdown(f"✅ **Boolean String:** `{bool_str}`")

        st.write("🤖 **Agent 2.5: Gathering Candidates...**")
        candidates_to_process = []
        if source_option == "Web Scraping (AI Search)":
            candidates_to_process = st.session_state.rec_sys.scraper.search_candidates(bool_str)
            st.write(f"🌐 Scraped {len(candidates_to_process)} candidates from the web.")
        elif source_option == "Manual Upload (CSV)":
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                candidates_to_process = df.to_dict('records')
                st.write(f"📁 Processed {len(candidates_to_process)} candidates from CSV.")
            else:
                st.error("Please upload a CSV file!")
        else:
            candidates_to_process = [
                {"name": "Alice Smith", "email": "alice@example.com", "phone": "123-456", "resume_text": "Expert in Python, FastAPI, React, and AWS with 10 years exp.", "experience": 10, "visa_status": "US Citizen", "budget": 120000},
                {"name": "Bob Jones", "email": "bob@example.com", "phone": "789-012", "resume_text": "Senior Python Developer with 7 years exp. Proficient in FastAPI.", "experience": 7, "visa_status": "Green Card", "budget": 130000},
            ]
            st.write(f"📦 Loaded {len(candidates_to_process)} internal candidates.")

        st.write("🤖 **Agent 3: Filtering & Scoring...**")
        filtered = st.session_state.rec_sys.agent_filter_and_score(candidates_to_process)
        st.session_state.pipeline_results['filtered'] = filtered
        if filtered:
            st.table([{"Name": c.name, "Score": f"{c.score:.2f}", "Visa": c.visa_status} for c in filtered])
        else:
            st.warning("No candidates passed the filters.")

        st.write("🤖 **Agent 4: Outreach & Negotiation...**")
        confirmed = st.session_state.rec_sys.agent_outreach_negotiate(filtered)
        st.session_state.pipeline_results['confirmed'] = confirmed
        
        st.write("🤖 **Agent 5: Preparing Final Submittals...**")
        proposals = st.session_state.rec_sys.agent_submit_proposal(confirmed)
        st.session_state.pipeline_results['proposals'] = proposals
        
        status.update(label="Pipeline Execution Complete!", state="complete", expanded=False)

if 'pipeline_results' in st.session_state and st.session_state.pipeline_results:
    res = st.session_state.pipeline_results
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Requirements & Sourcing")
        st.info(f"**Target Skills:** {', '.join(res['reqs'].skills)}")
        st.code(res['boolean'], language="text")
    with col2:
        st.subheader("🏆 Ranked Candidates")
        if res['filtered']:
            st.dataframe([{"Name": c.name, "Score": c.score, "Status": c.status} for c in res['filtered']])
        else:
            st.warning("No candidates passed the filters.")
    st.divider()
    st.subheader("📄 Final Submittal Proposals")
    if res['proposals']:
        for p in res['proposals']:
            st.text_area("Proposal Package", p, height=200)
    else:
        st.error("No candidates were successfully negotiated for submittal.")
