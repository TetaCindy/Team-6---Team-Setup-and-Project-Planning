/* Team 6 - MoMo SMS Data Analytics Platform
    Database Setup Script (Week 2)
*/

CREATE DATABASE IF NOT EXISTS momo_analytics_db;
USE momo_analytics_db;

-- 1. Table for unique participants (Team Members and XML contacts)
CREATE TABLE Account_Holders (
    holder_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(60) NOT NULL,
    contact_number VARCHAR(20) NULL UNIQUE,
    registered_on DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table for classifying MoMo transaction types
CREATE TABLE Service_Categories (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(150) NOT NULL UNIQUE,
    service_desc VARCHAR(255)
);

-- 3. Main table for transaction records derived from modified_sms_v2.xml
CREATE TABLE Financial_Logs (
    log_entry_id INT AUTO_INCREMENT PRIMARY KEY,
    initiator_id INT NOT NULL,
    recipient_id INT,
    service_type_id INT NOT NULL,
    external_tx_id VARCHAR(250) NOT NULL UNIQUE,
    trans_amount DECIMAL(10,2) NOT NULL CHECK (trans_amount >= 0),
    trans_fee DECIMAL(10,2) DEFAULT 0.00 CHECK (trans_fee >= 0),
    remaining_balance DECIMAL(10,2) CHECK (remaining_balance >= 0),
    occurred_at DATETIME NOT NULL,
    raw_content TEXT,
    CONSTRAINT fk_initiator FOREIGN KEY (initiator_id) REFERENCES Account_Holders(holder_id),
    CONSTRAINT fk_recipient FOREIGN KEY (recipient_id) REFERENCES Account_Holders(holder_id),
    CONSTRAINT fk_service FOREIGN KEY (service_type_id) REFERENCES Service_Categories(service_id)
);

-- 4. Junction table for M:N relationship resolution
CREATE TABLE Participant_Roles (
    entry_id INT NOT NULL,
    holder_id INT NOT NULL,
    assignment VARCHAR(25) NOT NULL,
    PRIMARY KEY (entry_id, holder_id),
    CONSTRAINT fk_role_log FOREIGN KEY (entry_id) REFERENCES Financial_Logs(log_entry_id),
    CONSTRAINT fk_role_holder FOREIGN KEY (holder_id) REFERENCES Account_Holders(holder_id)
);

-- 5. Table for ETL auditing
CREATE TABLE Operational_Audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    related_entry_id INT NOT NULL,
    status_level VARCHAR(50) NOT NULL,
    audit_msg TEXT,
    captured_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_log FOREIGN KEY (related_entry_id) REFERENCES Financial_Logs(log_entry_id)
);

CREATE INDEX idx_occurred_at ON Financial_Logs(occurred_at);

-- =======================================================
-- INITIAL DATA SEEDING
-- =======================================================

INSERT INTO Account_Holders (full_name, contact_number) VALUES
('Cindy Saro Teta', '250780000001'),
('Methode Duhujubumwe', '250780000002'),
('Mutoni Keira', '250780000003'),
('Sylivie Tumukunde', '250780000004'),
('Jane Smith', '*********013'),
('Robert Brown', '60033');

INSERT INTO Service_Categories (service_name, service_desc) VALUES
('Received', 'Funds received into account'),
('Payment', 'Outward payment for services/goods'),
('Transfer', 'Peer-to-peer money transfer'),
('Deposit', 'Cash inflow from bank or agent');

-- Data mapped from modified_sms_v2.xml
INSERT INTO Financial_Logs (initiator_id, recipient_id, service_type_id, external_tx_id, trans_amount, trans_fee, remaining_balance, occurred_at, raw_content) VALUES
(5, 1, 1, '76662021700', 2000.00, 0.00, 2000.00, '2024-05-10 16:30:51', 'You have received 2000 RWF from Jane Smith...'),
(1, 5, 2, '73214484437', 1000.00, 0.00, 1000.00, '2024-05-10 16:31:39', 'Your payment of 1,000 RWF to Jane Smith...'),
(2, 6, 2, '26811810649', 27000.00, 0.00, 31300.00, '2025-01-15 20:26:12', 'Your payment of 27,000 RWF to Robert Brown 60033...');

INSERT INTO Participant_Roles (entry_id, holder_id, assignment) VALUES
(1, 5, 'sender'),
(1, 1, 'receiver'),
(2, 1, 'sender'),
(2, 5, 'receiver'),
(3, 2, 'sender');

INSERT INTO Operational_Audit (related_entry_id, status_level, audit_msg) VALUES
(1, 'info', 'P2P Receive successfully parsed'),
(3, 'info', 'Payment verified from XML');

-- ==============================================================
-- VALIDATION QUERIES
-- ==============================================================

-- READ: Detailed Report
SELECT 
    f.external_tx_id AS 'TX_ID', 
    a.full_name AS 'Initiator', 
    s.service_name AS 'Type', 
    f.trans_amount AS 'Amount', 
    f.occurred_at AS 'Timestamp'
FROM Financial_Logs f
JOIN Account_Holders a ON f.initiator_id = a.holder_id
JOIN Service_Categories s ON f.service_type_id = s.service_id;

-- UPDATE: Member Contact
UPDATE Account_Holders SET contact_number = '250799999999' WHERE full_name = 'Mutoni Keira';

-- DELETE: Cleanup Audit
DELETE FROM Operational_Audit WHERE audit_id = 2;