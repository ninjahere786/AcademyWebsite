from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = "static/uploads"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirects unauthorized users to login page

# Ensure the upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# User model (Admin only)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Video model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@login_manager.unauthorized_handler
def unauthorized():
    flash("You must log in to access this page.", "warning")
    return redirect(url_for("login"))

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Ensure the database table exists
with app.app_context():
    db.create_all()


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        new_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        flash("Message sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# Home Page
@app.route("/") 
def home():
    videos = Video.query.all()
    return render_template("index.html", videos=videos)

@app.route("/messages")
@login_required  # Protect this page (only logged-in users can view)
def messages():
    all_messages = ContactMessage.query.all()
    return render_template("messages.html", messages=all_messages)


# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Admin Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # Make sure this is present
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")


# Admin Panel
@app.route("/dashboard")
@login_required
def dashboard():
    videos = Video.query.all()
    return render_template("dashboard.html", videos=videos)


# Upload Video
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    title = request.form["title"]
    video = request.files["video"]

    if video:
        filename = secure_filename(video.filename)
        video.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        new_video = Video(title=title, filename=filename)
        db.session.add(new_video)
        db.session.commit()
        flash("Video uploaded successfully!", "success")
    else:
        flash("No video uploaded!", "danger")

    return redirect(url_for("dashboard"))

# Delete Video
@app.route("/delete/<int:id>")
@login_required
def delete_video(id):
    video = Video.query.get(id)
    if video:
        video_path = os.path.join(app.config["UPLOAD_FOLDER"], video.filename)
        if os.path.exists(video_path):
            os.remove(video_path)  # Delete file safely
        db.session.delete(video)
        db.session.commit()
        flash("Video deleted!", "success")
    else:
        flash("Video not found!", "danger")

    return redirect(url_for("dashboard"))

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

# Initialize Database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Create admin user if not exists
        if not User.query.filter_by(username="admin").first():
            hashed_password = generate_password_hash("admin123", method="pbkdf2:sha256")
            new_admin = User(username="admin", password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            print("Admin account created! Username: admin, Password: admin123")

    app.run(debug=True)
