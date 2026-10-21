# 🏏 IPL Win Probability Predictor

An interactive Machine Learning web application to predict the win probability of the chasing team in IPL matches.

🌐 **Live Demo:** [https://ipl-win-probability-predictor-garima.streamlit.app/](https://ipl-win-probability-predictor-garima.streamlit.app/)

---

## 📌 Overview

This project calculates the real-time winning probability of IPL teams during the second innings of a match based on current match conditions such as target, current score, wickets lost, overs bowled, and venue.

---

## ✨ Features

- ⚡ **Live Win Probability:** Predicts real-time winning percentages for both batting and bowling teams.
- 🏏 **Official Team Logos & Flags:** Displays official logos for all 10 IPL teams.
- 📊 **Match Stats:** Shows runs required, balls remaining, Current Run Rate (CRR), and Required Run Rate (RRR).
- 🎨 **Clean Interface:** Simple, responsive, and easy-to-use UI built with Streamlit.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (Web Interface)
- **Scikit-Learn** (Machine Learning)
- **Pandas & NumPy** (Data Handling)

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GarimaVerma45/IPL-Win-Probability-Predictor.git
   cd IPL-Win-Probability-Predictor
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

Open your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```text
├── assets/
│   └── logos/         # Team logos (.png)
├── app.py             # Streamlit web application
├── matches.csv        # Match dataset
├── pipe.pkl           # Trained model pipeline
├── metadata.json      # Teams and venues data
├── requirements.txt   # Required Python libraries
└── README.md          # Project documentation
```

---

## 👤 Author

- **Garima Verma** - [GitHub Profile](https://github.com/GarimaVerma45)
