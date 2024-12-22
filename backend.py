import pyodbc

def create_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-P46QK96\MSSQLSERVER01;'
        'DATABASE=instgram_db;'
        'Trusted_Connection=yes;'  # Windows Authentication
        # For SQL Server Authentication, use these instead:
        # 'UID=your_username;'
        # 'PWD=your_password;'
    )

#only for testing connection
def test_connection():
    try:
        # Try to create a connection
        conn = create_connection()
        print("Connection successful!")

        # Try to execute a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        db_version = cursor.fetchone()
        print("SQL Server version:", db_version[0])

        # Test if we can access our database
        cursor.execute("SELECT COUNT(*) FROM [user]")
        user_count = cursor.fetchone()[0]
        print(f"Number of users in database: {user_count}")

        cursor.close()
        conn.close()
        return True

    except pyodbc.Error as e:
        print("Connection failed!")
        print("Error:", str(e))
        return False

# Function to create a new user with additional fields
def create_user(fname, lname, profile_name, email, password, bio, account_type):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO user (fname, lname, profile_name,email, password, bio, account_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (fname, lname, profile_name, email, password, bio, account_type))
    conn.commit()
    cursor.close()
    conn.close()

# Function to authenticate a user
def authenticate_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    SELECT * FROM user WHERE email = %s AND password = %s
    """
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Function to get user details by email
def get_user_by_email(email):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    SELECT * FROM user WHERE email = %s
    """
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


# Function to update user details
def update_user_data(email, fname, profile_pic_path ,lname, profile_name, bio, account_type):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    UPDATE user SET fname = %s, profile_pic_path = %s, lname = %s, profile_name = %s, bio = %s, account_type = %s WHERE email = %s
    """
    cursor.execute(query, (fname, profile_pic_path ,lname, profile_name, bio, account_type, email))
    conn.commit()
    cursor.close()
    conn.close()
