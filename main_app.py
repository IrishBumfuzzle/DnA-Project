import pymysql
import sys
from getpass import getpass

# --- Configuration ---
def get_db_connection(user, password, host='localhost', db='scp_foundation_db'):
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        print(" [SUCCESS] Connected to SCP Foundation Database.")
        return connection
    except pymysql.Error as e:
        print(f" [ERROR] Connection failed: {e}")
        return None

# --- READ Operations (Analysis & Selection) ---

# Req: Retrieve all anomalies of a class given a facility 
def get_anomalies_by_facility(conn):
    print("\n--- Retrieve Anomalies by Class & Facility ---")
    facility_id = input("Enter Facility ID (e.g., 19): ")
    obj_class = input("Enter Object Class (Safe/Euclid/Keter): ")
    
    sql = """
    SELECT scp_id, title, risk_level 
    FROM SCP_Object 
    WHERE facility_id = %s AND object_class = %s
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (facility_id, obj_class))
        results = cursor.fetchall()
        if not results:
            print("No anomalies found.")
        for row in results:
            print(f"ID: {row['scp_id']} | Title: {row['title']} | Risk: {row['risk_level']}")

# Req: Retrieving personnel with a certain clearance level 
def get_personnel_by_clearance(conn):
    print("\n--- Personnel by Clearance Level ---")
    level = input("Enter Minimum Clearance Level (1-5): ")
    
    sql = """
    SELECT p.personnel_id, p.first_name, p.last_name, p.clearance_level, f.facility_name 
    FROM Personnel p
    JOIN Facility f ON p.site_id = f.facility_id
    WHERE p.clearance_level >= %s
    ORDER BY p.clearance_level DESC
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (level,))
        results = cursor.fetchall()
        for row in results:
            print(f"ID: {row['personnel_id']} | Name: {row['first_name']} {row['last_name']} | Level: {row['clearance_level']} | Site: {row['facility_name']}")

# Req: Last breach in 30 days 
def get_recent_breaches(conn):
    print("\n--- Breaches in Last 30 Days ---")
    sql = """
    SELECT i.incident_id, i.scp_id, i.report_date, i.summary, s.object_class
    FROM Incident_Report i
    JOIN SCP_Object s ON i.scp_id = s.scp_id
    WHERE i.report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        if not results:
            print("No recent breaches recorded.")
        for row in results:
            print(f"Date: {row['report_date']} | SCP: {row['scp_id']} ({row['object_class']}) | Summary: {row['summary']}")

# Req: Number of SCPs per facility (Aggregator) 
def get_scps_per_facility(conn):
    print("\n--- Containment Load (SCPs per Facility) ---")
    sql = """
    SELECT f.facility_name, COUNT(s.scp_id) as scp_count
    FROM Facility f
    LEFT JOIN SCP_Object s ON f.facility_id = s.facility_id
    GROUP BY f.facility_id, f.facility_name
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(f"Facility: {row['facility_name']} | Count: {row['scp_count']}")

# Req: SCP Report Analysis (Complex Join) 
def generate_scp_report(conn):
    print("\n--- Detailed SCP Report ---")
    scp_input = input("Enter SCP ID (e.g., SCP-682): ")
    
    sql = """
    SELECT s.scp_id, s.title, s.object_class,
           COUNT(DISTINCT i.incident_id) as incident_count,
           COUNT(DISTINCT t.test_id) as test_count,
           SUM(i.casualties) as total_casualties
    FROM SCP_Object s
    LEFT JOIN Incident_Report i ON s.scp_id = i.scp_id
    LEFT JOIN Test_Log t ON s.scp_id = t.scp_id
    WHERE s.scp_id = %s
    GROUP BY s.scp_id
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (scp_input,))
        result = cursor.fetchone()
        if result:
            print(f"\nReport for {result['scp_id']} ({result['title']})")
            print(f"Class: {result['object_class']}")
            print(f"Total Incidents: {result['incident_count']}")
            print(f"Total Tests Conducted: {result['test_count']}")
            print(f"Total Casualties: {result['total_casualties'] if result['total_casualties'] else 0}")
        else:
            print("SCP not found.")

# --- WRITE Operations (Insert, Update, Delete) ---

# Req: Insert new Personnel 
def insert_personnel(conn):
    print("\n--- Onboard New Personnel ---")
    try:
        pid = int(input("ID: "))
        fname = input("First Name: ")
        lname = input("Last Name: ")
        site = int(input("Site ID: "))
        level = int(input("Clearance (1-5): "))
        joined = input("Date Joined (YYYY-MM-DD): ")
        role_type = input("Type (Researcher/Security): ").lower()

        with conn.cursor() as cursor:
            # 1. Insert into Parent Table
            sql_parent = "INSERT INTO Personnel (personnel_id, first_name, last_name, site_id, clearance_level, date_joined) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_parent, (pid, fname, lname, site, level, joined))
            
            # 2. Insert into Subclass Table
            if role_type.startswith('r'):
                spec = input("Specialization: ")
                proj = input("Current Project: ")
                sql_child = "INSERT INTO Researcher (personnel_id, specialization_field, current_project) VALUES (%s, %s, %s)"
                cursor.execute(sql_child, (pid, spec, proj))
            else:
                rank = input("Rank: ")
                wep = input("Weapon Certified (1=Yes, 0=No): ")
                sql_child = "INSERT INTO Security_Staff (personnel_id, rank_title, weapon_certified) VALUES (%s, %s, %s)"
                cursor.execute(sql_child, (pid, rank, wep))
                
        print("Personnel successfully added.")
    except Exception as e:
        print(f"Error inserting personnel: {e}")

# Req: Update clearance level 
def update_clearance(conn):
    print("\n--- Promote Personnel ---")
    pid = input("Enter Personnel ID: ")
    new_level = input("Enter New Clearance Level: ")
    
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE Personnel SET clearance_level = %s WHERE personnel_id = %s"
            cursor.execute(sql, (new_level, pid))
            if cursor.rowcount > 0:
                print("Clearance updated.")
            else:
                print("ID not found.")
    except Exception as e:
        print(f"Error updating: {e}")

# Req: Delete personnel (KIA/MIA) 
def delete_personnel(conn):
    print("\n--- Report Personnel Deceased/MIA ---")
    pid = input("Enter Personnel ID to remove: ")
    
    try:
        with conn.cursor() as cursor:
            # ON DELETE CASCADE in schema handles subclasses
            sql = "DELETE FROM Personnel WHERE personnel_id = %s"
            cursor.execute(sql, (pid,))
            if cursor.rowcount > 0:
                print("Personnel record removed.")
            else:
                print("ID not found.")
    except Exception as e:
        print(f"Error deleting: {e}")

# --- Main CLI ---
def main():
    print("Welcome to the SCP Foundation Database Terminal.")
    user = input("MySQL User: ")
    password = getpass("MySQL Password: ")
    
    conn = get_db_connection(user, password)
    if not conn:
        sys.exit(1)

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. [READ] Find Anomalies by Facility")
        print("2. [READ] Find Personnel by Clearance")
        print("3. [READ] Recent Breaches (30 Days)")
        print("4. [READ] Facility Containment Load")
        print("5. [READ] Detailed SCP Report")
        print("6. [WRITE] Onboard New Personnel")
        print("7. [WRITE] Promote Personnel")
        print("8. [WRITE] Remove Personnel")
        print("q. Quit")
        
        choice = input("Enter command: ").strip().lower()
        
        if choice == '1': get_anomalies_by_facility(conn)
        elif choice == '2': get_personnel_by_clearance(conn)
        elif choice == '3': get_recent_breaches(conn)
        elif choice == '4': get_scps_per_facility(conn)
        elif choice == '5': generate_scp_report(conn)
        elif choice == '6': insert_personnel(conn)
        elif choice == '7': update_clearance(conn)
        elif choice == '8': delete_personnel(conn)
        elif choice == 'q': 
            conn.close()
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
