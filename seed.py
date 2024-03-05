from models import User,Post,db,Tag
from app import app
from datetime import datetime



#create all tables
app_context = app.app_context()
app_context.push()

db.drop_all()
db.create_all()

u1 = User(first_name="Paulie",last_name="Walnuts")
u2 = User(first_name="James",last_name="Smith")
u3 = User(first_name="Tammy",last_name="Tams")
u4 = User(first_name="Michael",last_name="Jackson")
u5 = User(first_name="Phil",last_name="Ghale")

db.session.add_all([u1,u2,u3,u4,u5])
db.session.commit()

p1 = Post(title="first post" ,content="glad to be here", created_at=datetime.utcnow(),user_id=u1.id)
p2 = Post(title="second post" ,content="glad to be here again", created_at=datetime.utcnow(),user_id=u1.id)
p3 = Post(title="new here" ,content="thanks for the warm welcomes", created_at=datetime.utcnow(),user_id=u2.id)
p4 = Post(title="hello world" ,content="dogs r cool", created_at=datetime.utcnow(),user_id=u3.id)
p5 = Post(title="whats up" ,content="hows everyone doing", created_at=datetime.utcnow(),user_id=u4.id)
p6 = Post(title="cheers mates" ,content="whos going to the game tonight?", created_at=datetime.utcnow(),user_id=u5.id)

db.session.add_all([p1,p2,p3,p4,p5,p6])
db.session.commit()

#t1 = Tag(name = "funny")
#t2 = Tag(name = "fun")
#t3 = Tag(name = "happy")
#t4 = Tag(name = "art")
#t5 = Tag(name = "cool")
#t6 = Tag(name = "swag")
#t7 = Tag(name = "flaskCrew")

#db.session.add_all([t1,t2,t3,t4,t5,t6])
#db.session.commit()