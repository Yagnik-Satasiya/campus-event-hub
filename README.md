# 🎓 Campus Event Hub

Campus Event Hub is a full-stack Flask web application designed to help students discover clubs, register for campus events, view announcements, and receive email notifications. 

---

##  Tech Stack

-   **Backend**: Flask (Python)
-   **Database**: MySQL (via XAMPP / Local MySQL Server)
-   **Local Server & Administration**: phpMyAdmin
-   **Deployment**: Vercel (Optional cloud deployment)
-   **Styling**: HTML / CSS

---

##  Local Setup & Development (with XAMPP)

Follow these steps to set up and run the application locally on your machine.

### Prerequisites
1.  **Python 3.x** installed.
2.  **XAMPP** installed and running on your system.

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/campus-event-hub.git
cd campus-event-hub
```

### Step 2: Set Up XAMPP Database
1.  Open the **XAMPP Control Panel**.
2.  Start the **Apache** and **MySQL** services.
3.  Open your browser and navigate to **[http://localhost/phpmyadmin/](http://localhost/phpmyadmin/)**.
4.  Create a new database named: `campus_events_db`.
    *(Note: Flask-SQLAlchemy will automatically create the tables inside this database when the app runs for the first time).*

---

### Step 3: Install Dependencies
Open your project terminal and run:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory (based on `.env.example`) to connect to your local XAMPP MySQL database:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://root:@localhost/campus_events_db
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
```
*(Leave the password empty `root:@localhost` as XAMPP's default MySQL root user does not have a password).*

---

### Step 5: Run the Application
Start the Flask development server:
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser.
