import os
import json
import pickle
import pandas as pd
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="IPL Win Probability Predictor",
    page_icon="🏏",
    layout="centered"
)

# Custom header styling
st.markdown("""
<style>
    /* Top banner */
    .top-ipl-banner {
        background: linear-gradient(90deg, #8A1538 0%, #B81D4C 50%, #4A0E2E 100%);
        height: 12px;
        width: 100%;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #6B7280;
        font-size: 14px;
        margin-bottom: 25px;
    }
    .team-flag-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 12px;
        background-color: #F3F4F6;
        border-radius: 8px;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    .win-prob-header {
        font-size: 26px;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #1F2937;
    }
    .team-result-row {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 12px;
        font-size: 20px;
        font-weight: 700;
    }
</style>
<div class="top-ipl-banner"></div>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODEL & METADATA
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'pipe.pkl')
meta_path = os.path.join(base_dir, 'metadata.json')

@st.cache_resource
def load_resources():
    try:
        with open(model_path, 'rb') as f:
            pipe = pickle.load(f)
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception:
        # Resilient fallback: auto-train on cloud if pickle version differs
        from train_model import main as train_pipeline
        train_pipeline()
        with open(model_path, 'rb') as f:
            pipe = pickle.load(f)
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    return pipe, meta

try:
    pipe, meta = load_resources()
    teams = meta['teams']
    venues = meta['venues']
    team_codes = meta['team_codes']
    team_colors = meta['team_colors']
except Exception as e:
    st.error(f"Error loading model or metadata: {e}")
    st.stop()

def get_logo_path(team_name):
    code = team_codes.get(team_name, '')
    path = os.path.join(base_dir, 'assets', 'logos', f"{code}.png")
    if os.path.exists(path):
        return path
    return f"https://scores.iplt20.com/ipl/teamlogos/{code}.png"

# ==========================================
# TITLE
# ==========================================
st.markdown('<div class="main-title">IPL Win Probability Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Live 2nd Innings Win Probability Estimator</div>', unsafe_allow_html=True)

# ==========================================
# TEAMS SELECTION (With Flags)
# ==========================================
col_team1, col_team2 = st.columns(2)

with col_team1:
    default_bat_idx = teams.index("Chennai Super Kings") if "Chennai Super Kings" in teams else 0
    batting_team = st.selectbox("Batting Team", teams, index=default_bat_idx)
    
    # Flag display for Batting Team
    flag_col1, flag_col2 = st.columns([1, 4])
    with flag_col1:
        st.image(get_logo_path(batting_team), width=50)
    with flag_col2:
        st.markdown(f"**{batting_team}** <br><span style='color:#6B7280; font-size:12px;'>Batting (Chasing)</span>", unsafe_allow_html=True)

with col_team2:
    default_bowl_idx = teams.index("Sunrisers Hyderabad") if "Sunrisers Hyderabad" in teams else 1
    bowling_team = st.selectbox("Bowling Team", teams, index=default_bowl_idx)
    
    # Flag display for Bowling Team
    flag_col3, flag_col4 = st.columns([1, 4])
    with flag_col3:
        st.image(get_logo_path(bowling_team), width=50)
    with flag_col4:
        st.markdown(f"**{bowling_team}** <br><span style='color:#6B7280; font-size:12px;'>Bowling (Defending)</span>", unsafe_allow_html=True)

if batting_team == bowling_team:
    st.warning("⚠️ Batting and Bowling teams must be different!")

st.write("")

# ==========================================
# MATCH STATS INPUTS (Matches User's Demo Pic)
# ==========================================
col_in1, col_in2 = st.columns(2)

with col_in1:
    current_score = st.number_input("Current Score", min_value=0, max_value=350, value=79, step=1)
    overs_completed = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=10.0, step=0.1, format="%.2f")
    target_score = st.number_input("Target", min_value=1, max_value=350, value=135, step=1)

with col_in2:
    wickets_out = st.number_input("Wickets Out", min_value=0, max_value=10, value=1, step=1)

# Venue Selection
default_venue_idx = 0
for i, v in enumerate(venues):
    if "Sharjah" in v:
        default_venue_idx = i
        break

selected_venue = st.selectbox("Select venue", venues, index=default_venue_idx)

st.write("")

# ==========================================
# PREDICT BUTTON & DISPLAY RESULTS
# ==========================================
if st.button("Find Win Probability", type="primary", use_container_width=True):
    if batting_team == bowling_team:
        st.error("Please select two different teams!")
    else:
        full_overs = int(overs_completed)
        balls_in_over = int(round((overs_completed - full_overs) * 10))
        if balls_in_over >= 6:
            st.error("Invalid overs input! The balls value cannot exceed .5 (e.g., after 10.5 comes 11.0).")
            st.stop()
            
        balls_bowled = (full_overs * 6) + balls_in_over
        balls_left = 120 - balls_bowled
        runs_left = target_score - current_score
        wickets_left = 10 - wickets_out

        # Check match completion cases
        if runs_left <= 0:
            batting_win_pct = 100
            bowling_win_pct = 0
        elif wickets_left == 0 or (balls_left <= 0 and runs_left > 0):
            batting_win_pct = 0
            bowling_win_pct = 100
        else:
            crr = current_score / (balls_bowled / 6.0) if balls_bowled > 0 else 0.0
            rrr = (runs_left * 6.0) / balls_left if balls_left > 0 else 99.0

            input_df = pd.DataFrame([{
                'batting_team': batting_team,
                'bowling_team': bowling_team,
                'venue': selected_venue,
                'runs_left': runs_left,
                'balls_left': balls_left,
                'wickets_left': wickets_left,
                'target': target_score,
                'current_run_rate': round(crr, 2),
                'required_run_rate': round(rrr, 2)
            }])

            probabilities = pipe.predict_proba(input_df)[0]
            bowling_win_pct = int(round(probabilities[0] * 100))
            batting_win_pct = int(round(probabilities[1] * 100))
            
            # Ensure total equals 100%
            if batting_win_pct + bowling_win_pct != 100:
                bowling_win_pct = 100 - batting_win_pct

        # ==========================================
        # RESULT DISPLAY (Exact style of user's photo + Flags)
        # ==========================================
        st.markdown('<div class="win-prob-header">Win Probabilities</div>', unsafe_allow_html=True)
        
        # Batting Team Result Row
        res_col1, res_col2 = st.columns([1, 10])
        with res_col1:
            st.image(get_logo_path(batting_team), width=45)
        with res_col2:
            st.subheader(f"{batting_team}: {batting_win_pct}%")
        st.progress(batting_win_pct / 100.0)

        st.write("")

        # Bowling Team Result Row
        res_col3, res_col4 = st.columns([1, 10])
        with res_col3:
            st.image(get_logo_path(bowling_team), width=45)
        with res_col4:
            st.subheader(f"{bowling_team}: {bowling_win_pct}%")
        st.progress(bowling_win_pct / 100.0)

        # Match Equation Summary
        st.markdown(f"""
        ---
        **Match Equation:**
        - Need **{max(0, runs_left)}** runs in **{max(0, balls_left)}** balls with **{wickets_left}** wickets in hand.
        - **Current Run Rate (CRR):** {current_score / (overs_completed if overs_completed > 0 else 1):.2f}
        - **Required Run Rate (RRR):** {((max(0, runs_left) * 6) / max(1, balls_left)):.2f}
        """)
