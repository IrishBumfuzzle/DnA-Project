-- populate.sql
USE scp_foundation_db;

-- 1. Facilities
INSERT INTO Facility VALUES 
(1, 'Overseer HQ', NULL, 1, 'Washington', 'DC', 'USA', 500, 'Administrative'),
(19, 'Site-19', 1, 4, 'Lansing', 'Michigan', 'USA', 5000, 'Containment'),
(17, 'Site-17', 1, 4, 'Unknown', 'Nevada', 'USA', 2000, 'Research');

-- 2. SCP Objects
INSERT INTO SCP_Object VALUES 
('SCP-173', 'The Sculpture', 'Euclid', 'Concrete and rebar statue. Cannot move when observed.', '1993-01-01', 5, 19, 'Cell-001', 2),
('SCP-682', 'Hard-to-Destroy Reptile', 'Keter', 'Large reptile, extremely hostile and regenerative.', '1995-05-15', 10, 19, 'Acid-Vat-04', 4),
('SCP-096', 'The Shy Guy', 'Euclid', 'Humanoid that attacks if face is viewed.', '2004-12-10', 8, 19, 'Box-10', 3),
('SCP-999', 'The Tickle Monster', 'Safe', 'Orange translucent slime, induces happiness.', '2010-02-20', 1, 17, 'Playroom-A', 1);

-- 3. SCP Aliases
INSERT INTO SCP_Aliases VALUES 
('SCP-173', 'Peanut'),
('SCP-682', 'The Lizard'),
('SCP-096', 'Shy Guy');

-- 4. Personnel (Researchers and Security)
INSERT INTO Personnel VALUES 
(101, 'Jack', 'Bright', 19, 5, '1990-06-15'),
(102, 'Alto', 'Clef', 19, 5, '1995-08-20'),
(103, 'Elena', 'Ruiz', 17, 3, '2022-06-12'),
(201, 'Agent', 'Ulgrin', 19, 3, '2010-01-01'),
(202, 'Agent', 'Smith', 17, 2, '2015-03-15');

INSERT INTO Researcher VALUES 
(101, 'Bio-Engineering', 'Immortality Research'),
(102, 'Termination', 'SCP-682 Termination'),
(103, 'Psychology', 'SCP-999 Therapy');

INSERT INTO Security_Staff VALUES 
(201, 'Captain', TRUE),
(202, 'Officer', TRUE);

-- 5. Assignments
INSERT INTO Assignments VALUES 
(102, 'SCP-682', '2023-01-01', 'Lead Termination Researcher'),
(101, 'SCP-999', '2023-05-01', 'Stress Relief Testing'),
(201, 'SCP-173', '2023-02-15', 'Cell Cleaning Supervisor');

-- 6. Incidents
INSERT INTO Incident_Report (scp_id, report_date, severity_level, summary, casualties, reporting_personnel_id) VALUES 
('SCP-682', DATE_SUB(CURDATE(), INTERVAL 5 DAY), 5, 'Breach of acid vat. 4 D-Class consumed.', 4, 201),
('SCP-173', '2023-11-01', 3, 'Line of sight broken during cleaning.', 1, 201),
('SCP-096', '2024-01-15', 4, 'Photo leakage on social media.', 12, 102);

-- 7. Containment Procedures
INSERT INTO Containment_Procedure VALUES 
('SCP-173', 1, 'Maintain direct eye contact at all times.', NOW()),
('SCP-173', 2, 'Alert site command before entering cell.', NOW()),
('SCP-682', 1, 'Submerge in hydrochloric acid.', NOW());

-- 8. Test Logs
INSERT INTO Test_Log VALUES 
('SCP-682', 1, '2023-06-01', 'Attempted termination via acid. Failed.', 102),
('SCP-999', 1, '2023-07-20', 'Subject successfully cured depression in D-9021.', 103);