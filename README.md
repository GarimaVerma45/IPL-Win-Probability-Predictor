# 🏏 IPL Win Probability Predictor

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An end-to-end Machine Learning web application designed to predict the real-time win probability of the chasing team in the 2nd innings of an Indian Premier League (IPL) match. Built with **Scikit-Learn**, **Pandas**, and an interactive **Streamlit** user interface featuring official team flags and broadcast-style metrics.

---

## 🌟 Key Features

- **Real-Time Probability Estimation:** Computes live win percentages for both batting and bowling teams using calibrated logistic regression.
- **Official Team Crests & Flags:** High-resolution official logos dynamically rendered for all 10 active IPL franchises.
- **Match Equations & Metrics:** Instant calculation of:
  - Runs Required
  - Balls Remaining
  - Wickets in Hand
  - Current Run Rate (CRR)
  - Required Run Rate (RRR)
- **Edge-Case Handling:** Automatically detects completed chases (100% win for batting team), all-out scenarios, and over-limit validations.
- **Cleaned & Normalized Data:** Historical franchise renames unified, and defunct teams filtered out for accurate modeling.

---

## 📊 Data Preprocessing & Cleaning

In modern IPL history, several franchises underwent re-branding, while temporary franchises are no longer active. To ensure model integrity and prevent categorical bias, the following transformations are applied:

### 1. Franchise Name Replacements
- **Delhi Daredevils** ➡️ **Delhi Capitals**
- **Deccan Chargers** ➡️ **Sunrisers Hyderabad**
- **Kings XI Punjab** ➡️ **Punjab Kings**
- **Royal Challengers Bangalore** ➡️ **Royal Challengers Bengaluru**

### 2. Removal of Defunct / Temporary Teams
Matches involving teams that no longer participate in the IPL are excluded:
- ❌ *Gujarat Lions*
- ❌ *Rising Pune Supergiant / Supergiants*
- ❌ *Kochi Tuskers Kerala*
- ❌ *Pune Warriors India*

Following this step, the dataset contains matches exclusively between the **10 active IPL teams**:
1. Chennai Super Kings (CSK)
2. Delhi Capitals (DC)
3. Gujarat Titans (GT)
4. Kolkata Knight Riders (KKR)
5. Lucknow Super Giants (LSG)
6. Mumbai Indians (MI)
7. Punjab Kings (PBKS)
8. Rajasthan Royals (RR)
9. Royal Challengers Bengaluru (RCB)
10. Sunrisers Hyderabad (SRH)

### 3. Venue Standardization
Over 50 stadium variations are mapped and unified to eliminate duplicate categories (e.g., merging *"Wankhede Stadium"* and *"Wankhede Stadium, Mumbai"*).

---

## 🧠 Machine Learning Model

The predictive engine employs a **Scikit-Learn Pipeline** combining feature preprocessing with probabilistic classification:

1. **Feature Engineering:**
   - Categorical Features: `batting_team`, `bowling_team`, `venue`
   - Numerical Features: `runs_left`, `balls_left`, `wickets_left`, `target`, `current_run_rate`, `required_run_rate`
2. **ColumnTransformer:** `OneHotEncoder(handle_unknown='ignore')` transforms categorical team and venue inputs.
3. **Classifier:** `LogisticRegression(solver='liblinear')`
   - *Why Logistic Regression?* Unlike decision trees or random forests which produce discrete step-wise outputs, Logistic Regression outputs continuous, well-calibrated probabilities via its sigmoid activation function, making it ideal for sports win-loss odds.
4. **Model Performance:** Achieves **~78.5% accuracy** on hold-out test sets with balanced precision and recall.

---

## 📁 Repository Structure

```text
├── assets/
│   └── logos/                            # Official franchise badges (.png)
│       ├── CSK.png
│       ├── DC.png
│       ├── GT.png
│       ├── KKR.png
│       ├── LSG.png
│       ├── MI.png
│       ├── PBKS.png
│       ├── RCB.png
│       ├── RR.png
│       └── SRH.png
├── app.py                                # Streamlit web application
├── matches.csv                           # Preprocessed IPL match dataset
├── train_model.py                        # Automated data pipeline & training script
├── pipe.pkl                              # Serialized trained model pipeline
├── metadata.json                         # Team names, venues, codes, and color codes
├── IPL_Win_Probability_Predictor.ipynb   # Step-by-step Jupyter Notebook
├── requirements.txt                      # Python dependencies
├── .gitignore                            # Git ignore rules
└── README.md                             # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher installed on your system.
- Git installed.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GarimaVerma45/IPL-Win-Probability-Predictor.git
   cd IPL-Win-Probability-Predictor
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### 1. Run the Web Application
Launch the interactive Streamlit interface:
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

### 2. (Optional) Re-Train the Model
To re-run data cleaning, feature transformations, and serialize a new `pipe.pkl`:
```bash
python train_model.py
```

### 3. Interactive Notebook
To explore the exploratory data analysis (EDA) and pipeline steps interactively:
```bash
jupyter notebook IPL_Win_Probability_Predictor.ipynb
```

---

## 🌐 Deploy to Streamlit Cloud

To share this app publicly:
1. Fork or push this repository to your GitHub account.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New app"** and select:
   - **Repository:** `GarimaVerma45/IPL-Win-Probability-Predictor`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy!"** to get a live URL.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
