from flask import Flask, redirect, render_template, request, flash, url_for
from urllib.parse import quote
import pandas as pd
import os
import hashlib
import binascii
import datetime 
import random
import numpy as np
import ast
app = Flask(__name__)
app.config['SECRET_KEY'] = '24924d82ea'  # Required for session management
# Home Page >> Index.HTML
@app.route('/')
def homepage():
    return render_template('index.html')
def monte_carlo_simulation(email):
    # Fetch user data (replace this with actual logic from your dataset)
    # Fetch user data from CSV
    df2 = pd.read_csv("data.csv")
    for index, row in df2.iterrows():
        if row["Email"] == email:
            cd = ast.literal_eval(row["Info"])
            break
    
    # Input current footprint values from the user's data
    current_usage = cd[1]['usage']
    # Input current usage data from the user's info
    current_usage = cd[1]['usage']  # ['Transportation', 'Electricity', 'Waste', 'Food Production', 'Manufacturing']

    # Constants for Monte Carlo simulation
    num_simulations = 1000
    household_size = random.uniform(1, 6)  # Example: household size between 1 and 6
    miles_per_week = random.uniform(50, 300)  # Miles driven per week
    annual_kwh = random.uniform(4000, 12000)  # Annual electricity in kWh
    food_waste_per_week = random.uniform(2, 15)  # Food waste in pounds per week
    flights_per_year = random.uniform(0, 10)  # Flights per year
    
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
# Home Page >> Index.HTML

# @app.route('/dashboard')
# def dash():
#     return render_template('dashboard.html')
@app.route('/offset')
def offset():
    return render_template('offset.html')
@app.route('/entry/<email>', methods=['GET', 'POST'])
def entry(email):
    returned_message = None  # Message to show after form submission
    if request.method == 'POST':
        # Retrieve form data
        house_members = request.form.get("household_members", type=int)
        miles_driver = request.form.get("miles_driver", type=float)
        electricity = request.form.get("annual_electricity", type=float)
        waste = request.form.get("food_waste", type=float)
        plane = request.form.get("flights_per_year", type=float)
        print("HOIWER")
        # Validate inputs
        if (house_members is None or miles_driver is None or 
            electricity is None or waste is None or plane is None):
            returned_message = "Please fill in all fields."
        else:
            # Prepare data to append to CSV
            new_data = {
                "Household Members": house_members,
                "Miles Driven": miles_driver,
                "Annual Electricity": electricity,
                "Food Waste": waste,
                "Flights per Year": plane
            }
            print(new_data)
            df2 = pd.read_csv("ctrl.csv")
            for index, row in df2.iterrows():
                if row["Email"] == email:
                    cd = ast.literal_eval(row["Info"])
                    break
            print(cd)
            lst = list(new_data.values())
            for i in range(5):
                cd[1]["usage"][i] += lst[i]

            now = str(datetime.datetime.now())
            cd[0]["recents"][now] = sum(lst)
            
            
            # Find the row(s) where the 'email' column matches the provided email
            mask = df2['Email'] == email
            
            # If the email exists in the CSV, update the information
            if mask.any():print(new_data)
            df2 = pd.read_csv("ctrl.csv")
            for index, row in df2.iterrows():
                if row["Email"] == email:
                    cd = ast.literal_eval(row["Info"])
                    break

            lst = list(new_data.values())
            for  i in range(5):
                cd[1]["usage"][i] += lst[i]

            now = str(datetime.datetime.now())
            cd[0]["recents"][now] = sum(lst)
            
            
            # Find the row(s) where the 'email' column matches the provided email
            mask = df2['Email'] == email
            
            # If the email exists in the CSV, update the information
            if mask.any():print(new_data)
            df2 = pd.read_csv("ctrl.csv")
            for index, row in df2.iterrows():
                if row["Email"] == email:
                    cd = ast.literal_eval(row["Info"])
                    break

            lst = list(new_data.values())
            for  i in range(5):
                cd[1]["usage"][i] += lst[i]

            now = str(datetime.datetime.now())
            cd[0]["recents"][now] = sum(lst)
            
            
            # Find the row(s) where the 'email' column matches the provided email
            mask = df2['Email'] == email
            
            # If the email exists in the CSV, update the information
            if mask.any():
                # Update all columns (except 'email') with the new string
                for column in df2.columns:
                    if column != 'Email':  # Ensure we don't overwrite the email field
                        df2.loc[mask, column] = str(cd)
        
                # Save the updated DataFrame back to the CSV file
                df2.to_csv("ctrl.csv", index=False)
                # Redirect without quoting the email
        return redirect(url_for('dashboard', email=email))

    return render_template('entry.html', email=email)

@app.route('/dashboard/<email>', methods=['GET', 'POST'])
def dashboard(email):
    # Load the CSV and find the user's data based on the email
    df2 = pd.read_csv("ctrl.csv")
    print("Email received in dashboard:", email)  # Debugging statement
    
    # Initialize variable for user data
    cd = {}
    
    for index, row in df2.iterrows():
        if row["Email"] == email:
            cd = ast.literal_eval(row["Info"])
            break

    # Calculate pie_percent based on 'usage'
    nums = cd[1]['usage']
    pie_percent = []
    if nums != [0] * 5:
        pie_percent = [(num / sum(nums)) * 100 for num in nums]
        for i in range(5):
            if i == 1 or i == 2:
                s = ((nums[i] / sum(nums)) * 100) / 20000
                pie_percent.append(s)
            else:
                pie_percent.append((nums[i] / sum(nums)) * 100)
    else:
        pie_percent = [20] * 5  # Default values if no usage data

    # Prepare bar chart data
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
    nums = cd[1]["usage"]

    line_data = []
    line_x_axis = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    for i in range(4):
        line_data.append(((nums[i] + nums[i + 1]) / 2) + 0.1 * (random.randint(1, 5)))
    line_data.append(random.randint(1, 100400))

    # Create bar and pie chart data structures
    bar_graph = [{"x_labels": bar_x_axis}, {"y_data": data}]
    pie_graph = [{"labels": ["Transportation", "Electricity", "Waste", "Food Production", "Manufacturing"]}, {"data": pie_percent}]
    line_graph = [{"x_labels": line_x_axis}, {"y_data": line_data}] 
    # Print for debugging
    print("Bar Graph Data:", bar_graph)
    print("Pie Percent Data:", pie_percent)
    print("Line Graph:", line_graph)
    # Render the dashboard template with the appropriate data
    return render_template("dashboard.html", pieChart1=pie_graph, barChart1=bar_graph, lineChart1=line_graph, email=email)


# Home page >> register.HTML
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Initilize Returned Message
    returnedmessage = None

    if request.method == 'POST':
        # Assigning variables from request
        email = request.form['email'].lower()  # Force email to be lowercase to avoid duplicate issues
        password = request.form['password']
        confirm = request.form['confirm']

        # Validate email
        if not ("@" in email and "." in email):
            returnedmessage = "Your email is invalid."
        # Validate password
        elif not validate_password(password, confirm):
            returnedmessage = "Your password is invalid."

        else:
            # Hash the password with salt
            salted_hashed_password = hash_password_with_salt(password)

            # Initialize row for DataFrame
            s = "[{'recents': {}}, {'usage': [0, 0, 0, 0, 0]}]"
            df1 = pd.DataFrame({'Email': [email], 'Password': [salted_hashed_password], 'Info': [s]})

            empty = None
            try:
                df2 = pd.read_csv("ctrl.csv")
            except (pd.errors.EmptyDataError, FileNotFoundError):
                empty = True

            if not empty and (email in df2['Email'].values):
                returnedmessage = "You are already registered, please login."
                
            else:
                if empty:
                    df2 = pd.DataFrame(columns=['Email', 'Password', 'Info']) 
                # Concatenate the new user data to the existing DataFrame
                result_df = pd.concat([df2, df1], ignore_index=True)
                print("Updated DataFrame after adding user:n", result_df)  # Debugging output

                # Save the updated DataFrame back to CSV
                result_df.to_csv('ctrl.csv', index=False)
                print("Data successfully written to CSV.")  # Confirmation of successful write
                return redirect(url_for('dashboard', email=email))

    return render_template('register.html', returnedmessage=returnedmessage)

@app.route('/login', methods=['GET', 'POST'])
def login():
    returnedmessage = None

    if request.method == 'POST':
        email = request.form['email'].lower()  # Make sure to lower case the email for consistency
        password = request.form['password']
        empty = None

        try:
            df2 = pd.read_csv("ctrl.csv")
        except (pd.errors.EmptyDataError, FileNotFoundError):
            empty = True

        if empty:
            returnedmessage = 'No users registered yet. Please register first.'
            return render_template("login.html", returnedmessage=returnedmessage)

        # Check if email exists
        if email in df2['Email'].values:
            # Retrieve the stored password hash for the email
            stored_password = df2.loc[df2['Email'] == email, 'Password'].values[0]
            # Verify the provided password
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
    special_characters = "!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
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