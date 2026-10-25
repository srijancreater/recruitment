# Recruitment Multi-Agent System Architecture

## Agent Roles & Workflow

1.  **Requirement Agent (Agent 1)**
    *   **Input:** Job Description (JD).
    *   **Action:** Extracts key requirements (must-have skills, nice-to-have skills, years of experience, budget, location, visa requirements).
    *   **Output:** Structured Requirement Object.

2.  **Sourcing Agent (Agent 2)**
    *   **Input:** Structured Requirement Object.
    *   **Action:** Generates optimized Boolean search strings for LinkedIn, Indeed, Dice, etc.
    *   **Output:** Boolean Strings.

3.  **Filtering Agent (Agent 3)**
    *   **Input:** Candidate Profiles/Resumes + Requirement Object.
    *   **Action:** 
        *   Filter by Visa (Strictly GC/US Citizen).
        *   Filter by YOE and Budget.
        *   Perform JD vs Resume skill matching.
        *   Calculate a "Matching Score" (Skills in Resume / Skills in JD).
    *   **Output:** Ranked list of qualified candidates.

4.  **Outreach & Negotiation Agent (Agent 4)**
    *   **Input:** Ranked Candidate List.
    *   **Action:** 
        *   Email candidates to request current resume and confirm details (Budget, Location, Visa, Contact).
        *   Text/Call candidates in order of score.
        *   Negotiate hourly rate/salary based on budget.
    *   **Output:** Confirmed Candidates with agreed terms.

5.  **Submittal Agent (Agent 5)**
    *   **Input:** Confirmed Candidates.
    *   **Action:** Prepares the final submittal package/proposal.
    *   **Output:** Final Submittal.

## Technical Stack
- **Backend:** Python (FastAPI)
- **Agent Framework:** CrewAI or LangGraph (for stateful transitions)
- **LLM:** GPT-4o (for extraction and scoring)
- **Database:** SQLite/PostgreSQL (to track candidate state)
- **Integrations:** 
    - SendGrid/SMTP (Email)
    - Twilio (SMS/Calls)
- **Frontend:** Streamlit (for rapid deployment/UI)

## Deployment Plan
1. Develop Agent Logic $\rightarrow$ 2. Integrate Communication APIs $\rightarrow$ 3. Build Streamlit UI $\rightarrow$ 4. Deploy to Docker/Cloud.
