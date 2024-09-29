from flask import Flask, render_template, request, flash
import pandas as pd
import os
import hashlib
import binascii

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # Required for session management

# Function to hash password with salt using SHA-256
def hash_password_with_salt(password):
    salt = os.urandom(16)  # Generate a 16-byte salt
    salted_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return binascii.hexlify(salt).decode() + ":" + binascii.hexlify(salted_password).decode()

# Function to verify if a given password matches the stored password hash
def verify_password(stored_password, provided_password):
    salt, hashed_password = stored_password.split(":")
    salt = binascii.unhexlify(salt.encode())  # Convert the stored salt back to bytes
    hashed_provided_password = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return binascii.hexlify(hashed_provided_password).decode() == hashed_password

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    returnedmessage = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        # Validate email
        if not validate_email(email):
            returnedmessage = "Your email is invalid."
        # Validate password
        elif not validate_password(password, confirm):
            returnedmessage = "Your password is invalid."
        else:
            # Hash the password with salt
            salted_hashed_password = hash_password_with_salt(password)
            s = "[{'recents': []}, {'usage': [0, 0, 0, 0, 0]}]"
            df1 = pd.DataFrame({'Email': [email], 'Password': [salted_hashed_password], 'Info': [s]})
            
            # Check if the CSV file exists and read it
            if os.path.exists("data.csv"):
                df2 = pd.read_csv("data.csv")
            else:
                df2 = pd.DataFrame(columns=['Email', 'Password', 'Info'])  # Initialize empty DataFrame
            
            # Check if the email already exists
            if email in df2['Email'].values:
                returnedmessage = "You are already registered, please login."
            else:
                # Append new entries
                result_df = pd.concat([df2, df1], ignore_index=True)
                result_df.to_csv('data.csv', index=False)
                returnedmessage = "Registration successful! You can now log in."

    return render_template("register.html", returnedmessage=returnedmessage)

@app.route('/login', methods=['GET', 'POST'])
def login():
    returnedmessage = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the CSV file exists and read it
        if os.path.exists("data.csv"):
            df2 = pd.read_csv("data.csv")
        else:
            df2 = pd.DataFrame(columns=['Email', 'Password', 'Info'])  # Initialize empty DataFrame
        
        # Check if the user exists
        if email in df2['Email'].values:
            for index, row in df2.iterrows():
                if row["Email"] == email:
                    # Verify the password
                    if verify_password(row["Password"], password):
                        returnedmessage = "Login successful!"
                    else:
                        returnedmessage = "Invalid Email or Password"
                    break
        else:
            returnedmessage = "Invalid Email or Password"
    
    return render_template("login.html", returnedmessage=returnedmessage)

# Password validation function
def validate_password(password, confirm):
    errors = []
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    numbers = "0123456789"

    is_true = True
    if password != confirm:
        is_true = False
        errors.append("Password does not match the confirmation.")
    if len(password) < 8:
        is_true = False
        errors.append("Password is too short.")
    if len(password) > 15:
        is_true = False
        errors.append("Password is too long.")
    if not any(char in special_characters for char in password):
        is_true = False
        errors.append("Password is missing a special character.")
    if not any(char in numbers for char in password):
        is_true = False
        errors.append("Password is missing a numerical character.")
    
    if is_true:
        return True
    else:
        return ", ".join(errors)

# Email validation function
def validate_email(email):
    return "@" in email and "." in email

if __name__ == '__main__':
    app.run(debug=True)
