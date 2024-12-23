-- Create database
CREATE DATABASE instgram_db;
GO

USE instgram_db;
GO

CREATE TABLE [user] (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100),
    profile_name VARCHAR(100) UNIQUE NOT NULL,
    profile_pic_path VARCHAR(255),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    bio TEXT,
    signup_date DATETIME DEFAULT GETDATE(),
    account_type VARCHAR(20) CHECK (account_type IN ('regular', 'business')) NOT NULL
);

CREATE TABLE business_account (
    business_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES [user](user_id),
    business_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    website VARCHAR(255),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(15)
);

CREATE TABLE chats (
    chat_id INT IDENTITY(1,1) PRIMARY KEY,
    chat_name VARCHAR(100),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE chat_participants (
    chat_id INT FOREIGN KEY REFERENCES chats(chat_id),
    user_id INT FOREIGN KEY REFERENCES [user](user_id),
    joined_at DATETIME DEFAULT GETDATE(),
    role VARCHAR(50),
    PRIMARY KEY (chat_id, user_id)
);

CREATE TABLE message (
    message_id INT IDENTITY(1,1) PRIMARY KEY,
    sender_id INT FOREIGN KEY REFERENCES [user](user_id),
    receiver_id INT FOREIGN KEY REFERENCES [user](user_id),
    content TEXT NOT NULL,
    time_stamp DATETIME DEFAULT GETDATE(),
    is_read BIT DEFAULT 0
);

CREATE TABLE attachment (
    id INT IDENTITY(1,1) PRIMARY KEY,
    message_id INT FOREIGN KEY REFERENCES message(message_id),
    file_path VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    uploaded_at DATETIME DEFAULT GETDATE()
);
CREATE TABLE post_type (
    id INT IDENTITY(1,1) PRIMARY KEY,
    post_type_name VARCHAR(50)
);

insert into post_type(post_type_name)
values ('story'), ('post'), ('reel')


CREATE TABLE post (
    post_id INT IDENTITY(1,1) PRIMARY KEY,
    created_by_user_id INT FOREIGN KEY REFERENCES [user](user_id),
    created_datetime DATETIME DEFAULT GETDATE(),
    caption TEXT,
    location VARCHAR(255),
    post_type INT Foreign key references post_type(id)

);


CREATE TABLE filter (
    id INT IDENTITY(1,1) PRIMARY KEY,
    filter_name VARCHAR(100),
    filter_details TEXT
);

CREATE TABLE post_media (
    post_media_id INT IDENTITY(1,1) PRIMARY KEY,
    post_id INT FOREIGN KEY REFERENCES post(post_id) ON DELETE CASCADE,
    filter_id INT FOREIGN KEY REFERENCES filter(id),
    media_file VARCHAR(255) NOT NULL,
    longtude INT,
    latitude INT
);

CREATE TABLE effect (
    id INT IDENTITY(1,1) PRIMARY KEY,
    effect_name VARCHAR(100)
);

CREATE TABLE post_media_effect (
    post_media_id INT FOREIGN KEY REFERENCES post_media(post_media_id) ON DELETE CASCADE,
    effect_id INT FOREIGN KEY REFERENCES effect(id),
    PRIMARY KEY (post_media_id, effect_id)
);

CREATE TABLE reaction (
    user_id INT FOREIGN KEY REFERENCES [user](user_id),
    post_id INT FOREIGN KEY REFERENCES post(post_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, post_id)
);

CREATE TABLE comment (
    id INT IDENTITY(1,1) PRIMARY KEY,
    created_by_user_id INT FOREIGN KEY REFERENCES [user](user_id),
    post_id INT FOREIGN KEY REFERENCES post(post_id) ON DELETE CASCADE,
    created_datetime DATETIME DEFAULT GETDATE(),
    comment TEXT NOT NULL,
    comment_replied_to_id INT FOREIGN KEY REFERENCES comment(id)
);

CREATE TABLE product (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    business_id INT FOREIGN KEY REFERENCES business_account(business_id),
    product_name VARCHAR(100),
    price DECIMAL(10, 2),
    description TEXT,
    available_stock INT
);

CREATE TABLE post_product_tag (
    post_id INT FOREIGN KEY REFERENCES post(post_id) ON DELETE CASCADE,
    product_id INT FOREIGN KEY REFERENCES product(product_id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, product_id)
);

CREATE TABLE post_media_user_tag (
    post_media_id INT FOREIGN KEY REFERENCES post_media(post_media_id) ON DELETE CASCADE,
    user_id INT FOREIGN KEY REFERENCES [user](user_id),
    x_coordinate INT,
    y_coordinate INT,
    PRIMARY KEY (post_media_id, user_id)
);

CREATE TABLE advertisement (
    ad_id INT IDENTITY(1,1) PRIMARY KEY,
    created_by_user_id INT FOREIGN KEY REFERENCES [user](user_id),
    post_id INT FOREIGN KEY REFERENCES post(post_id) ON DELETE CASCADE,
    product_id INT FOREIGN KEY REFERENCES product(product_id) ON DELETE CASCADE,
    created_datetime DATETIME DEFAULT GETDATE(),
    target_audience TEXT,
    start_date DATE,
    end_date DATE
);

CREATE TABLE ad_insight (
    ad_id INT FOREIGN KEY REFERENCES advertisement(ad_id) ON DELETE CASCADE,
    views_count INT DEFAULT 0,
    clicks_count INT DEFAULT 0,
    impressions INT DEFAULT 0,
    engagement_rate DECIMAL(5, 2),
    cost_per_click DECIMAL(10, 2),
    cost_per_mille DECIMAL(10, 2),
    PRIMARY KEY (ad_id)
);

CREATE TABLE collection (
    collection_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES [user](user_id),
    collection_name VARCHAR(100),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE collection_post (
    collection_id INT FOREIGN KEY REFERENCES collection(collection_id),
    post_id INT FOREIGN KEY REFERENCES post(post_id) ON DELETE CASCADE,
    PRIMARY KEY (collection_id, post_id)
);

CREATE TABLE saved_post (
    user_id INT FOREIGN KEY REFERENCES [user](user_id),
    post_id INT FOREIGN KEY REFERENCES post(post_id) ON DELETE CASCADE,
    saved_at DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (user_id, post_id)
);

CREATE TABLE follower (
    following_user_id INT FOREIGN KEY REFERENCES [user](user_id),
    followed_user_id INT FOREIGN KEY REFERENCES [user](user_id),
    created_at DATETIME DEFAULT GETDATE(),
    status VARCHAR(50),
    PRIMARY KEY (following_user_id, followed_user_id)
);

CREATE TABLE user_activity (
    user_id INT FOREIGN KEY REFERENCES [user](user_id),
    activity_type VARCHAR(50),
    related_post_id INT FOREIGN KEY REFERENCES post(post_id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (user_id, related_post_id)
);