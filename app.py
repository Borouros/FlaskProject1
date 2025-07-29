from flask import Flask, render_template, send_file, request, redirect, flash, session, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'PortNewsThe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='viewer')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect('/')
    posts = Post.query.all()
    news_items = News.query.all()
    return render_template('code.html', posts=posts, news=news_items)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role not in ['admin', 'editor']:
        return "Access denied", 403
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            new_post = Post(title=title, content=content, author_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created.")
            return redirect('/admin')
        else:
            flash("Title and content are required.")
    user_posts = Post.query.filter_by(author_id=current_user.id).order_by(Post.id.desc()).all()
    all_users = User.query.all() if current_user.role == 'admin' else []
    news_items = News.query.all()
    return render_template('admin.html', posts=user_posts, users=all_users, news=news_items)

@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def serve_devtools_json():
    file_path = os.path.join(app.root_path, '.well-known/appspecific/com.chrome.devtools.json')
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/json')
    return "Devtools config not found", 404

@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    new_username = request.form.get('username')
    new_password = request.form.get('password')

    if not new_username or not new_password:
        flash("Username and password cannot be empty.", "danger")
        return redirect(url_for('editor'))

    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user and existing_user.id != current_user.id:
        flash("Username already taken.", "danger")
        return redirect(url_for('editor'))

    current_user.username = new_username
    current_user.password = generate_password_hash(new_password)
    db.session.commit()

    flash("Account updated successfully.", "success")
    return redirect(url_for('editor'))


@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.role == 'admin' or post.author_id == current_user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully.")
        except Exception as e:
            db.session.rollback()
            flash("Error deleting post.")
            print(f"Delete error: {e}")
        return redirect('/admin' if current_user.role == 'admin' else '/editor')
    flash("You do not have permission to delete this post.")
    return redirect('/')

@app.route('/update_role', methods=['POST'])
@login_required
def update_role():
    if current_user.role != 'admin':
        return "Access denied", 403
    user_id = request.form.get('user_id')
    new_role = request.form.get('role')
    user = User.query.get(user_id)
    if user:
        if user.id == current_user.id and new_role != 'admin':
            flash("You cannot demote yourself.")
            return redirect('/admin')
        user.role = new_role
        db.session.commit()
        flash(f"Updated {user.username} to {new_role}")
    else:
        flash("User not found.")
    return redirect('/admin')

@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return "Access denied", 403
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    if not all([username, password, role]):
        flash("All fields are required.")
        return redirect('/admin')
    if User.query.filter_by(username=username).first():
        flash("Username already taken.")
        return redirect('/admin')
    hashed_pw = generate_password_hash(password)
    try:
        user = User(username=username, password=hashed_pw, role=role)
        db.session.add(user)
        db.session.commit()
        flash(f"User {username} created with role {role}.")
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
        flash("An error occurred while creating the user.")
    return redirect('/admin')

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return "Access denied", 403
    if current_user.id == user_id:
        flash("You cannot delete yourself.")
        return redirect('/admin')
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} has been deleted.")
    return redirect('/admin')

@app.route('/update_user', methods=['POST'])
@login_required
def update_user():
    if current_user.role != 'admin':
        return "Access denied", 403
    user_id = request.form.get('user_id')
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    user = User.query.get(user_id)
    if user:
        if new_username:
            user.username = new_username
        if new_password:
            user.password = generate_password_hash(new_password)
        db.session.commit()
        flash(f"User {user.username} updated successfully.")
    else:
        flash("User not found.")
    return redirect('/admin')

@app.route('/editor', methods=['GET', 'POST'])
@login_required
def editor():
    if current_user.role != 'editor':
        return "Access denied", 403
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            new_post = Post(title=title, content=content, author_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created.")
            return redirect('/editor')
        else:
            flash("Title and content are required.")
    posts = Post.query.filter_by(author_id=current_user.id).order_by(Post.id.desc()).all()
    return render_template('editor.html', posts=posts)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if current_user.role != 'admin' and post.author_id != current_user.id:
        return "Access denied", 403

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash("Both title and content are required.")
            return redirect(f'/edit_post/{post_id}')

        post.title = title
        post.content = content
        db.session.commit()
        flash("Post updated successfully.")
        return redirect('/admin' if current_user.role == 'admin' else '/editor')

    return render_template('edit_post.html', post=post)

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    if current_user.role not in ['admin', 'editor']:
        return "Access denied", 403

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if title and content:
            item = News(title=title, content=content)
            db.session.add(item)
            db.session.commit()
            flash("News item added.")
            return redirect('/admin' if current_user.role == 'admin' else '/editor')
        flash("Title and content required.")
    
    return render_template('add_news.html')


@app.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    if current_user.role not in ['admin', 'editor']:
        return "Access denied", 403

    item = News.query.get_or_404(news_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash("Title and content required.")
            return redirect(f'/edit_news/{news_id}')
        item.title = title
        item.content = content
        db.session.commit()
        flash("News item updated.")
        return redirect('/admin' if current_user.role == 'admin' else '/editor')

    return render_template('edit_news.html', item=item)


@app.route('/delete_news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def delete_news(news_id):
    if current_user.role not in ['admin', 'editor']:
        return "Access denied", 403

    item = News.query.get_or_404(news_id)

    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash("News item deleted.")
        return redirect('/admin' if current_user.role == 'admin' else '/editor')

    return render_template('delete_news.html', item=item)


@app.route('/setup_user')
def setup_user():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='lukasMekk').first():
            users = User(
                username='lukasMekk',
                password=generate_password_hash('PortTheNews'),
                role='admin'
            )
            db.session.add(users)
            db.session.commit()
            return "User 'lukasMekk' created."
        return "User already exists."
    

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        new_username = request.form.get('user_username')
        new_password = request.form.get('user_password')

        user = User.query.get(current_user.id)

        if new_username and new_username != user.username:
            if User.query.filter_by(username=new_username).first():
                flash("Username already taken.", 'error')                
            else:
                user.username = new_username
                flash("Username updated successfully!")

        if new_password:
            user.password = generate_password_hash(new_password)
            flash("Password updated successfully!")

        db.session.commit()
    return render_template('account.html', user=current_user)

    

with app.app_context():
    db.create_all()



