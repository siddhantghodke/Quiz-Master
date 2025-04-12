from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# --------------------- User Model ---------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False) 
   

    # One user can attempt multiple quizzes
    scores = db.relationship('Score', back_populates='user', cascade="all, delete-orphan")


# --------------------- Subject Model ---------------------
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
   

    # One subject can have multiple chapters
    chapters = db.relationship('Chapter', back_populates='subject', cascade="all, delete-orphan")


# --------------------- Chapter Model ---------------------
class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    subject = db.relationship('Subject', back_populates='chapters')
    quizzes = db.relationship('Quiz', back_populates='chapter', cascade="all, delete-orphan")


# --------------------- Quiz Model ---------------------
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date_of_quiz = db.Column(db.DateTime, default=db.func.current_timestamp())
    time_duration = db.Column(db.Integer, nullable=False)  # In seconds
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)  # Can be NULL if no image
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    
    chapter = db.relationship('Chapter', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz', cascade="all, delete-orphan")
    scores = db.relationship('Score', back_populates='quiz', cascade="all, delete-orphan")


# --------------------- Question Model ---------------------
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Integer, nullable=False)  # Stores 1,2,3,4 as answer choices
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)

    quiz = db.relationship('Quiz', back_populates='questions')


# --------------------- Score Model ---------------------
class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time_stamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_score = db.Column(db.Integer, nullable=False)


    user = db.relationship('User', back_populates='scores')
    quiz = db.relationship('Quiz', back_populates='scores')
