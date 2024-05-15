from flask import Flask, render_template, request, session, url_for, redirect
import json
import random

app = Flask(__name__)

# Data Storage

usernameTest = "Admin1"

sessionData = {

    "admin": {
    "latestGuess": 0,
    "firstGuess": 0
    },

    "test": {
        "latestGuess": 0,
        "firstGuess": 0
    }
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(sessionData, f, ensure_ascii=False, indent=4)

userData = {
    "admin": "12345",
    "test" : "23456"
}

app.secret_key = "651289501007d1d5b611b9849a3453281fd1da46a8957063f7f65357b1b17faa"

# Index Page

@app.route('/')
def index():
    if "username" in session:
        info = "Du wurdest eingeloggt"
        print(session)
        loggedin = True
        return render_template("index.html", info=info, loggedin = loggedin)
    info = "Du bist nicht eingeloggt"
    return render_template("index.html", info=info)
    
# Login Logic

@app.route("/login", methods=["POST", "GET"])
def loginIncrementals():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if isValid(username, password, userData):
            session["username"] = request.form["username"]
            return redirect(url_for("index"))
        else:
            print("Wrong Name or Password")
            error = "Falscher Nutzername oder Passwort"
            return render_template("login.html", error=error)
    return render_template("login.html")

def isValid(userinputName, userinputPassword, data):
    username = userinputName
    password = data.get(userinputName)
    if userinputName == username and userinputPassword == password:
        return True
    else:
        return False



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

#           Game Page Logic
#
# Game 1 Guess against Computer

@app.route("/game2", methods=["POST", "GET"])
def game2():
    currentUser = "username" in session
    stateGame = False
    userGuess = None
    computersGuess = random.randrange(1, 100)
    latestGuess = None

    if request.method == "POST":
        try:
            stateGame = request.form["startGame"]
        except:
            print("Coudn't reach Gamestate")
        
        if stateGame == True:
            try:
                userGuess = request.form["userGuess"]
            except:
                print("No Values recieved")
                error = "Das Feld darf nicht leer sein!"
                return render_template("game2.html", error=error)

            if int(userGuess) > 100 or int(userGuess) < 1:
                error = "Zahl ist nicht im Bereich zwischen 1 und 100"
                return render_template("game2.html", error=error)
            elif latestGuess != None:
                userGuess = latestGuess
            else:
                startGame1(userGuess, currentUser, computersGuess)
        else:
            print("No Data Recieved")
            return render_template("game2.html")
                   
        
    else:
        return render_template("game2.html")
        
#           Game Page Logic
# Game 2 Computer against You


@app.route("/hello", methods=["POST", "GET"])
def recievedata():
    error = None
    stateGame = False
    firstNumber = 1
    secondNumber = 100
    numberToGuess = 0
    currentUser = "username" in session

    if request.method == "POST":

        # Testing for allowed values

        try:
            numberToGuess = request.form["guessMyNumber"]
        except:
            print("Coudn't recieve First or Second Number")

        try:
            numberToGuess = request.form["guessMyNumber"]
            stateGame = request.form["startGame"]
        except:
            print("Error getting state of the Game")
       
        try:
            numberToGuess.isdecimal()
        except:
            error = "Eingabe muss eine Zahl sein"
            return render_template("hello.html", error=error)

        # Start Game

        if bool(stateGame) == True and int(numberToGuess) > 0 and int(numberToGuess) < 100:
            return startGame2(bool(stateGame), int(numberToGuess))
        elif int(numberToGuess) > 0 or int(numberToGuess) < 100:
            print("Values are not in range of 1 - 100")
            error = "Die Zahl muss zwischen 1 und 100 liegen"
            return render_template("hello.html", error=error)
        else:
            print("No Values were returned")
            return render_template("hello.html", error=error)
    else:
        print("Startup, no Values transfered")
        return render_template("hello.html", error=error)

# Game Logic
# Game 1

def startGame1(userGuess, currentUser, computersGuess):

    with open("data.json") as f:
        userDict = json.load(f)
    print(userDict)
    guessesTaken = 0


    if userGuess == computersGuess:
        print("You won")
        info = "Du hast gewonnen"
        return render_template("game2.html", info=info, guessesTaken=guessesTaken, username=currentUser)
    
    elif userGuess > computersGuess:
        info = "Die Zahl ist niedriger"
        guessesTaken += 1
        return render_template("game2.html", info=info, guessesTaken=guessesTaken)
    
    elif userGuess < computersGuess:
        info = "Die Zahl ist größer"
        guessesTaken += 1
        return render_template("gamn2.html", info=info, guessesTaken=guessesTaken)

# Game Logic
# Game 2

def startGame2(stateGame, numberToGuess):

    computerguessed = 0
    lastsmallest = 1
    lastbiggest = 100
    stepstaken = 0

    while stateGame == True:

        if computerguessed == None or computerguessed == 0:
            computerguessed = int((lastsmallest + lastbiggest) / 2)
            stepstaken += 1
        
        if computerguessed == numberToGuess:
            print("You Lost")
            stepstaken += 1
            return render_template("hello.html",  rolled = numberToGuess, manysteps = stepstaken)
            break
        elif computerguessed > numberToGuess and stepstaken != 25:
            computerguessed = int((lastsmallest + lastbiggest) / 2)
            if computerguessed > numberToGuess:
                lastbiggest = computerguessed
                stepstaken += 1
                print(computerguessed)

        elif computerguessed < numberToGuess and stepstaken != 25:
            computerguessed = int((lastsmallest + lastbiggest) / 2)
            if computerguessed < numberToGuess:
                lastsmallest = computerguessed
                stepstaken += 1
                print(computerguessed)
        else:
            print("Error happend")
            error = "Something happend"
            return render_template("hello.html", error=error)
            break