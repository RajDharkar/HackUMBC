from flask import Flask, redirect, render_template, request, flash, url_for
import pandas as pd
import os
import hashlib
import binascii
import ast
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


# Home Page >> Index.HTML
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/dashboard/<email>', methods=['GET', 'POST'])
def dashboard(email):
    # Not empty and email already in
    df2 = pd.read_csv("data.csv")
    print(email)
    for index, row in df2.iterrows():
        if row["Email"] == email:
            cd = ast.literal_eval(row["Info"])
            break

    # Calculate pie_percent based on 'usage'
    nums = cd[1]['usage']
    if nums != [0] * 5:
        pie_percent = [(num / sum(nums)) * 100 for num in nums]
    else:
        pie_percent = [0] * 5  # Default values if no usage data

    # Prepare bar chart data (optional for your case)
    recents = cd[0]['recents']
    if len(recents) > 0:
        bar_x_axis = list(recents.keys())[-5:]  # Last 5 keys
        data = list(recents.values())[-5:]  # Last 5 values
    else:
        bar_x_axis = []
        data = []

    bar_graph = [{"x_axis": bar_x_axis}, {"y_data": data}]
    return render_template("dashboard.html", pie_data=pie_percent, barChart1=bar_graph)

# Home page >> register.HTML
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Initilize Returned Message
    returnedmessage = None

    if request.method == 'POST':
        # Assigning variables, From request
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        # Validate email
        if not ("@" in email and "." in email):
            returnedmessage = "Your email is invalid."
        # Validate password
        elif not validate_password(password, confirm) and returnedmessage == None:
            returnedmessage = "Your email and password are invalid."

        elif not validate_password(password, confirm) and returnedmessage != None: 
            returnedmessage = "Your password is invalid."

        else:
            # Hash the password with salt
            salted_hashed_password = hash_password_with_salt(password)

            # Intilize row for data frame
            s = "[{'recents': []}, {'usage': [0, 0, 0, 0, 0]}]"
            df1 = pd.DataFrame({'Email': [email], 'Password': [salted_hashed_password], 'Info': [s]})

            empty = None
            try:
                df2 = pd.read_csv("data.csv")

            except pd.errors.EmptyDataError:
                empty = True

            if not empty and (email in df2['Email'].values):
                returnedmessage = "You are already registered, please login."
                
            else:
                if empty:
                    df2 = pd.DataFrame(columns=['Email', 'Password', 'Info']) 
                result_df = pd.concat([df2, df1], ignore_index=True)
                result_df.to_csv('data.csv', index=False)
                return redirect(url_for('dashboard', email=email))
                # returnedmessage = "Registration successful! You can now log in."
                
                #ISHAAN
                # [{"bar": {"x axis": [], "data": []}, "pie": []}]
    return render_template('register.html', returnedmessage=returnedmessage)
@app.route('/login', methods=['GET', 'POST'])
def login():
    returnedmessage = None
    pie_percent = []
    bar_x_axis = []
    data = []
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        empty = None
        try:
            df2 = pd.read_csv("data.csv")

        except pd.errors.EmptyDataError:
            empty = True

        if empty:
            return render_template("login.html", returnedmessage='Invalid Username or Password')

        elif email in df2['Email'].values:
            for index, row in df2.iterrows():
                if row["Email"] == email:
                    # Compare the hashed password with the one in the CSV
                    if verify_password(row["Password"], password):
                        cd = ast.literal_eval(row["Info"])
                        break
                    else:
                        returnedmessage = "Invalid Email or Password"
                        return render_template("login.html", returnedmessage=returnedmessage)

            # Calculate pie_percent based on 'usage'
            nums = cd[1]['usage']
            if nums != [0] * 5:
                pie_percent = [(num / sum(nums)) * 100 for num in nums]
            else:
                pie_percent = [0] * 5  # Default values if no usage data

            # Prepare bar chart data (optional for your case)
            recents = cd[0]['recents']
            if len(recents) > 0:
                bar_x_axis = list(recents.keys())[-5:]  # Last 5 keys
                data = list(recents.values())[-5:]  # Last 5 values

            # Successful login, render pie.html with calculated pie_percent
            returnedmessage = "You are successfully logged in!"
            return redirect(url_for('dashboard', email=email))

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
        return False
    if len(password) < 8:
        return False
    if len(password) > 15:
        return False
    if not any(char in special_characters for char in password):
        return False
    if not any(char in numbers for char in password):
        return False
    
    return True

if __name__ == '__main__':
    app.run(debug=True)
