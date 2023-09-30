from flask import Flask, request, render_template, session
import random
from flask_session import Session

app = Flask(__name__)


def generate_random_number():
    return int(random.randint(1, 100))


app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = {
    'guesses': [],
    'user_number': 0,
    'show_guesses': True,
    'total_num_of_guesses': 0,
    'best_record': 0,
    'game_end': False
}

random_number = generate_random_number()


@app.route('/')
def home():
    if session['best_record']:
        db['best_record'] = session.get('best_record', 0)
    else:
        session['best_record'] = 100
    return render_template('home.html', best_record=db['best_record'])


@app.route('/check', methods=['POST'])
def check():
    global random_number

    if request.method == 'POST':
        db['total_num_of_guesses'] += 1
        db['show_guesses'] = True
        db['user_number'] = int(request.form.get('input'))

        if db['user_number'] == random_number:
            db['game_end'] = True
            db['guesses'].append(str(db['user_number']) + ' CORRECT')
        elif db['user_number'] > random_number:
            db['best_record'] += 1
            db['guesses'].append(str(db['user_number']) + ' TOO HIGH!')
        elif db['user_number'] < random_number:
            db['best_record'] += 1
            db['guesses'].append(str(db['user_number']) + ' TOO LOW!!')

        if db['user_number'] != random_number:
            db['best_record'] += 1

        elif db['user_number'] == random_number and db['total_num_of_guesses'] < session['best_record']:
            session['best_record'] = db['total_num_of_guesses']

    return render_template('home.html', guesses=reversed(db['guesses']), user_number=db['user_number'],
                           random_number=random_number, total_num_of_guesses=db['total_num_of_guesses'],
                           game_end=db['game_end'], best_record=session['best_record'])


@app.route('/restart', methods=['POST'])
def restart():
    global random_number

    if request.method == 'POST':
        db['show_guesses'] = False
        db['total_num_of_guesses'] = 0
        db['best_record'] = 0
        db['guesses'].clear()
        db['game_end'] = False
        random_number = generate_random_number()
    return render_template('home.html', guesses=db['guesses'], user_number=db['user_number'],
                           random_number=random_number, total_num_of_guesses=db['total_num_of_guesses'],
                           game_end=db['game_end'], best_record=session['best_record'])


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
