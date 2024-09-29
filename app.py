from flask import Flask, redirect, render_template, request, flash, url_for
import numpy as np
import pandas as pd
import os
import hashlib
import binascii
import ast
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # Required for session management



# Function to run the Monte Carlo simulation
def monte_carlo_simulation(email):
    # Fetch user data (replace this with actual logic from your dataset)
    df2 = pd.read_csv("data.csv")
    for index, row in df2.iterrows():
        if row["Email"] == email:
            cd = ast.literal_eval(row["Info"])
            break
    
    # Input current footprint values from the user's data
    current_usage = cd[1]['usage']
    
    # Define standard deviation for each category to simulate variability
    std_footprint = {
        'electricity': 0.2 * current_usage[1],  # 20% variability
        'transportation': 0.2 * current_usage[0],
        'waste': 0.2 * current_usage[2],
        'food_production': 0.2 * current_usage[3],
        'manufacturing': 0.2 * current_usage[4]
    }

    # Number of Monte Carlo iterations
    n_simulations = 1000

    # Run Monte Carlo simulation for each category
    electricity_simulation = np.random.normal(current_usage[1], std_footprint['electricity'], n_simulations)
    transportation_simulation = np.random.normal(current_usage[0], std_footprint['transportation'], n_simulations)
    waste_simulation = np.random.normal(current_usage[2], std_footprint['waste'], n_simulations)
    food_simulation = np.random.normal(current_usage[3], std_footprint['food_production'], n_simulations)
    manufacturing_simulation = np.random.normal(current_usage[4], std_footprint['manufacturing'], n_simulations)

    # Total carbon footprint simulation
    total_footprint_simulation = (
        electricity_simulation +
        transportation_simulation +
        waste_simulation +
        food_simulation +
        manufacturing_simulation
    )

    # Compute the mean, std, and 95% confidence interval
    mean_total_footprint = np.mean(total_footprint_simulation)
    std_total_footprint = np.std(total_footprint_simulation)
    confidence_interval = np.percentile(total_footprint_simulation, [2.5, 97.5])

    # Store the results for display on the dashboard
    results = {
        'mean': mean_total_footprint,
        'std': std_total_footprint,
        'confidence_interval': confidence_interval
    }

    return results
    
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
@app.route('/entry', methods=['GET', 'POST'])
def update():
    house_hold_members = request.form["household_members"]
    miles_driver = request.form["miles_driven"]
    anual_electricity = request.form["annual_electricity"]
    waste = request.form["food_waste"]
    flights_per_year = request.form["flights_per_year"]

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
    pie_graph = [{"labels": ["Transportation", "Electricity", "Waste", "Food Production", "Manufacturing"]}, {"data": pie_percent}]
    print(bar_graph)
    print(pie_percent)
    return render_template("dashboard.html", pieChart1=pie_graph, barChart1=bar_graph)
def compute_footprint(email):
    now = str(datetime.datetime.now())

    transportation = request.form["Transportation"]
    electricity = request.form["Electricity"]
    waste = request.form["Waste"]
    food_production = request.form["Food Production"]
    manufacturing = request.form["Manufacturing"]
    modes = [transportation, electricity, waste, food_production, manufacturing]
    df2 = pd.read_csv("data.csv")
    for index, row in df2.iterrows():
        if row["Email"] == email:
            cd = ast.literal_eval(row["Info"])
            break
    
    nums = cd[1]["usage"]
    for i in range(5):
        cd[1]["usage"][i] = nums[i] + modes[i]
            
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
        elif not validate_password(password, confirm):
            returnedmessage = "Your email and password are invalid."

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
            except FileNotFoundError:
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
        except FileNotFoundError:
            empty = True

        if empty:
            return render_template("login.html", returnedmessage='Invalid Username or Password')

        elif email in df2['Email'].values:
            return redirect(url_for('dashboard', email=email))

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
