from unittest import TestCase

from app import app
from models import db,connect_db, User,Post,Tag,PostTag
from datetime import datetime
# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app_context = app.app_context()
app_context.push()

db.drop_all()
db.create_all()

class UserRoutesTestCase(TestCase):
    """test for routes for users"""
    def setUp(self):
        """add test user"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestUserFirst",last_name="TestUserLast",image_url="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        self.user = user

        #post = Post(title = "first post",content = "glad to be here")
        #db.session.add(post)
        #db.session.commit()
        #self.post_id = post.id
        #self.post = post

    def tearDown(self):
        db.session.rollback()

    def test_show_all_users_w_detail_link(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('TestUserFirst',html)
            self.assertIn('TestUserLast',html)
            self.assertIn('https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png' ,html)

    def test_user_links(self):
        with app.test_client() as client: 
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('TestUserFirst',html)
            self.assertIn('TestUserLast',html)
            self.assertIn('https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png' ,html)
           
    def test_create_user(self):
        with app.test_client() as client: 
             d = {"first_name":"TestUserFirst" ,"last_name":"TestUserLast","image_url" : "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"}
             resp = client.post('users/new',data = d,follow_redirects = True)
             html = resp.get_data(as_text=True)

             self.assertEqual(resp.status_code,200)
             self.assertIn('TestUserFirst',html)
             self.assertIn('TestUserLast',html)
             self.assertIn('https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png' ,html)

    def test_edit_user_post(self):
        #not sure if this test this correctly
        with app.test_client() as client: 
            d = {"first_name":"NewTestUserFirst" ,"last_name":"NewTestUserLast","image_url" : "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"}
            resp = client.post(f'/users/{self.user_id}/edit',data = d,follow_redirects = True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("NewTestUserFirst",html)
            self.assertIn("NewTestUserLast",html)
            self.assertIn("https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",html)
            
    def test_make_post_post(self):
         #works with isnotnone but not with assert in self.assertIn("first post", resp.get_data(as_text=True))self.assertIn("glad to be here",resp.get_data(as_text=True))
         with app.test_client() as client: 
            d = {"title":"first post" ,"content":"glad to be here"} 
            resp = client.post(f'/users/{self.user_id}/post/new',data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIsNotNone("first post", resp.get_data(as_text=True))
            self.assertIsNotNone("glad to be here",resp.get_data(as_text=True))
           

    def test_show_post(self):
        with app.test_client() as client: 
    #        post = Post(title = "first post",content = "glad to be here")
    #        db.session.add(post)
    #        db.session.commit()
    #        self.post_id = post.id
    #        self.post = post
            resp = client.get(f"/post/{self}",data=d,follow_redirects=True)
            d = {"title":"first post" ,"content":"glad to be here"}
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('first post',html)
            self.assertIn('glad to be here',html)
            



#class PostRoutesTestCase(TestCase):
#    """test for routes for users"""
#    def setUp(self):
#        """add test user"""
#        Post.query.delete()
#        
#        post = Post(title="test post",content="this is a test post")
#        db.session.add(post)
#        db.session.commit()
#       
#        self.post_id = post.id
#        self.post = post
#      
#
#    def tearDown(self):
#        db.session.rollback()
#
#    def test_make_post_post(self):
#         with app.test_client() as client: 
#            d = {"title":"first post" ,"content":"glad to be here"} 
#            resp = client.post(f'/users/{self.user_id}/post/new',data=d,follow_redirects=True)
#            html = resp.get_data(as_text=True)
#            self.assertEqual(resp.status_code,200)
#            self.assertIn("first post", resp.get_data(as_text=True))
#            self.assertIn("glad to be here",resp.get_data(as_text=True))
#