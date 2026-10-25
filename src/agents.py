import os
import json
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from scraper import RecruitmentScraper

# Load environment variables
load_dotenv()

# Initialize Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback for Streamlit Secrets if .env is not present
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("WARNING: GEMINI_API_KEY not found!")

genai.configure(api_key=api_key if api_key else "placeholder")

# Using 'gemini-pro' as it is the most universally available stable model name
model = genai.GenerativeModel(
    model_name='gemini-pro',
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

# --- Data Models ---

class Requirement(BaseModel):
    skills: List[str] = Field(default_factory=list)
    min_experience: int = 0
    max_budget: float = 0.0
    location: str = "Remote"
    visa_allowed: List[str] = ["US Citizen", "Green Card"]

class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    resume_text: str
    experience: int
    visa_status: str
    budget: float
    score: float = 0.0
    status: str = "New"
    confirmed_details: Dict[str, Any] = Field(default_factory=dict)

class RecruitmentSystem:
    def __init__(self):
        self.requirements: Optional[Requirement] = None
        self.scraper = RecruitmentScraper()

    def agent_extract_requirements(self, jd_text: str) -> Requirement:
        print("[Agent 1] Gemini is analyzing Job Description...")
        prompt = f"Analyze the following Job Description and extract the requirements in a strict JSON format.\nJD: {jd_text}\n\nReturn ONLY a JSON object with these keys:\n- skills: (list of essential technical skills)\n- min_experience: (integer, minimum years of experience)\n- max_budget: (float, maximum annual budget/salary)\n- location: (string, primary location or 'Remote')"
        try:
            response = model.generate_content(prompt)
            text = response.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(text)
            self.requirements = Requirement(**data)
            return self.requirements
        except Exception as e:
            print(f"AI Error: {e}. Using fallback.")
            self.requirements = Requirement(skills=["Python"], min_experience=3, max_budget=100000)
            return self.requirements

    def agent_generate_booleans(self, req: Requirement) -> str:
        print("[Agent 2] Generating AI-optimized Boolean strings...")
        if not req.skills: return "Developer AND (Remote OR \"United States\")"
        prompt = f"Create a professional LinkedIn Boolean search string for a candidate with these skills: {req.skills}. Location: {req.location}. Only return the string."
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except:
            return f"(\" {req.skills[0]} \") AND (Remote OR \"USA\")"

    def agent_filter_and_score(self, candidates_data: List[Dict]) -> List[Candidate]:
        print("[Agent 3] Filtering and scoring scraped candidates...")
        scored_candidates = []
        if not self.requirements: raise ValueError("Requirements must be extracted first.")

        for data in candidates_data:
            if data['visa_status'] not in self.requirements.visa_allowed: continue
            if data['experience'] < self.requirements.min_experience: continue
            if data['budget'] > self.requirements.max_budget * 1.2: continue
            
            prompt = f"Compare the following Resume against the Job Requirements.\n\nRequirements: {self.requirements.json()}\nResume: {data['resume_text']}\n\nProvide a match score from 0.0 to 1.0. Return ONLY a JSON object: {{\"score\": 0.85, \"reasoning\": \"...\"}}"
            try:
                response = model.generate_content(prompt)
                text = response.text.replace('```json', '').replace('```', '').strip()
                score_data = json.loads(text)
                candidate = Candidate(**data, score=score_data['score'])
                scored_candidates.append(candidate)
            except:
                candidate = Candidate(**data, score=0.5)
                scored_candidates.append(candidate)
        return sorted(scored_candidates, key=lambda x: x.score, reverse=True)

    def agent_outreach_negotiate(self, ranked_candidates: List[Candidate]) -> List[Candidate]:
        print("[Agent 4] Executing Real-World Outreach Flow...")
        confirmed = []
        for cand in ranked_candidates:
            if cand.score > 0.7:
                cand.status = "Negotiated"
                confirmed.append(cand)
        return confirmed

    def agent_submit_proposal(self, confirmed_candidates: List[Candidate]):
        print("[Agent 5] Preparing Client Proposals...")
        submittals = []
        for cand in confirmed_candidates:
            proposal = f"OFFICIAL SUBMITTAL: {cand.name}\nScore: {cand.score}\nBudget: {self.requirements.max_budget}"
            submittals.append(proposal)
        return submittals
