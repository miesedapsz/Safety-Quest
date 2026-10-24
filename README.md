# Dhalia Safety Quest — Python demo

A pixel-inspired Streamlit prototype for a 10-question general workplace hazard-awareness quiz, with immediate feedback, a weekly 70% target, a garden metaphor, and local progress history.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create a virtual environment (recommended):
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `streamlit run app.py`
6. Open the local URL shown in the terminal.

## How the demo works

- Each run contains 10 multiple-choice questions.
- Each correct answer contributes 10 points; incorrect answers contribute zero.
- The score is shown as a 0–100 “Safety Meter”; the weekly target is 70%.
- The player receives an explanation after each answer.
- On the results page, the player can save a run.
- Saved attempts are written to `player_history.json` beside the app. The dashboard charts saved attempts.
- The weekly view uses the machine's local date and Monday as the start of the week.

## Important limitations

- This is a prototype, not a certified training course or proof of legal compliance.
- The “Safety Meter” is a quiz score, **not actual health, competence, or a guarantee of safe work**.
- A 70% threshold is a product-design choice for the demo, not a legal or evidence-based universal pass mark. For real deployment, set thresholds with safety specialists and customer policy; high-risk topics may require mastery of every critical step.
- The app is a single-player local demo. It has no authentication, employer dashboard, database, privacy controls, backups, or LMS integration.
- The content is general workplace hazard awareness. It must be validated and adapted to the relevant jurisdiction, worksite, job role, risk assessments, and procedures. Healthcare and construction require separate specialist-reviewed question banks.
- The app currently records saved attempts only; it does not enforce one attempt per week. It encourages weekly repetition and displays the best score from the current week.

## Evidence base consulted

- Singapore Ministry of Manpower, Risk management: https://www.mom.gov.sg/workplace-safety-and-health/safety-and-health-management-systems/risk-management
- Singapore Ministry of Manpower, WSH legislation: https://www.mom.gov.sg/legislation/workplace-safety-and-health
- Singapore Statutes Online, Workplace Safety and Health (Risk Management) Regulations: https://sso.agc.gov.sg/SL/WSHA2006-RG8
- US OSHA, Hazard identification and assessment: https://www.osha.gov/safety-management/hazard-identification
- US OSHA, Worker participation: https://www.osha.gov/safety-management/worker-participation
- US OSHA, Hazard Identification Training Tool: https://www.osha.gov/hazfinder/manual

The sources inform general principles such as hazard identification, risk assessment and control, reporting near misses, worker participation, and emergency/non-routine hazards. They do not mean that every question is a verbatim legal requirement or that the prototype is compliant in every country.
