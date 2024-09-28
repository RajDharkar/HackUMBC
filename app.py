from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

app = Flask(__name__)

# class User():

@app.route('/', methods=['GET', 'POST'])
def register():
    works = True
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if not validate_password():
            works = False
            flash('WHAT THE SIGMA DO YOU THINK YOU ARE DOING WITH YOUR PASSWORD FOOL', 'error')
        else:
            #stuff goes here
            flash("THIS IS SO SIGMA", 'lets gooooo')
    return render_template("index.html", works=works)

def validate_password():
    password = request.form['password']
    special_characters = [
    "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
    ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"]
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    if password != request.form['confirm']:
        return False
    if len(password) < 8 or len(password) > 15:
        return False
    
    is_true = False
    for letter in password:
        if letter in special_characters:
            return True
    if not is_true:
        return False
       
    is_true = False
    for letter in password:
        if letter in numbers:
            return True
    if not is_true:
        return False
    
def validade_emial():
    email = request.form['password']

if __name__ == '__main__':
    app.run(debug=True)
    
