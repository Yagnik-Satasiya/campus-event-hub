import matplotlib.pyplot as plt
import os
import json
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from config import Config
from models import db, User, Club, Event, News
from datetime import datetime, date
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.config.from_object(Config)
# --- MAIL CONFIGURATION ---
# Credentials are loaded from environment variables (set these in Vercel dashboard)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'govindshastri107@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', 'govindshastri107@gmail.com')

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config.get('SECRET_KEY', 'my_fallback_secret_key'))
db.init_app(app)

UPLOAD_FOLDER = 'static/uploads/news'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.context_processor
def inject_now():
    return {'now': datetime.now}

@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return dict(user=user)
    return dict(user=None)

# ---------------- HOME ----------------
@app.route('/')
def home():
    news_list = News.query.order_by(News.date_posted.desc()).limit(5).all()
    events = Event.query.order_by(Event.event_date.asc()).all()
    return render_template('home.html', news_list=news_list, events=events)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for('register'))

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            password_match = False
            
            # 1. Try plain-text first (for old admin test accounts)
            if user.password == password:
                password_match = True
            else:
                # 2. Try hash verification
                try:
                    if check_password_hash(user.password, password):
                        password_match = True
                except ValueError:
                    # This catches errors if the database string isn't a valid hash format
                    pass

            if password_match:
                # 3. Save ALL needed info into the session securely
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['is_admin'] = user.is_admin
                session['profile_picture'] = user.profile_picture

                flash("Login successful")

                if user.is_admin:
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('dashboard'))

        flash("Invalid email or password")
    return render_template('login.html')

# ---------------- ADMIN LOGIN ----------------
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = User.query.filter_by(email=email, is_admin=True).first()

        if admin and (check_password_hash(admin.password, password) or admin.password == password):
            session['user_id'] = admin.id
            session['user_name'] = admin.name
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))

        flash("Invalid admin credentials")

    return render_template('admin_login.html')


# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    events = Event.query.order_by(Event.event_date.asc()).all()
    clubs = Club.query.all()
    news_list = News.query.order_by(News.date_posted.desc()).all()

    total_events = Event.query.count()
    total_clubs = Club.query.count()
    total_users = User.query.count()
    total_news = News.query.count()

    # Data for Chart.js
    club_names = [club.name for club in clubs]
    member_counts = [len(club.members) for club in clubs]

    return render_template(
        'admin_dashboard.html',
        events=events,
        clubs=clubs,
        news_list=news_list,
        total_events=total_events,
        total_clubs=total_clubs,
        total_users=total_users,
        total_news=total_news,
        club_names=club_names,
        member_counts=member_counts
    )

@app.route('/admin-logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

# ---------------- USER DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    clubs = Club.query.all()
    events = Event.query.order_by(Event.event_date.asc()).all()
    participated_events = user.events
    return render_template(
        'dashboard.html',
        user=user,
        clubs=clubs,
        events=events,
        participated_events=participated_events
    )

# ---------------- USER PROFILE ----------------
# ---------------- USER PROFILE ----------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # 1. Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # 2. Get the current user from the database
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # 3. Grab the new name and password from the form
        new_name = request.form.get('name')
        new_password = request.form.get('password')
        
        # 4. Update the name if they typed one
        if new_name:
            user.name = new_name
            session['user_name'] = new_name  # This instantly updates the name in your Navbar!
            
        # 5. Update password ONLY if they typed a new one
        if new_password and new_password.strip():
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            
        # 5B. Handle Profile Picture Upload
        profile_pic = request.files.get('profile_picture')
        if profile_pic and profile_pic.filename != '':
            filename = secure_filename(profile_pic.filename)
            # Create a dedicated avatars folder if it doesn't exist
            pic_path = os.path.join(app.root_path, 'static', 'uploads', 'avatars')
            os.makedirs(pic_path, exist_ok=True)
            profile_pic.save(os.path.join(pic_path, filename))
            
            user.profile_picture = filename
            session['profile_picture'] = filename

        # 6. FORCE the database to save the changes
        db.session.add(user)
        db.session.commit()
        
        flash("Profile updated successfully!", "success")
        return redirect(url_for('dashboard'))
        
    return render_template('profile.html', user=user)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- ADD/EDIT/DELETE CLUB ----------------
@app.route('/add-club', methods=['GET', 'POST'])
def add_club():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        club = Club(name=request.form['name'], description=request.form['description'])
        db.session.add(club)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('add_club.html')

@app.route('/edit_club/<int:id>', methods=['GET', 'POST'])
def edit_club(id):
    if not session.get('is_admin'):
        flash("Access denied!")
        return redirect(url_for('admin_login'))

    club = Club.query.get_or_404(id)
    if request.method == 'POST':
        club.name = request.form['name']
        club.description = request.form['description']
        db.session.commit()
        flash("Club updated successfully!")
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_club.html', club=club)

@app.route('/delete-club/<int:id>')
def delete_club(id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    club = Club.query.get_or_404(id)
    db.session.delete(club)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


# ---------------- ADD/EDIT/DELETE EVENT ----------------
@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if not session.get('is_admin'):
        flash("Admins only")
        return redirect(url_for('admin_login'))

    clubs = Club.query.all()
    if request.method == 'POST':
        poster_file = request.files.get('poster')
        poster_filename = None

        if poster_file and poster_file.filename != '':
            poster_filename = secure_filename(poster_file.filename)
            poster_file.save(os.path.join(app.root_path, 'static/uploads', poster_filename))

        new_event = Event(
            title=request.form['title'],
            event_date=datetime.strptime(request.form['event_date'], "%Y-%m-%d").date(),
            reg_start=datetime.strptime(request.form['reg_start'], "%Y-%m-%d").date(),
            reg_end=datetime.strptime(request.form['reg_end'], "%Y-%m-%d").date(),
            location=request.form['location'],
            club_id=request.form['club_id'],
            form_link=request.form['form_link'],
            poster=poster_filename
        )

        db.session.add(new_event)
        db.session.commit()
        flash("Event added successfully!")
        return redirect(url_for('admin_dashboard'))

    return render_template('add_event.html', clubs=clubs)

@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    if not session.get('is_admin'):
        flash("Access denied!")
        return redirect(url_for('admin_login'))

    event = Event.query.get_or_404(id)
    clubs = Club.query.all()
    if request.method == 'POST':
        event.title = request.form['title']
        event.event_date = request.form['date']
        event.reg_start = request.form['reg_start']
        event.reg_end = request.form['reg_end']
        event.location = request.form['location']
        event.club_id = request.form['club_id']
        event.form_link = request.form.get('form_link')
        db.session.commit()
        flash("Event updated successfully!")
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_event.html', event=event, clubs=clubs)

@app.route('/delete-event/<int:id>')
def delete_event(id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


# ---------------- PUBLIC LISTINGS & SEARCH ----------------
@app.route('/clubs')
def clubs():
    clubs = Club.query.all()
    user = User.query.get(session['user_id']) if 'user_id' in session else None
    return render_template('clubs.html', clubs=clubs, user=user)

@app.route('/events')
def events():
    search_query = request.args.get('q', '')
    # Get the current page number from the URL (default is 1)
    page = request.args.get('page', 1, type=int)
    
    if search_query:
        # Show 6 events per page
        events_pagination = Event.query.filter(Event.title.ilike(f'%{search_query}%')).order_by(Event.event_date.asc()).paginate(page=page, per_page=6)
    else:
        events_pagination = Event.query.order_by(Event.event_date.asc()).paginate(page=page, per_page=6)
        
    today = date.today().isoformat()
    return render_template('events.html', events_pagination=events_pagination, today=today, search_query=search_query)


# ---------------- JOINING CLUBS & EVENTS ----------------
@app.route('/view-club/<int:id>')
def view_club(id):
    club = Club.query.get_or_404(id)
    events = Event.query.filter_by(club_id=id).order_by(Event.event_date.asc()).all()
    joined = False
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        joined = club in user.clubs
    return render_template('view_club.html', club=club, events=events, joined=joined)

@app.route('/join-club/<int:id>')
def join_club(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    club = Club.query.get_or_404(id)
    if club not in user.clubs:
        user.clubs.append(club)
        db.session.commit()
    return redirect(url_for('view_club', id=id))

@app.route('/participate/<int:event_id>')
def participate_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    event = Event.query.get_or_404(event_id)

    # Enforce capacity limit
    if event.participants.count() >= event.capacity:
        flash("Sorry, this event is already sold out!", "error")
        return redirect(url_for('events'))

    if event not in user.events:
        user.events.append(event)
        db.session.commit()
        
    return render_template("redirect_form.html", form_link=event.form_link)

# --- NEW: CALENDAR ROUTES ---
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/api/events')
def api_events():
    # This sends data to FullCalendar.js
    events = Event.query.all()
    events_data = []
    for event in events:
        events_data.append({
            'title': event.title,
            'start': str(event.event_date), # Native stringification forces YYYY-MM-DD for FullCalendar
            'url': url_for('participate_event', event_id=event.id),
            'color': '#6d28d9' if event.participants.count() < event.capacity else '#dc3545' # Purple if open, Red if full
        })
    return jsonify(events_data)

# ---------------- PASSWORD RESET ROUTES ----------------
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate a secure token valid for 1 hour
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_url = url_for('reset_token', token=token, _external=True)
            
            # Create and send the email
            msg = Message('Reset Your Password - Campus Events', recipients=[email])
            msg.body = f'''To reset your password, visit the following link:{reset_url}

If you did not make this request, simply ignore this email and no changes will be made.
'''
            try:
                mail.send(msg)
            except Exception as e:
                flash("Error sending email. Please check your Mail Configuration.", "error")
                return redirect(url_for('reset_password_request'))
                
        flash('If an account with that email exists, a reset link has been sent.', 'success')
        return redirect(url_for('login'))
        
    return render_template('reset_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    try:
        # Check if the token is valid and hasn't expired (3600 seconds = 1 hour)
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('reset_password_request'))
        
    if request.method == 'POST':
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user:
            user.password = password
            db.session.commit()
            flash('Your password has been updated! You can now log in.', 'success')
            return redirect(url_for('login'))
            
    return render_template('reset_token.html')

@app.route('/admin-event-users/<int:event_id>')
def admin_event_users(event_id):
    if not session.get('is_admin'):
        flash("Admins only!")
        return redirect(url_for('admin_login'))
    event = Event.query.get_or_404(event_id)
    users = event.participants.all()
    return render_template('admin_event_users.html', event=event, users=users)


# ---------------- NEWS MANAGEMENT ----------------
@app.route('/add-news', methods=['GET', 'POST'])
def add_news():
    if not session.get('is_admin'):
        flash("Access denied! Admins only.")
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        poster_file = request.files.get('poster')
        poster_filename = None
        if poster_file and poster_file.filename != '':
            poster_filename = secure_filename(poster_file.filename)
            poster_file.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))
        news_item = News(title=title, description=description, poster=poster_filename)
        db.session.add(news_item)
        db.session.commit()
        flash("News added successfully!")
        return redirect(url_for('admin_dashboard'))
    return render_template('add_news.html')

@app.route('/news/<int:id>')
def view_news(id):
    news = News.query.get_or_404(id)
    return render_template('view_news.html', news=news)

@app.route('/edit-news/<int:id>', methods=['GET', 'POST'])
def edit_news(id):
    if not session.get('is_admin'):
        flash("Access denied! Admins only.")
        return redirect(url_for('admin_login'))
    news_item = News.query.get_or_404(id)
    if request.method == 'POST':
        news_item.title = request.form['title']
        news_item.description = request.form['description']
        poster_file = request.files.get('poster')
        if poster_file and poster_file.filename != '':
            poster_filename = secure_filename(poster_file.filename)
            poster_file.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))
            news_item.poster = poster_filename
        db.session.commit()
        flash("News updated successfully!")
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_news.html', news=news_item)

@app.route('/delete-news/<int:id>')
def delete_news(id):
    if not session.get('is_admin'):
        flash("Access denied! Admins only.")
        return redirect(url_for('admin_login'))
    news_item = News.query.get_or_404(id)
    if news_item.poster:
        poster_path = os.path.join(app.config['UPLOAD_FOLDER'], news_item.poster)
        if os.path.exists(poster_path):
            os.remove(poster_path)
    db.session.delete(news_item)
    db.session.commit()
    flash("News deleted successfully!")
    return redirect(url_for('admin_dashboard'))

# ---------------- RUN ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    