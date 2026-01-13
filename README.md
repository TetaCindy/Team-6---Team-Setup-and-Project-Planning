## TEAM 6 - MoMo Analytics Platform

## Team Members
1. CINDY Saro Teta - Repository & DevOps Lead
2. Sylivie Tumukunde - Architecture & Documentation Lead
3. Methode Duhujubumwe - Scrum Master & Project Manager
4. Mutoni Keira - Technical Research & Planning Lead

##  Project Description
Enterprise-level fullstack application for processing, analyzing, and visualizing MoMo (Mobile Money) SMS transaction data. The system features an ETL pipeline, SQLite database storage, and an interactive web dashboard for data insights.

##  System Architecture
[Architecture diagram will be added here by Member 2]

##  Scrum Board
[[Project board link](https://trello.com/b/6kerVEZJ)]

##  Project Structure
```
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── db.sqlite3
│   └── logs/
├── etl/
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/ 
├── scripts/
└── tests/
```

##  Setup Instructions
*(Will be updated in future phases)*
```bash
# Clone the repository
git clone https://github.com/dumethode/momo-analytics-platform.git

# Navigate to project directory
cd momo-analytics-platform

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

##  Development Workflow
```bash
# Run ETL pipeline
bash scripts/run_etl.sh

# Export dashboard data
bash scripts/export_json.sh

# Serve frontend
bash scripts/serve_frontend.sh
```

##  Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_parse_xml.py
```
##  System Architecture Link:
[System Architecture Diagram](https://github.com/TetaCindy/Team-6---Team-Setup-and-Project-Planning/blob/main/System%20Architecture%20diagram.png)





---
This is a collaborative project for Enterprise Application Development - ALU
