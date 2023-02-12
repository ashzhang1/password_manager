import psycopg2
import maskpass

def display_menu():
    print("======================================")
    print("================ Menu ================")
    print("======================================")
    print("1. Add a new login credentials")
    print("2. Fetch login details")
    print("3. Edit an existing login record")
    print("Q. EXIT PROGRAM")

def verify_master_password(cur, conn, master_password):
    cur.execute("select login_password from password_manager.login_details where application_name = 'master_password';")
    conn.commit()
    master_passsword_db = cur.fetchone()
    if master_password != master_passsword_db[0]:
        print("login incorrect...")
        return False
    else:
        print("Welcome...")
        return True

def initiate_password_manager():
    print("======================================")
    print("========== Password Manager ==========")
    print("======================================")
    master_password = maskpass.askpass("Please enter your master password to begin: ")

    try: 
        conn = psycopg2.connect(f"dbname=ashleyzhang user=ashleyzhang")
        cur = conn.cursor()
    except (Exception, psycopg2.Error) as error:
        print(error)
        print("Error - connection could not be made to database...")
        return 'EXITING PROGRAM'

    if verify_master_password(cur, conn, master_password):
        user_choice = display_menu()

    conn.commit()
    cur.close()
    conn.close()




initiate_password_manager()