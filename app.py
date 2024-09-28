from flask import Flask, render_template, request, flash
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # Required for session management

@app.route('/dashboard', methods=['GET'], methods=["POST"])
def dashboard():
    # Transporation
    transportation = request.form["transportation"]
    
    return render_template("dashboard.html")  # Ensure you create dashboard.html in the templates folder

@app.route('/', methods=['GET', 'POST'])
def register():
    returnedmessage = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        # Validate email
        if not validate_email(email):
            returnedmessage = "Your email is terrible."
        # Validate password
        elif not validate_password(password, confirm):
            returnedmessage = "Your password is terrible."
        else:
            # Success message
            returnedmessage = "Your password is good."
            df1 = pd.DataFrame({'Email': [email], 'Password': [password]})

            # Check if the CSV file exists and is not empty
            if os.path.exists("data.csv") and os.stat("data.csv").st_size > 0:
                df2 = pd.read_csv("data.csv")
            else:
                df2 = pd.DataFrame(columns=['Email', 'Password'])  # Initialize empty DataFrame

            # Check if the user already exists
            if email in df2['Email'].values:
                returnedmessage = "You are already registered, why u doing this again :skull:"
            else:
                # Append new entries
                result_df = pd.concat([df2, df1], ignore_index=True)
                result_df.to_csv('data.csv', index=False)
                returnedmessage = "You are finally logged in bruh."

    return render_template("index.html", returnedmessage=returnedmessage)

def validate_password(password, confirm):
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    numbers = "0123456789"

    # Check for password confirmation and length constraints
    if password != confirm:
        return False
    if len(password) < 8 or len(password) > 15:
        return False
    if not any(char in special_characters for char in password):
        return False
    if not any(char in numbers for char in password):
        return False

    return True

def validate_email(email):
    # Check if the email contains "@" and "."
    return "@" in email and "." in email

if __name__ == '__main__':
    app.run(debug=True)
