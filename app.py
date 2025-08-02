from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Initialize balances
user_money = 1000
opponent_money = 1000

# Dares list
dares = [
    "Do 10 push-ups!",
    "Sing a song loudly!",
    "Do a funny dance!",
    "Tell a joke!",
    "Do an impression of your favorite actor!",
    "Spin around 5 times and walk straight!",
    "Send a silly selfie to a friend!",
    "Text 'I love pineapples' to your best friend!",
    "Act like a chicken for 30 seconds!"
]

@app.route('/')
def home():
    return render_template('home.html', user_money=user_money, opponent_money=opponent_money)

@app.route('/coinflip', methods=['GET', 'POST'])
def coinflip():
    global user_money, opponent_money
    result = None
    message = ""
    dare = None
    result_image = None

    if request.method == "POST":
        try:
            bet = int(request.form["bet"])
            guess = request.form["guess"]
            if bet <= 0 or bet > user_money:
                message = "❌ Invalid bet."
            else:
                flip_result = random.choice(["heads", "tails"])
                if guess == flip_result:
                    user_money += bet
                    opponent_money -= bet
                    message = f"🎉 You won! It was {flip_result}. +₹{bet}"
                else:
                    user_money -= bet
                    opponent_money += bet
                    message = f"❌ You lost! It was {flip_result}. -₹{bet}"
                    dare = random.choice(dares)
                result = flip_result
                result_image = f"coin_{result}.png"
        except:
            message = "⚠️ Invalid input."

    return render_template('coinflip.html', result=result, message=message, dare=dare,
                           user_money=user_money, opponent_money=opponent_money,
                           result_image=result_image)

@app.route('/dicegame', methods=['GET', 'POST'])
def dicegame():
    global user_money, opponent_money
    message = None
    dare = None

    if request.method == "POST":
        try:
            bet = int(request.form["bet"])
            if bet <= 0 or bet > user_money:
                message = "❌ Invalid bet."
            else:
                user_roll = random.randint(1, 6)
                opp_roll = random.randint(1, 6)
                if user_roll > opp_roll:
                    user_money += bet
                    opponent_money -= bet
                    message = f"🎉 <strong>You won!</strong><br>You rolled {user_roll}, opponent rolled {opp_roll}.<br>+₹{bet}<br>Your Money: ₹{user_money} | Opponent: ₹{opponent_money}"
                elif user_roll < opp_roll:
                    user_money -= bet
                    opponent_money += bet
                    message = f"❌ <strong>You lost!</strong><br>You rolled {user_roll}, opponent rolled {opp_roll}.<br>-₹{bet}<br>Your Money: ₹{user_money} | Opponent: ₹{opponent_money}"
                    dare = random.choice(dares)
                else:
                    message = f"🤝 It's a tie! Both rolled {user_roll}.<br>Your Money: ₹{user_money} | Opponent: ₹{opponent_money}"
        except:
            message = "⚠️ Invalid input."

    return render_template('dicegame.html', message=message, dare=dare,
                           user_money=user_money, opponent_money=opponent_money)

@app.route('/rps', methods=['GET', 'POST'])
def rps():
    global user_money, opponent_money
    message = ""
    dare = None
    result = None

    if request.method == "POST":
        try:
            bet = int(request.form["bet"])
            user_choice = request.form["choice"]
            comp_choice = random.choice(["rock", "paper", "scissors"])

            if bet <= 0 or bet > user_money:
                message = "❌ Invalid bet."
            else:
                if user_choice == comp_choice:
                    message = f"🤝 Tie! Both chose {user_choice}."
                elif (user_choice == "rock" and comp_choice == "scissors") or \
                     (user_choice == "paper" and comp_choice == "rock") or \
                     (user_choice == "scissors" and comp_choice == "paper"):
                    user_money += bet
                    opponent_money -= bet
                    message = f"🎉 You won with {user_choice} vs {comp_choice}! +₹{bet}"
                else:
                    user_money -= bet
                    opponent_money += bet
                    message = f"❌ You lost ({user_choice} vs {comp_choice}). -₹{bet}"
                    dare = random.choice(dares)
                result = comp_choice
        except:
            message = "⚠️ Invalid input."

    return render_template('rps.html', message=message, dare=dare, result=result,
                           user_money=user_money, opponent_money=opponent_money)

@app.route('/cardgame', methods=['GET', 'POST'])
def cardgame():
    global user_money, opponent_money
    result = None
    dare = None

    if request.method == 'POST':
        try:
            bet = int(request.form['bet'])
            if bet <= 0 or bet > user_money:
                result = "❌ Invalid bet."
            else:
                user_card = random.randint(1, 13)
                opp_card = random.randint(1, 13)
                if user_card > opp_card:
                    user_money += bet
                    opponent_money -= bet
                    result = f"🎉 You won! You: {user_card} vs Opponent: {opp_card}. +₹{bet}"
                elif user_card < opp_card:
                    user_money -= bet
                    opponent_money += bet
                    result = f"❌ You lost. You: {user_card} vs Opponent: {opp_card}. -₹{bet}"
                    dare = random.choice(dares)
                else:
                    result = f"🤝 It's a tie! Both drew {user_card}."
        except:
            result = "⚠️ Invalid input."

    return render_template('cardgame.html', result=result, dare=dare,
                           user_money=user_money, opponent_money=opponent_money)

@app.route('/slotgame', methods=['GET', 'POST'])
def slotgame():
    global user_money, opponent_money
    result = None
    dare = None
    symbols = ["🍒", "🍋", "🍊", "⭐", "🔔"]

    if request.method == 'POST':
        try:
            bet = int(request.form['bet'])
            if bet <= 0 or bet > user_money:
                result = "❌ Invalid bet."
            else:
                reel = [random.choice(symbols) for _ in range(3)]
                if reel[0] == reel[1] == reel[2]:
                    win = bet * 5
                    user_money += win
                    opponent_money -= win
                    result = f"{' '.join(reel)} 🎉 Jackpot! +₹{win}"
                else:
                    user_money -= bet
                    opponent_money += bet
                    result = f"{' '.join(reel)} ❌ You lost ₹{bet}"
                    dare = random.choice(dares)
        except:
            result = "⚠️ Invalid input."

    return render_template('slotgame.html', result=result, dare=dare,
                           user_money=user_money, opponent_money=opponent_money)

@app.route('/guessgame', methods=['GET', 'POST'])
def guessgame():
    global user_money, opponent_money
    secret = session.get("secret")
    if secret is None:
        secret = random.randint(1, 20)
        session["secret"] = secret

    message = ""
    dare = None

    if request.method == 'POST':
        try:
            bet = int(request.form['bet'])
            guess = int(request.form['guess'])

            if bet <= 0 or bet > user_money:
                message = "❌ Invalid bet."
            elif guess == secret:
                user_money += bet
                opponent_money -= bet
                message = f"🎉 Correct! It was {secret}. +₹{bet}"
                session.pop("secret", None)
            else:
                user_money -= bet
                opponent_money += bet
                hint = "higher" if guess < secret else "lower"
                message = f"❌ Wrong! Try {hint}."
                dare = random.choice(dares)
        except:
            message = "⚠️ Invalid input."

    return render_template('guessgame.html', message=message, dare=dare,
                           user_money=user_money, opponent_money=opponent_money)

if __name__ == '__main__':
    app.run(debug=True)
