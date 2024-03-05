"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User,Post,Tag,PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
from models import db

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def list_users():
    """shows list of users"""
    users = User.query.all()
    return render_template("home.html",users=users)

@app.route('/users')
def show_all_users_w_detail_link():
    #maybe add in this route links to post by them with the titltes being href?
    """show users with links to details"""
    users = User.query.all()
    return render_template("userdetails.html",users=users) 

@app.route('/users/new')
def create_new_users():
    """page to create user"""
    users = User.query.all()
    return render_template("form.html",users=users)

@app.route('/users/<int:users_id>')
def user_links(users_id):
    """show details for single user"""
    user = User.query.get_or_404(users_id)
    return render_template("singleuserdetails.html",user=user)


@app.route('/users/new',methods=["POST"])
def create_user():
    """POST route to create user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    if not image_url:
        image_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:users_id>/delete',methods=["POST"])
def delete_user(users_id):
    #could of done this with a classmethod and called it on User
    """POST for deleting a user at the id of tht user , on singleuserdetails page"""
    user = User.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:users_id>/edit')
def edit_user(users_id):
    """get user by id and than load page for editing"""
    user = User.query.get_or_404(users_id)
    return render_template("useredit.html",user=user)

@app.route('/users/<int:users_id>/edit',methods=['POST'])
def edit_user_post(users_id):
    """POST for editing a user , handles the form and updates edits """
    user = User.query.get_or_404(users_id)
    
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    if not image_url:
        image_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
    if first_name:
       user.first_name = first_name
    if last_name:
       user.last_name = last_name
    if image_url:
       user.image_url = image_url
    
    db.session.commit()

    return render_template("singleuserdetails.html",user=user)


@app.route('/users/<int:user_id>/post/new')
def make_post(user_id):
    """get req for post form to make new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('newpost.html',user=user,tags=tags)

@app.route('/users/<int:user_id>/post/new',methods=['POST'])
def make_post_post(user_id):
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    selected_tags_id = [int(tag_id) for tag_id in request.form.getlist('tag')]
    selected_tags = [tag for tag in tags if tag.id in selected_tags_id]
    new_post = Post(title=title,content=content,user=user,tags=selected_tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    #user = User.query.get_or_404(post.user_id)
    return render_template("post_page.html",post=post)

@app.route('/post/<int:post_id>/edit')
def edit_post(post_id):
    """get for edit form"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("postedit.html",post=post,tags=tags)

@app.route('/post/<int:post_id>/edit',methods=['POST'])
def edit_post_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    title = request.form['title']
    content = request.form['content']
    selected_tags_id = [int(tag_id) for tag_id in request.form.getlist('tag')]

    
   ##logic for removing already selected tags
    updated_tags = Tag.query.filter(Tag.id.in_(selected_tags_id)).all()
    post.tags = updated_tags
    #MUST FIX THIS DOESNT REMOVE FROM ALREADY SELECTED WHEN PICKING FROM ALREADY SELECTED LISTY
    #if selected_tags_id:
   
    if title:
        post.title = title
    if content:
        post.content = content
   
    
    db.session.commit()

    return redirect(f'/post/{post_id}')

@app.route('/post/<int:post_id>/delete',methods=["POST"])
def delete_post(post_id):
    """POST for deleting a post at the post of tht user , on singleuserdetails page"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/post/all')
def all_post():
     post = Post.query.all()
     return render_template("allpost.html",post=post)


@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('listtags.html',tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tags = Tag.query.get_or_404(tag_id)
    return render_template('tagdetails.html',tags=tags)

@app.route('/tags/new')
def new_tag():
    tags = Tag.query.all()
    return render_template("newtag.html",tags=tags)

@app.route('/tags/new',methods=['POST'])
def new_tag_post():
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
     tags = Tag.query.get_or_404(tag_id)
     return render_template('edittag.html',tags=tags)

@app.route('/tags/<int:tag_id>/edit',methods=['POST'])
def eidt_tag_post(tag_id):
    tags = Tag.query.get_or_404(tag_id)
    name = request.form['name']
    if name:
        tags.name= name

    db.session.commit()

    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete',methods=['POST'])
def delete_tag(tag_id):
    tags = Tag.query.get_or_404(tag_id)
    db.session.delete(tags)
    db.session.commit()
    return redirect('/tags')