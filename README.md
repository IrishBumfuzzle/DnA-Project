# Phase 4: SCP Foundation Database Implementation

**Team Members:**
* Ojas Kataria (2024114008)
* Ayush SM (2024101074)
* Manan Trivedi (2024101048)

## Project Overview
This project implements the database backend and Python CLI frontend for the SCP Foundation "Mini World" schema. It allows for the management of anomalous objects, personnel, containment facilities, and incident reports.

## Setup Instructions

1.  **Install Dependencies:**
    Ensure you have the MySQL driver installed:
    ```bash
    pip install pymysql cryptography
    ```

2.  **Database Initialization:**
    Log in to your MySQL client and execute the SQL scripts in the following order:
    1.  `source src/schema.sql;` (Creates tables and constraints)
    2.  `source src/populate.sql;` (Inserts realistic dummy data)

3.  **Run Application:**
    Navigate to the `src` directory and run:
    ```bash
    python main_app.py
    ```

---

## Application Features & Command List

The following list corresponds to the menu options available in the CLI application. 

### READ Operations (Queries)

**1. Find Anomalies by Facility**
* **Description:** Prompts the user for a Facility ID (e.g., `19`) and an Object Class (e.g., `Euclid`). It returns a list of all SCPs matching those criteria currently stored at that location[cite: 383].

**2. Find Personnel by Clearance**
* **Description:** Prompts for a minimum clearance level (1-5). It retrieves a list of all personnel who hold that clearance level or higher, along with their assigned site[cite: 384].

**3. Recent Breaches (30 Days)**
* **Description:** Automatically calculates the date 30 days prior to today and lists all `Incident_Report` entries that have occurred since then, showing the SCP involved and the summary[cite: 385].

**4. Facility Containment Load**
* **Description:** An aggregation query that groups data by facility to count the total number of SCP objects currently contained at each site[cite: 393].

**5. Detailed SCP Report**
* **Description:** A complex analysis query. Prompts for an SCP ID (e.g., `SCP-682`) and joins data from `Incident_Report` and `Test_Log` to calculate total incidents, total tests, and total casualties associated with that specific entity[cite: 398].

### WRITE Operations (Modifications)

*Note: For the video demonstration, please run a relevant READ query (e.g., Option 2) before and after these operations to prove the data has changed.*

**6. Onboard New Personnel (INSERT)**
* **Description:** Interactive wizard that collects details (ID, Name, Site, Clearance) to add a new employee. It handles the superclass/subclass relationship, asking if the new hire is "Researcher" or "Security" and prompting for specific attributes (e.g., Specialization or Rank) accordingly [cite: 403-406].

**7. Promote Personnel (UPDATE)**
* **Description:** Prompts for a Personnel ID and a new Clearance Level. It updates the database record to reflect the promotion[cite: 410].

**8. Remove Personnel (DELETE)**
* **Description:** Prompts for a Personnel ID to remove from the database (simulating a KIA or MIA status). Due to `ON DELETE CASCADE` settings in the schema, this will automatically clean up related records in the subclass tables[cite: 415].

