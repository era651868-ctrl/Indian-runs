import json
from datetime import datetime

def calculate_candidate_score(candidate):
    """
    Evaluates a candidate profile against Redrob rules, filtering out traps.
    """
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    
    # 1. HARD FILTER: Trap Non-Technical Profiles
    title = profile.get("current_title", "").lower()
    if any(word in title for word in ["marketing", "operations", "sales", "hr", "support"]):
        return None
        
    # 2. HEURISTIC CHECK: IT Services vs Product Company
    company = profile.get("current_company", "").lower()
    industry = profile.get("current_industry", "").lower()
    is_it_services = "services" in industry or any(corp in company for corp in ["wipro", "tcs", "infosys", "mindtree"])
    
    # 3. BASE SCORE: Years of Experience
    score = float(profile.get("years_of_experience", 0)) * 5.0
    
    # 4. BONUSES & PENALTIES
    if not is_it_services:
        score += 25.0  # Strategic product background bonus
        
    score += float(signals.get("recruiter_response_rate", 0.0)) * 20.0
    score += (float(signals.get("github_activity_score", 0)) / 100.0) * 15.0
    
    # 5. LIVENESS CHECK: Ghost profile penalty
    last_active = signals.get("last_active_date", "2026-01-01")
    try:
        days_inactive = (datetime.strptime("2026-06-29", "%Y-%m-%d") - datetime.strptime(last_active, "%Y-%m-%d")).days
        if days_inactive > 180:
            score -= 20.0
    except:
        pass
        
    reasoning = f"Engineered candidate with {profile.get('years_of_experience')} YOE at {profile.get('current_company') or 'Tech Corp'}."
    
    return {
        "candidate_id": candidate["candidate_id"],
        "score": round(max(0.0, score), 4),
        "reasoning": reasoning
      }
  
