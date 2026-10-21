# 🏏 IPL Win Probability Predictor Project

An end-to-end Machine Learning web application predicting the live win probability of the chasing team in Indian Premier League (IPL) matches, built with **Python**, **Scikit-Learn**, and **Streamlit**.

---

## 📌 Project Structure

```text
ipl-win-probability-predictor/
├── assets/
│   └── logos/                  # Official high-resolution team logos/flags (.png)
│       ├── CSK.png
│       ├── DC.png
│       ├── GT.png
│       ├── KKR.png
│       ├── LSG.png
│       ├── MI.png
│       ├── PBKS.png
│       ├── RR.png
│       ├── RCB.png
│       └── SRH.png
├── matches.csv                 # Raw IPL dataset (736 matches)
├── IPL_Win_Probability_Predictor.ipynb  # Step-by-step Jupyter Notebook
├── train_model.py              # Automated data cleaning & model training script
├── pipe.pkl                    # Serialized Scikit-Learn trained Pipeline
├── metadata.json               # Active teams, venues, and color palettes
├── app.py                      # Interactive Streamlit Web Application
├── requirements.txt            # Project dependencies
└── README.md                   # Complete documentation & guide
```

---

## 🧭 Step-by-Step Guide: Ye Steps Kha Se Start Karein? (Where to Start)

Jab aap Jupyter Notebook ya Python script mein kaam shuru karte hain, to steps ka sahi order ye hota hai:

### Step 1: Dataset Load Karna
Sabse pehle pandas se CSV file load karein:
```python
import pandas as pd
df = pd.read_csv('matches.csv')
```

### Step 2: Teams Replace Karna (Rename)
Data load karne ke turant baad teams ka naam update karein:
```python
team_replace = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Kings XI Punjab': 'Punjab Kings',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru'
}

df['batting_team'] = df['batting_team'].replace(team_replace)
df['bowling_team'] = df['bowling_team'].replace(team_replace)
```

### Step 3: Defunct Teams Ko Hatana (Filter Out)
Jo teams ab IPL nahi khelti unko filter karein:
```python
teams_to_remove = [
    'Gujarat Lions', 
    'Rising Pune Supergiant', 
    'Rising Pune Supergiants', 
    'Kochi Tuskers Kerala', 
    'Kochi Tkers Kerala',
    'Pune Warriors'
]

# Dono columns (batting_team aur bowling_team) se filter karein:
df = df[~df['batting_team'].isin(teams_to_remove)]
df = df[~df['bowling_team'].isin(teams_to_remove)]
```
> Ab aapke dataset mein exactly **10 active IPL teams** bachengi:
> `Chennai Super Kings`, `Delhi Capitals`, `Gujarat Titans`, `Kolkata Knight Riders`, `Lucknow Super Giants`, `Mumbai Indians`, `Punjab Kings`, `Rajasthan Royals`, `Royal Challengers Bengaluru`, `Sunrisers Hyderabad`.

### Step 4: Venues Ko Standardize Karna
Stadiums ke duplicate ya varied names ko clean karein (jaise Wankhede Stadium, Mumbai aur Wankhede Stadium ko merge karna).

### Step 5: Feature Selection aur Model Training
Features extract karke `LogisticRegression` pipeline train karein:
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

features = ['batting_team', 'bowling_team', 'venue', 'runs_left', 'balls_left', 'wickets_left', 'target', 'current_run_rate', 'required_run_rate']
X = df[features]
y = df['batting_team_won']

trf = ColumnTransformer([
    ('trf', OneHotEncoder(sparse_output=False, drop=None, handle_unknown='ignore'), ['batting_team', 'bowling_team', 'venue'])
], remainder='passthrough')

pipe = Pipeline([
    ('step1', trf),
    ('step2', LogisticRegression(solver='liblinear', random_state=42))
])

pipe.fit(X_train, y_train)
```

### Step 6: Model Ko Save Karna (`pipe.pkl`)
```python
import pickle
with open('pipe.pkl', 'wb') as f:
    pickle.dump(pipe, f)
```

---

## 🚀 How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Re-train Model
```bash
python train_model.py
```

### 3. Launch Streamlit Web App
```bash
streamlit run app.py
```
App will open in your browser at `http://localhost:8501`.

---

## 🎨 Features of the Web App (`app.py`)
- **Official Team Flags & Logos:** Automatically displays each team's crest/flag alongside the batting and bowling selectors.
- **Dynamic Match Preview:** Displays a dynamic "VS" card with the teams' primary colors.
- **Match Controls:** Number inputs for Current Score, Wickets Out, Overs Completed, Target, and Venue Dropdown (matching your demo UI).
- **Instant Probabilities:** Clear win percentage cards and colored progress bars for both teams.
- **Match Equations:** Live calculations of runs needed, balls remaining, Current Run Rate (CRR), and Required Run Rate (RRR).
