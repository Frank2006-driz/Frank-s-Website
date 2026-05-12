# My Website - Complete Web Application Setup

A modern, full-featured website built with Flask, featuring user authentication, database storage, categories, search functionality, admin panel, and analytics.

## Features

✅ **User Authentication** - Register, login, logout system with secure passwords  
✅ **Database** - SQLite database with user, post, category, and analytics models  
✅ **Create Posts** - Users can create, edit, and delete their posts  
✅ **Categories** - Organize posts by categories  
✅ **Search Functionality** - Full-text search for posts by title and content  
✅ **Admin Panel** - Manage users, categories, and posts  
✅ **Analytics** - Track views, user activity, and post performance  
✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile  
✅ **Form Validation** - Client and server-side validation  
✅ **View Tracking** - Track page views with IP addresses  
✅ **Security** - Password hashing, CSRF protection, admin-only routes  

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── register.html     # Registration page
│   ├── login.html        # Login page
│   ├── dashboard.html    # User dashboard
│   ├── create_post.html  # Create post page
│   ├── view_post.html    # View single post
│   ├── edit_post.html    # Edit post page
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── static/
│   ├── css/
│   │   └── style.css     # Responsive stylesheet
│   └── js/
│       └── main.js       # JavaScript functionality
└── website.db            # SQLite database (created on first run)
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database and Create Admin User

```bash
python setup.py
```

Follow the prompts to:
1. Create database tables
2. Create your admin user account
3. Initialize sample categories

### Step 4: Run the Application

```bash
python app.py
```

The website will be available at `http://localhost:5000`

## Usage

### Creating an Account
1. Click "Register" in the navigation
2. Enter username (min 3 chars), email, and password (min 6 chars)
3. Confirm your password and submit
4. Log in with your credentials

### Logging In
1. Click "Login" in the navigation
2. Enter your username and password
3. You'll be redirected to your dashboard

### Creating a Post
1. After logging in, click "New Post"
2. Enter the post title and content
3. Optionally select a category
4. Click "Publish Post"

### Editing/Deleting Posts
1. Go to your dashboard
2. Click "Edit" to modify a post or "Delete" to remove it
3. Changes are saved immediately

### Viewing Posts
1. Browse all posts on the homepage
2. Use the category filter on the left sidebar
3. Use the search bar to find posts by title or content
4. Click "Read More" on any post to view full content
5. If you're the author, you can edit or delete from the post view

### Search and Filter
- Use the **search bar** in the navigation to find posts
- **Filter by category** on the homepage sidebar
- **View category pages** to see all posts in a specific category

### Admin Panel (Admin Users Only)
1. Click "Admin" in the navigation (only visible for admin users)
2. Access admin dashboard with statistics
3. Manage categories, posts, and users
4. View detailed analytics:
   - Total views and engagement metrics
   - Top posts by view count
   - Posts by category
   - Recent page view activity

#### Admin Features:
- **Dashboard**: Overview of site statistics and recent activity
- **Categories**: Create, view, and delete post categories
- **Posts**: View all posts and delete inappropriate content
- **Users**: View all users and assign/revoke admin privileges
- **Analytics**: Track page views, user activity, and performance metrics

## API Endpoints

### GET /api/posts
Returns paginated posts in JSON format.

**Parameters:**
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 10)
- `category_id` - Filter by category

**Response:**
```json
{
    "posts": [
        {
            "id": 1,
            "title": "Post Title",
            "author": "username",
            "category": "Technology",
            "views": 42,
            "created_at": "2024-01-01T12:00:00"
        }
    ],
    "total": 100,
    "pages": 10,
    "current_page": 1
}
```

### GET /api/categories
Returns all available categories.

**Response:**
```json
[
    {
        "id": 1,
        "name": "Technology",
        "slug": "technology",
        "post_count": 15
    }
]
```

### GET /search
Search for posts by keyword and filter by category.

**Parameters:**
- `q` - Search query
- `category` - Category ID to filter

### GET /category/<id>
View all posts in a specific category.

## New Advanced Features

### 📊 Analytics Dashboard
Track comprehensive site statistics including:
- Total users, posts, and views
- Top performing posts
- Posts grouped by category
- Recent page view history with IP tracking
- Daily/weekly view trends

### 🔍 Search & Filter
- Full-text search across post titles and content
- Filter posts by category
- Combined search + category filtering
- Paginated results

### 📁 Categories
- Organize posts into logical categories
- Browse posts by category
- Category-based view tracking
- Admin category management

### 👥 Admin Panel
Complete site management interface:
- User management with role assignment
- Post moderation and deletion
- Category creation and management
- Detailed analytics and statistics
- Real-time activity tracking

### 📈 View Tracking
- Track page views per post
- Record visitor IP addresses
- Monitor user engagement
- Historical view analytics

## Customization

### Change Secret Key
In `app.py`, replace the secret key (line 11):
```python
app.config['SECRET_KEY'] = 'your-very-secret-key-here'
```

### Change Database
To use PostgreSQL or MySQL instead:
1. Install the database driver: `pip install psycopg2` (PostgreSQL) or `pip install mysql-connector-python` (MySQL)
2. Update `app.py` line 12 with your database URI:
```python
# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'

# MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:password@localhost/dbname'
```

### Change Port
In `app.py`, modify the last line:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change port to 8000
```

### Change Theme Colors
Edit `static/css/style.css` CSS variables (lines 8-18):
```css
:root {
    --primary-color: #007bff;  /* Blue */
    --danger-color: #dc3545;   /* Red */
    /* ... other colors ... */
}
```

## Security Notes

⚠️ **Important for Production:**
1. Set `debug=False` in `app.py`
2. Change the `SECRET_KEY` to a random value
3. Use environment variables for sensitive data
4. Set up HTTPS/SSL
5. Use a production WSGI server (Gunicorn, Waitress)
6. Keep dependencies updated

## Troubleshooting

### Database Issues
- Delete `website.db` and restart the app to reset the database
- Run `python app.py` once to initialize the database

### Port Already in Use
Change the port number in `app.py` from 5000 to another available port

### Dependencies Error
```bash
pip install --upgrade -r requirements.txt
```

## Deployment

### Deploy to Heroku
1. Add `Procfile`:
```
web: gunicorn app:app
```

2. Install Gunicorn:
```bash
pip install gunicorn
```

3. Create Heroku app and deploy:
```bash
heroku create
git push heroku main
```

### Deploy to PythonAnywhere
1. Upload files to PythonAnywhere
2. Create virtual environment
3. Configure WSGI file
4. Reload web app

## Support & Documentation

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Flask-Login: https://flask-login.readthedocs.io/

## License

This project is open source and available under the MIT License.

---

**Happy Coding!** 🚀
