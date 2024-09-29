from flask import Flask, redirect, render_template, request, flash, url_for
import numpy as np
import pandas as pd
import os
import hashlib
import binascii
import ast
import datetime
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # Required for session management



# Function to run the Monte Carlo simulation
# Monte Carlo simulation function to predict carbon footprint variability for the next 5 days
def monte_carlo_simulation(email):
    # Fetch user data from CSV
    df2 = pd.read_csv("data.csv")
    for index, row in df2.iterrows():
        if row["Email"] == email:
            cd = ast.literal_eval(row["Info"])
            break
    
    # Input current usage data from the user's info
    current_usage = cd[1]['usage']  # ['Transportation', 'Electricity', 'Waste', 'Food Production', 'Manufacturing']

    # Constants for Monte Carlo simulation
    num_simulations = 1000
    household_size = random.uniform(1, 6)  # Example: household size between 1 and 6
    miles_per_week = random.uniform(50, 300)  # Miles driven per week
    annual_kwh = random.uniform(4000, 12000)  # Annual electricity in kWh
    food_waste_per_week = random.uniform(2, 15)  # Food waste in pounds per week
    flights_per_year = random.uniform(0, 10)  # Flights per year
    
    # Base carbon footprint components
    base_transportation = miles_per_week * 0.404  # Example multiplier
    base_electricity = annual_kwh * 0.92 / 52  # Convert annual to weekly
    base_waste = food_waste_per_week * 2.5
    base_food_production = food_waste_per_week * 1.5
    base_manufacturing = household_size * 3.0

    # Variables to hold the prediction results for the next 5 days
    future_predictions = []

    # Run Monte Carlo simulation for the next 5 days
    for day in range(5):
        daily_predictions = []
        for _ in range(num_simulations):
            transportation = random.gauss(base_transportation, base_transportation * 0.1)  # 10% variability
            electricity = random.gauss(base_electricity, base_electricity * 0.1)
            waste = random.gauss(base_waste, base_waste * 0.1)
            food_production = random.gauss(base_food_production, base_food_production * 0.1)
            manufacturing = random.gauss(base_manufacturing, base_manufacturing * 0.1)
            
            # Total carbon footprint for that simulation
            total_footprint = transportation + electricity + waste + food_production + manufacturing
            daily_predictions.append(total_footprint)
        
        # Average of the Monte Carlo simulations for that day
        avg_prediction = np.mean(daily_predictions)
        future_predictions.append(avg_prediction)
    print(future_predictions)
    #return future_predictions
    
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

@app.route('/offset')
def offset():
    return render_template('offset.html')

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
    if len(recents) > 5:
        bar_x_axis = list(recents.keys())[-5:]  # Last 5 keys
        data = list(recents.values())[-5:]  # Last 5 values
    elif 0 < len(recents) < 5:
        bar_x_axis = list(recents.keys())
        data = list(recents.values())
    else:
        bar_x_axis = [0, 0, 0, 0, 0]
        data = [0, 0, 0, 0, 0]

    bar_graph = [{"x_labels": bar_x_axis}, {"y_data": data}]
    pie_graph = [{"labels": ["Transportation", "Electricity", "Waste", "Food Production", "Household Members"]}, {"data": pie_percent}]
    print(bar_graph)
    print(pie_graph)
    return render_template("dashboard.html", pieChart1=pie_graph, barChart1=bar_graph)
@app.route('/entry', methods=['GET', 'POST'])
def update():
    now = str(datetime.datetime.now())
    house_members = request.form["household_members"]
    miles_driver = request.form["miles_driver"]
    electricity = request.form["annual_electricity"]
    waste = request.form["food_waste"]
    plane = request.form["flights_per_year"]

    df = pd.read_cs("data.csv")
    #for index, row
    return render_template("entry.html")



    
@app.route('/live_leaderboard', methods=['GET', 'POST'])
def live_leaderboard(email):
    # Not empty and email already in
    df2 = pd.read_csv("data.csv")
    print(email)
    for index, row in df2.iterrows():
        if row["Email"] == email:
            cd = ast.literal_eval(row["Info"])
            break
    
    nums = cd[1]['usage']
    labels = ["Transportation", "Electricity", "Waste", "Food Production", "Manufacturing"]
    result = []
    for i, j in zip(nums, labels):
        result.append({"Mode": j, "Usage": i}) 
    sorted_t = sorted({labels : nums for i, j in zip(nums, labels)}, key=lambda x: x["Usage"])
    return sorted_t[2::]
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    returnedmessage = None

    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']
        confirm = request.form['confirm']

        # Validate email and password
        if not ("@" in email and "." in email):
            returnedmessage = "Your email is invalid."
        elif not validate_password(password, confirm):
            returnedmessage = "Your password is invalid."
        else:
            # Hash the password
            salted_hashed_password = hash_password_with_salt(password)

            # New user info to be added to CSV
            user_info = "[{'recents': []}, {'usage': [0, 0, 0, 0, 0]}]"
            new_user_data = pd.DataFrame({'Email': [email], 'Password': [salted_hashed_password], 'Info': [user_info]})

            try:
                df2 = pd.read_csv("data.csv")
                # Ensure required columns exist in the CSV
                if set(['Email', 'Password', 'Info']).issubset(df2.columns):
                    print("File contains required columns.")
                else:
                    print("CSV file missing required columns, initializing.")
                    # Reinitialize the DataFrame with correct columns if missing
                    df2 = pd.DataFrame(columns=['Email', 'Password', 'Info'])

            except (FileNotFoundError, pd.errors.EmptyDataError):
                print("CSV file not found or empty, initializing.")
                df2 = pd.DataFrame(columns=['Email', 'Password', 'Info'])  # Initialize new DataFrame if empty or missing

            # Check if the email already exists in the CSV
            if email in df2['Email'].values:
                returnedmessage = "You are already registered, please login."
            else:
                # Append new user data to the dataframe
                df2 = pd.concat([df2, new_user_data], ignore_index=True)

                # Save to CSV
                df2.to_csv('data.csv', index=False)

                # Redirect to dashboard after successful registration
                return redirect(url_for('dashboard', email=email))

    return render_template('register.html', returnedmessage=returnedmessage)
@app.route('/login', methods=['GET', 'POST'])
def login():
    returnedmessage = None
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        empty = False
        try:
            df2 = pd.read_csv("data.csv")
        except pd.errors.EmptyDataError:
            empty = True
        except FileNotFoundError:
            empty = True

        if empty:
            df2 = pd.DataFrame(columns=['Email', 'Password', 'Info']) 
            returnedmessage = 'Invalid Username or Password'

        elif email in df2['Email'].values:
            # Fetch the stored hashed password from the CSV
            for index, row in df2.iterrows():
                if row['Email'] == email:
                    stored_password = row['Password']
                    break

            # Validate the provided password
            if verify_password(stored_password, password):
                return redirect(url_for('dashboard', email=email))
            else:
                returnedmessage = 'Invalid Username or Password'
        else:
            returnedmessage = 'Invalid Username or Password'

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
