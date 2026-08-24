#  Campus Event Hub

Campus Event Hub is a full-stack Flask web application designed to help students discover clubs, register for campus events, view announcements, and receive email notifications. The project is fully configured for deployment on **Vercel** with a cloud **MySQL** database.

##  Features

-   **User Authentication**: Secure sign-up and login with password hashing.
-   **Club Directory**: Explore campus clubs and their members.
-   **Event Registration**: Register for events with capacity limits.
-   **News Feed**: View announcements and campus updates.
-   **Email Alerts**: Automated mail confirmations sent via Flask-Mail.
-   **Vercel Ready**: Configured using Vercel Serverless Functions (`vercel.json` & `api/index.py`).

---

##  Tech Stack

-   **Backend**: Flask (Python)
-   **Database**: MySQL / Flask-SQLAlchemy
-   **Deployment**: Vercel
-   **Styling**: HTML / CSS

---

##  Local Setup & Development

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/campus-event-hub.git
cd campus-event-hub
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory based on the `.env.example` template:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://root:@localhost/campus_events_db
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
```

### 4. Run the Application
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
