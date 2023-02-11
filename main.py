import psycopg2


print("Welcome to your password manager!")
db_password = input("Please enter your master password to begin:\n")
conn = psycopg2.connect(f"dbname=ashleyzhang user=ashleyzhang password={db_password}")
cur = conn.cursor()
# cur.execute("insert into password_manager.login_details values ('faceboook', 'username', 'password');")
conn.commit()
cur.close()
conn.close()


# print('hello world')