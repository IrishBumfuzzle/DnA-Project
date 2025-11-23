-- schema.sql
DROP DATABASE IF EXISTS scp_foundation_db;
CREATE DATABASE scp_foundation_db;
USE scp_foundation_db;

-- 1. Facility (Recursive Relationship for Parent Facility) [cite: 72]
CREATE TABLE Facility (
    facility_id INT PRIMARY KEY,
    facility_name VARCHAR(100) NOT NULL,
    parent_facility_id INT,
    region_id INT,
    address_city VARCHAR(100),
    address_state VARCHAR(100),
    address_country VARCHAR(100),
    capacity INT,
    type ENUM('Containment', 'Research', 'Administrative') NOT NULL,
    FOREIGN KEY (parent_facility_id) REFERENCES Facility(facility_id) ON DELETE SET NULL
);

-- 2. SCP_Object [cite: 29]
CREATE TABLE SCP_Object (
    scp_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    object_class ENUM('Safe', 'Euclid', 'Keter', 'Thaumiel', 'Apollyon', 'Archon') NOT NULL,
    description TEXT,
    creation_date DATE,
    risk_level INT CHECK (risk_level BETWEEN 1 AND 10),
    facility_id INT NOT NULL, -- "location" in design
    room_number VARCHAR(20),
    min_clearance_level INT CHECK (min_clearance_level BETWEEN 1 AND 5),
    FOREIGN KEY (facility_id) REFERENCES Facility(facility_id) ON DELETE RESTRICT
);

-- 3. SCP_Aliases (Multivalued Attribute) [cite: 43]
CREATE TABLE SCP_Aliases (
    scp_id VARCHAR(20),
    alias VARCHAR(100),
    PRIMARY KEY (scp_id, alias),
    FOREIGN KEY (scp_id) REFERENCES SCP_Object(scp_id) ON DELETE CASCADE
);

-- 4. Personnel (Superclass) [cite: 46]
CREATE TABLE Personnel (
    personnel_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    site_id INT,
    clearance_level INT CHECK (clearance_level BETWEEN 1 AND 5),
    date_joined DATE,
    FOREIGN KEY (site_id) REFERENCES Facility(facility_id) ON DELETE SET NULL
);

-- 5. Personnel_Contact_Numbers (Multivalued Attribute) [cite: 58]
CREATE TABLE Personnel_Contact_Numbers (
    personnel_id INT,
    phone_number VARCHAR(20),
    PRIMARY KEY (personnel_id, phone_number),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id) ON DELETE CASCADE
);

-- 6. Researcher (Subclass) [cite: 59]
CREATE TABLE Researcher (
    personnel_id INT PRIMARY KEY,
    specialization_field VARCHAR(100),
    current_project VARCHAR(100),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id) ON DELETE CASCADE
);

-- 7. Security_Staff (Subclass) [cite: 64]
CREATE TABLE Security_Staff (
    personnel_id INT PRIMARY KEY,
    rank_title VARCHAR(50),
    weapon_certified BOOLEAN,
    FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id) ON DELETE CASCADE
);

-- 8. Assignments (M:N Relation: Personnel <-> SCP) 
CREATE TABLE Assignments (
    personnel_id INT,
    scp_id VARCHAR(20),
    assignment_date DATE,
    role VARCHAR(100),
    PRIMARY KEY (personnel_id, scp_id),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id) ON DELETE CASCADE,
    FOREIGN KEY (scp_id) REFERENCES SCP_Object(scp_id) ON DELETE CASCADE
);

-- 9. Incident_Report [cite: 83]
CREATE TABLE Incident_Report (
    incident_id INT PRIMARY KEY AUTO_INCREMENT,
    scp_id VARCHAR(20),
    report_date DATE,
    severity_level INT CHECK (severity_level BETWEEN 1 AND 5),
    summary TEXT,
    casualties INT DEFAULT 0,
    reporting_personnel_id INT, -- "Reported_By" Relation [cite: 126]
    FOREIGN KEY (scp_id) REFERENCES SCP_Object(scp_id) ON DELETE CASCADE,
    FOREIGN KEY (reporting_personnel_id) REFERENCES Personnel(personnel_id) ON DELETE SET NULL
);

-- 10. Containment_Procedure (Weak Entity) [cite: 94]
CREATE TABLE Containment_Procedure (
    scp_id VARCHAR(20),
    procedure_id INT,
    instructions TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (scp_id, procedure_id),
    FOREIGN KEY (scp_id) REFERENCES SCP_Object(scp_id) ON DELETE CASCADE
);

-- 11. Test_Log (Weak Entity) [cite: 102]
CREATE TABLE Test_Log (
    scp_id VARCHAR(20),
    test_id INT,
    test_date DATE,
    result_summary TEXT,
    researcher_id INT, -- "Test_Conducted_By" Relation [cite: 146]
    PRIMARY KEY (scp_id, test_id),
    FOREIGN KEY (scp_id) REFERENCES SCP_Object(scp_id) ON DELETE CASCADE,
    FOREIGN KEY (researcher_id) REFERENCES Researcher(personnel_id) ON DELETE SET NULL
);