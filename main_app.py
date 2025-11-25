import pymysql
import sys
from getpass import getpass
import os

SCP_LOGO = "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣴⣤⣤⣤⣤⣤⡄⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⠟⢋⣵⣿⣿⣿⡿⠛⣩⣤⣿⣿⣿⣿⣿⣿⣿⣬⣙⠻⣿⣿⣿⣷⡍⠛⢿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⠟⢹⠃⣠⣾⣿⣿⡿⢋⣴⣿⣿⣿⣿⠿⠿⠈⠿⢿⣿⣿⣿⣷⣤⡙⣿⣿⣿⢦⡀⢣⠙⣿⣿⣿⣿\n⣿⣿⡿⡿⠀⡯⠊⣡⣿⣿⠏⣴⣿⣿⣿⠟⠁⣀⣤⣤⠀⣤⣤⡀⠙⠻⣿⣿⣿⣌⢻⣿⣧⡉⠺⡄⢸⠹⣿⣿\n⣿⣿⠃⢷⠀⡠⢺⣿⣿⡏⣰⣿⣿⡟⠁⣠⣾⣿⣿⠿⠀⠿⣿⣿⣷⡄⠘⣿⣿⣿⡄⣿⣿⣯⠢⡀⢸⠀⢹⣿\n⣿⣿⠀⢸⠊⣠⣿⣿⣿⢀⣿⣿⣿⠁⣰⣿⣿⣿⣿⣆⢀⣼⣿⣿⣿⣿⡄⢸⣿⣿⣿⣹⣿⣿⣦⠈⢺⠀⢸⣿\n⣿⠹⡆⠀⣴⢻⣿⣿⣿⢸⣿⣿⣿⠀⣿⣿⡿⠿⠿⢿⣿⠿⠿⠿⣿⣿⡇⢈⣿⣿⣿⠀⣿⣿⣿⠳⡀⢀⡇⢸\n⣿⡀⠹⣸⠉⣿⣿⡿⢋⣠⣿⣿⣿⡀⠸⠟⢋⣀⢠⣾⣿⣷⡀⣀⡙⠻⠁⢸⣿⣿⣿⣈⠻⣿⣿⡄⠹⡜⠀⣸\n⣿⢧⠀⠇⢠⣿⣿⣷⡘⣿⣿⣿⣟⣁⡀⠘⢿⣿⣿⣿⣿⣿⣿⣿⠿⠀⣠⣉⣿⣿⣿⡿⢠⣿⡿⢧⠀⠁⣰⢿\n⣿⡌⢷⡄⣾⠀⣿⣿⣷⡜⢿⣿⣿⣿⣿⣦⣄⠈⠉⠛⠛⠛⠉⢁⣠⣾⣿⣿⣿⣿⡟⣰⣿⣿⡇⢸⢀⡴⠃⣼\n⣿⣷⣄⠙⢿⠀⣿⢿⣿⣿⣌⠿⠟⡻⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⣿⡿⠛⠿⠟⣼⣿⡿⢫⠃⢸⠋⢀⣼⣿\n⣿⣿⣟⣶⣄⡀⢸⡀⢻⣿⣿⣾⣿⣿⣶⣍⣙⠛⠿⠿⠿⠿⠿⠛⣋⣥⣶⣿⣿⣾⣿⣿⠁⣸⢀⣴⣶⣯⣿⣿\n⣿⣿⣿⣿⣿⣿⠾⣧⠀⢯⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⡿⢫⠃⢠⢷⣛⣉⣽⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣄⣁⡈⢧⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣠⢋⣀⣠⣴⣾⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣯⣉⠉⠉⠉⣀⣀⡭⠟⠛⢛⣛⠛⠛⠛⣛⠛⠛⠩⣥⣀⣈⢁⢀⣀⣴⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣝⡛⢉⣁⣀⣤⠖⣫⣴⣿⣿⣷⣬⡙⣦⣤⣀⡈⣉⣩⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
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

# Req: Retrieve all anomalies of a class given a facility [cite: 172]
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

# Req: Retrieving personnel with a certain clearance level [cite: 173]
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

# Req: Last breach in 30 days [cite: 174]
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

# Req: Number of SCPs per facility (Aggregator) [cite: 182]
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

# Req: SCP Report Analysis (Complex Join) [cite: 187]
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

# Req: Insert new Personnel [cite: 192]
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

# Req: Update clearance level [cite: 199]
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

# Req: Delete personnel (KIA/MIA) [cite: 204]
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

# --- Utility Functions ---
def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def wait_for_esc():
    """Wait for ESC key press to continue"""
    print("\n" + "="*80)
    print("Press [ESC] to go back to main menu...")
    while True:
        try:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # ESC key
                    break
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            # Fallback for systems without termios
            input("Press ENTER to go back...")
            break

def print_header():
    """Print SCP logo and header"""
    clear_screen()
    print(SCP_LOGO)
    print()

# ...existing code...

# --- Main CLI ---
def main():
    clear_screen()
    
    # Split the logo into lines
    logo_lines = SCP_LOGO.split('\n')
    
    # Print title
    print("=" * 100)
    print("SCP FOUNDATION DATABASE TERMINAL".center(100))
    print("=" * 100)
    print()
    
    # Define the login form lines
    login_form = [
        "",
        "╔════════════════════════════════╗",
        "║  AUTHENTICATION REQUIRED       ║",
        "╚════════════════════════════════╝",
        "",
        "MySQL Username: ",
        "",
        "MySQL Password: "
    ]
    
    # Calculate where to start the login form vertically (middle of logo)
    start_line = (len(logo_lines) - len(login_form)) // 2
    
    # Print logo with login form aligned to the right
    for i, line in enumerate(logo_lines):
        print(line, end="")
        
        # Add login form content on the right at appropriate lines
        form_index = i - start_line
        if 0 <= form_index < len(login_form):
            print("    " + login_form[form_index], end="")
        
        print()  # Newline after each row
    
    # Now we need to go back and capture the inputs
    # Calculate cursor position for username input
    username_row = start_line + 5  # The "MySQL Username: " line
    password_row = start_line + 7  # The "MySQL Password: " line
    
    # Move cursor up to username line
    lines_to_move_up = len(logo_lines) - username_row
    print(f"\033[{lines_to_move_up}A", end="")  # Move cursor up
    print(f"\033[{len(logo_lines[0]) + 4 + len('MySQL Username: ')}C", end="")  # Move cursor right
    
    # Get username
    sys.stdout.flush()
    user = input()
    
    # After input, cursor is at beginning of next line
    # Move cursor to password line (accounting for where we are now)
    lines_down = password_row - username_row - 1  # -1 because input already moved us down one
    if lines_down > 0:
        print(f"\033[{lines_down}B", end="")  # Move down
    print(f"\033[{len(logo_lines[0]) + 4 + len('MySQL Password: ')}C", end="")  # Move right from start
    
    # Get password
    sys.stdout.flush()
    password = getpass("")
    
    # Move cursor to bottom (we're already 1 line below password line)
    lines_to_bottom = len(logo_lines) - password_row - 1
    if lines_to_bottom > 0:
        print(f"\033[{lines_to_bottom}B")
    
    print()
    print("Connecting to database...".center(100))
    
    conn = get_db_connection(user, password)
    if not conn:
        sys.exit(1)
    
    input("\nPress ENTER to continue...")

    # Rest of your menu code stays the same
    while True:
        print_header()
        print("========== MAIN MENU ==========")
        print("1. [READ] Find Anomalies by Facility")
        print("2. [READ] Find Personnel by Clearance")
        print("3. [READ] Recent Breaches (30 Days)")
        print("4. [READ] Facility Containment Load")
        print("5. [READ] Detailed SCP Report")
        print("6. [WRITE] Onboard New Personnel")
        print("7. [WRITE] Promote Personnel")
        print("8. [WRITE] Remove Personnel")
        print("q. Quit")
        print()
        
        choice = input("Enter command: ").strip().lower()
        
        if choice == '1':
            clear_screen()
            get_anomalies_by_facility(conn)
            wait_for_esc()
        elif choice == '2':
            clear_screen()
            get_personnel_by_clearance(conn)
            wait_for_esc()
        elif choice == '3':
            clear_screen()
            get_recent_breaches(conn)
            wait_for_esc()
        elif choice == '4':
            clear_screen()
            get_scps_per_facility(conn)
            wait_for_esc()
        elif choice == '5':
            clear_screen()
            generate_scp_report(conn)
            wait_for_esc()
        elif choice == '6':
            clear_screen()
            insert_personnel(conn)
            wait_for_esc()
        elif choice == '7':
            clear_screen()
            update_clearance(conn)
            wait_for_esc()
        elif choice == '8':
            clear_screen()
            delete_personnel(conn)
            wait_for_esc()
        elif choice == 'q': 
            clear_screen()
            conn.close()
            print("Connection terminated. Stay safe.")
            break
        else:
            print("Invalid command.")
            input("Press ENTER to continue...")

if __name__ == "__main__":
    main()