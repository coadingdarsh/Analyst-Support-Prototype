# Analyst Assist: Investigation Summary Automation

A lightweight prototype for a GeoComply-style Business Automation Intern conversation.

## What it does
- Loads synthetic flagged cases
- Scores each case using explainable rules
- Generates an analyst-ready summary
- Recommends a next action
- Shows an operations dashboard in Streamlit

## Why this is relevant
GeoComply publicly emphasizes geolocation compliance, anti-fraud, device intelligence, VPN/proxy detection, and workflows that help teams understand suspicious activity. This prototype does **not** replicate GeoComply's products. It demonstrates an intern-sized automation opportunity: reduce repetitive case triage work once risk signals already exist.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Interview positioning
Say:
"I built an early workflow automation prototype that turns multiple flagged-case signals into an explainable risk score, a recommended action, and an analyst-ready investigation summary. I wanted to explore where automation can reduce manual compliance work and improve triage consistency."

## Files
- `app.py` - Streamlit prototype
- `data/mock_cases.csv` - synthetic cases
- `interview_kit.md` - how to explain it confidently
