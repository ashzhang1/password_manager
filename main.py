import psycopg2
import maskpass

def add_new_login_record(cur, conn):
    print("======================================")
    print("========== ADD NEW LOGIN =============")
    print("======================================")
    user_confirmed = False

    while user_confirmed == False:
        application_name = str(input("What is the application_name: "))
        elected_username = str(input("What is your chosen username: "))
        elected_password = str(input("What is your chosen password: "))
        print("======================================")
        print(f"application: {application_name}\nusername: {elected_username}\npassword: {elected_password}")

        user_choice = str(input("Confirm the above information correct: (y/n) "))
        if  user_choice == 'y':
            user_confirmed = True
            break
        elif user_choice == 'n':
            user_confirmed = False
        else:
            print("Invalid choice...")
    print("======================================")
    print(f"Adding new login credentials for {application_name}...")
    try:
        cur.execute(f"insert into password_manager.login_details values ('{application_name}', '{elected_username}', '{elected_password}');")
        conn.commit()
        print(f"Success - Completeed adding login credentials for {application_name}")
        return True
    except (Exception, psycopg2.Error) as error:
        print(error)
        print("ERROR - Could not insert new record....")
        return False




def display_menu():
    print("======================================")
    print("================ Menu ================")
    print("======================================")
    print("1. Add a new login credentials")
    print("2. Fetch login details")
    print("3. Edit an existing login record")
    print("Q. EXIT PROGRAM")
    choice_valid = False

    while choice_valid == False:
        users_choice = str(input("Please select one of the above: "))
        if users_choice in ['1', '2', '3', 'Q']:
            choice_valid = True
        if choice_valid == True:
            return users_choice
        print("INVALID CHOICE - try again...")

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
        users_choice = display_menu()
        if users_choice == '1':
            add_new_login_record(cur, conn)
        elif users_choice == '2':
            pass
        elif users_choice == '3':
            pass
        elif users_choice == 'Q':
            pass


    conn.commit()
    cur.close()
    conn.close()




initiate_password_manager()