from faker import Faker
import random
from datetime import datetime, timedelta
from backend import create_connection


def populate_users(count=100):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()
        for _ in range(count):
            fname = fake.first_name()
            lname = fake.last_name()
            profile_name = f"{fname.lower()}{fake.random_number(digits=4)}"
            email = f"{profile_name}@{fake.domain_name()}"
            password = fake.password()
            bio = fake.sentence()
            account_type = random.choice(['regular', 'business'])

            cursor.execute(
                """
                INSERT INTO [user] (fname, lname, profile_name, email, password, bio, account_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (fname, lname, profile_name, email, password, bio, account_type)
            )
        conn.commit()


def populate_business_accounts(count=50):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM [user]")
        user_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(count):
            user_id = random.choice(user_ids)
            business_name = fake.company()[:100]
            category = fake.bs()[:100]
            website = fake.url()[:255]
            contact_email = fake.email()[:100]
            contact_phone = fake.numerify('###-###-####')  # Fixed length phone number

            cursor.execute(
                """
                INSERT INTO business_account 
                (user_id, business_name, category, website, contact_email, contact_phone)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, business_name, category, website, contact_email, contact_phone)
            )

            cursor.execute(
                """
                UPDATE [user] SET account_type = 'business' WHERE user_id = ?
                """,
                (user_id,)
            )
        conn.commit()


def populate_posts(post_count=10):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM [user]")
        user_ids = [row[0] for row in cursor.fetchall()]

        for user_id in user_ids:
            for _ in range(post_count):
                caption = fake.sentence()
                location = fake.city()
                post_type = random.randint(1, 3)  # 1=story, 2=post, 3=reel

                cursor.execute(
                    """
                    INSERT INTO post (created_by_user_id, caption, location, post_type)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, caption, location, post_type)
                )

                cursor.execute("SELECT SCOPE_IDENTITY()")
                post_id = cursor.fetchone()[0]

        conn.commit()


def populate_products(product_count=10):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT business_id FROM business_account")
        business_ids = [row[0] for row in cursor.fetchall()]

        for business_id in business_ids:
            for _ in range(product_count):
                product_name = fake.word().capitalize()
                price = round(random.uniform(10, 1000), 2)
                description = fake.text(max_nb_chars=200)
                available_stock = random.randint(0, 100)

                cursor.execute(
                    """
                    INSERT INTO product 
                    (business_id, product_name, price, description, available_stock)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (business_id, product_name, price, description, available_stock)
                )
        conn.commit()


def populate_followers(count=100):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM [user]")
        user_ids = [row[0] for row in cursor.fetchall()]
        for _ in range(count):
            follower_id, followed_id = random.sample(user_ids, 2)
            cursor.execute(
                """
                INSERT INTO follower (following_user_id, followed_user_id, status)
                VALUES (?, ?, ?)
                """,
                (follower_id, followed_id, 'active')
            )
        conn.commit()


def populate_comments(comment_count=50):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM [user]")  # Corrected
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT post_id FROM post")
        post_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM comment")
        existing_comment_ids = [row[0] for row in cursor.fetchall()]

        try:
            for _ in range(comment_count):
                if not user_ids or not post_ids:
                    print("No users or posts available to create comments.")
                    return

                created_by_user_id = random.choice(user_ids)
                post_id = random.choice(post_ids)
                comment_text = fake.sentence(nb_words=random.randint(5, 15))
                comment_replied_to_id = (
                    random.choice(existing_comment_ids)
                    if existing_comment_ids and random.choice([True, False])
                    else None
                )

                cursor.execute("""
                    INSERT INTO comment 
                    (created_by_user_id, post_id, comment, comment_replied_to_id)
                    VALUES (?, ?, ?, ?)
                """, (created_by_user_id, post_id, comment_text, comment_replied_to_id))

                cursor.execute("SELECT SCOPE_IDENTITY()")
                new_comment_id = cursor.fetchone()[0]
                existing_comment_ids.append(new_comment_id)
                print(f"Created comment ID: {new_comment_id} by user ID: {created_by_user_id} on post ID: {post_id}")

            conn.commit()
        except Exception as e:
            print(f"Error populating comments: {str(e)}")
            conn.rollback()


def populate_advertisements(ad_count=50):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()

        # Fetch user IDs, post IDs, and product IDs
        cursor.execute("SELECT user_id FROM [user]")  # Corrected
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT post_id FROM post")
        post_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT product_id FROM product")
        product_ids = [row[0] for row in cursor.fetchall()]

        try:
            for _ in range(ad_count):
                if not user_ids or not post_ids or not product_ids:
                    print("No users, posts, or products available to create advertisements.")
                    return

                created_by_user_id = random.choice(user_ids)
                post_id = random.choice(post_ids)
                product_id = random.choice(product_ids)

                target_audience = fake.sentence(nb_words=random.randint(5, 15))
                start_date = fake.date_this_year()
                end_date = start_date + timedelta(days=random.randint(7, 30))

                cursor.execute("""
                    INSERT INTO advertisement 
                    (created_by_user_id, post_id, product_id, target_audience, start_date, end_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (created_by_user_id, post_id, product_id, target_audience, start_date, end_date))

                cursor.execute("SELECT SCOPE_IDENTITY()")  # Fetch last inserted ID
                new_ad_id = cursor.fetchone()[0]
                print(f"Created advertisement ID: {new_ad_id} by user ID: {created_by_user_id} for post ID: {post_id}")

            conn.commit()
        except Exception as e:
            print(f"Error populating advertisements: {str(e)}")
            conn.rollback()

def populate_ad_insights(ad_count=50):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()

        # Fetch advertisement IDs
        cursor.execute("SELECT ad_id FROM advertisement")
        ad_ids = [row[0] for row in cursor.fetchall()]

        try:
            for _ in range(ad_count):
                # Select random advertisement
                if not ad_ids:
                    print("No advertisements available to create ad insights.")
                    return

                ad_id = random.choice(ad_ids)

                # Check if the ad_insight already exists for the ad_id
                cursor.execute("SELECT COUNT(*) FROM ad_insight WHERE ad_id = %s", (ad_id,))
                if cursor.fetchone()[0] > 0:
                    print(f"Ad insight already exists for advertisement ID: {ad_id}")
                    continue  # Skip this ad_id and move to the next one

                # Generate random ad insight details
                views_count = random.randint(0, 10000)
                clicks_count = random.randint(0, views_count)  # Clicks cannot exceed views
                impressions = random.randint(0, 10000)
                engagement_rate = round(random.uniform(0.1, 10.0), 2)
                cost_per_click = round(random.uniform(0.1, 5.0), 2)
                cost_per_mille = round(random.uniform(0.1, 10.0), 2)

                # Insert the ad insight into the database
                cursor.execute("""
                    INSERT INTO ad_insight (ad_id, views_count, clicks_count, impressions, engagement_rate, cost_per_click, cost_per_mille)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (ad_id, views_count, clicks_count, impressions, engagement_rate, cost_per_click, cost_per_mille))

                print(f"Created ad insight for advertisement ID: {ad_id}")

            # Commit all changes
            conn.commit()
        except Exception as e:
            print(f"Error populating ad insights: {str(e)}")
            conn.rollback()

def populate_reactions(reaction_count=50):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()

        # Fetch user IDs and post IDs
        cursor.execute("SELECT user_id FROM [user]")  # Updated
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT post_id FROM post")
        post_ids = [row[0] for row in cursor.fetchall()]

        # Ensure there are users and posts to react to
        if not user_ids or not post_ids:
            print("No users or posts available to create reactions.")
            return

        try:
            # Keep track of inserted combinations to avoid duplicates
            existing_reactions = set()

            for _ in range(reaction_count):
                user_id = random.choice(user_ids)
                post_id = random.choice(post_ids)

                # Ensure the combination is unique
                if (user_id, post_id) in existing_reactions:
                    continue  # Skip duplicate

                # Insert the reaction into the database
                cursor.execute("""
                    INSERT INTO reaction (user_id, post_id)
                    VALUES (?, ?)
                """, (user_id, post_id))

                # Add to the set of existing reactions
                existing_reactions.add((user_id, post_id))

                print(f"Created reaction: user ID {user_id} reacted to post ID {post_id}")

            # Commit all changes
            conn.commit()
        except Exception as e:
            print(f"Error populating reactions: {str(e)}")
            conn.rollback()

def populate_collections(collection_count=20):
    fake = Faker()
    with create_connection() as conn:
        cursor = conn.cursor()

        # Fetch user IDs
        cursor.execute("SELECT user_id FROM [user]")
        user_ids = [row[0] for row in cursor.fetchall()]

        if not user_ids:
            print("No users available to create collections.")
            return

        try:
            for _ in range(collection_count):
                # Randomly select a user
                user_id = random.choice(user_ids)

                # Generate collection name
                collection_name = fake.sentence(nb_words=3)

                # Insert collection into the database
                cursor.execute("""
                    INSERT INTO collection (user_id, collection_name, created_at)
                    VALUES (?, ?, ?)
                """, (user_id, collection_name, fake.date_time_this_year()))

                print(f"Created collection: {collection_name} for user ID: {user_id}")

            # Commit all changes
            conn.commit()
        except Exception as e:
            print(f"Error populating collections: {str(e)}")
            conn.rollback()


def populate_collection_posts(max_posts_per_collection=10):
    with create_connection() as conn:
        cursor = conn.cursor()

        # Fetch collection IDs and post IDs
        cursor.execute("SELECT collection_id FROM collection")
        collection_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT post_id FROM post")
        post_ids = [row[0] for row in cursor.fetchall()]

        if not collection_ids or not post_ids:
            print("No collections or posts available to associate.")
            return

        try:
            for collection_id in collection_ids:
                # Randomly assign posts to the collection
                assigned_posts = random.sample(post_ids, min(max_posts_per_collection, len(post_ids)))

                for post_id in assigned_posts:
                    cursor.execute("""
                        INSERT INTO collection_post (collection_id, post_id)
                        VALUES (?, ?)
                    """, (collection_id, post_id))

                print(f"Assigned {len(assigned_posts)} posts to collection ID: {collection_id}")

            # Commit all changes
            conn.commit()
        except Exception as e:
            print(f"Error populating collection posts: {str(e)}")
            conn.rollback()



def main():
    print("Populating database...")
    populate_users()
    print("Users table populated.")
    populate_business_accounts()
    print("bussiness_account table populated.")
    populate_products()
    print("bussiness_account table populated.")
    populate_posts()
    print("Posts table populated.")
    populate_followers()
    print("Followers table populated.")
    populate_comments()
    print("Comments table populated.")
    populate_advertisements()
    print("Advertisements table populated.")
    populate_ad_insights()
    print("Ad insights table populated.")
    populate_reactions()
    print("Reactions table populated.")
    populate_collections()
    print("Populate Collections table populated.")
    populate_collection_posts()
    print("Populate Collections Posts table populated.")


if __name__ == "__main__":
    main()
