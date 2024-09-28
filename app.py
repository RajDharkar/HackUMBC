from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

app = Flask(__name__)

# class User():

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if not validate():
            flash('WHAT THE SIGMA DO YOU THINK YOU ARE DOING FOOL', 'error')
        else:


    names = []

    return render_template("index.html", names=names)

def validate():
    if request.form['password'] != request.form['confirm']:
        return False
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
