import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta
import time

fake = Faker()


def create_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-P46QK96\MSSQLSERVER01;'
        'DATABASE=instgram_db;'
        'Trusted_Connection=yes;'
    )


def generate_users(conn, num_users=100):
    cursor = conn.cursor()
    users = []
    for _ in range(num_users):
        fname = fake.first_name()
        lname = fake.last_name()
        profile_name = fake.user_name()
        email = fake.email()
        password = fake.password()
        bio = fake.text(max_nb_chars=200)
        account_type = random.choice(['regular', 'business'])

        cursor.execute("""
        INSERT INTO [user] (fname, lname, profile_name, email, password, bio, account_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       (fname, lname, profile_name, email, password, bio, account_type))

        cursor.execute("SELECT SCOPE_IDENTITY()")
        user_id = cursor.fetchone()[0]
        users.append(user_id)

    conn.commit()
    return users


def generate_business_accounts(conn, user_ids):
    cursor = conn.cursor()
    business_accounts = []

    for user_id in user_ids:
        if random.random() < 0.3:  # 30% chance of being a business account
            cursor.execute("""
            INSERT INTO business_account (user_id, business_name, category, website, contact_email, contact_phone)
            VALUES (?, ?, ?, ?, ?, ?)""",
                           (user_id, fake.company(), fake.job(), fake.url(), fake.company_email(), fake.phone_number()))

            cursor.execute("SELECT SCOPE_IDENTITY()")
            business_accounts.append(cursor.fetchone()[0])

    conn.commit()
    return business_accounts


def generate_posts(conn, user_ids, num_posts=200):
    cursor = conn.cursor()
    posts = []

    for _ in range(num_posts):
        user_id = random.choice(user_ids)
        caption = fake.text(max_nb_chars=200)
        location = fake.city()
        post_type = random.randint(1, 3)  # 1=story, 2=post, 3=reel

        cursor.execute("""
        INSERT INTO post (created_by_user_id, caption, location, post_type)
        VALUES (?, ?, ?, ?)""",
                       (user_id, caption, location, post_type))

        cursor.execute("SELECT SCOPE_IDENTITY()")
        posts.append(cursor.fetchone()[0])

    conn.commit()
    return posts


def generate_reactions_and_comments(conn, user_ids, post_ids):
    cursor = conn.cursor()

    # Generate reactions
    for post_id in post_ids:
        num_reactions = random.randint(0, 50)
        reacting_users = random.sample(user_ids, min(num_reactions, len(user_ids)))

        for user_id in reacting_users:
            try:
                cursor.execute("""
                INSERT INTO reaction (user_id, post_id)
                VALUES (?, ?)""",
                               (user_id, post_id))
            except:
                continue

    # Generate comments
    for post_id in post_ids:
        num_comments = random.randint(0, 10)
        for _ in range(num_comments):
            user_id = random.choice(user_ids)
            comment_text = fake.text(max_nb_chars=100)

            cursor.execute("""
            INSERT INTO comment (created_by_user_id, post_id, comment)
            VALUES (?, ?, ?)""",
                           (user_id, post_id, comment_text))

    conn.commit()


def generate_followers(conn, user_ids):
    cursor = conn.cursor()

    for user_id in user_ids:
        num_followers = random.randint(0, 20)
        potential_followers = list(set(user_ids) - {user_id})
        followers = random.sample(potential_followers, min(num_followers, len(potential_followers)))

        for follower_id in followers:
            try:
                cursor.execute("""
                INSERT INTO follower (following_user_id, followed_user_id, status)
                VALUES (?, ?, ?)""",
                               (follower_id, user_id, 'active'))
            except:
                continue

    conn.commit()


def main():
    conn = create_connection()
    try:
        print("Generating users...")
        user_ids = generate_users(conn, 1000)

        print("Generating business accounts...")
        business_accounts = generate_business_accounts(conn, user_ids)

        print("Generating posts...")
        post_ids = generate_posts(conn, user_ids, 1000)

        print("Generating reactions and comments...")
        generate_reactions_and_comments(conn, user_ids, post_ids)

        print("Generating followers...")
        generate_followers(conn, user_ids)

        print("Data generation complete!")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()