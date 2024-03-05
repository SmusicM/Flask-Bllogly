"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    @classmethod
    def get_fullname(cls,first_name,last_name):
        return f"{first_name}{last_name}"

    def  __repr__(self):
        u=self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url = {u.image_url}"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                          nullable = False,
                          unique=False) #may change and may change unique for obvi reaso
    last_name = db.Column(db.String(50),
                          nullable = False,
                          unique = False)
    image_url = db.Column(db.String(300),
                          nullable = False,
                          unique = False,
                          default = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                          nullable = False,
                          unique=False)
    content = db.Column(db.String(300),
                        nullable=False,
                        unique=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)

    user = db.relationship("User",backref="posts")

    post_tags_assign = db.relationship('PostTag',backref = "post")

    tags = db.relationship('Tag',secondary = "post_tag",backref = "posts")
    def __repr__(self):
        return f"<Posts {self.title} {self.content} {self.created_at}>"
    

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text,nullable=False,unique=True)

    post_tags_assign = db.relationship('Post',secondary = "post_tag",backref = "tag")

class PostTag(db.Model):
    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"),primary_key = True)

    tag_id = db.Column(db.Integer,db.ForeignKey("tags.id"),primary_key = True)