import streamlit as st
import pandas as pd
import json
from pipeline import calculate_candidate_score

st.set_page_config(page_title="Redrob Candidate Ranker", page_icon="🎯", layout="wide")

st.title("🎯 Intelligent Candidate Discovery & Ranking Dashboard")
st.write("Production-ready heuristic evaluation engine designed for the Redrob Challenge.")

uploaded_file = st.file_uploader("Upload a sample JSONL candidate file", type=["jsonl", "json"])

if uploaded_file is not None:
    candidates = []
    
    # Parse lines safely
    for line in uploaded_file:
        if line.strip():
            try:
                candidates.append(json.loads(line))
            except:
                continue
                
    results = []
    for c in candidates:
        res = calculate_candidate_score(c)
        if res:
            results.append(res)
            
    if results:
        df = pd.DataFrame(results)
        df = df.sort_values(by="score", ascending=False).head(100)
        df.insert(1, "rank", range(1, len(df) + 1))
        
        st.subheader("🏆 Top Ranked Candidates (Exact Output Format)")
        st.dataframe(df[["candidate_id", "rank", "score", "reasoning"]], use_container_width=True)
        
        # Download Button for Submission Spec compliance
        csv = df[["candidate_id", "rank", "score", "reasoning"]].to_csv(index=False)
        st.download_button("📥 Download team_submission.csv", csv, "team_submission.csv", "text/csv")
    else:
        st.warning("No valid candidate profiles matched the core technical filtering criteria.")

