import psycopg2
import maskpass
from cryptography.fernet import Fernet

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

        try:
            verify_unique_application_query = f"select application_name from password_manager.login_details where application_name ilike '{application_name}';"
            cur.execute(verify_unique_application_query)
            conn.commit()
            existing_application_name = ''
            existing_application_name += cur.fetchone()[0]
            if application_name == existing_application_name:
                print(f"Login credentials aready exist for {application_name}")
                print("Please select: 3. Edit an existing login record")
                return 0
        except (Exception, psycopg2.Error) as error:
            pass

        print(f"application: {application_name}\nusername: {elected_username}\npassword: {elected_password}")

        user_choice = str(input("Confirm the above information correct: (y/n) "))
        if user_choice == 'y':
            user_confirmed = True
            break
        elif user_choice == 'n':
            user_confirmed = False
        else:
            print("Invalid choice...")

    #user has confirmed yes!
    print("======================================")
    print(f"Adding new login credentials for {application_name}...")
    try:
        #ADD PASSWORD ENCRYPTION
        elected_password = symmetric_key.encrypt(elected_password.encode()).decode()
        cur.execute(f"insert into password_manager.login_details values ('{application_name}', '{elected_username}', '{elected_password}');")
        conn.commit()
        print(f"Success - Completed adding login credentials for {application_name}")
        return True
    except (Exception, psycopg2.Error) as error:
        print(error)
        print("ERROR - Could not insert new record....")
        return False

def get_new_choice(choice, application_name):
    user_confirmed = False

    while user_confirmed == False:
        if choice == 'u':
            new_choice = str(input(f"Please enter your new username for {application_name}: "))
            print("======================================")
            print(f"Your new username will be: {new_choice}")
            print("======================================")
        elif choice == 'p':
            new_choice = str(input(f"Please enter your new password for {application_name}: "))
            print("======================================")
            print(f"Your new password will be: {new_choice}")
            print("======================================")

        user_choice = str(input("Confirm the above information correct: (y/n) "))
        if user_choice == 'y':
            user_confirmed = True
            break
        elif user_choice == 'n':
            user_confirmed = False
        else:
            print("Invalid choice...")
    
    return new_choice
    

def get_current_login(cur, conn, application_name, choice):
    if choice == 'username':
        query = f"select login_username from password_manager.login_details where application_name ilike '{application_name}';"
    elif choice == 'password':
        #ADD PASSWORD DECRYPTION
        query = f"select login_password from password_manager.login_details where application_name ilike '{application_name}';"
    try:
        cur.execute(query)
        result = cur.fetchone()[0]
        conn.commit()
        if choice == 'password':
            result = symmetric_key.decrypt(result).decode()
        return result
    except (Exception, psycopg2.Error) as Error:
        print(Error)
    return None

def edit_login_record(cur, conn):
    print("======================================")
    print("========= EDIT EXISTING LOGIN ========")
    print("======================================")
    user_confirmed = False

    while user_confirmed == False:
        application_name = str(input("What is the application_name: "))
        try:
            verify_unique_application_query = f"select application_name from password_manager.login_details where application_name ilike '{application_name}';"
            cur.execute(verify_unique_application_query)
            result = cur.fetchone()[0]
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print(f"There is no exisiting login credentials for {application_name}")
            print("Please select: 1. Add a new login credentials")
            return 0

        user_choice = str(input("Would you like to edit your username or password?: (u/p)"))

        if user_choice == 'u':
            print("======================================")
            print("============ EDIT USERNAME ===========")
            print("======================================")
            current_username = get_current_login(cur, conn, application_name, 'username')
            print(f"The current username for {application_name} is: {current_username}")
            new_choice = get_new_choice('u', application_name)
            user_confirmed = True
            break
        elif user_choice == 'p':
            print("======================================")
            print("============ EDIT PASSWORD ===========")
            print("======================================")
            current_password = get_current_login(cur, conn, application_name, 'password')
            print(f"The current password for {application_name} is: {current_password}")
            new_choice = get_new_choice('p', application_name)
            user_confirmed = True
            break
        else:
            print("invalid choice...")
    
    try:
        if user_choice == 'u':
            query = f"update password_manager.login_details set login_username = '{new_choice}' where application_name = '{application_name}';"
        elif user_choice == 'p':
            #ADD PASSWORD ENCRYPTION
            new_choice = symmetric_key.encrypt(new_choice.encode()).decode()
            query = f"update password_manager.login_details set login_password = '{new_choice}' where application_name = '{application_name}';"
        cur.execute(query)
        conn.commit()
        print("Changes have been successfully made...")
        return True
    except (Exception, psycopg2.Error) as Error:
        print(Error)
        return False

def verify_login_exists(cur, conn, application_name):
    query = f"select application_name from password_manager.login_details where application_name = '{application_name}';"
    try:
        cur.execute(query)
        conn.commit()
        result = cur.fetchone()[0]
        if str(result) == application_name:
            return True
        else:
            return False
    except (Exception, psycopg2.Error) as error:
        print(error)
        return False


def fetch_login_details(cur, conn):
    print("======================================")
    print("======== Fetch Login Details =========")
    print("======================================")
    user_confirmed = False

    while user_confirmed == False:
        application_name = str(input("For which application would you like your login details to: "))

        user_choice = str(input("Confirm the above information correct: (y/n) "))
        verification = verify_login_exists(cur, conn, application_name)
        if user_choice == 'y' and verification == True:
                user_confirmed = True
                break
        elif user_choice == 'n':
            user_confirmed = False
        elif verification == False:
            print("Invalid choice...")
    
    print("======================================")
    print("========= Login Details for: =========")
    print(f"{application_name}")
    username_query = f"select login_username from password_manager.login_details where application_name = '{application_name}';"
    #ADD PASSWORD DECRYPTION
    password_query = f"select login_password from password_manager.login_details where application_name = '{application_name}';"
    try:
        cur.execute(username_query)
        conn.commit()
        username_db = cur.fetchone()[0]
        print(f"username: {username_db}")

        cur.execute(password_query)
        conn.commit()
        password_db = cur.fetchone()[0]
        password_db = symmetric_key.decrypt(password_db).decode()
        print(f"password: {password_db}")

        print("======================================")
        return True
    except (Exception, psycopg2.Error) as error:
        print(error)
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
    file = open('master_key.key', 'rb')
    key = file.read()
    file.close()
    f = Fernet(key)

    cur.execute("select login_password from password_manager.login_details where application_name = 'master_password';")
    conn.commit()
    master_passsword_db = cur.fetchone()[0]
    master_passsword_db = f.decrypt(master_passsword_db).decode()
    if master_password != master_passsword_db:
        print("login incorrect...")
        return False
    else:
        print("Welcome...")
        return True

def initiate_menu(cur, conn):
    users_choice = display_menu()
    if users_choice == '1':
        add_new_login_record(cur, conn)
        return True
    elif users_choice == '2':
        fetch_login_details(cur, conn)
        return True
    elif users_choice == '3':
        edit_login_record(cur, conn)
        return True
    elif users_choice == 'Q':
        print("Thank-you - Ending Program")
        return False

def read_key():
    file = open('key.key', 'rb')
    global symmetric_key
    key = file.read()
    symmetric_key = Fernet(key)
    file.close()
    return symmetric_key

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

    continue_flag = True
    if verify_master_password(cur, conn, master_password):
        read_key()
        while continue_flag == True:
            continue_flag = initiate_menu(cur, conn)

    conn.commit()
    cur.close()
    conn.close()




initiate_password_manager()