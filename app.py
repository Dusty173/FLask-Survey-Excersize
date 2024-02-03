from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def survey_home():
    """Shows survey selection page"""

    return render_template('survey_home.html', survey=survey)

@app.route('/start', methods=['POST'])
def begin_survey():
    """Clear out previous responses"""
    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def get_question():
    """Take response, save and move to next question"""

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/completed')
    else:
        return redirect(f'/questions/{len(responses)}')
    
@app.route('/questions/<int:id>')
def display_question(id):
    """Display current question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect('/completed')
    
    if (len(responses) != id):
        flash(f'Invalid question ID: {id}.')
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[id]
    return render_template('questions.html', question_num=id, question=question)

@app.route('/completed')
def completed():
    """No more questions, show final page"""
    return render_template('completed.html')