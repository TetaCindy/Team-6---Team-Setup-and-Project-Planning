## TEAM 6 - MoMo Analytics Platform

## Team Members
1. CINDY Saro Teta - Repository & DevOps Lead
2. Sylivie Tumukunde - Architecture & Documentation Lead
3. Methode Duhujubumwe - Scrum Master & Project Manager
4. Mutoni Keira - Technical Research & Planning Lead

##  Project Description
Enterprise-level fullstack application for processing, analyzing, and visualizing MoMo (Mobile Money) SMS transaction data. The system features an ETL pipeline, SQLite database storage, and an interactive web dashboard for data insights.

##  System Architecture
https://github.com/TetaCindy/Team-6---Team-Setup-and-Project-Planning/blob/main/System%20Architecture%20diagram.png)

##  Scrum Board
[[Project board link](https://trello.com/b/6kerVEZJ)]

## Tean Participation Sheet
[[Tean Participation Sheet](https://docs.google.com/spreadsheets/d/1yB8mh1U3vzHcHDPnDFGUAXl1nHhIx0UPYm2Lo0quDeE/edit?gid=0#gid=0)]


##  Project Structure
```
.
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── database/                   # Week 2: SQL Implementation
│   └── database_setup.sql      # Schema, Constraints, and DDL
├── docs/                       # Week 2: Documentation
│   └── erd_diagram.png         # Entity Relationship Diagram
├── examples/                   # Week 2: JSON Modeling
│   ├── transaction_categories.json
│   └── json_schemas.json
├── web/
│   ├── styles.css
│   └── chart_handler.js
├── data/
│   ├── raw/
│   └── processed/
├── etl/
│   ├── parse_xml.py
│   └── load_db.py
└── tests/
```
##  Setup Instructions
*(Will be updated in future phases)*
```bash
# Clone the repository
git clone https://github.com/TetaCindy/Team-6---Team-Setup-and-Project-Planning

# Navigate to project directory
cd Team-6---Team-Setup-and-Project-Planning

```

##  Development Workflow
```bash
# Run ETL pipeline
python dsa/parse_to_json.py
# data will be saved in data/ folder as transactions.json

# Perform CRUD operations with plain python codes and run it
python app.py

```


##  System Architecture Link:
[System Architecture Diagram](https://github.com/TetaCindy/Team-6---Team-Setup-and-Project-Planning/blob/main/System%20Architecture%20diagram.png)

### Architecture Overview

The MoMo Transaction Analyzer follows a **5-layer architecture**:

1. **Data Source Layer** (XML) - Raw transaction data input
2. **ETL Pipeline Layer** (Python) - Data processing in 4 stages:
   - Parse XML
   - Clean & Normalize
   - Categorize Transactions
   - Load to Database
3. **Data Storage Layer** (SQLite) - Persistent storage
4. **API Layer** (FastAPI - Optional) - RESTful data access
5. **Presentation Layer** (Web Dashboard) - User interface

**Data Flow:** XML → ETL Processing → Database → API/JSON → Frontend Dashboard


---





---
