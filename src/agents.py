import os
import json
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    # --- Agent 1: Requirement Grabber (GPT-4o Powered) ---
    def agent_extract_requirements(self, jd_text: str) -> Requirement:
        print("[Agent 1] AI is analyzing Job Description...")
        
        prompt = f"""
        Analyze the following Job Description and extract the requirements in a strict JSON format.
        JD: {jd_text}
        
        Return ONLY a JSON object with these keys:
        - skills: (list of essential technical skills)
        - min_experience: (integer, minimum years of experience)
        - max_budget: (float, maximum annual budget/salary)
        - location: (string, primary location or 'Remote')
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a professional recruitment analyst. Output strict JSON."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        self.requirements = Requirement(**data)
        return self.requirements

    # --- Agent 2: Boolean String Generator (AI Optimized) ---
    def agent_generate_booleans(self, req: Requirement) -> str:
        print("[Agent 2] Generating AI-optimized Boolean strings...")
        if not req.skills:
            return "Developer AND (Remote OR \"United States\")"
        
        # We use GPT to create a high-converting Boolean string
        prompt = f"Create a professional LinkedIn Boolean search string for a candidate with these skills: {req.skills}. Location: {req.location}. Only return the string."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    # --- Agent 3: Filter, Compare & Score (Deep AI Analysis) ---
    def agent_filter_and_score(self, candidates_data: List[Dict]) -> List[Candidate]:
        print("[Agent 3] Performing Deep AI Scoring (JD vs Resume)...")
        scored_candidates = []
        
        if not self.requirements:
            raise ValueError("Requirements must be extracted first.")

        for data in candidates_data:
            # Hard Filters (Visa, Exp, Budget)
            if data['visa_status'] not in self.requirements.visa_allowed:
                continue
            if data['experience'] < self.requirements.min_experience:
                continue
            if data['budget'] > self.requirements.max_budget * 1.2:
                continue
                
            # AI SCORING: We send the resume and JD to GPT-4o to get a real professional score
            prompt = f"""
            Compare the following Resume against the Job Requirements.
            
            Requirements: {self.requirements.json()}
            Resume: {data['resume_text']}
            
            Provide a match score from 0.0 to 1.0 based on technical fit and experience.
            Return ONLY a JSON object: {{"score": 0.85, "reasoning": "Strong AWS experience but missing React"}}
            """
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are an expert technical recruiter."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            score_data = json.loads(response.choices[0].message.content)
            candidate = Candidate(**data, score=score_data['score'])
            scored_candidates.append(candidate)
            
        return sorted(scored_candidates, key=lambda x: x.score, reverse=True)

    # --- Agent 4: Outreach & Negotiation (Simulated Real-World) ---
    def agent_outreach_negotiate(self, ranked_candidates: List[Candidate]) -> List[Candidate]:
        print("[Agent 4] Executing Real-World Outreach Flow...")
        confirmed = []
        
        for cand in ranked_candidates:
            print(f"Processing {cand.name} (Score: {cand.score})...")
            # Simulation of the Email -> Text -> Call sequence
            # In Phase 2, these will be Twilio/SendGrid API calls
            if cand.score > 0.7:
                cand.status = "Negotiated"
                confirmed.append(cand)
                
        return confirmed

    # --- Agent 5: Submittal ---
    def agent_submit_proposal(self, confirmed_candidates: List[Candidate]):
        print("[Agent 5] Preparing Client Proposals...")
        submittals = []
        for cand in confirmed_candidates:
            proposal = f"OFFICIAL SUBMITTAL: {cand.name}\nScore: {cand.score}\nBudget: {self.requirements.max_budget}"
            submittals.append(proposal)
        return submittals
