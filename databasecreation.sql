-- Active: 1734728961827@@127.0.0.1@3306@instgram_db
CREATE DATABAES instgram_db;

USE instgram_db;

CREATE TABLE user (
    user_id SERIAL PRIMARY KEY,
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100),
    profile_name VARCHAR(100) UNIQUE NOT NULL,
    profile_pic_path VARCHAR(255),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    bio TEXT,
    signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account_type VARCHAR(20) CHECK (account_type IN ('regular', 'business')) NOT NULL
);

CREATE TABLE business_account (
    business_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user(user_id),
    business_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    website VARCHAR(255),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(15)
);

CREATE TABLE chats (
    chat_id SERIAL PRIMARY KEY,
    chat_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_participants (
    chat_id INT REFERENCES chats(chat_id),
    user_id INT REFERENCES user(user_id),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(50),
    PRIMARY KEY (chat_id, user_id)
);

CREATE TABLE message (
    message_id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES user(user_id),
    receiver_id INT REFERENCES user(user_id),
    content TEXT NOT NULL,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);

CREATE TABLE attachment (
    id SERIAL PRIMARY KEY,
    message_id INT REFERENCES message(message_id),
    file_path VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post (
    post_id SERIAL PRIMARY KEY,
    created_by_user_id INT REFERENCES user(user_id),
    created_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    caption TEXT,
    location VARCHAR(255),
    post_type VARCHAR(50) -- This will be linked later with the post_type table
);

CREATE TABLE post_type (
    id SERIAL PRIMARY KEY,
    post_type_name VARCHAR(50)
);

CREATE TABLE post_media (
    post_media_id SERIAL PRIMARY KEY,
    post_id INT REFERENCES post(post_id) ON DELETE CASCADE,
    filter_id INT REFERENCES filter(id),
    media_file VARCHAR(255) NOT NULL,
    longtude INT,
    latitude INT
);


CREATE TABLE filter (
    id SERIAL PRIMARY KEY,
    filter_name VARCHAR(100),
    filter_details TEXT
);

CREATE TABLE effect (
    id SERIAL PRIMARY KEY,
    effect_name VARCHAR(100)
);

CREATE TABLE post_media_effect (
    post_media_id INT REFERENCES post_media(post_media_id) on delete cascade,
    effect_id INT REFERENCES effect(id),
    PRIMARY KEY (post_media_id, effect_id)
);

CREATE TABLE reaction (
    user_id INT REFERENCES user(user_id),
    post_id INT REFERENCES post(post_id) on delete cascade
);

CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    created_by_user_id INT REFERENCES user(user_id),
    post_id INT REFERENCES post(post_id) on delete cascade,
    created_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment TEXT NOT NULL,
    comment_replied_to_id INT REFERENCES comment(id)
);

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    business_id INT REFERENCES business_account(business_id),
    product_name VARCHAR(100),
    price DECIMAL(10, 2),
    description TEXT,
    available_stock INT
);

CREATE TABLE post_product_tag (
    post_id INT REFERENCES post(post_id) on delete cascade,
    product_id INT REFERENCES product(product_id) on delete cascade,
    PRIMARY KEY (post_id, product_id)
);

CREATE TABLE post_media_user_tag (
    post_media_id INT REFERENCES post_media(post_media_id) on delete CASCADE,
    user_id INT REFERENCES user(user_id),
    x_coordinate INT,
    y_coordinate INT,
    PRIMARY KEY (post_media_id, user_id)
);


CREATE TABLE advertisement (
    ad_id SERIAL PRIMARY KEY,
    created_by_user_id INT REFERENCES user(user_id),
    post_id INT REFERENCES post(post_id) on delete cascade,
    product_id INT REFERENCES product(product_id) on delete cascade,
    created_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    target_audience TEXT,
    start_date DATE,
    end_date DATE
);


CREATE TABLE ad_insight (
    ad_id INT REFERENCES advertisement(ad_id) on delete CASCADE,
    views_count INT DEFAULT 0,
    clicks_count INT DEFAULT 0,
    impressions INT DEFAULT 0,
    engagement_rate DECIMAL(5, 2),
    cost_per_click DECIMAL(10, 2),
    cost_per_mille DECIMAL(10, 2),
    PRIMARY KEY (ad_id)
);


CREATE TABLE collection (
    collection_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user(user_id),
    collection_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE collection_post (
    collection_id INT REFERENCES collection(collection_id),
    post_id INT REFERENCES post(post_id) on delete cascade,
    PRIMARY KEY (collection_id, post_id)
);


CREATE TABLE saved_post (
    user_id INT REFERENCES user(user_id),
    post_id INT REFERENCES post(post_id) on delete CASCADE,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id)
);


CREATE TABLE follower (
    following_user_id INT REFERENCES user(user_id),
    followed_user_id INT REFERENCES user(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    PRIMARY KEY (following_user_id, followed_user_id)
);

CREATE TABLE user_activity (
    user_id INT REFERENCES user(user_id),
    activity_type VARCHAR(50),
    related_post_id INT REFERENCES post(post_id) on delete cascade,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
