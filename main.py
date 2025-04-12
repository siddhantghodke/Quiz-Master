from flask import Flask, url_for, render_template, redirect, request, flash, session, request
from model import *
import os
from forms import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = "khdeiuhuefhrnkjbfjkhj"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(current_dir, "database.sqlite3") 

db.init_app(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.username == "Admin" and user.password == form.password.data:
            session['user'] = user.username
            login_user(user)
            flash("Admin Login Successfull!", "success")
            return redirect('admin_dashboard')

        if user and user.password == form.password.data:
            session['user'] = user.username
            login_user(user)
            flash("You have been logged in!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Credentials", "error")

    return render_template('login.html', form = form)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect('login')
    return render_template('signup.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    flash('You are now logged out')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    quiz = Quiz.query.all()
    if 'user' in session:
        user = session['user']
        return render_template('dashboard.html', quiz=quiz, user=user)
    
    else:
        flash('You are not logged in')
        return redirect(url_for('login'))
    

@app.route('/filter', methods=['POST', 'GET'])
def filter():
    value = request.form['searchKey']
    searchType = request.form['filterOptions']
    if searchType == "Quiz_Name":
        result = Quiz.query.filter(Quiz.name.like('%' + value + '%')).all()
    elif searchType == "Date":
        result = Quiz.query.filter(Quiz.date_of_quiz.like('%' + value + '%')).all()
    # Filter by Chapters
    elif searchType == "Chapters":
        result = Quiz.query.join(Chapter).filter(Chapter.name.like('%' + value + '%')).all()

    # Filter by Subjects
    elif searchType == "Subjects":
        result = Quiz.query.join(Chapter).join(Subject).filter(Subject.name.like('%' + value + '%')).all()

    return render_template('filter.html', data=result)


@app.route('/search_chapters', methods=['POST','GET'])
@login_required
def search_chapters():
    if request.method=='POST':
        searchkey = request.form.get('searchkey')    
        chapter_results = Chapter.query.filter(Chapter.name.ilike(f"{searchkey}%")).all()
    return render_template('/Admin/search_chapters.html',chapter=chapter_results)


@app.route('/search_subjects', methods=['POST','GET'])
@login_required
def search_subjects():
    if request.method=='POST':
        searchkey = request.form.get('searchkey')
        subject_results = Subject.query.filter(Subject.name.ilike(f"{searchkey}%")).all()
    return render_template('/Admin/search_subjects.html',subject = subject_results)

@app.route('/search_quiz', methods=['POST','GET'])
@login_required
def search_quiz():
    if request.method=='POST':
        searchkey = request.form.get('searchkey')
        quiz_results = Quiz.query.filter(Quiz.name.ilike(f"{searchkey}%")).all()
    return render_template('/Admin/search_quiz.html',quiz=quiz_results)

@app.route('/search_user', methods=['POST','GET'])
@login_required
def search_user():
    if request.method=='POST':
        searchkey = request.form.get('searchkey')
        user_results = User.query.filter(User.username.ilike(f"{searchkey}%")).all()
    return render_template('/Admin/search_user.html',user=user_results)

@app.route('/search_score', methods=['POST','GET'])
@login_required
def search_score():
    if request.method=='POST':
        searchkey = request.form.get('searchkey')
        score_results = Score.query.filter(Score.total_score.ilike(f"{searchkey}%")).all()
    return render_template('/Admin/search_score.html',score= score_results)



@app.route('/admin_dashboard')
def Admin_Dashboard():
    quizzes = Quiz.query.all()
    quiz_names = [quiz.name for quiz in quizzes]
    average_scores = []
    completion_rates = []

    for quiz in quizzes:
        scores = Score.query.filter_by(quiz_id=quiz.id).all()
        if scores:
            average_score = sum([score.total_score for score in scores]) / len(scores) if scores else 0
            user_attempted = len(scores)
            completion_rate = (user_attempted / (User.query.count() - 1)) * 100
        else:
            average_score = 0
            completion_rate = 0
        average_scores.append(average_score)
        completion_rates.append(completion_rate)
    return render_template('Admin/admin_dashboard.html', quiz_names=quiz_names, 
                                                         average_scores=average_scores, 
                                                        completion_rates=completion_rates)


@app.route('/manage_quizzes')
def manage_quizzes():
    quizzes = Quiz.query.all()
    return render_template('Admin/manage_quizzes.html', quizzes=quizzes)

@app.route('/add_quiz', methods=['POST', 'GET'])
@login_required
def add_quiz():
    form = QuizForm()
    form.chapter_id.choices = [(chapter.id, chapter.name) for chapter in Chapter.query.all()]
    if form.validate_on_submit():
        quiz = Quiz(
            name=form.quiz_name.data,
            date_of_quiz=form.date_of_quiz.data,
            time_duration=form.time_duration.data,
            description=form.description.data,
            image=form.image.data,
            chapter_id=form.chapter_id.data)
        db.session.add(quiz)
        db.session.commit()
        flash("Quiz added successfully!", "success")
        return redirect(url_for('manage_quizzes'))
    return render_template('Admin/add_quiz.html', form=form)

@app.route('/edit_quiz/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    form = QuizForm(obj=quiz)
    form.chapter_id.choices = [(chapter.id, chapter.name) for chapter in Chapter.query.all()]
    if form.validate_on_submit():
        quiz.name = form.quiz_name.data
        quiz.date_of_quiz = form.date_of_quiz.data
        quiz.time_duration = form.time_duration.data
        quiz.description = form.description.data
        quiz.image = form.image.data
        quiz.chapter_id = form.chapter_id.data
        db.session.commit()
        flash("Quiz updated successfully!", "success")
        return redirect(url_for('manage_quizzes'))
    return render_template('Admin/edit_quiz.html', form=form, quiz=quiz)

@app.route('/delete_quiz/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted successfully!", "success")
    return redirect(url_for('manage_quizzes'))


@app.route('/manage_users')
def manage_users():
    users = User.query.all()
    return render_template('Admin/manage_users.html', users=users)

@app.route('/add_user', methods=['POST', 'GET'])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User added successfully!", "success")
        return redirect(url_for('manage_users'))
    return render_template('Admin/add_user.html', form=form)

@app.route('/edit_user/<int:id>', methods=['POST', 'GET'])
@login_required 
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('manage_users'))
    return render_template('Admin/edit_user.html', form=form, user=user)

@app.route('/delete_user/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for('manage_users'))


@app.route('/manage_chapters')
def manage_chapters():
    chapters = Chapter.query.all()
    return render_template('Admin/manage_chapters.html', chapters=chapters)

@app.route('/add_chapter', methods=['POST', 'GET'])
@login_required
def add_chapter():
    form = ChapterForm()
    form.subject_id.choices = [(subject.id, subject.name) for subject in Subject.query.all()]
    if form.validate_on_submit():
        chapter = Chapter(
            name=form.chapter_name.data,
            description=form.description.data,
            subject_id=form.subject_id.data)
        db.session.add(chapter)
        db.session.commit()
        flash("Chapter added successfully!", "success")
        return redirect(url_for('manage_chapters'))
    return render_template('Admin/add_chapter.html', form=form)

@app.route('/edit_chapter/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    form = ChapterForm(obj=chapter)
    form.subject_id.choices = [(subject.id, subject.name) for subject in Subject.query.all()]
    if form.validate_on_submit():
        chapter.name = form.chapter_name.data
        chapter.description = form.description.data
        chapter.subject_id = form.subject_id.data
        db.session.commit()
        flash("Chapter updated successfully!", "success")
        return redirect(url_for('manage_chapters'))
    return render_template('Admin/edit_chapter.html', form=form, chapter=chapter)

@app.route('/delete_chapter/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted successfully!", "success")
    return redirect(url_for('manage_chapters'))




@app.route('/manage_subjects')
def manage_subjects():
    subjects = Subject.query.all()
    return render_template('Admin/manage_subjects.html', subjects=subjects)

@app.route('/add_subject', methods=['POST', 'GET'])
@login_required
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.subject_name.data,
            description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash("Subject added successfully!", "success")
        return redirect(url_for('manage_subjects'))
    return render_template('Admin/add_subject.html', form=form)

@app.route('/edit_subject/<int:id>', methods=['POST', 'GET'])
@login_required
def subject_edit(id):
    subject = Subject.query.get_or_404(id)
    form = SubjectForm(obj=subject)
    if form.validate_on_submit():
        subject.name = form.subject_name.data
        subject.description = form.description.data
        db.session.commit()
        flash("Subject updated successfully!", "success")
        return redirect(url_for('manage_subjects'))
    return render_template('Admin/edit_subject.html', form=form, subject=subject)

@app.route('/delete_subject/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully!", "success")
    return redirect(url_for('manage_subjects'))

@app.route('/manage_questions/<int:quiz_id>', methods=['POST', 'GET'])
@login_required
def manage_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    return render_template('Admin/manage_questions.html', quiz=quiz, questions=questions)

@app.route('/add_question/<int:quiz_id>', methods=['POST', 'GET'])
@login_required
def add_question(quiz_id):
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            question=form.question.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            answer=form.answer.data,
            quiz_id=quiz_id)
        db.session.add(question)
        db.session.commit()
        flash("Question updates successfully!", "success")
        return redirect(url_for('manage_questions', quiz_id=quiz_id))
    return render_template('Admin/add_question.html', form=form, quiz_id=quiz_id)

@app.route('/edit_question/<int:quiz_id>', methods=['POST', 'GET'])
@login_required
def edit_question(quiz_id):
    form = QuestionForm()
    question = Question.query.get_or_404(quiz_id)
    if form.validate_on_submit():
        question.question = form.question.data
        question.option1 = form.option1.data
        question.option2 = form.option2.data
        question.option3 = form.option3.data
        question.option4 = form.option4.data
        question.answer = form.answer.data
        db.session.commit()
        flash("Question updated successfully!", "success")
        return redirect(url_for('manage_questions', quiz_id=quiz_id))
    return render_template('Admin/edit_question.html', form=form, question=question)

@app.route('/delete_question/<int:quiz_id>', methods=['POST', 'GET'])
@login_required 
def delete_question(quiz_id):
    question = Question.query.get_or_404(quiz_id)
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully!", "success")
    return redirect(url_for('manage_questions', quiz_id=quiz_id))

@app.route("/attempt_quiz/<int:id>", methods=['POST', 'GET'])
@login_required
def attempt_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    questions = quiz.questions
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer and int(user_answer) == question.answer:
                score += 1
        user_score = Score(
            quiz_id=quiz.id,
            user_id=current_user.id,
            total_score=score)
        db.session.add(user_score)
        db.session.commit()
        flash(f"Quiz submitted successfully! Your Score is { score }", "success")
        return redirect(url_for('quiz_results', quiz_id=quiz.id))
    return render_template('attempt_quiz.html', quiz=quiz, questions=questions, quiz_id=quiz.id)

@app.route('/quiz_results/<int:quiz_id>', methods=['POST', 'GET'])
@login_required
def quiz_results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    scores = Score.query.filter_by(user_id = current_user.id, quiz_id=quiz_id).first()
    return render_template('quiz_results.html', quiz=quiz, scores=scores)


@app.route('/manage_scores')
def manage_scores():
    score = Score.query.all()
    return render_template('Admin/manage_scores.html', score=score)

@app.route('/delete_score/<int:score_id>', methods=['POST', 'GET'])
@login_required 
def delete_score(score_id):
    score = Score.query.get_or_404(score_id)
    db.session.delete(score)
    db.session.commit()
    flash("Score deleted successfully!", "success")
    return redirect(url_for('manage_scores', score_id=score_id))

@app.route('/user_summary/<int:user_id>', methods=['POST', 'GET'])
@login_required
def user_summary(user_id):
    scores = Score.query.filter_by(user_id=current_user.id).all()
    total_attempted_quizzes = len(scores)
    average_score = sum([score.total_score for score in scores]) / len(scores) if scores else 0
    user_id = current_user.id
    subject_attempts = (
        db.session.query(Subject.name, db.func.count(Score.id))
        .join(Chapter, Chapter.subject_id == Subject.id)
        .join(Quiz, Quiz.chapter_id == Chapter.id)
        .join(Score, Score.quiz_id == Quiz.id)
        .filter(Score.user_id == user_id)
        .group_by(Subject.name)
        .all()
    )
    labels = [subject[0] for subject in subject_attempts]  # Subject names
    values = [subject[1] for subject in subject_attempts]  # Number of attempts

    # Fetch all quizzes
    quizzes = Quiz.query.all()  

    # Fetch user scores
    scores1 = Score.query.filter_by(user_id=current_user.id).all()
    # Convert to dictionary mapping {quiz_id: total_score}
    score_dict = {score.quiz_id: score.total_score for score in scores1}  # ✅ Corrected
    # Create lists for Chart.js
    quiz_labels = [quiz.name for quiz in quizzes]  # X-axis labels (quiz names)
    score0 = [score_dict.get(quiz.id, 0) for quiz in quizzes]  # Y-axis values (scores, default to 0) 
    if 'user' in session:
        user = session['user']
        return render_template('user_summary.html',score0 = score0, quiz_labels = quiz_labels,  labels=labels, values=values, user=user, user_id=user_id ,total_attempted_quizzes=total_attempted_quizzes, average_score=average_score)
    

    
@app.route('/previously_attempted/<int:user_id>', methods=['POST', 'GET'])
@login_required
def previously_attempted(user_id):
    scores = Score.query.filter_by(user_id=current_user.id).all()
    total_attempted_quizzes = len(scores)
    average_score = sum([score.total_score for score in scores]) / len(scores) if scores else 0
    user_id = current_user.id
    if 'user' in session:
        user = session['user']
        return render_template('previously_attempted.html', scores = scores, user=user, user_id=user_id ,total_attempted_quizzes=total_attempted_quizzes, average_score=average_score)
    
@app.cli.command('db-create')
def create_db():
    db.create_all()
    
    #create Admin
    admin = User.query.filter_by(username='Admin').first()
    if not admin:
        admin = User(
        username = "Admin",
        email = 'admin@quiz.com',
        password = 'admin123'
        )
    
        db.session.add(admin)
        db.session.commit()
        print('Admin was created')
    else:
        print('Admin already Exists')
    print('database created')

@app.cli.command('db-drop_all')
def drop_db():
    db.drop_all()
    return ('database deleted')


 

if __name__ == '__main__': 
    app.debug = True 
    app.run(host = '0.0.0.0',port = 5000)