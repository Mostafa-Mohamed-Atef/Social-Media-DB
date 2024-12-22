import mysql.connector

# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="P@ssw0rd",
        database="instgram_db"
    )


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
