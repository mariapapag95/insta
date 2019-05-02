import sqlite3

connection = sqlite3.connect('insta.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE, 
    password VARCHAR
    );''')

cursor.execute('''CREATE TABLE posts(
    post_id INTEGER PRIMARY KEY,
    username INTEGER,
    photo BLOB, 
    caption TEXT,
    time VARCHAR,
    likes INTEGER DEFAULT '0',
    reposts INTEGER DEFAULT '0',
    type VARCHAR,
    reposted_from VARCHAR,
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (reposted_from) REFERENCES users(username)
    );''')    

cursor.execute('''CREATE TABLE reposts(
    repost_id INTEGER PRIMARY KEY,
    user_who_reposted VARCHAR,
    reposted_from VARCHAR,
    post_id INTEGER,
    time VARCHAR,
    FOREIGN KEY (user_who_reposted) REFERENCES users(username)
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);''')

cursor.execute('''CREATE TABLE likes(
    like_id INTEGER PRIMARY KEY,
    user_who_liked VARCHAR,
    liked_from VARCHAR,
    post_id INTEGER,
    time VARCHAR,
    FOREIGN KEY (user_who_liked) REFERENCES users(username)
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);''')

connection.commit()
cursor.close()