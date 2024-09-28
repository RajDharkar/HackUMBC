from flask import Flask, render_template, request, flash
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # Required for session management

@app.route('/', methods=['GET', 'POST'])
def register():
    works = None  # Default to None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        # Validate email
        if not validate_email(email):
            flash("Invalid email address", "error")
            return render_template("index.html", works=works)

        # Validate password
        if not validate_password(password, confirm):
            flash("Password validation failed", "error")
        else:
            works = True
            print("Password validated successfully")

            df1 = pd.DataFrame({'Email': [email], 'Password': [password]})

            # Check if the CSV file exists and is not empty
            if os.path.exists("data.csv") and os.stat("data.csv").st_size > 0:
                df2 = pd.read_csv("data.csv")
            else:
                df2 = pd.DataFrame(columns=['Email', 'Password'])  # Initialize empty DataFrame

            # Check if the user already exists
            if email in df2['Email'].values:
                flash("User already registered", "error")
            else:
                # Append new entries
                result_df = pd.concat([df2, df1], ignore_index=True)
                result_df.to_csv('data.csv', index=False)
                flash("User registered successfully!", "success")

    return render_template("index.html", works=works)

def validate_password(password, confirm):
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    numbers = "0123456789"

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
    return "@" in email and "." in email

if __name__ == '__main__':
    app.run(debug=True)
