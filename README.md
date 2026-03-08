# Analyst Assist — Investigation Summary Automation

**Live Demo**  
https://analyst-assist.streamlit.app/

Analyst Assist is a small prototype that explores how automation can support fraud and compliance analysts during the early stages of case investigation.

The tool aggregates suspicious signals from flagged cases, assigns an explainable risk score, and generates a short investigation summary to help analysts quickly understand why a case may be risky and what action should be taken next.

The goal of this project is to explore **workflow automation for investigation triage**, not to replace fraud detection systems.

---

## Problem

Fraud and compliance teams often review large volumes of flagged cases every day.

Each case may contain multiple signals such as:

- VPN or proxy usage  
- device anomalies  
- location mismatches  
- suspicious login behavior  
- previous fraud history  

Analysts typically review these signals manually before deciding whether to escalate or investigate further.

When case volumes increase, this process becomes repetitive and time-consuming.

This project explores how these signals can be automatically summarized to support faster triage decisions.

---

## Solution

This prototype simulates an **investigation assistant** that:

1. Reads flagged case data  
2. Evaluates suspicious signals  
3. Calculates a risk score  
4. Classifies the case as Low, Medium, or High risk  
5. Generates an investigation summary  
6. Recommends a next action  

---

## Investigation Workflow
Flagged Case
↓
Signal Evaluation
(VPN, Proxy, Device, Location, Behavior)
↓
Risk Score Calculation
↓
Risk Level Classification
↓
Generated Investigation Summary
↓
Recommended Analyst Action

This workflow represents how automation can help analysts quickly understand and triage flagged cases.

---

## Signals Evaluated

The prototype evaluates several example signals:

- VPN detection  
- Proxy detection  
- GPS spoofing signal  
- Emulator environment  
- Remote desktop usage  
- Device mismatch  
- Previous fraud history  
- Claimed vs detected country mismatch  
- High failed login attempts  
- Suspicious session activity  
- High-value transactions  

Each signal contributes to the overall risk score.

---

## Technology Stack

**Programming Language**

- Python

**Libraries**

- Pandas  
- Streamlit  

---

## Project Structure
Analyst-Support-Prototype
│
├── app.py
├── requirements.txt
├── README.md
│
└── data
└── mock_cases.csv

**app.py**  
Main Streamlit application containing the scoring logic and dashboard.

**requirements.txt**  
Dependencies required to run the project.

**mock_cases.csv**  
Synthetic dataset used to simulate investigation cases.

---

## Run the Project Locally

Install dependencies:pip install -r requirements.txt


Run the Streamlit app:


streamlit run app.py


The application will start locally and open in your browser.

---

## Future Improvements

Potential future improvements include:

- analyst investigation notes  
- case prioritization  - analyst investigation notes  
- case prioritization  
- escalation workflows  
- integration with ticketing systems  
- operational analytics dashboards  
- machine learning models for case prioritization  

---

## Author

**Darshal Thumar**  
Computer Science (Honours) Student  
Algoma University

