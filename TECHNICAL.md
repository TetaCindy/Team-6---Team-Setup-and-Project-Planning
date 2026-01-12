# MoMo Analytics Platform - Technical Documentation

## Table of Contents
1. [Python Libraries & Dependencies](#python-libraries--dependencies)
2. [MoMo Transaction Data Structure](#momo-transaction-data-structure)
3. [Transaction Categorization Rules](#transaction-categorization-rules)
4. [Database Schema Design](#database-schema-design)
5. [Frontend UI Wireframe & Mockup](#frontend-ui-wireframe--mockup)
6. [Technical Decisions & Rationale](#technical-decisions--rationale)

---

## Python Libraries & Dependencies

### Core ETL Libraries

#### 1. **lxml** (Version 5.1.0)
XML Processing library for parsing MoMo transaction feeds.
- **Why lxml**: C-based implementation, faster than built-in xml module, XPath support
- **Usage**: Parse XML transactions, extract fields, handle malformed data
- **Example**:
  ```python
  from lxml import etree
  tree = etree.parse('data/raw/momo.xml')
  for transaction in tree.findall('.//transaction'):
      amount = transaction.find('amount').text
  ```

#### 2. **python-dateutil** (Version 2.8.2)
Flexible date parsing and timezone handling.
- **Why**: Handles various date formats, timezone conversions, robust parsing
- **Usage**: Parse SMS timestamps, normalize dates across regions
- **Example**:
  ```python
  from dateutil import parser
  date_obj = parser.parse("2024-01-12 14:30:00")
  ```

#### 3. **sqlite3** (Built-in to Python)
Embedded SQL database for transaction storage.
- **Why**: No external server needed, ACID compliance, easy backup/portability
- **Usage**: Store processed transactions, analytics data, merchant info
- **Example**:
  ```python
  import sqlite3
  conn = sqlite3.connect('data/db.sqlite3')
  cursor = conn.cursor()
  ```

### API Framework (Optional)

#### 4. **FastAPI** (Version 0.109.0)
Modern web framework for building APIs.
- **Purpose**: RESTful endpoints for frontend data access
- **Endpoints**: GET /api/transactions, /api/analytics, /api/categories

#### 5. **Uvicorn** (Version 0.27.0)
ASGI server for running FastAPI applications.
- **Purpose**: High-performance async web server
- **Run**: `uvicorn api.app:app --reload`

#### 6. **Pydantic** (Version 2.5.3)
Data validation and serialization using type hints.
- **Purpose**: Validate API requests/responses, ensure data integrity

### Data Processing

#### 7. **Pandas** (Version 2.2.0)
Data manipulation and analysis.
- **Optional**: Use for advanced ETL transformations, aggregations, summaries

### Testing

#### 8. **pytest** (Version 8.0.0)
Testing framework for unit and integration tests.
- **Usage**: `pytest tests/`
- **Coverage**: Parse, clean, categorize, load modules

---

## MoMo Transaction Data Structure

### Source XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<momo_feed>
  <date_generated>2024-01-12T10:30:00Z</date_generated>
  <transaction_batch>
    <transaction>
      <id>TXN001234567</id>
      <timestamp>2024-01-12 09:15:32</timestamp>
      <phone_from>+237612345678</phone_from>
      <phone_to>+237687654321</phone_to>
      <amount>15000</amount>
      <currency>XAF</currency>
      <sms_raw_text>You have sent 15000 XAF to +237687654321. Balance: 45000 XAF</sms_raw_text>
      <transaction_code>SEND</transaction_code>
      <status>SUCCESS</status>
      <balance_before>60000</balance_before>
      <balance_after>45000</balance_after>
      <merchant_name>Direct Transfer</merchant_name>
      <merchant_id>SELF</merchant_id>
      <reference_number>REF20240112091532</reference_number>
    </transaction>
  </transaction_batch>
</momo_feed>
```

### Normalized Transaction Structure

```python
{
    'transaction_id': 'TXN001234567',
    'phone_number': '+237612345678',
    'transaction_date': '2024-01-12',
    'transaction_time': '09:15:32',
    'amount': 15000.00,
    'currency': 'XAF',
    'merchant_name': 'Direct Transfer',
    'transaction_type': 'TRANSFER',  # After categorization
    'status': 'SUCCESS',
    'balance_after': 45000.00,
    'sms_raw_text': 'You have sent 15000 XAF to +237687654321. Balance: 45000 XAF'
}
```

### Expected Data Quality Issues

| Issue | Frequency | Mitigation |
|-------|-----------|-----------|
| Missing phone numbers | 2-5% | Flag for manual review or exclude |
| Duplicate transactions | 5-10% | Deduplicate by (phone, amount, timestamp) |
| Malformed SMS text | 3% | Use fallback pattern matching |
| Missing balance info | 1% | Flag but don't block processing |
| Timezone inconsistencies | Varies | Normalize to UTC |
| Negative amounts | <1% | Flag as error, investigate |
| Future timestamps | <0.5% | Validate against current time |

---

## Transaction Categorization Rules

### Category Definitions

#### 1. **TRANSFER**
- **Indicators**: "sent", "transferred", transaction_code=SEND
- **Characteristics**: P2P, variable amounts, receiver present
- **Rule**: `transaction_code LIKE '%SEND%'`

#### 2. **PAYMENT**
- **Indicators**: "paid", "payment", merchant is utility/vendor
- **Examples**: Bills, subscriptions, merchant payments
- **Rule**: Merchant is business entity (not phone number)

#### 3. **AIRTIME**
- **Indicators**: "airtime", "credit", "top-up", transaction_code=AIRTIME
- **Characteristics**: Amount 500-10,000 XAF, merchant=telecom
- **Rule**: `merchant_name IN ('MTN', 'Orange', 'Nexttel')`

#### 4. **WITHDRAWAL**
- **Indicators**: "withdraw", "cash out", merchant=agent/ATM
- **Rule**: `merchant_name LIKE '%AGENT%' OR '%ATM%'`

#### 5. **DEPOSIT**
- **Indicators**: "received", "deposited", balance_after > balance_before
- **Rule**: `status='SUCCESS' AND balance_after > balance_before`

#### 6. **SERVICE_FEE**
- **Indicators**: Small amounts (<100 XAF), merchant=platform
- **Rule**: `merchant_id='PLATFORM' OR amount < 100`

#### 7. **REFUND**
- **Indicators**: "refund", "reversal", transaction_code=REFUND
- **Rule**: `transaction_code LIKE '%REFUND%'`

### Categorization Algorithm (Priority-Based)

```
Step 1: Check transaction_code (Most Reliable)
  IF code IN [SEND, TRANSFER] → TRANSFER (confidence: 0.95)
  IF code IN [AIRTIME, TOPUP] → AIRTIME (confidence: 0.90)
  IF code IN [WITHDRAW] → WITHDRAWAL (confidence: 0.85)
  IF code IN [RECEIVE, DEPOSIT] → DEPOSIT (confidence: 0.90)
  IF code IN [REFUND, REVERSAL] → REFUND (confidence: 0.95)

Step 2: Check Merchant Pattern (Secondary)
  IF merchant IN telecom_list AND amount 500-10000 → AIRTIME (confidence: 0.80)
  IF merchant IN agent_list AND balance_decrease → WITHDRAWAL (confidence: 0.75)
  IF merchant_id = PLATFORM → SERVICE_FEE (confidence: 0.85)

Step 3: Check Balance Logic (Tertiary)
  IF balance_after > balance_before → DEPOSIT (confidence: 0.80)
  IF amount < 100 → SERVICE_FEE (confidence: 0.65)

Step 4: Check SMS Keywords (Fallback)
  IF sms_contains('sent') OR ('transfer') → TRANSFER (confidence: 0.70)
  IF sms_contains('airtime') → AIRTIME (confidence: 0.75)

Step 5: Default
  → TRANSFER (conservative default, confidence: 0.50)

Flag for manual review if confidence < 0.60
```

### Sample Categorization Examples

| SMS Text | Code | Amount | Balance | Merchant | Category | Confidence |
|----------|------|--------|---------|----------|----------|-----------|
| "Sent 5000 to John" | SEND | 5000 | ↓ | John | TRANSFER | 0.95 |
| "MTN 1000 purchased" | AIRTIME | 1000 | ↓ | MTN | AIRTIME | 0.95 |
| "Withdrawal 50000" | WITHDRAW | 50000 | ↓ | Agent | WITHDRAWAL | 0.90 |
| "Received 100000" | RECEIVE | 100000 | ↑ | Salary | DEPOSIT | 0.95 |
| "Fee charged" | FEE | 50 | ↓ | PLATFORM | SERVICE_FEE | 0.90 |
| "Refunded 2000" | REFUND | 2000 | ↑ | Vendor | REFUND | 0.95 |

---

## Database Schema Design

### Table: `transactions`
Core transaction records with normalized fields.

```sql
CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    phone_number TEXT NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_time TIME NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency TEXT DEFAULT 'XAF',
    merchant_name TEXT,
    merchant_id TEXT,
    transaction_type_id INTEGER FOREIGN KEY REFERENCES transaction_types(type_id),
    status TEXT DEFAULT 'SUCCESS',
    balance_after DECIMAL(15,2),
    sms_raw_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE INDEX idx_phone ON transactions(phone_number);
CREATE INDEX idx_date ON transactions(transaction_date);
CREATE INDEX idx_type ON transactions(transaction_type_id);
CREATE INDEX idx_phone_date ON transactions(phone_number, transaction_date);
```

### Table: `transaction_types`
Reference table for transaction categories.

```sql
CREATE TABLE transaction_types (
    type_id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL UNIQUE,
    description TEXT,
    color_code TEXT
);

INSERT INTO transaction_types VALUES
(1, 'TRANSFER', 'Send money to another person', '#FF6B6B'),
(2, 'PAYMENT', 'Bill or merchant payment', '#4ECDC4'),
(3, 'AIRTIME', 'Mobile credit purchase', '#45B7D1'),
(4, 'WITHDRAWAL', 'Cash withdrawal', '#FFA07A'),
(5, 'DEPOSIT', 'Money received/incoming', '#98D8C8'),
(6, 'SERVICE_FEE', 'Platform or bank charges', '#F7DC6F'),
(7, 'REFUND', 'Transaction reversal/refund', '#BB8FCE');
```

### Table: `merchants`
Merchant/recipient dimension table.

```sql
CREATE TABLE merchants (
    merchant_id TEXT PRIMARY KEY,
    merchant_name TEXT NOT NULL,
    phone_number TEXT UNIQUE,
    category TEXT,
    total_transactions INTEGER DEFAULT 0,
    total_volume DECIMAL(15,2) DEFAULT 0,
    last_transaction_date DATE
);
```

### Table: `analytics`
Pre-computed summary statistics for dashboard.

```sql
CREATE TABLE analytics (
    analytics_id INTEGER PRIMARY KEY,
    analysis_date DATE NOT NULL,
    period TEXT,
    total_transactions INTEGER,
    total_volume DECIMAL(15,2),
    average_transaction DECIMAL(15,2),
    transaction_type_id INTEGER,
    top_merchant_id TEXT,
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(type_id),
    FOREIGN KEY (top_merchant_id) REFERENCES merchants(merchant_id)
);
```

### Table: `dead_letter_queue`
Failed records for manual review and retry.

```sql
CREATE TABLE dead_letter_queue (
    dlq_id INTEGER PRIMARY KEY,
    raw_data TEXT NOT NULL,
    error_message TEXT,
    error_stage TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'PENDING',
    resolved_by TEXT
);
```

---

## Frontend UI Wireframe & Mockup

### Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                   MoMo Analytics Dashboard                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [Logo]  Home  Reports  Settings              [User] [Logout]    │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                        OVERVIEW CARDS                             │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  ┌───────────┐ │
│  │  Total Txns │  │Total Volume │  │ Avg Txn  │  │Active Users│ │
│  │ 1,245,831   │  │XAF 4.2B     │  │XAF 3,372 │  │  45,230    │ │
│  └─────────────┘  └─────────────┘  └──────────┘  └───────────┘ │
│                                                                   │
│  Filters: [From: Jan 1] [To: Jan 12] [Category ▼] [Export ▼]    │
│                                                                   │
│  ┌────────────────────────────┐  ┌──────────────────────────────┐ │
│  │ 7-Day Transaction Trend    │  │ Category Distribution        │ │
│  │                            │  │ □ TRANSFER 45% (1.9B)        │ │
│  │ XAF M                      │  │ □ DEPOSIT  20% (0.8B)        │ │
│  │    800│    ╱╲    ╱╲       │  │ □ AIRTIME  15% (0.6B)        │ │
│  │    600├───╱  ╲──╱  ╲      │  │ □ PAYMENT  10% (0.4B)        │ │
│  │    400└──────────────      │  │ □ WITHDRAW 10% (0.4B)        │ │
│  │       6  7  8  9 10 11 12  │  │                              │ │
│  └────────────────────────────┘  └──────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Top 5 Merchants                                              │ │
│  ├─────────────────────────────────────────────────────────────┤ │
│  │ #│ Merchant    │ Count   │ Volume      │ Trend             │ │
│  ├─────────────────────────────────────────────────────────────┤ │
│  │1│ MTN Airtime │ 234,567 │ XAF 1.2B    │ ↑ +15%            │ │
│  │2│ P2P Xfers   │ 189,234 │ XAF 2.3B    │ ↑ +8%             │ │
│  │3│ Electricity │ 123,456 │ XAF 0.5B    │ → 0%              │ │
│  │4│ Orange      │ 98,765  │ XAF 0.4B    │ ↓ -3%             │ │
│  │5│ School Fees │ 45,678  │ XAF 0.8B    │ ↑ +12%            │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Recent Transactions                           [View All]     │ │
│  ├─────────────────────────────────────────────────────────────┤ │
│  │ Date   │ Type      │ Amount │ Merchant      │ Status       │ │
│  ├─────────────────────────────────────────────────────────────┤ │
│  │Jan 12  │ TRANSFER  │ 5,000↑ │ John Doe      │ ✓ Success    │ │
│  │Jan 12  │ AIRTIME   │ 2,000↓ │ MTN           │ ✓ Success    │ │
│  │Jan 12  │ DEPOSIT   │50,000↑ │ Salary        │ ✓ Success    │ │
│  │Jan 11  │ PAYMENT   │15,000↓ │ Electricity   │ ✓ Success    │ │
│  │Jan 11  │ WITHDRAW  │30,000↓ │ ATM Agent     │ ✓ Success    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Header**: Logo, navigation, user menu
2. **KPI Cards**: 4 summary metrics with color indicators
3. **Filters**: Date range, category dropdown, export button
4. **Line Chart**: Daily/weekly transaction trends
5. **Pie Chart**: Category breakdown with percentages
6. **Merchant Table**: Top 5 merchants ranked by volume
7. **Transaction Table**: Recent transactions with sorting

### Frontend Technologies

- **HTML5**: Semantic markup
- **CSS3**: Responsive design, media queries
- **JavaScript**: Vanilla JS for simplicity, Chart.js for visualizations
- **Optional**: Vue.js or React for future enhancements

### Sample Frontend Code

```html
<!DOCTYPE html>
<html>
<head>
    <title>MoMo Analytics Dashboard</title>
    <link rel="stylesheet" href="web/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <div class="kpi-cards" id="kpiCards"></div>
        <div class="filters">
            <input type="date" id="dateFrom">
            <input type="date" id="dateTo">
            <button onclick="applyFilters()">Filter</button>
        </div>
        <div class="charts">
            <canvas id="trendChart"></canvas>
            <canvas id="categoryChart"></canvas>
        </div>
        <table id="transactionsTable"></table>
    </div>
    <script src="web/chart_handler.js"></script>
</body>
</html>
```

---

## Technical Decisions & Rationale

### Decision 1: SQLite vs PostgreSQL
**Chosen: SQLite**
- **Pros**: Zero configuration, embedded, no external server, perfect for MVP
- **Cons**: Limited concurrency, scalability ceiling at ~10GB
- **Migration Strategy**: Move to PostgreSQL if data exceeds 10GB or concurrent users >1000

### Decision 2: Python for ETL
**Chosen: Python**
- **Reasoning**: 
  - Mature libraries (lxml, pandas, python-dateutil)
  - Easy to learn and maintain for team
  - Strong data processing ecosystem
- **Alternatives Rejected**: Java (overkill), Go (smaller ecosystem), Node.js (fewer ETL libs)

### Decision 3: Batch Processing vs Real-time Streaming
**Chosen: Batch Processing**
- **Approach**: Schedule ETL runs (daily/hourly via cron/APScheduler)
- **Pros**: Simpler architecture, lower infrastructure, sufficient for analytics
- **Future**: Migrate to Kafka/RabbitMQ for real-time dashboards if needed

### Decision 4: Vanilla JavaScript vs Framework
**Chosen: Vanilla JavaScript + Chart.js**
- **Pros**: No build step, direct browser compatibility, quick prototyping
- **Cons**: Limited state management for complex interactions
- **Future**: Migrate to React/Vue if dashboard complexity increases

### Decision 5: Error Handling Strategy
**Approach: Three-tier model**
1. **Prevent**: Input validation, schema enforcement
2. **Contain**: Try-catch, detailed logging, error tracking
3. **Recover**: Dead-letter queue for manual intervention

**Benefits**: Pipeline resilience, no single record failures, audit trail for debugging

