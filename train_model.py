import os
import json
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

def clean_venue(v):
    v_low = str(v).lower().strip()
    if 'wankhede' in v_low:
        return 'Wankhede Stadium, Mumbai'
    elif 'chinnaswamy' in v_low:
        return 'M Chinnaswamy Stadium, Bengaluru'
    elif 'eden gardens' in v_low:
        return 'Eden Gardens, Kolkata'
    elif 'chidambaram' in v_low or 'chepauk' in v_low:
        return 'MA Chidambaram Stadium, Chennai'
    elif 'kotla' in v_low or 'arun jaitley' in v_low:
        return 'Arun Jaitley Stadium, Delhi'
    elif 'rajiv gandhi' in v_low or 'uppal' in v_low:
        return 'Rajiv Gandhi Stadium, Hyderabad'
    elif 'punjab cricket' in v_low or 'bindra' in v_low or 'mohali' in v_low:
        return 'PCA Stadium, Mohali'
    elif 'sawai mansingh' in v_low or 'jaipur' in v_low:
        return 'Sawai Mansingh Stadium, Jaipur'
    elif 'narendra modi' in v_low or 'motera' in v_low or 'sardar patel' in v_low:
        return 'Narendra Modi Stadium, Ahmedabad'
    elif 'ekana' in v_low or 'lucknow' in v_low:
        return 'BRSABV Ekana Stadium, Lucknow'
    elif 'dy patil' in v_low:
        return 'DY Patil Stadium, Mumbai'
    elif 'brabourne' in v_low:
        return 'Brabourne Stadium, Mumbai'
    elif 'dubai' in v_low:
        return 'Dubai International Cricket Stadium'
    elif 'sharjah' in v_low:
        return 'Sharjah Cricket Stadium'
    elif 'zayed' in v_low:
        return 'Sheikh Zayed Stadium, Abu Dhabi'
    elif 'dharamsala' in v_low or 'himachal' in v_low:
        return 'HPCA Stadium, Dharamsala'
    elif 'visakhapatnam' in v_low or 'rajasekhara' in v_low:
        return 'ACA-VDCA Stadium, Visakhapatnam'
    elif 'mca' in v_low or 'maharashtra cricket' in v_low or 'pune' in v_low or 'subrata' in v_low:
        return 'MCA Stadium, Pune'
    elif 'barsapara' in v_low or 'guwahati' in v_low:
        return 'Barsapara Stadium, Guwahati'
    elif 'mullanpur' in v_low or 'new chandigarh' in v_low:
        return 'MYS Stadium, Mullanpur'
    elif 'jsca' in v_low or 'ranchi' in v_low:
        return 'JSCA Stadium, Ranchi'
    elif 'holkar' in v_low or 'indore' in v_low:
        return 'Holkar Stadium, Indore'
    elif 'barabati' in v_low or 'cuttack' in v_low:
        return 'Barabati Stadium, Cuttack'
    elif 'raipur' in v_low or 'veer narayan' in v_low:
        return 'SVNS Stadium, Raipur'
    return v.strip()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'matches.csv')

    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Initial shape: {df.shape}")

    # ==========================================
    # STEP 1: TEAM REPLACEMENTS (User's instruction)
    # ==========================================
    # - Delhi Daredevils -> Delhi Capitals
    # - Deccan Chargers -> Sunrisers Hyderabad
    # - Kings XI Punjab -> Punjab Kings
    # - Royal Challengers Bangalore -> Royal Challengers Bengaluru
    team_replace = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Deccan Chargers': 'Sunrisers Hyderabad',
        'Kings XI Punjab': 'Punjab Kings',
        'Royal Challengers Bangalore': 'Royal Challengers Bengaluru'
    }
    df['batting_team'] = df['batting_team'].replace(team_replace)
    df['bowling_team'] = df['bowling_team'].replace(team_replace)
    print("\n[Step 1] Team names replaced successfully.")

    # ==========================================
    # STEP 2: REMOVE DEFUNCT TEAMS (User's instruction)
    # ==========================================
    # - Gujarat Lions
    # - Rising Pune Supergiant(s)
    # - Kochi Tuskers Kerala
    # - Pune Warriors
    teams_to_remove = [
        'Gujarat Lions', 
        'Rising Pune Supergiant', 
        'Rising Pune Supergiants', 
        'Kochi Tuskers Kerala', 
        'Kochi Tkers Kerala',
        'Pune Warriors'
    ]
    df = df[~df['batting_team'].isin(teams_to_remove)]
    df = df[~df['bowling_team'].isin(teams_to_remove)]
    print(f"[Step 2] Obsolete teams removed. Filtered shape: {df.shape}")

    # ==========================================
    # STEP 3: VENUE STANDARDIZATION
    # ==========================================
    df['venue'] = df['venue'].apply(clean_venue)
    print(f"[Step 3] Venues standardized. Unique venues: {df['venue'].nunique()}")

    # ==========================================
    # STEP 4: CLEANING & SANITY CHECKS
    # ==========================================
    df = df[df['balls_left'] > 0]
    df = df[df['target'] > 0]
    df = df[(df['required_run_rate'] >= 0) & (df['required_run_rate'] < 50)]
    df = df[df['wickets_left'] >= 0]
    df = df[df['runs_left'] >= 0]
    print(f"[Step 4] Sanity checks passed. Final dataset rows: {len(df)}")

    # Unique teams and venues to save
    active_teams = sorted(list(set(df['batting_team'].unique()) | set(df['bowling_team'].unique())))
    active_venues = sorted(list(df['venue'].unique()))

    print(f"Active Teams ({len(active_teams)}): {active_teams}")
    print(f"Venues ({len(active_venues)}) available.")

    # ==========================================
    # STEP 5: FEATURE SELECTION
    # ==========================================
    features = [
        'batting_team', 
        'bowling_team', 
        'venue', 
        'runs_left', 
        'balls_left', 
        'wickets_left', 
        'target', 
        'current_run_rate', 
        'required_run_rate'
    ]
    X = df[features]
    y = df['batting_team_won']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ==========================================
    # STEP 6: PIPELINE BUILDING
    # ==========================================
    step1 = ColumnTransformer(
        transformers=[
            ('trf', OneHotEncoder(sparse_output=False, drop=None, handle_unknown='ignore'), ['batting_team', 'bowling_team', 'venue'])
        ],
        remainder='passthrough'
    )

    step2 = LogisticRegression(solver='liblinear', random_state=42, C=1.0)

    pipe = Pipeline([
        ('step1', step1),
        ('step2', step2)
    ])

    # ==========================================
    # STEP 7: TRAIN & EVALUATE
    # ==========================================
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n==========================================")
    print(f"Model Training Completed! Accuracy: {acc * 100:.2f}%")
    print(f"==========================================")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # ==========================================
    # STEP 8: SAVE MODEL & METADATA
    # ==========================================
    model_path = os.path.join(base_dir, 'pipe.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(pipe, f)
    print(f"Pipeline saved to: {model_path}")

    metadata = {
        'teams': active_teams,
        'venues': active_venues,
        'accuracy': round(acc * 100, 2),
        'team_codes': {
            'Chennai Super Kings': 'CSK',
            'Delhi Capitals': 'DC',
            'Gujarat Titans': 'GT',
            'Kolkata Knight Riders': 'KKR',
            'Lucknow Super Giants': 'LSG',
            'Mumbai Indians': 'MI',
            'Punjab Kings': 'PBKS',
            'Rajasthan Royals': 'RR',
            'Royal Challengers Bengaluru': 'RCB',
            'Sunrisers Hyderabad': 'SRH'
        },
        'team_colors': {
            'Chennai Super Kings': '#F9CD05',
            'Delhi Capitals': '#004C97',
            'Gujarat Titans': '#1B2133',
            'Kolkata Knight Riders': '#3A225D',
            'Lucknow Super Giants': '#0057E7',
            'Mumbai Indians': '#004BA0',
            'Punjab Kings': '#ED1B24',
            'Rajasthan Royals': '#EA1A85',
            'Royal Challengers Bengaluru': '#EC1C24',
            'Sunrisers Hyderabad': '#F26522'
        }
    }
    meta_path = os.path.join(base_dir, 'metadata.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved to: {meta_path}")

if __name__ == '__main__':
    main()
