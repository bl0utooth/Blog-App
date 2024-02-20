"""Models for Blogly."""

from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Windows_10_Default_Profile_Picture.svg/640px-Windows_10_Default_Profile_Picture.svg.png'

class User(db.model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, 
    primary_key=True)
    first_name = db.Column(db.Text, 
    nullable=False)
    last_name = db.Column(db.Text, 
    nullable=False)
    image_url = db.Column(db.Text, 
    nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, 
    primary_key=True)
    title = db.Column(db.Text,
    nullable=False)
    content = db.Column(db.Text,
    nullable=False)
    create_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        return self.create_time.strftime("%b %-d, %Y")

class TaggedPost(db.model):
   __tablename__ = 'tag_posts'

   post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key = True)
   tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False, unique = True)

    posts = db.relationship(
        'Post',
        secondary = 'posts_tags',
        backred = 'tags',
    ) 

def connect_db(app):
    db.app = app
    db.init_app(app)