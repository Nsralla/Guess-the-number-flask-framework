
from flask import Flask, request, render_template
import random

app = Flask(__name__)


def generate_random_number(): # function to generate random number
    return int(random.randint(1, 100))


random_number = generate_random_number()  # generate random number
guesses = []  # to store my code response for user input
user_number = None
show_guesses = True  # to hide guesses when restart is clicked
total_num_of_guesses = 0
game_end = False


@app.route('/')
def home():
    # we have generated a random number
    # when user clicks the check me button:
    # 1- take the number
    return render_template('home.html')


@app.route('/check', methods=['POST'])
def check():
    global user_number
    global show_guesses
    global total_num_of_guesses

    if request.method == 'POST':
        total_num_of_guesses += 1
        show_guesses = True
        user_number = int(request.form.get('input'))
        print(random_number)
        # compare the 2 numbers
        if user_number == random_number:
            guesses.append(f'{user_number} CORRECT')
        elif user_number > random_number:
            guesses.append(f'{user_number} TOO HIGH!')
        elif user_number < random_number:
            guesses.append(f'{user_number} TOO LOW!!')

    return render_template('home.html', guesses=reversed(guesses), user_number=user_number, random_number=random_number,total_num_of_guesses=total_num_of_guesses,game_end=game_end)


@app.route('/restart', methods=['POST'])
def restart():
    global show_guesses
    global user_number
    global guesses
    global random_number
    global total_num_of_guesses
    if request.method == 'POST':
        show_guesses = False
        total_num_of_guesses = 0
        guesses.clear()
        random_number = generate_random_number()
    return render_template('home.html', guesses=guesses, user_number=user_number, random_number=random_number,total_num_of_guesses=total_num_of_guesses)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
