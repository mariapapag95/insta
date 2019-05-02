from mapper import Database
import sqlite3
import datetime

class User:

    def __init__(self, username):
        self.username = username

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
        # TODO

    def signup(self, username, password, confirm):
        try:
            if password == confirm:
                with Database() as db:
                    db.cursor.execute('''INSERT INTO users (username, password)
                                        VALUES(?,?);''',
                                        (username, password))
                return True
        except sqlite3.IntegrityError:
            return False

    def login(self, password):
        with Database() as db:
            db.cursor.execute('''SELECT password FROM users WHERE username="{username}";'''
                .format(username=self.username))
            correct_password = db.cursor.fetchone()
            if correct_password is None:
                return False
            else:
                if correct_password[0] == password:
                    return True
                else:
                    return False

    def post(self, photo, caption):
        time_ = datetime.datetime.now()
        time_ = time_.strftime("%c")
        with Database() as db: 
            db.cursor.execute('''INSERT INTO posts (username, photo, caption, time, type)
                                VALUES (?, ?, ?, ?, ?);''',
                                (self.username, photo, caption, time_, "original"))
            return True

    def like(self, post_id):
        time_ = datetime.datetime.now()
        time_ = time_.strftime("%c")
        with Database() as db:
            db.cursor.execute('''SELECT post_id FROM likes WHERE user_who_liked='{username}' and post_id='{post_id}';'''
                                .format(username = self.username, post_id = post_id))
            user_liked_this_post = db.cursor.fetchone()
            print('USER LIKED THIS POST USER LIKED THIS POST USER LIKED THIS POST')
            print(user_liked_this_post)
            if user_liked_this_post is None:
                print("this user has not yet liked this post")
                db.cursor.execute('''UPDATE posts SET likes = likes + 1 WHERE post_id={post_id};'''
                                    .format(post_id = post_id))
                db.cursor.execute('''INSERT INTO likes (user_who_liked, post_id, time)
                                        VALUES(?,?,?);''',
                                        (self.username, post_id, time_))   
            else: 
                print("THIS IS THE UNLIKE CONDITION")
                db.cursor.execute('''UPDATE posts SET likes = likes - 1 WHERE post_id={post_id};'''
                                    .format(post_id =post_id))                    
                db.cursor.execute('''DELETE FROM likes WHERE post_id={post_id};'''
                                    .format(post_id = post_id))
            return True

# NOW I MUST MAKE THE LIKES UPDATE ON THE POST AND LIKE TABLES FOR THE ORIGINAL POST AS WELL AS THE RETWEETED POSTS 
# THE REPOST COUNTER WORKS FOR THE REPOST FUNCITON 
# THE LIKES MUST ALSO TOGGLE BETWEEN ON AND OFF AND BE COUNTED BY HOW MANY ARE ON 
# I'M PRETTY SURE THIS WOULD WORK BETTER IN THE FRONT END WITH REACT SO LETS TRY IT WHY NOT!
# FOR NOW I NEED RESTART THE DATABASE AND GET THE LIKES UPDATING CORRECTLY 

    def repost(self, post_id):
        reposted_from = '123456789'
        time_ = datetime.datetime.now()
        time_ = time_.strftime("%c")
        with Database() as db:
            db.cursor.execute('''UPDATE posts SET reposts = reposts + 1 WHERE post_id={post_id};'''
                                    .format(post_id = int(post_id)))
            db.cursor.execute('''SELECT * FROM posts WHERE post_id={post_id};'''
                                    .format(post_id = int(post_id)))
            post = db.cursor.fetchall()
            post = post[0]
            db.cursor.execute('''INSERT INTO reposts (user_who_reposted, reposted_from, post_id, time)
                                    VALUES(?,?,?,?);''',
                                    (self.username, reposted_from, post_id, time_))
            db.cursor.execute('''INSERT INTO posts (username, photo, caption, time, likes, reposts, type, reposted_from)
                                VALUES (?,?,?,?,?,?,?,?);''',
                                (self.username, post[2], post[3], time_, post[5], post[6], "repost", post[1]))
        return True
                

class Posts:

    def __init__(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
        # TODO

    def allposts(self):
        with Database() as db:
            db.cursor.execute('''SELECT * FROM posts ORDER BY time DESC;''')
            allposts = db.cursor.fetchall()
            return allposts

    def user_page(self, username):
        with Database() as db:
            db.cursor.execute('''SELECT * FROM posts WHERE username='{username}' ORDER BY time DESC;'''
                    .format(username = username))
            user_posts = db.cursor.fetchall()
            return user_posts