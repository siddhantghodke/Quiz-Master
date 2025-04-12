# Quiz Master - V1 🎓✨  

Welcome to **Quiz Master - V1**, a multi-user quiz application built by me to help users prepare for exams across multiple courses! This platform features two roles: **Admin** (Quiz Master) and **Users**, enabling efficient quiz creation and management while providing an engaging experience for learners. 🚀  

---

## Features 🌟  

### **Admin (Quiz Master)** 🧑‍🏫  
- Full root access with no registration required.  
- Manage users, subjects, chapters, quizzes, and questions effortlessly.  
- Create subjects and subdivide them into chapters.  
- Add quizzes under chapters with multiple-choice questions (MCQs).  
- Specify quiz dates, durations, and remarks.  
- View summary charts and search users/subjects/quizzes.  

### **User** 👩‍🎓👨‍🎓  
- Register/login to access the platform.  
- Attempt quizzes from various subjects and chapters.  
- View previous quiz scores and attempts.  
- Enjoy a user-friendly dashboard with summary charts.  

---

## Technologies Used 💻  

### **Back-End** 🔧  
- Flask  

### **Front-End** 🎨  
- Jinja2 templating  
- HTML, CSS, Bootstrap  

### **Database** 🗄️  
- SQLite  

---

## Installation & Setup 🛠️  

Follow these steps to set up the application on your local machine:  

1. **Clone the repository:**  
```
git clone https://github.com/<your-github-username>/quiz-master-v1.git
cd quiz-master-v1
```

2. **Create a virtual environment:**  
```
python -m venv env
source env/bin/activate # For Linux/Mac
env\Scripts\activate # For Windows
```

3. **Install dependencies:**  
```
pip install -r requirements.txt
```

4. **Run the application:**  
```
python main.py
```

5. **Access the app:**  
Open your browser and navigate to `http://127.0.0.1:5000`. 🎉  

---

## Database Initialization 📂  

The database is created programmatically when you run the application for the first time. No manual database creation is required! The admin account will be pre-configured in the database upon initialization.  

---

## Functionalities Implemented 🔍  

- Summary charts using external libraries like Chart.js 📊.  
- Frontend validation using HTML5 and JavaScript ✅.  
- Backend validation within controllers 🔐.  
- Responsive designs using CSS/Bootstrap ✨.  
- Secure login system using Flask extensions like `flask_login` 🔒.

---








