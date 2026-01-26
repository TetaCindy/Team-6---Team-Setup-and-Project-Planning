/* Creating a database */
CREATE DATABASE IF NOT EXISTS x_database;

/* Moving inside the newely created database by USE keyword/command */
USE x_database;

/* TABLES CREATION */

/* Creating table called "Users" to store the names of sender and reciver gotten from the body */
CREATE TABLE Users (
    Id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'id given to each user for identification', 
    Name VARCHAR(30) NOT NULL COMMENT 'Column to keep users name',
    Tel VARCHAR(25) NULL UNIQUE COMMENT 'Users telephone number',
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Accoun creation date'
  
);

/* Creating table called "Transaction_categories" */
CREATE TABLE Transaction_categories (
    Category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique category identifier',
    Name VARCHAR(200) NOT NULL COMMENT 'Category name',
    Description VARCHAR(200) COMMENT 'Category description'

);


/* Creating table called "Transactions" to store all the transactions */
CREATE TABLE Transactions (
    Transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique transaction identifier',
    Sender_id INT NOT NULL COMMENT 'Foreign Key to Users - sender',
    Receiver_id INT COMMENT 'Foreign Key to Users - receiver',
    Category_id INT NOT NULL COMMENT 'Forign Key to Transaction_Categories',
    TxId VARCHAR(250) NOT NULL UNIQUE COMMENT 'Financial Transaction Id from SMS',
    Amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0) COMMENT 'Transaction amount',
    Fee DECIMAL(10,2) DEFAULT 0 CHECK (fee >= 0) COMMENT 'Transaction fee charged',
    Balance DECIMAL(10,2) CHECK (balance >= 0) COMMENT 'Balance after transaction',
    Time DATETIME NOT NULL COMMENT 'Transaction timestamp',
    SMS_body TEXT COMMENT 'Original SMS body',
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES Users(id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES Users(id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Transaction_categories(category_id)

);

/* Indexes for faster lookups */
CREATE INDEX idx_tx_time ON Transactions(time);
CREATE INDEX idx_tx_sender ON Transactions(sender_id);


/* Creating table called "Users_Transaction" */
CREATE TABLE Users_transaction (
    Transaction_id INT NOT NULL COMMENT 'Foreign Key to transaction',
    User_id INT NOT NULL COMMENT 'Foreign Key to user',
    Role VARCHAR(20) NOT NULL COMMENT 'Role of user in transaction (sender/receiver/agent)',
    PRIMARY KEY (transaction_id, user_id),
    CONSTRAINT fk_tu_tx FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id),
    CONSTRAINT fk_tu_user FOREIGN KEY (user_id) REFERENCES Users(id)
);

/* Creating table called "System_logs" */
CREATE TABLE System_logs (
    Log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique log identifier',
    Transaction_id INT NOT NULL COMMENT 'FK to Transactions',
    Log_type VARCHAR(250) NOT NULL COMMENT 'Type of log entry (info/error/warning)',
    Message TEXT COMMENT 'Log details',
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Log creation timestamp',
    CONSTRAINT fk_log_tx FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id)
);


/* SAMPLE TESTS */

/* Inserting into table "Users" */
INSERT INTO Users (Name, Tel) VALUES
('MUTONI Keira', '+44 345 344 22'),
('Sylivie TUMUKUNDE', '+44 345 344 45'),
('Cindy Saro Teta', '+44 345 345 345 23'),
('Methode Duhujubumwe', '+44 345 980 89'),
('Tosin Aderabioyo', NULL);

/* Inserting into table "Transaction_categories" */
INSERT INTO Transaction_categories (name, description) VALUES
('Deposit', 'Deposited money into account'),
('Payment', 'Payment made to merchant'),
('Transfer', 'Money transferred between accounts'),
('Airtime', 'Airtime purchase'),
('Other', 'Miscellaneous transactions');

/* Inserting into table "Transactions" */
INSERT INTO Transactions (Sender_id, Receiver_id, Category_id, TxId, Amount, Fee, Balance, Time, SMS_body) VALUES
(1, 1, 2, '67662021700', 2000000.00, 0.00, 2000000.00, '2025-05-10 16:30:51', 'You have received 2,000,000 RWF...'),
(1, 2, 2, '43214484437', 1000.00, 0.00, 1000.00, '2025-05-10 16:31:39', 'Your payment of 1,000 RWF...'),
(1, 4, 2, '53732411227', 600.00, 0.00, 400.00, '2025-05-10 21:32:32', 'Your payment of 600 RWF...'),
(4, 1, 1, '67818959211', 400000.00, 0.00, 404000.00, '2025-05-11 18:43:49', 'A bank deposit of 400,000 RWF...'),
(1, 3, 3, '34113964658', 3500.00, 0.00, 10880.00, '2025-05-12 13:34:25', 'Your payment of 3,500 RWF...');

/* Inserting into table "Users_transaction" */
INSERT INTO Users_transaction (Transaction_id, User_id, Role) VALUES
(1, 1, 'sender'),
(1, 2, 'receiver'),
(2, 1, 'sender'),
(2, 2, 'receiver'),
(3, 1, 'receiver');

/* Inserting into table "System_logs" */
INSERT INTO System_logs (Transaction_id, Log_type, Message) VALUES
(1, 'info', 'Transaction processed successfully'),
(2, 'info', 'Transaction processed successfully'),
(3, 'warning', 'Balance low after transaction'),
(4, 'info', 'Deposit recorded'),
(5, 'error', 'Delayed confirmation message');
