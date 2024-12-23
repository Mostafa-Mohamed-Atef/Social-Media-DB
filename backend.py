import pyodbc
from datetime import datetime


def create_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-P46QK96\MSSQLSERVER01;'
        'DATABASE=instgram_db;'
        'Trusted_Connection=yes;'
    )

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
test_connection()
class User:
    @staticmethod
    def create_user(fname, lname, profile_name, email, password, bio="", account_type="regular"):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO [user] (fname, lname, profile_name, email, password, bio, account_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (fname, lname, profile_name, email, password, bio, account_type))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def create_business_account(user_id, business_name, category, website=None, contact_email=None, contact_phone=None):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO business_account (user_id, business_name, category, website, contact_email, contact_phone)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, business_name, category, website, contact_email, contact_phone))
            cursor.execute("UPDATE [user] SET account_type = 'business' WHERE user_id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0


class Post:
    @staticmethod
    def create_post(user_id, caption, location, post_type, media_files, filters=None, coordinates=None, product_tags=None):
        with create_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO post (created_by_user_id, caption, location, post_type)
                    OUTPUT INSERTED.post_id
                    VALUES (?, ?, ?, ?)
                """, (user_id, caption, location, post_type))
                post_id = cursor.fetchone()[0]

                for idx, media_file in enumerate(media_files):
                    filter_id = filters[idx] if filters and idx < len(filters) else None
                    long, lat = coordinates if coordinates else (None, None)
                    cursor.execute("""
                        INSERT INTO post_media (post_id, filter_id, media_file, longtude, latitude)
                        VALUES (?, ?, ?, ?, ?)
                    """, (post_id, filter_id, media_file, long, lat))

                if product_tags:
                    for product_id in product_tags:
                        cursor.execute("""
                            INSERT INTO post_product_tag (post_id, product_id)
                            VALUES (?, ?)
                        """, (post_id, product_id))

                conn.commit()
                return post_id
            except Exception as e:
                conn.rollback()
                raise e


class Social:
    @staticmethod
    def follow_user(follower_id, followed_id):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO follower (following_user_id, followed_user_id, status)
                VALUES (?, ?, 'active')
            """, (follower_id, followed_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def react_to_post(user_id, post_id):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reaction (user_id, post_id)
                VALUES (?, ?)
            """, (user_id, post_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def comment_on_post(user_id, post_id, comment_text, reply_to_id=None):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO comment (created_by_user_id, post_id, comment, comment_replied_to_id)
                VALUES (?, ?, ?, ?)
            """, (user_id, post_id, comment_text, reply_to_id))
            conn.commit()
            return cursor.rowcount > 0


class Business:
    @staticmethod
    def create_product(business_id, name, price, description, stock):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO product (business_id, product_name, price, description, available_stock)
                VALUES (?, ?, ?, ?, ?)
            """, (business_id, name, price, description, stock))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def create_advertisement(user_id, post_id, product_id, target_audience, start_date, end_date):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO advertisement (created_by_user_id, post_id, product_id, 
                                        target_audience, start_date, end_date)
                OUTPUT INSERTED.ad_id
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, post_id, product_id, target_audience, start_date, end_date))
            ad_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO ad_insight (ad_id)
                VALUES (?)
            """, (ad_id,))
            conn.commit()
            return ad_id


class Chat:
    @staticmethod
    def create_chat(chat_name=None):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chats (chat_name)
                OUTPUT INSERTED.chat_id
                VALUES (?)
            """, (chat_name,))
            return cursor.fetchone()[0]

    @staticmethod
    def send_message(sender_id, receiver_id, content, attachment_path=None):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO message (sender_id, receiver_id, content)
                OUTPUT INSERTED.message_id
                VALUES (?, ?, ?)
            """, (sender_id, receiver_id, content))
            message_id = cursor.fetchone()[0]

            if attachment_path:
                cursor.execute("""
                    INSERT INTO attachment (message_id, file_path)
                    VALUES (?, ?)
                """, (message_id, attachment_path))
            conn.commit()
            return message_id