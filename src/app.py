import streamlit as st
from agents import RecruitmentSystem, Candidate

st.set_page_config(page_title="AI Recruitment Agent System", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .agent-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }
    .success-text { color: #28a745; font-weight: bold; }
    .fail-text { color: #dc3545; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 AI Multi-Agent Recruitment Pipeline")
st.markdown("An automated end-to-end system for requirement extraction, sourcing, filtering, and submittal.")

# Session State Initialization
if 'rec_sys' not in st.session_state:
    st.session_state.rec_sys = RecruitmentSystem()
if 'pipeline_results' not in st.session_state:
    st.session_state.pipeline_results = {}

# Sidebar - System Controls
st.sidebar.header("⚙️ System Configuration")
jd_input = st.sidebar.text_area(
    "Job Description (JD)", 
    "We are looking for a Senior Python Developer with 5+ years of experience. Must be an expert in FastAPI, React, and AWS. Budget is 150000. Only US Citizens or Green Card holders will be considered.",
    height=300
)

# Mock Candidate Database (Inputs for the system to process)
st.sidebar.subheader("👥 Candidate Database (Mock)")
mock_candidates = [
    {"name": "Alice Smith", "email": "alice@example.com", "phone": "123-456", "resume_text": "Expert in Python, FastAPI, React, and AWS with 8 years exp.", "experience": 8, "visa_status": "US Citizen", "budget": 140000},
    {"name": "Bob Jones", "email": "bob@example.com", "phone": "789-012", "resume_text": "Python developer with 4 years exp. Knows AWS.", "experience": 4, "visa_status": "US Citizen", "budget": 130000},
    {"name": "Charlie Brown", "email": "charlie@example.com", "phone": "345-678", "resume_text": "Fullstack Python, FastAPI, React, AWS expert. 10 years exp.", "experience": 10, "visa_status": "H1B", "budget": 160000},
    {"name": "Diana Prince", "email": "diana@example.com", "phone": "901-234", "resume_text": "Python and AWS developer, 6 years exp. No React.", "experience": 6, "visa_status": "Green Card", "budget": 145000},
    {"name": "Evan Wright", "email": "evan@example.com", "phone": "567-890", "resume_text": "Senior Python and FastAPI dev, 7 years exp. Expert in AWS.", "experience": 7, "visa_status": "US Citizen", "budget": 170000},
]

if st.sidebar.button("🚀 Execute Pipeline"):
    with st.status("Agent Coordination in Progress...", expanded=True) as status:
        # --- AGENT 1 ---
        st.write("🤖 **Agent 1: Extracting Requirements...**")
        reqs = st.session_state.rec_sys.agent_extract_requirements(jd_input)
        st.session_state.pipeline_results['reqs'] = reqs
        st.markdown(f"✅ **Extracted:** Skills: `{reqs.skills}`, Exp: `{reqs.min_experience}+ yrs`, Budget: `${reqs.max_budget}`")

        # --- AGENT 2 ---
        st.write("🤖 **Agent 2: Generating Sourcing Strings...**")
        bool_str = st.session_state.rec_sys.agent_generate_booleans(reqs)
        st.session_state.pipeline_results['boolean'] = bool_str
        st.markdown(f"✅ **Boolean String:** `{bool_str}`")

        # --- AGENT 3 ---
        st.write("🤖 **Agent 3: Filtering & Scoring Candidates...**")
        filtered = st.session_state.rec_sys.agent_filter_and_score(mock_candidates)
        st.session_state.pipeline_results['filtered'] = filtered
        st.table([{"Name": c.name, "Score": f"{c.score:.2f}", "Visa": c.visa_status, "Exp": c.experience} for c in filtered])

        # --- AGENT 4 ---
        st.write("🤖 **Agent 4: Outreach & Negotiation...**")
        confirmed = st.session_state.rec_sys.agent_outreach_negotiate(filtered)
        st.session_state.pipeline_results['confirmed'] = confirmed
        st.markdown(f"✅ **Confirmed Candidates:** {', '.join([c.name for c in confirmed])}")

        # --- AGENT 5 ---
        st.write("🤖 **Agent 5: Preparing Final Submittals...**")
        proposals = st.session_state.rec_sys.agent_submit_proposal(confirmed)
        st.session_state.pipeline_results['proposals'] = proposals
        st.write(f"✅ **Successfully prepared {len(proposals)} proposals.**")

        status.update(label="Pipeline Execution Complete!", state="complete", expanded=False)

# --- Display Results ---
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
