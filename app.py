from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, or_, func
from functools import wraps
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    page_views = db.relationship('PageView', backref='viewer', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='category', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    page_views = db.relationship('PageView', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Post {self.title}>'

class PageView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ip_address = db.Column(db.String(50))
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    total_views = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    new_posts = db.Column(db.Integer, default=0)
    new_users = db.Column(db.Integer, default=0)

# ==================== DECORATORS ====================

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return 'Access Denied', 403
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== HELPER FUNCTIONS ====================

def get_client_ip():
    if request.environ.get('HTTP_CF_CONNECTING_IP'):
        return request.environ.get('HTTP_CF_CONNECTING_IP')
    return request.remote_addr

def record_page_view(post_id):
    page_view = PageView(
        post_id=post_id,
        user_id=current_user.id if current_user.is_authenticated else None,
        ip_address=get_client_ip()
    )
    db.session.add(page_view)
    post = Post.query.get(post_id)
    if post:
        post.views += 1
    db.session.commit()

def create_slug(text):
    return text.lower().replace(' ', '-').replace('_', '-')

# ==================== ROUTES ====================

# Home and Public Routes
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    category_id = request.args.get('category', type=int)

    query = Post.query.order_by(Post.created_at.desc())

    if search_query:
        query = query.filter(
            or_(
                Post.title.ilike(f'%{search_query}%'),
                Post.content.ilike(f'%{search_query}%')
            )
        )

    if category_id:
        query = query.filter_by(category_id=category_id)

    posts = query.paginate(page=page, per_page=10)
    categories = Category.query.all()

    return render_template('index.html', posts=posts, categories=categories, search_query=search_query, category_id=category_id)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category', type=int)
    page = request.args.get('page', 1, type=int)

    posts_query = Post.query

    if query:
        posts_query = posts_query.filter(
            or_(
                Post.title.ilike(f'%{query}%'),
                Post.content.ilike(f'%{query}%')
            )
        )

    if category_id:
        posts_query = posts_query.filter_by(category_id=category_id)

    posts = posts_query.order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    categories = Category.query.all()

    return render_template('search.html', posts=posts, query=query, categories=categories, category_id=category_id)

@app.route('/category/<int:category_id>')
def view_category(category_id):
    page = request.args.get('page', 1, type=int)
    category = Category.query.get_or_404(category_id)
    posts = category.posts
    posts = sorted(posts, key=lambda x: x.created_at, reverse=True)
    
    from flask_sqlalchemy import Pagination
    total = len(posts)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    items = posts[start:end]
    
    paginated = Pagination(query=None, page=page, per_page=per_page, total=total, items=items)
    categories = Category.query.all()

    return render_template('category.html', category=category, posts=paginated, categories=categories)

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        errors = []

        if not username or not email or not password:
            errors.append('All fields are required')

        if len(username) < 3:
            errors.append('Username must be at least 3 characters')

        if len(password) < 6:
            errors.append('Password must be at least 6 characters')

        if password != confirm_password:
            errors.append('Passwords do not match')

        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')

        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')

        if errors:
            return render_template('register.html', errors=errors), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid username or password'), 401

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# User Dashboard Routes
@app.route('/dashboard')
@login_required
def dashboard():
    user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all()
    total_views = sum(post.views for post in user_posts)
    stats = {
        'total_posts': len(user_posts),
        'total_views': total_views,
        'avg_views': total_views // len(user_posts) if user_posts else 0
    }
    return render_template('dashboard.html', posts=user_posts, stats=stats)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category_id = request.form.get('category_id', type=int)

        errors = []

        if not title or not content:
            errors.append('Title and content are required')

        if len(title) < 5:
            errors.append('Title must be at least 5 characters')

        if len(content) < 20:
            errors.append('Content must be at least 20 characters')

        if errors:
            categories = Category.query.all()
            return render_template('create_post.html', errors=errors, categories=categories), 400

        post = Post(title=title, content=content, user_id=current_user.id, category_id=category_id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('dashboard'))

    categories = Category.query.all()
    return render_template('create_post.html', categories=categories)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    record_page_view(post_id)
    return render_template('view_post.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id and not current_user.is_admin:
        return 'Unauthorized', 403

    if request.method == 'POST':
        post.title = request.form.get('title', '').strip()
        post.content = request.form.get('content', '').strip()
        post.category_id = request.form.get('category_id', type=int)
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))

    categories = Category.query.all()
    return render_template('edit_post.html', post=post, categories=categories)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id and not current_user.is_admin:
        return 'Unauthorized', 403

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('dashboard'))

# Admin Routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_categories = Category.query.count()
    total_views = sum(post.views for post in Post.query.all())

    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    stats = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_categories': total_categories,
        'total_views': total_views,
    }

    return render_template('admin/dashboard.html', stats=stats, recent_posts=recent_posts, recent_users=recent_users)

@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        slug = create_slug(name)

        if not name:
            return render_template('admin/categories.html', error='Category name is required'), 400

        if Category.query.filter_by(slug=slug).first():
            return render_template('admin/categories.html', error='Category already exists'), 400

        category = Category(name=name, description=description, slug=slug)
        db.session.add(category)
        db.session.commit()

        return redirect(url_for('manage_categories'))

    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/category/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('manage_categories'))

@app.route('/admin/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return 'Cannot change your own admin status', 400
    user.is_admin = not user.is_admin
    db.session.commit()
    return redirect(url_for('manage_users'))

@app.route('/admin/posts')
@login_required
@admin_required
def manage_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/posts.html', posts=posts)

@app.route('/admin/post/<int:post_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('manage_posts'))

# Analytics Routes
@app.route('/admin/analytics')
@login_required
@admin_required
def analytics():
    # Get analytics data
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_views = sum(post.views for post in Post.query.all())

    # Top posts by views
    top_posts = Post.query.order_by(Post.views.desc()).limit(10).all()

    # Posts by category
    category_stats = db.session.query(
        Category.name,
        func.count(Post.id).label('count')
    ).join(Post).group_by(Category.name).all()

    # Recent activity
    recent_views = PageView.query.order_by(PageView.viewed_at.desc()).limit(20).all()

    # Views over time (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_views = db.session.query(
        func.date(PageView.viewed_at).label('date'),
        func.count(PageView.id).label('count')
    ).filter(PageView.viewed_at >= thirty_days_ago).group_by(
        func.date(PageView.viewed_at)
    ).all()

    stats = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_views': total_views,
        'top_posts': top_posts,
        'category_stats': category_stats,
        'daily_views': daily_views,
    }

    return render_template('admin/analytics.html', stats=stats, recent_views=recent_views)

# API Routes
@app.route('/api/posts')
def api_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)

    query = Post.query.order_by(Post.created_at.desc())

    if category_id:
        query = query.filter_by(category_id=category_id)

    posts = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'posts': [{
            'id': post.id,
            'title': post.title,
            'author': post.author.username,
            'category': post.category.name if post.category else None,
            'views': post.views,
            'created_at': post.created_at.isoformat()
        } for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    })

@app.route('/api/categories')
def api_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'slug': cat.slug,
        'post_count': len(cat.posts)
    } for cat in categories])

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
