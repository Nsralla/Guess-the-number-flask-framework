from flask import Flask, request, render_template, session
import random
from flask_session import Session

app = Flask(__name__)


def generate_random_number():  # function to generate random number
    return int(random.randint(1, 100))


app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
random_number = generate_random_number()  # generate random number
guesses = []  # to store my code response for user input
user_number = None
show_guesses = True  # to hide guesses when restart is clicked
total_num_of_guesses = 0
best_record = 0
game_end = False


@app.route('/')
def home():
    global best_record
    best_record = session.get('best_record', 0)
    return render_template('home.html', best_record=best_record)


@app.route('/check', methods=['POST'])
def check():
    global user_number
    global show_guesses
    global total_num_of_guesses
    global best_record
    global game_end

    if request.method == 'POST':
        total_num_of_guesses += 1
        # update best score

        show_guesses = True
        user_number = int(request.form.get('input'))
        print(f'random_number={random_number}')
        # compare the 2 numbers
        if user_number == random_number:
            game_end = True
            guesses.append(f'{user_number} CORRECT')
        elif user_number > random_number:
            best_record += 1
            guesses.append(f'{user_number} TOO HIGH!')
        elif user_number < random_number:
            best_record += 1
            guesses.append(f'{user_number} TOO LOW!!')

        if user_number != random_number:
            best_record += 1

        elif user_number == random_number and best_record < session['best_record']:
            session['best_record'] = best_record

    return render_template('home.html', guesses=reversed(guesses), user_number=user_number,
                           random_number=random_number, total_num_of_guesses=total_num_of_guesses
                           , game_end=game_end, best_record=session['best_record'])


@app.route('/restart', methods=['POST'])
def restart():
    global show_guesses
    global user_number
    global guesses
    global random_number
    global total_num_of_guesses
    global game_end
    global best_record
    print(best_record)
    if request.method == 'POST':
        show_guesses = False
        total_num_of_guesses = 0
        best_record = 0
        guesses.clear()
        game_end = False
        random_number = generate_random_number()
    return render_template('home.html', guesses=guesses, user_number=user_number,
                           random_number=random_number, total_num_of_guesses=total_num_of_guesses,game_end=game_end,
                           best_record=session['best_record'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
