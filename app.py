from flask import Flask, render_template, request, flash
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # Required for flash messages to work

@app.route('/', methods=['GET', 'POST'])
def register():
    works = None  # Use None to check if form was submitted
    if request.method == 'POST':  # Only process if form is submitted via POST
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if not validate_password(password, confirm):
            works = False
            flash('WHAT THE SIGMA DO YOU THINK YOU ARE DOING WITH YOUR PASSWORD FOOL', 'error')
        if validate_password(password, confirm):
            works = True
            flash("THIS IS SO SIGMA", 'success')  # Only flash success if validation passes

        df1 = pd.DataFrame({'Email': [email], 'Password': [password]})
        
        if os.path.exists("data.csv"):
            df2 = pd.read_csv("data.csv")
        else:
            df2 = pd.DataFrame(columns=['Email', 'Password'])  # Create an empty DataFrame with the same columns

        merged = pd.merge(df1, df2, on=['Email', 'Password'], how='inner')

        if not merged.empty:
            flash("gang u have already signed in", 'success')
        else:
            # Append new entries
            result_df = pd.concat([df2, df1], ignore_index=True)
            result_df.to_csv('data.csv', index=False)

    return render_template("index.html", works=works)

def validate_password(password, confirm):
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    numbers = "0123456789"

    # Check if passwords match
    if password != confirm:
        return False

    # Check password length
    if len(password) < 8 or len(password) > 15:
        return False
    
    # Check for at least one special character
    if not any(char in special_characters for char in password):
        return False
    
    # Check for at least one number
    if not any(char in numbers for char in password):
        return False

    return True

def validate_email(email):
    return "@" in email and "." in email

if __name__ == '__main__':
    app.run(debug=True)