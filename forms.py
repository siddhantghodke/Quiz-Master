from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeLocalField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add User')

class QuizForm(FlaskForm):
    quiz_name = StringField('Quiz Name', validators=[DataRequired()])
    date_of_quiz = DateTimeLocalField('Date of Quiz', validators=[DataRequired()])
    time_duration = IntegerField('Time Duration', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    chapter_id = SelectField('Chapter ID', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Quiz')

class QuestionForm(FlaskForm):  
    question = StringField('Question', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    answer = IntegerField('Correct Option (1-4)', validators=[DataRequired()])
    submit = SubmitField('Add Question')

class ChapterForm(FlaskForm):
    chapter_name = StringField('Chapter Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Chapter')

class SubjectForm(FlaskForm):
    subject_name = StringField('Subject Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Subject')
