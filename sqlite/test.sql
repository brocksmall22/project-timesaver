'''im using an sql visualizer, so please look over this to make sure its what we want'''
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Employee
CREATE TABLE Employee (name STRING, number SMALLINT PRIMARY KEY);

-- Table: Responded
CREATE TABLE Responded (empNumber STRING REFERENCES Employee (number), runNumber TINYINT REFERENCES Run (number), date DATE REFERENCES Run (date), payRate FLOAT);

-- Table: Run
CREATE TABLE Run (number TINYINT PRIMARY KEY, date DATE, startTime SMALLINT, stopTime SMALLINT, runTime TINYINT);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;